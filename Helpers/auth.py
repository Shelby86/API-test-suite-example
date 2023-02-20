import requests
import pytest
import json
from requests import Session
sess = Session()
import logging as log
import json

class Auth():


    def get_cookie():
        req = sess.post(url="https://apidev.geminishale.com/auth/login",
        headers={'Content-Type':'application/json',
                                 "Accept": '*/*'},
                                 data=json.dumps({'username':'bkonek+devauto@gmail.com',
                                 'password':'Testing$1234'}))
        resp = req.headers
        rh = dict(resp)
        auth_cookie = rh['Set-Cookie']
        auth_cookie = auth_cookie[0:20] + auth_cookie[100:]

        return auth_cookie

    def default_headers(self):
        cookie = self.get_auth_cookie()
        header = {
            "Accept": '*/*',
            "Content-Type": 'application/json',
            "Cookie": cookie
        }

        return header

