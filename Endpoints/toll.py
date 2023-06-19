import logging as log

import requests
from requests import Session
sess = Session()
import json

class Toll:

    def create_toll(base_url,cookie,file):
        req = sess.post(url=f'{base_url}/TicketToll',headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},
                        data=json.dumps(file))

        resp = req.status_code

        return resp
