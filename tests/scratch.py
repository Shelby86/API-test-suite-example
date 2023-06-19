# print(4)
# import pyodbc
#
#
# server = 'geminishaledev01.database.windows.net'
# database = 'GeminiShale'
# username = 'Automation'
# password = '0lIvquRHSRe2cvYkNiFG'
# # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
#
# cursor.execute("""
#             SELECT TOP (10) Account
#             FROM audit.AccountCode
#             """)
# row = cursor.fetchone()
# while row:
#     print(row[0])
#     row = cursor.fetchone()

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

    # def default_headers(self):
    #     cookie = self.get_auth_cookie()
    #     header = {
    #         "Accept": '*/*',
    #         "Content-Type": 'application/json',
    #         "Cookie": cookie
    #     }
    #
    #     return header


req = sess.post(url="https://apidev.geminishale.com/auth/login",
                        headers={'Content-Type': 'application/json',
                                 "Accept": '*/*'},
                        data=json.dumps({"grant_type": "password",
                        "username": "principle@api.geminishale.com",
                        "password": "Test$1234",
                        "client_id": "geminishale.web",
                        "client_secret": "GeminiShaleService@2019"
                        }))
print(req.text)







