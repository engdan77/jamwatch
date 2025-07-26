from typing import Protocol

from .error import MountError
from .log import logger
import subprocess


class Mount(Protocol):
    path: str

    def is_mounted(self) -> bool:
        ...

    def mount(self) -> bool:
        ...

    def free_space(self) -> int:
        """Return free space in bytes"""
        ...


class LocalMount(Mount):
    def is_mounted(self) -> bool:
        return True

    def mount(self):
        logger.info(f"Mounting {self.path} to local (mocked)")
        ...

    def free_space(self) -> int:
        ...


class MtpMount(Mount):
    def _detect_command(self) -> tuple[int, str]:
        """Run mtp-detect and return the command output"""
        _rc, _out = subprocess.getstatusoutput('mtp-detect')
        if _rc != 0:
            message = f"Check that mtp-tools is installed: {_out}"
            logger.error(message)
            raise MountError(message)
        return _rc, _out

    def is_mounted(self, detect_string: str = 'Garmin Forerunner') -> bool:
        rc, out = self._detect_command()
        mtp_mounted = rc == 0 and detect_string in out
        return bool(mtp_mounted)

    def free_space(self) -> int:
        rc, out = self._detect_command()
        free_space = next(
            (int(line.split(':').pop().strip()) for line in out.split('\n') if 'FreeSpaceInBytes:' in line), 0)
        return free_space
