from unittest import TestCase
from unittest import mock

import pytest

from docker_games.exceptions import MemorySizeError
from docker_games.servers import Minecraft, TeamSpeak, Factorio


class TestMinecraft(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.name = 'mcserver'
        cls.mem_size = '512MB'
        cls.data_dir = '/tmp/mcdata'

    @pytest.mark.slow
    def test_init_valid_values(self):
        mc = Minecraft('name', '1g', 'data_dir')
        self.assertIsNotNone(mc)

    @pytest.mark.slow
    def test_init_memory_size_valid_but_too_low(self):
        with pytest.raises(MemorySizeError):
            mc = Minecraft('name', '10MB', '/data_dir')

    @pytest.mark.slow
    def test_init_memory_size_invalid_and_too_low(self):
        with pytest.raises(ValueError):
            mc = Minecraft('name', '0GB', '/data_dir')

    def test_end_to_end_valid(self):
        minecraft = Minecraft(self.name, self.mem_size, self.data_dir)
        volume = {self.data_dir: {'bind': '/data'}}
        self.assertDictEqual(volume, minecraft.volume.dict())

    def test_docker_parameters(self):
        minecraft = Minecraft(self.name, self.mem_size, self.data_dir)
        minecraft.add_ports(25565, 25565)
        minecraft.accept_license()
        minecraft.online_mode()
        expected = {
            'name': minecraft.name,
            'volumes': {'/tmp/mcdata': {'bind': '/data', 'mode': 'rw'}},
            'ports': {25565: 25565},
            'environment': {
                'ONLINE_MODE': 'TRUE',
                'EULA': 'TRUE'
            }
        }
        self.assertDictEqual(expected, minecraft.parameters)


@pytest.mark.slow
class TestTeamSpeak(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.name = 'tsserver'
        cls.data_dir = '/tmp/tsdata'

    def test_init(self):
        ts = TeamSpeak(self.name, self.data_dir)
        self.assertEqual(self.name, ts.name)
        self.assertEqual(self.data_dir, ts.volume.source)

    def test_docker_parameters(self):
        ts = TeamSpeak(self.name, self.data_dir)
        ts.add_ports(9987, '9987/udp')
        ts.add_ports(10011, 10011)
        ts.add_ports(30033, 30033)
        ts.accept_license()
        expected = {
            'name': self.name,
            'volumes': {self.data_dir: {'bind': '/var/ts3server', 'mode': 'rw'}},
            'ports': {9987: '9987/udp', 10011: 10011, 30033: 30033},
            'environment': {
                'TS3SERVER_LICENSE': 'accept'
            }
        }
        self.assertDictEqual(expected, ts.parameters)


def ensure_data_dir_owner():
    pass


@pytest.mark.slow
class TestFactorio(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.name = 'factorio_tests'
        cls.data_dir = '/tmp/factorio_tests'

    @mock.patch('docker_games.servers.Factorio._ensure_data_dir_owner', side_effect=ensure_data_dir_owner)
    def test_init(self, _):
        server = Factorio(self.name, self.data_dir)
        self.assertEqual(self.name, server.name)
        self.assertEqual(self.data_dir, server.volume.source)

    @mock.patch('docker_games.servers.Factorio._ensure_data_dir_owner', side_effect=ensure_data_dir_owner)
    def test_docker_parameters(self, _):
        server = Factorio(self.name, self.data_dir)
        server.add_ports(34197, '34197/udp')
        server.add_ports(27015, '27015/tcp')
        expected = {
            'name': self.name,
            'volumes': {self.data_dir: {'bind': '/factorio', 'mode': 'rw'}},
            'ports': {34197: '34197/udp', 27015: '27015/tcp'},
            'environment': {}
        }
        self.assertDictEqual(expected, server.parameters)
