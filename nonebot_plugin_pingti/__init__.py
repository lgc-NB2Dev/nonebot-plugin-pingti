from pathlib import Path

from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.2.0"
__plugin_meta__ = PluginMetadata(
    name="最佳平替",
    description="用更低价的搜索词购物",
    usage=(
        "指令：平替 商品名\n"
        " \n"
        "同一件商品，不同的搜索词，价格可能会天差地别。\n"
        "这个工具旨在帮助你找到最便宜的搜索词：\n"
        "输入你想搜索的商品名，AI 会给出低价的替代品，结果可能不准，开心就好 :)\n"
        "经济寒冬，商品可以平替，但你的生活无法被平替。"
    ),
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-pingti",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_waiter",
    ),
    extra={"License": "MIT", "Author": "student_2333"},
)

OLD_DATA_DIR = Path.cwd() / "data" / "pingti"
if OLD_DATA_DIR.exists():
    import shutil

    shutil.rmtree(OLD_DATA_DIR)
