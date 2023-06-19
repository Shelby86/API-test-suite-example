import pytest
import pyodbc
from Helpers.auth import Auth
from pytest import fixture

@pytest.fixture()
def db():
    server = 'geminishaledev01.database.windows.net'
    database = 'GeminiShale'
    username = 'QA Automation'
    password = '3K8V999CreIYZoY'
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';ENCRYPT=yes;UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    return cursor

@pytest.fixture(scope='session')
def default_headers():
    header = {
        "Accept": '*/*',
        "Content-Type": 'application/json',
        "Cookie": Auth.get_cookie()
    }

    return header

@pytest.fixture(scope='session')
def principle_headers():
    header = {
        "Accept": '*/*',
        "Content-Type": 'application/json',
        "Authorization": f"Bearer {Auth.principle_auth_token()}",
        "subscription-key": "79cdfab0c0384339ae01a050bb687e96"
    }

    return header

@pytest.fixture(scope='session')
def base_url():
    url = 'https://apidev.geminishale.com'

    return url



    
