import itertools
import os
from typing import Protocol
from pathlib import Path
import fsspec
from typing import TypedDict
from . import log as logger
from persist_cache import cache
from datetime import timedelta


class FtpFile(TypedDict):
    name: str
    size: int
    modify: str
    type: str


class FileReader(Protocol):
    def get_files(self) -> list[FtpFile]:
        ...


class FtpFileReader(FileReader):
    def __init__(self, host: str, username: str, password: str, path: str, port: int = 21) -> None:
        self.fs = fsspec.filesystem('ftp', host=host, username=username, password=password, port=port)
        self.path = path
        ...

    @cache(expiry=timedelta(days=5))
    def get_files(self) -> list[FtpFile]:
        logger.info(f"Getting files from {self.path}")
        list_of_files: list[FtpFile] = []
        files = self.fs.walk(self.path, detail=True)
        for i, records in enumerate(files):
            for record in records:
                if not isinstance(record, dict) or record == {}:
                    continue
                for _ in itertools.chain(r for r in record.values() if isinstance(r, dict)):
                    file: FtpFile = _
                    if file.get('type', None) != 'file' and Path(file.get('name', '')).suffix.lower() != '.mp3':
                        continue
                    logger.info(f"File {i} : {file}")
                    list_of_files.append(file)
        return list_of_files


if __name__ == "__main__":
    ftp_reader = FtpFileReader(host=os.getenv('HOST'), username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'), path=os.getenv('FTP_PATH'), port=int(os.getenv('PORT')))
    files = ftp_reader.get_files()
    print(files)