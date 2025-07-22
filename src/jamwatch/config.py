from pathlib import Path

from platformdirs import site_config_dir
import json
from .log import logger
from .app_types import FilterDistributionStat, Config


def load_config() -> Config:
    config_file = Path(site_config_dir("jamwatch")) / "config.json"
    logger.info(f"Loading config from {config_file}")
    if not config_file.exists():
        return Config(distribution_stats=[FilterDistributionStat(percentage=100, filter=">1900")])
    return Config(**json.loads(config_file.read_text()))


def save_config(config: Config):
    config_file = Path(site_config_dir("jamwatch")) / "config.json"
    logger.info(f"Saving config to {config_file}")
    config_file.write_text(json.dumps(config.__dict__))
