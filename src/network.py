from enum import Enum

from validators import PortNumber


class Protocol(Enum):
    ANY = ''
    TCP = 'tcp'
    UDP = 'udp'

    def __str__(self) -> str:
        return self.value


class PortMapping(object):
    source_port = PortNumber()
    destination_port = PortNumber()

    def __init__(self, source, dest, protocol=Protocol.ANY):
        self.source_port = source
        self.destination_port = dest
        self.protocol: Protocol = protocol

    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}, {self}'

    def __str__(self) -> str:
        out = f'{self.source_port}:{self.destination_port}'
        if self.protocol is not Protocol.ANY:
            out += f':{self.protocol}'
        return out
