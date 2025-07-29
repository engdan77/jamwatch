import subprocess
import tempfile
from pathlib import Path
from typing import Protocol

from jamwatch.error import FileWriteError
from .log import logger
import stamina
import jamwatch


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


@stamina.retry(on=jamwatch.error.FileWriteError)
def _write_mtp(content, tempfile_obj, filename):
    tempfile_obj.write(content)
    cmd = f'mtp-sendfile "{tempfile_obj.name}" "{filename}"'
    _rc, out_new_file = subprocess.getstatusoutput(cmd)
    _new_file_id = next((int(line.split(':').pop().strip()) for line in out_new_file.split('\n') if
                         line.startswith('New file ID:')), None)
    send_file_success = bool(_rc == 0 and _new_file_id)
    if not send_file_success:
        print(out_new_file)
        message = f'Error uploading file to MTP: {filename} by the command: "{cmd}" ensure you have root authorities to target'
        logger.error(message)
        raise FileWriteError(message)
    logger.info(f'{filename} uploaded with id {_new_file_id}')


class MtpFileWriter(FileWriter):
    def __init__(self) -> None:
        ...

    def write_content(self, content: bytes, filename: str):
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as f:
            _write_mtp(content, f, filename)

    def erase(self):
        all_files = self._get_all_files()
        for _id, _filename in all_files:
            _rc, _out = subprocess.getstatusoutput(f'mtp-delfile 0 -n {_id}')
            _del_success = bool(_rc == 0 and 'Failed' not in _out)
            logger.info(f'{_filename} deleted')
            if not _del_success:
                logger.error('ERROR')
                logger.error(_out)
                break
        else:
            print('All files deleted')

    @staticmethod
    def _get_all_files() -> list:
        _, mtp_files_raw = subprocess.getstatusoutput('mtp-filetree')
        mtp_files_mp3 = [line.strip().split(maxsplit=1) for line in mtp_files_raw.split('\n') if line.endswith('.mp3')]
        return mtp_files_mp3


if __name__ == "__main__":
    local_writer = LocalFileWriter(path='./')
    local_writer.write_content(content=b'hello world', filename='test.txt')