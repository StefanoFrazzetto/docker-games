import logging
from abc import ABC, abstractmethod
from typing import List, Union

from docker.models.containers import ContainerCollection, Container

from .client import Docker
from .network import ServerPort
from .validators import String, MemorySize, Directory, DockerImage
from .volumes import DockerVolume

logger = logging.getLogger(__name__)


class Server(ABC):
    name = String()
    image_name = DockerImage()
    data_dir = Directory()

    def __init__(self, name, data_dir, target_dir):
        self.name: str = name
        self.volume: DockerVolume = DockerVolume(data_dir, target_dir, 'bind')
        self.ports: List[ServerPort] = []
        self.environment: dict = {}
        super().__init__()

    @abstractmethod
    def accept_license(self) -> None:
        raise NotImplementedError

    def add_ports(self, source, dest) -> None:
        port_mapping = ServerPort(source, dest)
        self.ports.append(port_mapping)


class DockerServer(Server, ABC):
    docker_client: Docker = Docker()

    def __init__(self, name, data_dir, target_dir, *args, **kwargs):
        super().__init__(name, data_dir, target_dir)

    @property
    def parameters(self) -> dict:
        return {
            'name': self.name,
            'volumes': {
                self.volume.source: {
                    self.volume.volume_type: self.volume.target, 'mode': 'rw'
                },
            },
            'ports': ServerPort.list_to_dict(self.ports),
            'environment': self.environment
        }

    def start(self, detach: bool = True, **kwargs) -> Union[ContainerCollection, Container]:
        return self.docker_client.run(
            self.image_name,
            detach=detach,
            **{**self.parameters, **kwargs}
        )


class TeamSpeak(DockerServer):

    def __init__(self, name: str, data_dir: str):
        self.image_name = 'teamspeak'
        super().__init__(name, data_dir, '/var/ts3server')

    def accept_license(self) -> None:
        logger.info("You accepted TeamSpeak 3 server license agreement:")
        logger.info("https://teamspeak.com/en/features/licensing/")
        self.environment['TS3SERVER_LICENSE'] = 'accept'


class Minecraft(DockerServer):
    memory = MemorySize('512MB')  # e.g. 500MB, 16GB, etc.

    def __init__(self, name: str, memory: str, data_dir: str, online_mode=False):
        self.image_name = 'itzg/minecraft-server'
        self.memory = memory
        super().__init__(name, data_dir, '/data')
        if online_mode:
            self.online_mode()

    def accept_license(self) -> None:
        logger.info("You agreed to Minecraft End User License Agreement and Privacy Policy:")
        logger.info("https://account.mojang.com/documents/minecraft_eula")
        logger.info("https://privacy.microsoft.com/en-gb/privacystatement")
        self.environment['EULA'] = 'TRUE'

    def online_mode(self) -> None:
        self.environment['ONLINE_MODE'] = 'TRUE'


class Factorio(DockerServer):

    def __init__(self, name: str, data_dir: str):
        self.image_name = 'factoriotools/factorio'
        super().__init__(name, data_dir, '/factorio')
        self._ensure_data_dir_owner()

    def _ensure_data_dir_owner(self):
        # game server runs as 'factorio' user with user id 845
        if self.volume.source_dir_owner_id != 845 or self.volume.source_dir_group_id != 845:
            e = f'Did you forget to set the owner of the data directory?'
            e += f'\nYour server might not work as intended;'
            e += f' please set uid and guid for {self.data_dir} to 845, e.g.'
            e += f'\nsudo chown 845:845 {self.volume.source}'
            logger.warning(e)

    def accept_license(self) -> None:
        pass
