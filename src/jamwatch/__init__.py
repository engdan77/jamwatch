import importlib
import get_version

try:
    __version__ = get_version.get_version(__file__)
except Exception:
    __version__ = importlib.metadata.version("jamwatch")
