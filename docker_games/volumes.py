import os

from .validators import Directory, OneOf


class DockerVolume:
    source = Directory(allow_not_exist=True)
    volume_type = OneOf('bind', 'volume')

    def __init__(self, source, target, volume_type='bind'):
        self.source = source
        self.target: str = target
        self.volume_type = volume_type
        if not os.path.exists(self.source):
            os.makedirs(self.source)

    def __repr__(self):
        return f'{self.__class__.__qualname__} ({self.volume_type}): {self.source} -> {self.target}'

    @property
    def source_dir_owner_id(self):
        return os.stat(self.source).st_uid

    @property
    def source_dir_group_id(self):
        return os.stat(self.source).st_gid

    def dict(self) -> dict:
        return {
            self.source: {'bind': self.target}
        }
