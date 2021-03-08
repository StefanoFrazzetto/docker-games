from abc import ABC
from typing import List

from network import PortMapping
from validators import String, MemorySize, Directory, DockerImage
from volumes import DockerVolume


class Server(ABC):
    name = String()
    image_name = DockerImage()
    data_dir = Directory()
    ports: List[PortMapping]

    def __init__(self, name, data_dir):
        self.name: str = name
        self.data_dir: str = data_dir
        super().__init__()


class TeamSpeak(Server):

    def __init__(self, name: str, data_dir: str):
        super().__init__(name, data_dir)


class Minecraft(Server):
    memory = MemorySize('500MB')  # e.g. 500MB, 16GB, etc.

    def __init__(self, name: str, memory: str, data_dir: str, online_mode=False):
        self.image_name = 'itzg/minecraft-server'
        self.memory = memory
        self.online_mode: bool = online_mode
        self.volume = DockerVolume(data_dir, '/data', 'bind')
        super().__init__(name, data_dir)
