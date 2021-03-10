from unittest import TestCase

from container import Docker
from src.servers import Minecraft


def suppress_resource_warning():
    import warnings
    # filter warning
    # ResourceWarning: unclosed <socket.socket fd=5, family=AddressFamily.AF_UNIX,
    # type=SocketKind.SOCK_STREAM, proto=0, raddr=/var/run/docker.sock>
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


def kill_and_remove_container(container):
    container.kill()
    container.remove()


def make_minecraft_server():
    minecraft = Minecraft('mcserver', '1GB', '/tmp/mcserver')
    minecraft.add_ports(25565, 25565)
    return minecraft


class TestMinecraft(TestCase):

    def test_run_server(self):
        suppress_resource_warning()
        docker = Docker()
        minecraft = make_minecraft_server()
        container = docker.run(minecraft)
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)

    def test_run_container_raw(self):
        import docker
        client = docker.from_env()
        container = client.containers.run(
            'itzg/minecraft-server',
            detach=True,
            environment={'EULA': 'TRUE'}
        )
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)
