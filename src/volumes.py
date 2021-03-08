from validators import Directory, OneOf


class Volume(object):
    source = Directory(allow_not_exist=True)

    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return f'{self.__class__.__qualname__}: {self.source}'


class DockerVolume(Volume):
    volume_type = OneOf('bind', 'volume')

    def __init__(self, source, target, volume_type='bind'):
        self.target: str = target
        self.volume_type = volume_type
        super().__init__(source)

    def dict(self) -> dict:
        return {
            self.source: {'bind': self.target}
        }
