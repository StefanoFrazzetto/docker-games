from unittest import TestCase

import pytest

from src.exceptions import MemorySizeError
from src.servers import Minecraft, TeamSpeak


class TestMinecraft(TestCase):

    def test_init_valid_values(self):
        mc = Minecraft('name', '1g', 'data_dir')
        self.assertIsNotNone(mc)

    def test_init_memory_size_valid_but_too_low(self):
        with pytest.raises(MemorySizeError):
            mc = Minecraft('name', '10MB', '/data_dir')

    def test_init_memory_size_invalid_and_too_low(self):
        with pytest.raises(ValueError):
            mc = Minecraft('name', '0GB', '/data_dir')

    def test_end_to_end_valid(self):
        data_dir = '/tmp/mcdata'
        minecraft = Minecraft('mcserver', '500MB', data_dir)
        volume = {data_dir: {'bind': '/data'}}
        self.assertEqual(volume, minecraft.volume.dict())


class TestTeamSpeak(TestCase):

    def test_init(self):
        ts = TeamSpeak('name')
