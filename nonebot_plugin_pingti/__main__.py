from cookit.loguru import logged_suppress
from cookit.nonebot import CommandArgPlaintext
from cookit.nonebot.alconna import RecallContext
from nonebot import logger, on_command
from nonebot.matcher import Matcher
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_waiter import prompt

from .config import config
from .data_source import PingTiAPI

MAX_NAME_LEN = 15


cmd_ping_ti = on_command("平替")


@cmd_ping_ti.handle()
async def _(m: Matcher, arg: str = CommandArgPlaintext()):
    if not arg:

        def handler(arg: str = CommandArgPlaintext()) -> str:
            return arg

        x = await prompt("请回复一个你想寻找平替的商品名吧", handler=handler)
        if x is None:
            await m.finish()  # timeout
        if not x:
            await m.finish("无效输入，已取消操作")
        arg = x

    if len(arg) > MAX_NAME_LEN:
        await m.finish("输入的名称太长啦，换一个短点的重新试试吧 qwq")

    async with RecallContext() as ctx:
        if config.pingti_send_tip:
            await (ctx if config.pingti_recall_tip else m).send("正在寻找平替……")

        async with PingTiAPI() as api:
            try:
                chat_resp = (await api.chat(arg)).parsed
            except Exception:
                logger.exception("Failed to request chat")
                await m.finish("出现了一些问题，请稍后再试吧 >_<")

            feedback = None
            with logged_suppress("Failed to request feedback"):
                feedback = (await api.get_feedback(arg, chat_resp.response)).parsed

        msg = UniMessage()
        msg += f"{chat_resp.response}\n{chat_resp.reason}"
        if feedback:
            feedback_items: list[str] = [
                f"{e} {c}"
                for e, c in (
                    ("👍", feedback.up),
                    ("👎", feedback.down),
                    ("😂", feedback.funny),
                )
                if config.pingti_show_zero_feedback or c > 0
            ]
            if feedback_items:
                msg += f"\n{'  '.join(feedback_items)}"
        await msg.finish()
