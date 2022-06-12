from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture()
def example_website():
    example_website = (
        Path(__file__).parent / "../fixtures/example_data/example_website.html"
    )
    with open(example_website, "r") as f:
        yield BeautifulSoup(f.read(), "html.parser")
