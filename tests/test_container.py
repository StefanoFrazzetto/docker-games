from unittest import TestCase

import pytest

from src.container import Docker
from src.servers import Minecraft


def kill_and_remove_container(container):
    container.kill()
    container.remove()


def make_minecraft_server():
    minecraft = Minecraft('mcserver', '1GB', '/tmp/mcserver')
    minecraft.add_ports(25565, 25565)
    return minecraft


class TestMinecraft(TestCase):
    @pytest.mark.slow
    def test_run_server(self):
        docker = Docker()
        minecraft = make_minecraft_server()
        container = docker.run(minecraft)
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)

    @pytest.mark.slow
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
