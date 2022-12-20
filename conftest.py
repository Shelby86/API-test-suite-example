import pytest
import os
from pytest import fixture

@pytest.fixture()
def username():
    return 'your email here'

@pytest.fixture()
def password():
    return 'Your password here'

@pytest.fixture()
def base_url():
    return 'https://dev.geminishale.com'

