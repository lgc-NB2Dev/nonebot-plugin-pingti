from typing import Optional

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    pingti_proxy: Optional[str] = None
    pingti_request_timeout: float = 5
    pingti_send_tip: bool = True
    pingti_recall_tip: bool = True


config: ConfigModel = get_plugin_config(ConfigModel)
