import importlib
import get_version
import warnings
from .log import logger

warnings.filterwarnings("ignore")

try:
    __version__ = get_version.get_version(__file__)
except Exception:
    __version__ = importlib.metadata.version("jamwatch")
