import docker
from docker.client import DockerClient
from docker.errors import DockerException
from docker.models.containers import ContainerCollection


class Docker:

    def __init__(self):
        self._client: DockerClient = self._init_client()

    @staticmethod
    def _init_client() -> DockerClient:
        try:
            return docker.from_env()
        except DockerException as e:
            raise RuntimeError('Please ensure Docker is running on your system.') from e.__class__(e)

    @property
    def client(self) -> DockerClient:
        return self._client

    @property
    def containers(self) -> ContainerCollection:
        return self._client.containers

    def run(self, *args, **kwargs):
        return self.containers.run(*args, **kwargs)
