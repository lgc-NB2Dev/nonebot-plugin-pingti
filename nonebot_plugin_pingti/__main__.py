from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.exceptions import SpecialOptionTriggered
from nonebot import logger
from nonebot_plugin_alconna import AlconnaMatcher, CommandResult, UniMessage, on_alconna
from nonebot_plugin_alconna.uniseg import Receipt

from .config import config
from .data_source import get_alternative_put_queue, query_from_db


async def captured_recall(r: Receipt):
    try:
        await r.recall()
    except Exception as e:
        logger.warning(f"Recall failed: {type(e).__name__}: {e}")
        logger.opt(exception=e).debug("Stack trace:")


mat_pingti = on_alconna(
    Alconna(
        "平替",
        Args["kw", str],
        meta=CommandMeta(example="平替 猫窝"),
    ),
    skip_for_unmatch=False,
    use_cmd_start=True,
)


@mat_pingti.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}")


@mat_pingti.handle()
async def _(matcher: AlconnaMatcher, kw: str):
    kw = kw.strip()
    if not kw:
        await matcher.finish("名称不能为空")
    if len(kw) > 15:
        await matcher.finish("输入的名称太长啦，换一个短一点的商品试试吧~")

    if not (val := await query_from_db(kw)):
        receipt = (
            (await UniMessage("正在寻找平替……").send()) if config.pingti_send_tip else None
        )
        try:
            val = await get_alternative_put_queue(kw)
        except Exception:
            await matcher.finish("出现了一些问题，请稍后再试吧 >_<")
        finally:
            if receipt and config.pingti_recall_tip:
                await captured_recall(receipt)

    if val:
        await matcher.finish(f"{kw} 的平替是：{val}")
    # 有可能返回值为空，不知道是什么情况
    await matcher.finish("好像并没有找到平替呢")
