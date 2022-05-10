import random
import string
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from utilities import string_operations


def random_string_generator(size: int = 15, chars: str = '') -> str:
    default_chars = string.ascii_letters + string.digits + chars
    generated_string = ''.join(random.choice(default_chars) for _ in range(size))
    if chars in generated_string:
        return generated_string
    return generated_string.join(random.choice(chars))


class TestChangeName:
    filenames = (
        string_operations.change_name(random_string_generator() + '.jpeg'),
        string_operations.change_name(random_string_generator() + '.png'),
        string_operations.change_name(random_string_generator() + '.jpg.webp'),
        string_operations.change_name(random_string_generator() + '.jpeg.jpg.webp'),
        string_operations.change_name(random_string_generator(128) + '.jpeg.png.webp'),
        string_operations.change_name(random_string_generator(1) + '.jpg'),
    )
    expected_extensions = ('.jpeg', '.png', '.webp', '.webp', '.webp', '.jpg')

    @pytest.mark.parametrize(('filename', 'expected_extension'), zip(filenames, expected_extensions))
    def test_extension_should_be_correct(self, filename, expected_extension):
        assert filename.count('.') == 1
        assert filename[-5:] == expected_extension or filename[-4:] == expected_extension

    @pytest.mark.parametrize('filename', filenames)
    def test_extension_should_be_in_lowercase(self, filename):
        assert filename.rsplit('.', 1)[1].islower()

    @pytest.mark.parametrize('filename', filenames)
    def test_extension_should_be_in_right_length(self, filename):
        if len(filename) == 40:
            assert len(filename[:-4]) == 36
        elif len(filename) == 41:
            assert len(filename[:-5]) == 36
        else:
            raise AssertionError('Filename is too long.')


class TestCheckCorrectnessOfTheData:
    forbidden = '"#$%^&*\\()=, „”-/<>|;ąćęłńóśźż{}[]`'
    data_with_none = (
        (None, None),
        (random_string_generator(), None),
        (None, random_string_generator()),
        ('', ''),
        (random_string_generator(16), ''),
        ('', random_string_generator(16)),
        (None, None),
    )
    to_long_data = (
        (random_string_generator(16), random_string_generator(), (random_string_generator()+'@wp.com')),
        (random_string_generator(), random_string_generator(257), (random_string_generator()+'@onet.pl')),
        (random_string_generator(), random_string_generator(), (random_string_generator(311)+'@gmail.com')),
        (random_string_generator(16), random_string_generator(257), (random_string_generator(311)+'@gmail.com')),
        (random_string_generator(312), random_string_generator(624), (random_string_generator(1248)+'@gmail.com')),
    )
    correct_data = (
        (random_string_generator(), random_string_generator(), random_string_generator()+'@wp.pl'),
        (random_string_generator(), random_string_generator(), random_string_generator()+'@o2.pl'),
        (random_string_generator(), random_string_generator(), random_string_generator()+'@gmail.com'),
        (random_string_generator(), random_string_generator(),
         random_string_generator()+'@'+random_string_generator(9)+'.pl'),
    )
    data_with_forbidden_char = (
        (random_string_generator(chars=forbidden), random_string_generator(),
         random_string_generator()+'@wp.pl'),
        (random_string_generator(), random_string_generator(chars=forbidden),
         random_string_generator()+'@wp.pl'),
        (random_string_generator(), random_string_generator(),
         random_string_generator(chars=forbidden)+'@wp.pl'),
        (random_string_generator(), random_string_generator(chars=forbidden),
         random_string_generator(chars=forbidden)+'@wp.pl'),
        (random_string_generator(chars=forbidden), random_string_generator(chars=forbidden),
         random_string_generator()+'@wp.pl'),
        (random_string_generator(chars=forbidden), random_string_generator(),
         random_string_generator(chars=forbidden)+'@wp.pl'),
        (random_string_generator(chars=forbidden), random_string_generator(chars=forbidden),
         random_string_generator(chars=forbidden)+'@wp.pl'),
    )

    @pytest.mark.parametrize(('login', 'password'), data_with_none)
    def test_empty_data_should_not_pass(self, login, password):
        assert string_operations.check_correctness_of_the_data(login, password) is False

    @pytest.mark.parametrize(('login', 'password', 'email'), to_long_data)
    def test_too_long_data_should_be_not_accepted(self, login, password, email):
        assert string_operations.check_correctness_of_the_data(login, password, email) is False

    @pytest.mark.parametrize(('login', 'password', 'email'), data_with_forbidden_char)
    def test_forbidden_char_should_return_false(self, login, password, email):
        assert string_operations.check_correctness_of_the_data(login, password, email) is False

    def test_email_address_without_at_symbol_should_be_not_accepted(self):
        login = random_string_generator()
        password = random_string_generator()
        email = random_string_generator()
        assert string_operations.check_correctness_of_the_data(login, password, email) is False

    @pytest.mark.parametrize(('login', 'password', 'email'), correct_data)
    def test_correct_data_should_return_true(self, login, password, email):
        assert string_operations.check_correctness_of_the_data(login, password, email) is True


class TestPrepareSrcAndAlt:
    @pytest.fixture()
    def load_test_data(self):
        example_website = Path(__file__).parent / "../tests/webscraper/example_data.html"
        with open(example_website, 'r') as f:
            website_data = BeautifulSoup(f.read(), 'html.parser')
        return string_operations.prepare_src_and_alt(website_data.select('img.full-image'))

    expected_data_keys = (
        'https://i1.kwejk.pl/k/obrazki/2022/05/o8uKBb4zeG00XnjZ.jpg',
        'https://i1.kwejk.pl/k/obrazki/2015/04/dfaf35b0704d0b0ba9fe99134e837984.gif',
        'https://i1.kwejk.pl/k/obrazki/2022/05/5x3pk26xUoziMQeJ.jpg',
        'https://i1.kwejk.pl/k/obrazki/2022/05/bxhWDUc9PufHQx9k.jpg',
        'https://i1.jbzd.com.pl/contents/2022/04/normal/leo7AfstltPJpuiY6njKtn9Blm93y0Mm.jpeg',
        'https://i1.kwejk.pl/k/obrazki/2022/05/hHYNUYFWkazFsLt8.jpg'
    )
    expected_data_values = (
        'Mieszkania', 'Deszcz', 'Trzeba zdenazyfikowac Watykan', 'Bo nie zjadly kanapek', 'piesek w pracy', 'Wohoo'
    )

    @pytest.mark.parametrize(('img_src', 'img_alt'), zip(expected_data_keys, expected_data_values))
    def test_output_have_proper_data(self, load_test_data, img_src, img_alt):
        data = load_test_data
        assert data[img_src] == img_alt

    @pytest.mark.parametrize('img_src', expected_data_keys)
    def test_had_all_keys(self, load_test_data, img_src):
        assert img_src in load_test_data.keys()

    @pytest.mark.parametrize('img_alt', expected_data_values)
    def test_had_all_keys(self, load_test_data, img_alt):
        assert img_alt in load_test_data.values()
