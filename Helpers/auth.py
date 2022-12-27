import requests
import pytest
import os
from pytest import fixture
import json
from requests import Session
sess = Session()
import logging as log
import json
from requests import session
sess = Session()

class Auth():


    def get_cookie():
        req = sess.post(url="https://apidev.geminishale.com/auth/login",
        headers={'Content-Type':'application/json',
                                 "Accept": '*/*'},
                                 data=json.dumps({'username':'shelby.nester@geminishale.com',
                                 'password':'W0rk3rB33!'}))
        resp = req.headers
        rh = dict(resp)
        auth_cookie = rh['Set-Cookie']
        log.info(auth_cookie)

        return auth_cookie
