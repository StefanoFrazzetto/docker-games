from .validators import Directory, OneOf


class DockerVolume:
    source = Directory(allow_not_exist=True)
    volume_type = OneOf('bind', 'volume')

    def __init__(self, source, target, volume_type='bind'):
        self.source = source
        self.target: str = target
        self.volume_type = volume_type

    def __repr__(self):
        return f'{self.__class__.__qualname__} ({self.volume_type}): {self.source} -> {self.target}'

    def dict(self) -> dict:
        return {
            self.source: {'bind': self.target}
        }
