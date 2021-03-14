from unittest import TestCase, mock

import pytest

from docker_games.client import Docker
from docker_games.servers import Minecraft, TeamSpeak, Factorio


def kill_and_remove_container(container):
    container.kill()
    container.remove()


def make_minecraft_server():
    minecraft = Minecraft('mcserver', '1GB', '/tmp/mcserver')
    minecraft.add_ports(25565, 25565)
    return minecraft


def make_teamspeak_server():
    server = TeamSpeak('tsserver', '/tmp/tsserver')
    server.add_ports(9987, '9987/udp')
    server.add_ports(10011, 10011)
    server.add_ports(30033, 30033)
    return server


def make_factorio_server():
    server = Factorio('factorio_tests', '/tmp/factorio_tests')
    server.add_ports(34197, '34197/udp')
    server.add_ports(27015, '27015/tcp')
    return server


def ensure_data_dir_owner():
    pass


@pytest.mark.slow
class TestServers(TestCase):

    def setUp(self) -> None:
        self.docker = Docker()

    def test_run_minecraft_simple(self):
        import docker
        client = docker.from_env()
        container = client.containers.run(
            'itzg/minecraft-server',
            detach=True,
            environment={'EULA': 'TRUE'}
        )
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)

    def test_run_minecraft(self):
        minecraft = make_minecraft_server()
        container = minecraft.start()
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)

    def test_run_teamspeak(self):
        teamspeak = make_teamspeak_server()
        container = teamspeak.start()
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)

    @mock.patch('docker_games.servers.Factorio._ensure_data_dir_owner', side_effect=ensure_data_dir_owner)
    def test_run_factorio(self, _):
        factorio = make_factorio_server()
        container = factorio.start()
        self.assertEqual('created', container.status)
        kill_and_remove_container(container)
