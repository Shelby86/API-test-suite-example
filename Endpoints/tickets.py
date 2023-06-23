import logging

import requests
from requests import Session
sess = Session()
import json
from Helpers.auth import Auth

class Tickets():

    # def create_ticket(headers,base_url,file_name):
    #     req = sess.post(url=f'{base_url}/ticket',
    #                     headers=headers,
    #                     data=json.dumps(file_name))
    #
    #     resp = {
    #         'data': req.json(),
    #         'status_code': req.status_code
    #     }
    #
    #     return resp

    def create_ticket(base_url,cookie,file):
        req = sess.post(url=f'{base_url}/ticket',headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},
                        data=json.dumps(file))

        resp = {
           "data": req.json(),
            "status_code": req.status_code
        }
        return resp

        # resp = req.headers
        # rh = dict(resp)
        # print(req.status_code)
        # print(resp)

        # loc = rh['Location']
        # ticket_id = loc[-6:]
        #
        # return ticket_id

    # def delete_ticket(default_headers,base_url,ticket_id):
    #     url = base_url
    #     headers = default_headers
    #     req = sess.delete(url=f'{url}/ticket/{ticket_id}',
    #     headers=headers)
    #
    #     status_code = req.status_code
    #     data = req.json()
    #
    #     res = {
    #         "status_code": status_code,
    #         "data": data
    #     }
    #
    #     return res
    #
    def create_npt_ticket(base_url,file,cookie):

        req = sess.post(url=f'{base_url}/nonproductivetimeticket',
                        headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"},data=json.dumps(file))

        resp = {
            "data": req.json(),
            "status_code": req.status_code
        }

        return resp


    #
    # def delete_npt_ticket(base_url,default_headers,ticket_id):
    #     req = sess.delete(url=f'{base_url}/nonproductivetimeticket/{ticket_id}',
    #                       headers=default_headers)
    #
    #     status_code = req.status_code
    #     data = req.json()
    #
    #     res = {
    #         "status_code": status_code,
    #         "data": data
    #     }
    #
    #     return res

    def approve_ticket(base_url,cookie,id):
        url = f"{base_url}/Ticket/{id}/approve"
        print(url)
        req = sess.post(url=url,
                        headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"})

        print

        res = {
            # "data": req.json(),
            "status_code": req.status_code
        }

        return res

    def approve_npt_ticket(base_url,id,cookie):
        req = sess.post(url=f'{base_url}/NonProductiveTimeTicket/{id}/approve',
                        headers={"Cookie": cookie, "Accept": "*/*", "Content-Type": "application/json"})

        res = {
            "data": req.json(),
            "status_code": req.status_code
        }

        return res







        



        