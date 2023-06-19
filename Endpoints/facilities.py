import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth


class Facilities:

    @staticmethod
    def create_facilities_ticket(base_url,default_headers,file):
        req = sess.post(url=f'{base_url}/facility', headers=default_headers,data=json.dumps(file))

        res = {
            "status": req.status_code,
            "data": req.text
        }

        return res
