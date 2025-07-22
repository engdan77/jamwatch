from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, NotRequired
from musicplayer import Track
from platformdirs import site_config_dir


class File(TypedDict):
    name: str
    size: int
    modify: NotRequired[str]
    type: NotRequired[str]
    track: Track


@dataclass
class FilterDistributionStat:
    percentage: float
    filter: str


@dataclass
class Config:
    distribution_stats: list[FilterDistributionStat]
    config_file: Path = Path(site_config_dir("jamwatch")) / "config.json"
