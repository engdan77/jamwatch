import time
from dataclasses import dataclass
from pathlib import Path

from jamwatch.blink import Blink
from jamwatch.config import load_config
from jamwatch.filter import filter_files
from jamwatch.app_types import Config
from jamwatch.error import MountError
from jamwatch.file_reader import DiskFileReader, FileReader
from jamwatch.file_writer import LocalFileWriter, FileWriter
from jamwatch.mount import LocalMount, Mount
from jamwatch.log import logger


@dataclass
class OrchestratorParams:
    file_reader: FileReader
    file_writer: FileWriter
    mount: Mount
    progress_blinker: Blink


def ensure_mount(mount: Mount):
    for _ in range(3):
        if not mount.is_mounted():
            logger.info(f"Mounting {mount.path} to local attempt {_ + 1}")
            mount.mount()
        else:
            break
        time.sleep(1)
    else:
        raise MountError(f'Unable to mount {mount.path}')


class Orchestrator:
    def __init__(self, orchestrator_config: OrchestratorParams):
        self.orchestrator_config: OrchestratorParams = orchestrator_config
        self.config: Config = load_config()
        self.running = False
        self.copy_in_progress = False

    def start_loop(self):
        self.running = True

    def stop_loop(self):
        self.running = False

    def loop(self):
        while self.running:
            ...

    def copy(self):
        if self.copy_in_progress:
            logger.warning("Copy already in progress")
            return
        self.copy_in_progress = True
        logger.info(f"Starting copy from {self.orchestrator_config.file_reader.path} to {self.orchestrator_config.file_writer.path}")
        mount = self.orchestrator_config.mount
        ensure_mount(mount)
        source_files = self.orchestrator_config.file_reader.get_files_list()
        writer = self.orchestrator_config.file_writer
        filtered_files = filter_files(
            filter_distribution=self.config.distribution_stats,
            files_list=source_files,
            max_mb=self.config.max_mb_size
        )

        self.orchestrator_config.file_writer.erase()
        for i, track in enumerate(filtered_files):
            current_perc = int((i / len(filtered_files)) * 100)
            self.orchestrator_config.progress_blinker.percentage(current_perc)
            source_file = Path(track['name'])
            writer.write_content(content=source_file.read_bytes(), filename=source_file.name)
            logger.info(f"Copied {source_file.name} to {writer.path}")
        self.copy_in_progress = False

