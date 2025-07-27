from pathlib import Path
from typing import Annotated

from jamwatch import config
from jamwatch.blink import Blink
from jamwatch.button import Button, ButtonConfig
from jamwatch.file_reader import DiskFileReader
from jamwatch.file_writer import LocalFileWriter, MtpFileWriter
from jamwatch.mount import LocalMount, MtpMount
from jamwatch.orchestrator import OrchestratorParams, Orchestrator
from jamwatch.log import logger
from cyclopts import App as CycloptsApp
from cyclopts import Parameter, validators

cyclopts_app = CycloptsApp()


@cyclopts_app.default
def test_copy():
    logger.info("Starting Orchestrator")
    orchestrator_config = OrchestratorParams(
        file_reader=DiskFileReader('/Users/edo/tmp/mp3'),
        file_writer=LocalFileWriter('/Users/edo/tmp/mp3_out'),
        mount=LocalMount('/Users/edo/tmp/mp3_out'),
        progress_blinker=Blink(gpio_pin=17)
    )
    orchestrator = Orchestrator(orchestrator_config)
    orchestrator.copy()
    ...


@cyclopts_app.command
def copy(source_folder: Annotated[Path, Parameter(validator=validators.Path(exists=True))]):
    """Copy files from a folder to a MTP device"""
    logger.info("Starting copying")
    orchestrator = get_orchestrator_instance(source_folder)
    orchestrator.copy()
    logger.info('Copy completed')


def start_server(source_folder: Annotated[Path, Parameter(validator=validators.Path(exists=True))]):
    """Start server that listens for button presses to start copying files"""
    logger.info("Starting server")
    orchestrator = get_orchestrator_instance(source_folder)
    button_config = ButtonConfig(
        gpio_pin=22,
        hold_time=2,
        pressed_func=orchestrator.copy
    )
    button = Button(button_config)
    button.start_event_loop()
    logger.info('Server stopped')


def get_orchestrator_instance(source_folder):
    orchestrator_config = OrchestratorParams(
        file_reader=DiskFileReader(source_folder.as_posix()),
        file_writer=MtpFileWriter(),
        mount=MtpMount(),
        progress_blinker=Blink(gpio_pin=17),
    )
    orchestrator = Orchestrator(orchestrator_config)
    return orchestrator


@cyclopts_app.command
def show_config_path():
    """Show the path to the config file"""
    print(config.config_file)


@cyclopts_app.command
def create_config():
    """Create a new config file"""
    current_config = config.load_config()
    config.save_config(current_config)


@cyclopts_app.command
def show_free_space():
    """Show the free space in the target device"""
    mtp = MtpMount()
    free_space = mtp.free_space()
    logger.info(f"Target available with {free_space:_.2f} MB free")


def main():
    cyclopts_app()


if __name__ == "__main__":
    main()
