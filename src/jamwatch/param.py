from dataclasses import dataclass

from jamwatch.file_reader import FileReader
from jamwatch.file_writer import FileWriter
from jamwatch.mount import Mount


@dataclass
class Param:
    file_reader: FileReader
    file_writer: FileWriter
    mount: Mount
