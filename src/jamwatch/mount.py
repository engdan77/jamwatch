from typing import Protocol


class Mount(Protocol):
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
        ...

