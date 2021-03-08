from typing import List

from validators import PortNumber


class PortMapping(object):
    source_port = PortNumber()
    destination_port = PortNumber()

    def __init__(self, source, dest):
        self.source_port = source
        self.destination_port = dest

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}, {self}'

    def __str__(self) -> str:
        return f'{self.source_port}:{self.destination_port}'

    @staticmethod
    def list_to_dict(values: List['PortMapping']):
        return {port.source_port: port.destination_port for port in values}
