from typing import List

from .validators import PortNumber


class ServerPort(object):
    source_port = PortNumber()
    destination_port = PortNumber()

    def __init__(self, *ports):
        parsed_ports = self._parse_ports(*ports)
        self.source_port = parsed_ports[0]
        self.destination_port = parsed_ports[1]

    @staticmethod
    def _parse_ports(*ports):
        if len(ports) == 1 and isinstance(ports[0], str):
            return ports[0].split(':')
        if len(ports) == 2:
            return ports

        e = f'Wrong ports format {ports}, expected:'
        e += f'\n(source:destination) or (source, destination)'
        raise ValueError()

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}, {self}'

    def __str__(self) -> str:
        return f'{self.source_port}:{self.destination_port}'

    @staticmethod
    def list_to_dict(values: List['ServerPort']):
        return {port.source_port: port.destination_port for port in values}
