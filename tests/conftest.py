import pytest


@pytest.fixture(scope="session")
def base_url():
    return "https://collectionapi.metmuseum.org/public/collection/v1"
