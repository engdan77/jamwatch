import gc
import time
from dataclasses import dataclass
from pathlib import Path

from jamwatch.blink import Blink
from jamwatch.button import Button
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
    mount_blinker: Blink = None


def ensure_mount(mount: Mount):
    for _ in range(3):
        if not mount.is_mounted():
            logger.info(f"Mounting - attempt {_ + 1}")
            mount.mount()
        else:
            break
        time.sleep(1)
    else:
        message = f"Unable to mount {mount}"
        logger.error(message)
        raise MountError(f'Unable to mount {mount}')


class Orchestrator:
    def __init__(self, orchestrator_config: OrchestratorParams):
        self.orchestrator_config: OrchestratorParams = orchestrator_config
        self.config: Config = load_config()
        self.running = False
        self.copy_in_progress = False

    def start_loop(self):
        self.running = True

    def stop(self):
        logger.info("Stopping orchestrator")
        self.orchestrator_config.progress_blinker.led = None
        self.orchestrator_config.mount_blinker.led = None
        self.running = False
        # TODO: fix gpiozero/threading RuntimeError: cannot join current thread
        gc.collect()

    def loop(self):
        logger.info("Starting loop")
        self.orchestrator_config.start_button.add_pressed_func(self.copy)
        while self.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                break

    def copy(self):
        """Begins the copy process by reading files from the source and writing them to the destination."""
        if self.copy_in_progress:
            logger.warning("Copy already in progress")
            return
        self.copy_in_progress = True
        logger.info(f"Starting copy from {self.orchestrator_config.file_reader.path}")
        mount = self.orchestrator_config.mount
        logger.info(f"Ensuring target is available")
        ensure_mount(mount)
        free_space = mount.free_space()
        logger.info(f"Target available with {free_space:_.2f} MB free")
        logger.info(f"Retrieve list of files from {self.orchestrator_config.file_reader.path} and filter by percentage and size.")
        self.orchestrator_config.progress_blinker.percentage(70)
        source_files = self.orchestrator_config.file_reader.get_files_list(verbose=True)
        writer = self.orchestrator_config.file_writer
        logger.info(f'Start filtering files by percentage and size.')
        filtered_files = filter_files(
            filter_distribution=self.config.distribution_stats,
            files_list=source_files,
            max_mb=self.config.max_mb_size
        )
        logger.info(f'Erasing target')
        self.orchestrator_config.progress_blinker.percentage(90)
        self.orchestrator_config.file_writer.erase()
        logger.info(f'Copying {len(filtered_files)} files')
        tot_files = len(list(filtered_files))
        for i, track in enumerate(filtered_files):
            current_perc = int((i / len(filtered_files)) * 100)
            self.orchestrator_config.progress_blinker.percentage(current_perc)
            source_file = Path(track['name'])
            writer.write_content(content=source_file.read_bytes(), filename=source_file.name)
            logger.info(f"[{i/tot_files:.2%}] Copied {source_file.name} to target")
        free_space = mount.free_space()
        logger.info(f"Target available with {free_space:_.2f} MB free")
        self.copy_in_progress = False


