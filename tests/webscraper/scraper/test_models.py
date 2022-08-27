import pytest
from _pytest.fixtures import SubRequest

from webscraper.scraper.models import Image


class TestImage:
    @pytest.fixture(scope="class")
    def prepare_image_object(self, request: SubRequest) -> Image:
        image_data = request.param
        yield Image(
            source=image_data["source"],
            title=image_data["title"],
            filename=image_data["filename"],
            url_address=image_data["url_address"],
            author_id=image_data["author_id"],
        )

    image_model_data = {
        "source": "https://webludus.pl/images/logo.png",
        "title": "Logo",
        "filename": "c8c26a00-2794-43d5-a61e-defab4e07c19.png",
        "url_address": "https://webludus.pl",
        "author_id": 1,
    }

    @pytest.mark.parametrize("prepare_image_object", (image_model_data,), indirect=True)
    def test_property_as_dict_should_have_proper_data(
        self, prepare_image_object: Image
    ):
        image = prepare_image_object

        assert isinstance(image.as_dict, dict)
        assert image.as_dict == self.__class__.image_model_data
