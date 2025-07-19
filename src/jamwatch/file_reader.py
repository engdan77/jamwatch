import itertools
import os
from typing import Protocol, NotRequired
from abc import ABC, abstractmethod
from pathlib import Path
import fsspec
from typing import TypedDict
from . import log as logger
from persist_cache import cache
from datetime import timedelta


class File(TypedDict):
    name: str
    size: int
    modify: NotRequired[str]
    type: NotRequired[str]


class FileReader(ABC):
    fs = None
    path = None

    def get_files_list(self) -> list[File]:
        logger.info(f"Getting files from {self.path}")
        list_of_files: list[File] = []
        files = self.fs.walk(self.path, detail=True)
        for i, records in enumerate(files):
            for record in records:
                if not isinstance(record, dict) or record == {}:
                    continue
                for _ in itertools.chain(r for r in record.values() if isinstance(r, dict)):
                    file: File = _
                    if file.get('type', None) != 'file' and Path(file.get('name', '')).suffix.lower() != '.mp3':
                        continue
                    logger.info(f"File {i} : {file}")
                    list_of_files.append(file)
        return list_of_files

    def get_file_content(self, file: File) -> bytes:
        return self.fs.cat(file['name'])


class DiskFileReader(FileReader):
    def __init__(self, path: str) -> None:
        self.fs = fsspec.filesystem('file')
        self.path = path


class FtpFileReader(FileReader):
    def __init__(self, host: str, username: str, password: str, path: str, port: int = 21) -> None:
        self.fs = fsspec.filesystem('ftp', host=host, username=username, password=password, port=port)
        self.path = path


if __name__ == "__main__":
    # reader = FtpFileReader(host=os.getenv('HOST'), username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'), path=os.getenv('FTP_PATH'), port=int(os.getenv('PORT')))
    reader = DiskFileReader(path='/Users/edo/tmp/mp3')
    files = reader.get_files_list()
    print(files)