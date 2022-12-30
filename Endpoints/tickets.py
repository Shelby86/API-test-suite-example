import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth

class Tickets():
    def create_ticket(default_headers,base_url,file):
        url = base_url
        headers = default_headers
        req = sess.post(url=f'{url}/ticket',
        headers=headers,
        data=file)

        resp = req.headers
        rh = dict(resp)

        loc = rh['Location']
        ticket_id = loc[-6:]

        return ticket_id

    def delete_ticket(default_headers,base_url,ticket_id):
        url = base_url
        headers = default_headers
        req = sess.delete(url=f'{url}/ticket/{ticket_id}',
        headers=headers)

        status_code = req.status_code
        data = req.json()

        res = {
            "status_code": status_code,
            "data": data
        }

        return res





        



        