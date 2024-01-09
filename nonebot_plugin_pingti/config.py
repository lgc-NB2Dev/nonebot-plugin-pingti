from typing import Optional

from nonebot import get_driver
from pydantic import BaseModel


class ConfigModel(BaseModel):
    proxy: Optional[str] = None
    pingti_request_timeout: float = 5


config: ConfigModel = ConfigModel.parse_obj(get_driver().config)
