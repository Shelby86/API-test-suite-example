import pymysql
import pytest
import os

from credentials import credentials
from pytest import fixture
import json
from requests import Session
sess = Session()
import logging as log
from Endpoints.auth import Auth
from Helpers.db_utility import DBUtility
import pymysql.connections
import sshtunnel



@pytest.fixture()
def username():
    return 'bkonek+devauto@gmail.com'

@pytest.fixture()
def password():
    return 'Testing$1234'

@pytest.fixture()
def base_url():
    return "https://apidev.geminishale.com"

@pytest.fixture()
def get_cookie():
        req = sess.post(url=f'{base_url}auth/login',
                        headers={'Content-Type':'application/json',
                                 "Accept": '*/*'},
                        data = json.dumps({
    "username": username,
    "password": password
        }))
        resp = req.headers
        rh = dict(resp)
        auth_cookie = rh['Set-Cookie']
        log.info(auth_cookie)

        return auth_cookie

@pytest.fixture()
def default_headers():
    headers = {
        "Accept": '*/*',
        "Content-Type": 'application/json',
        "Cookie": Auth.get_auth_cookie()
    }

    return headers


@pytest.fixture()
def create_ssh():
    ssh_host = '1.2.3.4'
    ssh_username = 'Automation'
    ssh_password = '0lIvquRHSRe2cvYkNiFG'
    database_username = 'Automation'
    database_password = '0lIvquRHSRe2cvYkNiFG'
    database_name = 'GeminiShale'
    localhost = '127.0.0.1'
    tunnel = sshtunnel.SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username='Automation',
        ssh_password='0lIvquRHSRe2cvYkNiFG',
        remote_bind_address=('127.0.0.1', 3306)
    )

    tunnel.start()

    conn = pymysql.connect(host='geminishaledev01.database.windows.net', user='Automation',
                           password='0lIvquRHSRe2cvYkNiFG', database='GeminiShale')

    return conn

@pytest.fixture()
def create_connection():
        conn = pymysql.connect(host='geminishaledev01.database.windows.net',user='Automation',
        password='0lIvquRHSRe2cvYkNiFG',database='GeminiShale')

        return conn









