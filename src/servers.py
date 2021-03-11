from abc import ABC
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
    ports: List[PortMapping] = []

    def __init__(self, name, data_dir, target_dir):
        self.name: str = name
        self.volume = DockerVolume(data_dir, target_dir, 'bind')
        super().__init__()

    def add_ports(self, source, dest):
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
        }


class TeamSpeak(Server):

    def __init__(self, name: str, data_dir: str):
        super().__init__(name, data_dir, '/tmp/tsdata')


class Minecraft(Server):
    memory = MemorySize('512MB')  # e.g. 500MB, 16GB, etc.

    def __init__(self, name: str, memory: str, data_dir: str, online_mode=False):
        self.image_name = 'itzg/minecraft-server'
        self.memory = memory
        self.online_mode: bool = online_mode
        super().__init__(name, data_dir, '/data')

    def docker_parameters(self) -> dict:
        params = super().docker_parameters()
        params.update({
            'environment': {
                'EULA': 'TRUE',
                'ONLINE_MODE': 'TRUE',
            }
        })
        return params
