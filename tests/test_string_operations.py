import pytest
import random
import string
from utilities import string_operations


class TestChangeName:
    def test_file_split_positive(self):
        jpeg = random_string_generator()+'.jpeg'
        jpg = random_string_generator(68)+'.jpg'

        jpeg = string_operations.change_name(jpeg)
        jpg = string_operations.change_name(jpg)

        assert jpeg[-5:] == '.jpeg'
        assert jpg[-4:] == '.jpg'
        assert len(jpeg[:-5]) == 36
        assert len(jpg[:-4]) == 36

    def test_file_split_negative(self):
        pass


def random_string_generator(size: int = 16, chars: str = string.ascii_letters + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))
