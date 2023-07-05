import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth


class Invoice:

    def invoice_tickets(base_url,file_name,cookie):
        request = sess.post(url=f'{base_url}/Document/Invoice',
                            headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},
                            data=json.dumps(file_name))


        return request.status_code