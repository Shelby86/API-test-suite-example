import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth

class AssignCost:

    def assign_cost(base_url,cookie,file):
        req = sess.post(url=f'{base_url}/TicketCostAssignment',
                        headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},
                        data=json.dumps(file))

        res = req.status_code

        return res