import itertools
from abc import ABC
from pathlib import Path
import fsspec
import msgspec

from jamwatch.mp3 import get_track_details
from jamwatch.app_types import File
from .log import logger


class FileReader(ABC):
    fs = None
    path = None

    def get_files_list(self, randomize:bool = True, verbose: bool = False) -> list[File]:
        logger.info(f"Getting files from {self.path}")
        list_of_files: list[File] = []
        files = self.fs.walk(self.path, detail=True)
        current_file_count = 0
        for records in files:
            for record in records:
                if not isinstance(record, dict) or record == {}:
                    continue
                file_list = list(itertools.chain(r for r in record.values() if isinstance(r, dict)))
                for i, _ in enumerate(file_list):
                    file: File = _
                    if file.get('type', None) != 'file' and Path(file.get('name', '')).suffix.lower() != '.mp3':
                        continue
                    if verbose:
                        logger.info(f"[{current_file_count}] Get track details for {file['name']}")
                    current_file_count += 1
                    try:
                        file['track'] = get_track_details(file)
                    except msgspec.DecodeError as e:
                        logger.error(f"Error decoding file {file['name']}: {e}")
                        continue
                    list_of_files.append(file)
        if randomize:
            import random
            random.shuffle(list_of_files)
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