from unittest import TestCase

import pytest

from docker_games.network import ServerPort


class TestPortMapping(TestCase):

    def test_valid_mapping(self):
        source = 4242
        dest = 6969
        mapping = ServerPort(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_valid_mapping_as_string(self):
        ports = '4242:6969'
        mapping = ServerPort(ports)
        self.assertEqual(f'{ports}', str(mapping))

    def test_valid_mapping_as_string_with_protocol(self):
        ports = '4242/tcp:6969'
        mapping = ServerPort(ports)
        self.assertEqual(f'{ports}', str(mapping))

    def test_valid_mapping_source_with_protocol(self):
        source = '4242/udp'
        dest = 6969
        mapping = ServerPort(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_valid_mapping_dest_with_protocol(self):
        source = 4242
        dest = '6969/tcp'
        mapping = ServerPort(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_invalid_mapping(self):
        source = 4242
        dest = 22
        with pytest.raises(ValueError):
            mapping = ServerPort(source, dest)

    def test_list_to_dict(self):
        ports = [
            ServerPort('8081/tcp', 8080),
            ServerPort(3500, 4040),
        ]

        result = ServerPort.list_to_dict(ports)
        expected = {3500: 4040, '8081/tcp': 8080}
        self.assertDictEqual(expected, result)
