from pathlib import Path
from typing import Protocol
from .log import logger


class FileWriter(Protocol):
    path: str

    def write_content(self, content: bytes, filename: str):
        ...

    def erase(self):
        ...


class LocalFileWriter(FileWriter):
    def __init__(self, path: str) -> None:
        self.path = path

    def write_content(self, content: bytes, filename: str):
        with open(f"{self.path}/{filename}", 'wb') as f:
            f.write(content)

    def erase(self):
        for f in Path(self.path).rglob('*'):
            f.unlink(missing_ok=True)
            logger.info(f"Deleted {f.as_posix()}")


if __name__ == "__main__":
    local_writer = LocalFileWriter(path='./')
    local_writer.write_content(content=b'hello world', filename='test.txt')