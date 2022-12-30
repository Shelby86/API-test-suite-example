import logging
import pytest
from Helpers.auth import Auth
from Helpers.base import Base
from Helpers.db_helper import DBHelper
from Helpers.db_utility import DBUtility
from Endpoints.tickets import Tickets
from Helpers.file_opener import FileOpener as FO
from requests import session
sess = session()
import json

@pytest.mark.y
def test_print():
        print('Hi') 
        logging.info('Hi')
        logging.info(Auth.get_cookie())
        c = Auth.get_cookie()
        print(c)

@pytest.mark.pr
def test_print_headers():
        print(Base.default_headers())
        logging.info(Base.default_headers())

@pytest.mark.sql_maybe
def test_create_ticket():
        q = DBHelper.query_runner_as_dict(query="""
            SELECT TOP (10) Account
            FROM audit.AccountCode
            """)

        print(q)

@pytest.mark.ticket
def test_real_ticket():
        url = Base.base_url()
        defautl_headers = Base.default_headers()
        body = FO.open_file(file_name='tests/Data/ticket.json')
        
        request = sess.post(url=f'{url}/ticket',headers=defautl_headers,
        data=body)

        resp = request.status_code
        print(resp)

      
       
        





        

       
        







  