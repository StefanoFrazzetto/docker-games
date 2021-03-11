from abc import ABC, abstractmethod
from typing import List

from .validators import String, MemorySize, Directory, DockerImage, PortNumber
from .volumes import DockerVolume


class PortMapping(object):
    source_port = PortNumber()
    destination_port = PortNumber()

    def __init__(self, source, dest):
        self.source_port = source
        self.destination_port = dest

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}, {self}'

    def __str__(self) -> str:
        return f'{self.source_port}:{self.destination_port}'

    @staticmethod
    def list_to_dict(values: List['PortMapping']):
        return {port.source_port: port.destination_port for port in values}


class Server(ABC):
    name = String()
    image_name = DockerImage()
    data_dir = Directory()

    def __init__(self, name, data_dir, target_dir):
        self.name: str = name
        self.volume: DockerVolume = DockerVolume(data_dir, target_dir, 'bind')
        self.ports: List[PortMapping] = []
        self.environment: dict = {}
        super().__init__()

    @abstractmethod
    def accept_license(self) -> None:
        raise NotImplementedError

    def add_ports(self, source, dest) -> None:
        port_mapping = PortMapping(source, dest)
        self.ports.append(port_mapping)

    def docker_parameters(self) -> dict:
        return {
            'name': self.name,
            'volumes': {
                self.volume.source: {
                    self.volume.volume_type: self.volume.target, 'mode': 'rw'
                },
            },
            'ports': PortMapping.list_to_dict(self.ports),
            'environment': self.environment
        }


class TeamSpeak(Server):

    def __init__(self, name: str, data_dir: str):
        self.image_name = 'teamspeak'
        super().__init__(name, data_dir, '/var/ts3server')

    def accept_license(self) -> None:
        print("You accepted TeamSpeak 3 server license agreement:")
        print("https://teamspeak.com/en/features/licensing/")
        self.environment['TS3SERVER_LICENSE'] = 'accept'


class Minecraft(Server):
    memory = MemorySize('512MB')  # e.g. 500MB, 16GB, etc.

    def __init__(self, name: str, memory: str, data_dir: str, online_mode=False):
        self.image_name = 'itzg/minecraft-server'
        self.memory = memory
        super().__init__(name, data_dir, '/data')
        if online_mode:
            self.online_mode()

    def accept_license(self) -> None:
        print("You agreed to Minecraft End User License Agreement and Privacy Policy:")
        print("https://account.mojang.com/documents/minecraft_eula")
        print("https://privacy.microsoft.com/en-gb/privacystatement")
        self.environment['EULA'] = 'TRUE'

    def online_mode(self) -> None:
        self.environment['ONLINE_MODE'] = 'TRUE'


class Factorio(Server):

    def __init__(self, name: str, data_dir: str):
        self.image_name = 'factoriotools/factorio'
        super().__init__(name, data_dir, '/factorio')

    def accept_license(self) -> None:
        pass
