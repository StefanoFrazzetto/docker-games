from unittest import TestCase

import pytest

from network import PortMapping, Protocol


class TestPortMapping(TestCase):

    def test_valid_mapping(self):
        source = 4242
        dest = 6969
        mapping = PortMapping(source, dest)
        self.assertEqual(f'{source}:{dest}', str(mapping))

    def test_valid_mapping_with_protocol(self):
        source = 4242
        dest = 6969
        protocol = Protocol.UDP
        mapping = PortMapping(source, dest, protocol)
        self.assertEqual(f'{source}:{dest}:{protocol}', str(mapping))

    def test_invalid_mapping(self):
        source = 4242
        dest = 22
        with pytest.raises(ValueError):
            mapping = PortMapping(source, dest)
