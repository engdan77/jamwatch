from typing import TypedDict, NotRequired
from musicplayer import Track


class File(TypedDict):
    name: str
    size: int
    modify: NotRequired[str]
    type: NotRequired[str]
    track: Track
