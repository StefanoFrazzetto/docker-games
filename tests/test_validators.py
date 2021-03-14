import os
from unittest import TestCase

import pytest

from docker_games.validators import IPAddress, MemorySize, String, Directory, PortNumber, DockerImage


class TestMemorySize(TestCase):

    def setUp(self):
        self.validator = MemorySize()

    def test_valid_value(self):
        self.validator.validate('2g')

    def test_invalid_value_int(self):
        with pytest.raises(TypeError):
            self.validator.validate(1024)

    def test_invalid_value_str_amount_only(self):
        with pytest.raises(ValueError):
            self.validator.validate('1024')

    def test_invalid_value_str_unit_only(self):
        with pytest.raises(ValueError):
            self.validator.validate('g')


class TestIPAddress(TestCase):

    def setUp(self) -> None:
        self.validator = IPAddress()

    def test_valid_ip_address(self):
        ip_addr = '127.0.0.1'
        self.validator.validate(ip_addr)

    def test_malformed_ip_address(self):
        ip_addr = '192.168.'
        with pytest.raises(ValueError):
            self.validator.validate(ip_addr)


class TestPortNumber(TestCase):

    def test_valid_port_number(self):
        number = 1024
        validator = PortNumber()
        validator.validate(number)

    def test_invalid_port_number_str(self):
        number = ''
        validator = PortNumber()
        with pytest.raises(ValueError):
            validator.validate(number)

    def test_invalid_port_number_reserved(self):
        number = 22
        validator = PortNumber()
        with pytest.raises(ValueError):
            validator.validate(number)

    def test_invalid_port_number_too_high(self):
        number = 70000
        validator = PortNumber()
        with pytest.raises(ValueError):
            validator.validate(number)


class TestString(TestCase):

    def test_valid_default(self):
        validator = String()
        validator.validate('foo')

    def test_valid_minlength(self):
        validator = String(2)
        validator.validate('fo')

    def test_invalid_minlength(self):
        validator = String(2)
        with pytest.raises(ValueError):
            validator.validate('f')

    def test_valid_maxlength(self):
        validator = String(maxsize=3)
        validator.validate('foo')

    def test_invalid_maxlength(self):
        validator = String(maxsize=2)
        with pytest.raises(ValueError):
            validator.validate('foo')

    def test_predicate_success(self):
        validator = String(predicate=str.isupper)
        validator.validate('FOO')

    def test_predicate_error(self):
        validator = String(predicate=str.isupper)
        with pytest.raises(ValueError):
            validator.validate('FOo')


class TestDirectory(TestCase):

    def setUp(self) -> None:
        path = '/tmp/awsgs/tests'
        file = f'{path}/file.test'
        self.make_dir(path)
        self.make_file(file)
        self.dir_path = path
        self.file_path = file

    @staticmethod
    def make_dir(path):
        try:
            os.makedirs(path)
        except OSError:
            print(f'Failed to create "{path}"')

    @staticmethod
    def make_file(path):
        try:
            os.mknod(path)
        except FileExistsError:
            print(f'File {path} exists already!')

    def test_dir_exists(self):
        validator = Directory(allow_not_exist=False)
        validator.validate(self.dir_path)

    def test_dir_does_not_exists_not_allowed(self):
        validator = Directory(allow_not_exist=False)
        with pytest.raises(ValueError):
            validator.validate(f'{self.dir_path}/somedir/')

    def test_dir_does_not_exists_allowed(self):
        validator = Directory(allow_not_exist=True)
        validator.validate(f'{self.dir_path}/somedir/')

    def test_file_exists(self):
        validator = Directory(allow_not_exist=False)
        with pytest.raises(ValueError):
            validator.validate(self.file_path)

    def test_file_not_exists(self):
        validator = Directory(allow_not_exist=False)
        with pytest.raises(ValueError):
            validator.validate(f'{self.dir_path}/random.file')

    def tearDown(self) -> None:
        os.remove(self.file_path)
        os.removedirs(self.dir_path)
        if os.path.exists(self.file_path) or os.path.exists(self.dir_path):
            raise RuntimeError(f'Failed to "{self.dir_path}" and/or its contents')


@pytest.mark.slow
class TestDockerImage(TestCase):

    def test_get_images(self):
        validator = DockerImage()
        images = validator.get_images('ubuntu')
        self.assertIsNotNone(images)

    def test_validate_ubuntu(self):
        validator = DockerImage()
        validator.validate('ubuntu')

    def test_validate_itzg_minecraft_server(self):
        validator = DockerImage()
        validator.validate('itzg/minecraft-server')
