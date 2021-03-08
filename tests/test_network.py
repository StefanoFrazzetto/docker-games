from unittest import TestCase

import pytest

from network import PortMapping


class TestPortMapping(TestCase):

    def test_valid_mapping(self):
        source = 4242
        dest = 6969
        mapping = PortMapping(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_valid_mapping_source_with_protocol(self):
        source = '4242/udp'
        dest = 6969
        mapping = PortMapping(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_valid_mapping_dest_with_protocol(self):
        source = 4242
        dest = '6969/tcp'
        mapping = PortMapping(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_invalid_mapping(self):
        source = 4242
        dest = 22
        with pytest.raises(ValueError):
            mapping = PortMapping(source, dest)
