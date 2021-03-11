from unittest import TestCase

import pytest

from src.exceptions import MemorySizeError
from src.servers import Minecraft, TeamSpeak


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
        self.assertEqual(volume, minecraft.volume.dict())

    def test_docker_parameters(self):
        minecraft = Minecraft(self.name, self.mem_size, self.data_dir)
        minecraft.add_ports(25565, 25565)
        expected = {
            'name': minecraft.name,
            'volumes': {'/tmp/mcdata': {'bind': '/data', 'mode': 'rw'}},
            'ports': {25565: 25565},
            'environment': {
                'ONLINE_MODE': 'TRUE',
                'EULA': 'TRUE'
            }
        }
        self.assertEqual(expected, minecraft.docker_parameters())


@pytest.mark.slow
class TestTeamSpeak(TestCase):

    def test_init(self):
        ts = TeamSpeak('name', '/tmp/tsdata')
