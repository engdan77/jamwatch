import threading
import time
from typing import Protocol

from .blink import Blink
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


class MountChecker:
    def __init__(self, mount: Mount, blinker: Blink, sleep_secs=2) -> None:
        self.mount = mount
        self.blink = blinker
        self.sleep_secs = sleep_secs
        self.running = False

    def start(self):
        threading.Thread(target=self._start_loop).start()

    def _start_loop(self):
        self.running = True
        last_is_mounted = self.mount.is_mounted()
        while self.running:
            mounted = self.mount.is_mounted()
            self.blink.percentage(100 if mounted else 0)
            if mounted != last_is_mounted:
                logger.info(f"Mounted: {mounted}")
            last_is_mounted = mounted
            time.sleep(self.sleep_secs)

    def stop(self):
        self.running = False
