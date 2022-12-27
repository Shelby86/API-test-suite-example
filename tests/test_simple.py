import logging
import pytest
from Helpers.auth import Auth

@pytest.mark.y
def test_print():
        print('Hi') 
        logging.info('Hi')
        logging.info(Auth.get_cookie())
        c = Auth.get_cookie()
        print(c)


  