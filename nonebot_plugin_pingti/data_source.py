import asyncio
from typing import Any, Awaitable, Callable, Optional

from attr import dataclass
from httpx import AsyncClient
from nonebot import get_driver, logger
from nonebot_plugin_orm import Model
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import select

from .config import config

# region db


class Item(Model):
    kw: Mapped[str] = mapped_column(primary_key=True)
    resp: Mapped[str]


async def query_from_db(
    session: async_scoped_session[AsyncSession],
    kw: str,
) -> Optional[str]:
    try:
        res = await session.execute(select(Item).where(Item.kw == kw))
        item = res.scalars().first()
    except Exception:
        logger.exception("Error when querying database")
    else:
        if item is not None:
            return item.resp
    return None


async def save_to_db(
    session: async_scoped_session[AsyncSession],
    kw: str,
    resp: str,
) -> None:
    try:
        session.add(Item(kw=kw, resp=resp))
        await session.commit()
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
    async def call(it_: QueueItem, val: Optional[str]) -> None:
        try:
            await it_.callback(val)
        except Exception:
            logger.exception("Error when calling callback")

    while True:
        it = await queue.get()
        try:
            resp = await request_alternative(it.kw)
        except Exception:
            logger.exception("Error when doing request")
            await call(it, None)
        else:
            await call(it, resp)
        queue.task_done()
        await asyncio.sleep(2)


driver = get_driver()


@driver.on_startup
async def _():
    asyncio.create_task(handle_queue())


# endregion
