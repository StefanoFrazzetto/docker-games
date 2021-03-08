from abc import ABC
from typing import List

from network import PortMapping
from validators import String, MemorySize, Directory
from volumes import DockerVolume


class Server(ABC):
    name = String()
    ports: List[PortMapping]

    def __init__(self, name):
        self.name: str = name
        super().__init__()


class TeamSpeak(Server):

    def __init__(self, name):
        super().__init__(name)


class Minecraft(Server):
    memory = MemorySize('500MB')  # e.g. 500MB, 16GB, etc.
    data_dir = Directory()

    def __init__(self, name, memory, data_dir: str, online_mode=False):
        self.memory = memory
        self.online_mode: bool = online_mode
        self.volume = DockerVolume(data_dir, '/data', 'bind')
        super().__init__(name)
