import logging

import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth

class CostAssignmentReview:

    def approve_cost(base_url,default_headers,cookie,file):
        req = sess.post(url=f'{base_url}/TicketCostAssignmentReview/approve',
                        headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},
                        data=json.dumps(file))

        res = req.status_code

        return res




