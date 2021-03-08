from abc import ABC
from typing import List

from network import PortMapping
from validators import String, MemorySize, OneOf, Directory


class Volume(object):
    source = Directory(allow_not_exist=True)
    volume_type = OneOf('bind', 'volume')

    def __init__(self, source, target, volume_type='bind'):
        self.source = source
        self.target: str = target
        self.volume_type = volume_type

    def dict(self):
        return {
            self.source: {'bind': self.target}
        }


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
    memory = MemorySize('500MB')  # 1024 MB to 64 GB
    data_dir = Directory()

    def __init__(self, name, memory, data_dir: str, online_mode=False):
        self.memory = memory
        self.online_mode: bool = online_mode
        self.volume = Volume(data_dir, '/data', 'bind')
        super().__init__(name)
