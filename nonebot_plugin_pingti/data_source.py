import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, Optional, Union, cast

from httpx import AsyncClient
from nonebot import get_driver, logger

from .config import config

# region db
# 操你妈，完全不会用关系型数据库和 ORM，我是废物 😭😭😭

DATA_DIR = Path.cwd() / "data" / "pingti"
DATA_FILE = DATA_DIR / "cache.json"
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("{}", "u8")
else:
    _d: Dict[str, str] = json.loads(DATA_FILE.read_text("u8"))
    if any((not v) for v in _d.values()):
        DATA_FILE.write_text(
            json.dumps({k: v for k, v in _d.items() if v}, ensure_ascii=False),
            encoding="u8",
        )


async def query_from_db(kw: str) -> Optional[str]:
    kw = kw.lower()
    try:
        data: Dict[str, str] = json.loads(DATA_FILE.read_text("u8"))
    except Exception:
        logger.exception("Error when querying database")
    else:
        if kw in data:
            return data[kw]
    return None


async def save_to_db(kw: str, resp: str) -> None:
    kw = kw.lower()
    try:
        data: Dict[str, str] = json.loads(DATA_FILE.read_text("u8"))
        data[kw] = resp
        DATA_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="u8")
    except Exception:
        logger.exception("Error when committing database")


# endregion

# region queue


@dataclass
class QueueItem:
    kw: str
    callback: Callable[[Union[str, Exception]], Awaitable[Any]]


queue = asyncio.Queue[QueueItem]()


async def request_alternative(kw: str) -> str:
    async with AsyncClient(
        proxies=config.pingti_proxy,
        timeout=config.pingti_request_timeout,
        follow_redirects=True,
    ) as client:
        logger.debug(f"Requesting alternative for `{kw}`")
        resp = await client.post(
            "https://www.pingti.app/api/chat",
            json={"messages": [{"role": "user", "content": kw}]},
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.0.0 "
                    "Safari/537.36"
                ),
            },
        )
        resp.raise_for_status()
        return resp.text


async def get_alternative_put_queue(kw: str) -> str:
    async def wait():
        val = ...

        async def callback(r: Union[str, Exception]) -> None:
            nonlocal val
            val = r

        await queue.put(QueueItem(kw, callback))

        while val is ...:
            await asyncio.sleep(0)
        return cast(Union[str, Exception], val)

    resp = await asyncio.wait_for(wait(), timeout=config.pingti_request_timeout + 1)
    if isinstance(resp, Exception):
        raise resp
    return resp


async def handle_queue():
    async def call(it: QueueItem, val: Union[str, Exception]) -> None:
        try:
            await it.callback(val)
        except Exception:
            logger.exception("Error when calling callback")

    async def once():
        it = await queue.get()
        if x := await query_from_db(it.kw):
            await call(it, x)
            queue.task_done()
            return

        try:
            val = await request_alternative(it.kw)
        except Exception as e:
            logger.exception("Error when doing request")
            await call(it, e)
        else:
            if val:
                await save_to_db(it.kw, val)
            await call(it, val)
        queue.task_done()
        await asyncio.sleep(2)

    while True:
        try:
            await once()
        except Exception:
            logger.exception("Unexpected error when handling queue")


driver = get_driver()


@driver.on_startup
async def _():
    asyncio.create_task(handle_queue())


# endregion
