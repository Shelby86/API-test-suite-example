import logging

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
                                 data=json.dumps({'username':'shelby.nester@geminishale.com',
                                 'password':'W0rk3rB33!'}))
        resp = req.headers
        rh = dict(resp)
        auth_cookie = rh['Set-Cookie']
        auth_cookie = auth_cookie[0:20] + auth_cookie[100:]

        return auth_cookie

    # def default_headers(self):
    #     cookie = self.get_auth_cookie()
    #     header = {
    #         "Accept": '*/*',
    #         "Content-Type": 'application/json',
    #         "Cookie": cookie
    #     }
    #
    #     return header


    def principle_auth_token():
        req = sess.post(url='https://apidev.geminishale.com/auth-service/token',
                        headers={'Content-Type': "application/json",
                                 "Accept": "*/*"},
                        data=json.dumps({
                            "grant_type": "password",
                            "username": "principle@api.geminishale.com",
                            "password": "Test$1234",
                            "client_id": "geminishale.web",
                            "client_secret": "GeminiShaleService@2019"
                        }))

        resp = req.json()

        return(resp['access_token'])

    def impoersonate(base_url,default_headers,file):
        req = sess.post(url=f'{base_url}/auth/impersonate',headers=default_headers,
                        data=json.dumps(file))


        resp = req.headers
        rh = dict(resp)
        auth_cookie = rh['Set-Cookie']
        auth_cookie = auth_cookie[0:20] + auth_cookie[100:]

        return auth_cookie








