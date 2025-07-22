from dataclasses import dataclass
from pathlib import Path

from jamwatch.file_reader import FileReader
from jamwatch.file_writer import FileWriter
from jamwatch.mount import Mount
from platformdirs import site_config_dir
import json


@dataclass
class OrchestratorParams:
    file_reader: FileReader
    file_writer: FileWriter
    mount: Mount


@dataclass
class FilterDistributionStat:
    percentage: float
    filter: str


@dataclass
class Config:
    distribution_stats: list[FilterDistributionStat]
    config_file: Path = Path(site_config_dir("jamwatch")) / "config.json"


def load_config() -> Config:
    config_file = Path(site_config_dir("jamwatch")) / "config.json"
    if not config_file.exists():
        return Config(distribution_stats=[FilterDistributionStat(percentage=100, filter=">1900")])
    return Config(**json.loads(config_file.read_text()))


def save_config(config: Config):
    config_file = Path(site_config_dir("jamwatch")) / "config.json"
    config_file.write_text(json.dumps(config.__dict__))
