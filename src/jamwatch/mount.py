from typing import Protocol
from .log import logger


class Mount(Protocol):
    path: str

    def is_mounted(self) -> bool:
        ...

    def mount(self):
        ...


class LocalMount(Mount):
    def __init__(self, path: str) -> None:
        self.path = path

    def is_mounted(self) -> bool:
        return True

    def mount(self):
        logger.info(f"Mounting {self.path} to local (mocked)")
        ...


class JmtpfsMount(Mount):
    def __init__(self, path: str) -> None:
        self.path = path


