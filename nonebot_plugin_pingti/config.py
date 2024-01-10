from typing import Optional

from nonebot import get_driver
from pydantic import BaseModel


class ConfigModel(BaseModel):
    pingti_proxy: Optional[str] = None
    pingti_request_timeout: float = 5
    pingti_send_tip: bool = True
    pingti_recall_tip: bool = True


config: ConfigModel = ConfigModel.parse_obj(get_driver().config)
