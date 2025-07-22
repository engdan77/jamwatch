from typing import Protocol
from . import log as logger


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

