import pytest
from script._setup_script import deploy

@pytest.fixture
def counter_contract():
    return deploy()