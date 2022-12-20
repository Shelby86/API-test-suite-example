import pytest
import logging as log

@pytest.mark.test_me
def test_print_username(username,base_url):
    log.info(f'\n {username}')
    print(username)
    print(base_url)


