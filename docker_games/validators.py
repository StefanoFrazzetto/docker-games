import ipaddress
import os
import re
from abc import ABC, abstractmethod
from typing import Tuple

from .exceptions import MemorySizeError


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        raise NotImplementedError


class String(Validator):

    def __init__(self, minsize=0, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a str')
        if len(value) < self.minsize:
            raise ValueError(f'String is too short, must be at least {self.minsize} long')
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(f'String is too long, must be no bigger than {self.maxsize} long')
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f'Expected {value} to be true for {self.predicate !r}')


class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'{value!r} not a valid option.  should be one of: {self.options}')


class Number(Validator):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Expected an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f'{value} is too small.  Must be at least {self.minvalue}.')
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(f'{value} is too big.  Must be no more than {self.maxvalue}.')


class MemorySize(Validator):

    def __init__(self, minsize='500MB'):
        self.validate_value_format(minsize)
        self.minsize: str = minsize

    def validate(self, value):
        self.validate_value_format(value)
        self.validate_memory_size(value)

    @staticmethod
    def validate_value_format(value):
        if not isinstance(value, str):
            raise TypeError(f'Expected a string for memory size, got {value!r}')
        if not re.match(r'[1-9][0-9]*[m|M|g|G]+[b|B]?', value):
            raise ValueError(f'Invalid memory size {value}, expected <size>[m|M|g|G][b|B] (e.g. 500MB)')

    def validate_memory_size(self, value):
        value_size, value_unit = MemorySize.parse_value(value)
        min_size, min_unit = MemorySize.parse_value(self.minsize)
        if value_size < min_size:
            if value_unit.upper() == 'MB' and min_unit.upper() == 'MB':
                raise MemorySizeError(f'Memory size should at least {self.minsize} MB, got {value}')

    @staticmethod
    def parse_value(value: str) -> Tuple[int, str]:
        num = value.rstrip('kKmMgGbB')
        unit = value[len(num):]
        return int(num), unit


class PortNumber(Validator):

    def validate(self, value):
        if not isinstance(value, (int, str)):
            raise TypeError('Expected an int or str, e.g. 8080, "8080/tcp"')
        if isinstance(value, int):
            PortNumber.validate_port_number(value)
        if isinstance(value, str):
            parts = value.split('/')
            if len(parts) > 1 and parts[1] not in ['udp', 'tcp']:
                raise ValueError(f'Invalid protocol for port {value}')
            port_number = int(parts[0])
            PortNumber.validate_port_number(port_number)

    @staticmethod
    def validate_port_number(value: int):
        number_validator = Number(1024, 65535)
        number_validator.validate(value)


class IPAddress(Validator):

    def validate(self, value):
        ipaddress.ip_address(value)


class Directory(Validator):

    def __init__(self, allow_not_exist=True):
        self.allow_not_exist: bool = allow_not_exist

    def validate(self, value):
        if os.path.isfile(value):
            raise ValueError(f'The path "{value}" is a file')
        if not self.allow_not_exist and not os.path.isdir(value):
            raise ValueError(f'The directory "{value}" does not exist')


class DockerImage(Validator):

    def validate(self, value):
        images = DockerImage.get_images(value)
        names = [image['name'] for image in images]
        if not images or value not in names:
            raise ValueError(f'Could not find Docker image "{value}"')

    @staticmethod
    def get_images(name: str):
        from docker_games.client import Docker
        docker = Docker()
        # docker search does not find images when repository is specified
        image_name = name.split('/')[-1]  # get last string after '/'
        return docker.client.images.search(image_name)
