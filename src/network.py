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
