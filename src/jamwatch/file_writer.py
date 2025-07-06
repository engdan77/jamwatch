from typing import Protocol


class FileWriter(Protocol):
    def write_content(self, content: bytes, filename: str):
        ...


class LocalFileWriter(FileWriter):
    def __init__(self, path: str) -> None:
        self.path = path

    def write_content(self, content: bytes, filename: str):
        with open(f"{self.path}/{filename}", 'wb') as f:
            f.write(content)


if __name__ == "__main__":
    local_writer = LocalFileWriter(path='./')
    local_writer.write_content(content=b'hello world', filename='test.txt')