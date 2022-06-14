from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture()
def example_website() -> BeautifulSoup:
    """Loads HTML document and prepare BeautifulSoup object based on document data.

    Returns: BeautifulSoup object."""
    example_website_path = (
        Path(__file__).parent / "../fixtures/example_data/example_website.html"
    )
    with open(example_website_path, "r") as f:
        return BeautifulSoup(f.read(), "html.parser")
