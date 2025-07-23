from jamwatch.blink import Blink
from jamwatch.file_reader import DiskFileReader
from jamwatch.file_writer import LocalFileWriter
from jamwatch.mount import LocalMount
from jamwatch.orchestrator import OrchestratorParams, Orchestrator
from jamwatch.log import logger
from cyclopts import App as CycloptsApp

cyclopts_app = CycloptsApp()


@cyclopts_app.default
def test():
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


def main():
    cyclopts_app()


if __name__ == "__main__":
    main()
