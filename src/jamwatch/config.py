from pathlib import Path

from platformdirs import user_config_path
from .log import logger
from .app_types import FilterDistributionStat, Config
import jsons

STOPPED = False  # For other threads to check

config_file = Path(user_config_path("jamwatch")) / "config.json"
config_file.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> Config:
    logger.info(f"Loading config from {config_file}")
    if not config_file.exists():
        default_config = Config(distribution_stats=[FilterDistributionStat(percentage=100, filter=">1900")])
        save_config(default_config)
        return default_config
    return jsons.loads(config_file.read_text(), Config)


def save_config(config: Config):
    logger.info(f"Saving config to {config_file}")
    config_file.write_text(jsons.dumps(config))



