import docker
from docker.errors import DockerException

from .servers import Server


class Docker:

    @property
    def client(self) -> docker.DockerClient:
        try:
            client = docker.from_env()
            return client
        except DockerException as e:
            raise RuntimeError('Please ensure Docker is running on your system.') from e

    def run(self, server: Server):
        return self.client.containers.run(
            server.image_name,
            detach=True,
            **server.docker_parameters()
        )
