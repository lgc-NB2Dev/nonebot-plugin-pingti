import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable, Optional

from httpx import AsyncClient
from nonebot import get_driver, logger

from .config import config

# region db
# 操你妈，完全不会用关系型数据库和 ORM，我是废物 😭😭😭

DATA_DIR = Path.cwd() / "data" / "pingti"
DATA_FILE = DATA_DIR / "cache.json"


async def query_from_db(kw: str) -> Optional[str]:
    try:
        data = json.loads(DATA_FILE.read_text("u8"))
    except Exception:
        logger.exception("Error when querying database")
    else:
        if kw in data:
            return data[kw]
    return None


async def save_to_db(kw: str, resp: str) -> None:
    try:
        data = json.loads(DATA_FILE.read_text("u8"))
        data[kw] = resp
        DATA_FILE.write_text(json.dumps(data, ensure_ascii=False), "u8")
    except Exception:
        logger.exception("Error when committing database")


# endregion

# region queue


@dataclass
class QueueItem:
    kw: str
    callback: Callable[[Optional[str]], Awaitable[Any]]


queue = asyncio.Queue[QueueItem]()


async def request_alternative(kw: str) -> str:
    async with AsyncClient(
        proxies=config.proxy,
        timeout=config.pingti_request_timeout,
    ) as client:
        resp = await client.post(
            "https://www.pingti.xyz/api/chat",
            json={"messages": [{"role": "user", "content": kw}]},
        )
        resp.raise_for_status()
        return resp.text


async def get_alternative_put_queue(kw: str) -> str:
    val = ...

    async def callback(resp: Optional[str]) -> None:
        nonlocal val
        val = resp
        if resp is None:
            return

    await queue.put(QueueItem(kw, callback))
    while val is ...:
        await asyncio.sleep(0)
    return val


async def handle_queue():
    async def call(it: QueueItem, val: Optional[str]) -> None:
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
        except Exception:
            logger.exception("Error when doing request")
            await call(it, None)
        else:
            await call(it, val)
            await save_to_db(it.kw, val)
        queue.task_done()
        await asyncio.sleep(2)

    while True:
        try:
            await once()
        except Exception:
            logger.exception("Error when handling queue")


driver = get_driver()


@driver.on_startup
async def _():
    asyncio.create_task(handle_queue())


# endregion
