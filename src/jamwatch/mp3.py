import eyed3
import persist_cache

from .types import File, Track


@persist_cache.cache
def get_track_details(file: File) -> Track:
    return Track(eyed3.load(file['name']))


def clear_mp3_cache():
    get_track_details.clear()