from abc import ABC
from types import TracebackType
from typing import Generic, Optional, TypeVar
from typing_extensions import override

from httpx import AsyncClient, Response
from nonebot.compat import type_validate_python
from pydantic import BaseModel

from .config import config

PING_TI_BASE_URL = "https://pingti.app"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/131.0.0.0"
    " Safari/537.36"
)


class ChatResp(BaseModel):
    response: str
    reason: str


class FeedbackResp(BaseModel):
    up: int
    down: int
    funny: int


M = TypeVar("M", bound=BaseModel)


class APIResponse(Generic[M]):
    def __init__(self, resp: Response, model: type[M]):
        self.resp = resp
        self.model = model
        self.parsed = type_validate_python(self.model, self.resp.json())


class BaseAPI(ABC):  # noqa: B024
    def __init__(self, **cli_kwargs) -> None:
        super().__init__()
        self.cli_kwargs = cli_kwargs
        self.cli = self.create_client()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        await self.cli.aclose()

    def create_client(self):
        return AsyncClient(**self.cli_kwargs)


class PingTiAPI(BaseAPI):
    @override
    def __init__(self, **cli_kwargs) -> None:
        cli_kwargs.setdefault("base_url", PING_TI_BASE_URL)
        cli_kwargs.setdefault("proxy", config.pingti_proxy)
        cli_kwargs.setdefault("timeout", config.pingti_request_timeout)
        cli_kwargs.setdefault("headers", {})
        cli_kwargs["headers"].setdefault("User-Agent", USER_AGENT)
        super().__init__(**cli_kwargs)

    async def chat(self, content: str):
        r = await self.cli.post(
            "/api/chat",
            json={"messages": [{"role": "user", "content": content}]},
        )
        r.raise_for_status()
        return APIResponse(r, ChatResp)

    async def get_feedback(self, input_content: str, output_content: str):
        r = await self.cli.get(
            "/api/feedback",
            params={"input": input_content, "output": output_content},
        )
        r.raise_for_status()
        return APIResponse(r, FeedbackResp)
