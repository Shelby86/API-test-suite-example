import json

import pytest
import logging as log
from Endpoints.auth import Auth
from Endpoints.tickets import Tickets
from requests import Session
sess = Session()


def get_cookie_headers():
    l = Auth.get_auth_cookie()
    return l

# @pytest.mark.test_me
# def test_print_cookie():
#     print(get_cookie_headers())


# @pytest.mark.operator_maybe
# def test_operator_maybe(base_url):
#     req = sess.post(url=f'{base_url}/auth/impersonate',
#               headers={
#                             'Accept': '*/*',
#                             'Content-Type': 'application/json',
#                             'Cookie': get_cookie_headers()
#                         },
#               data=json.dumps({
#     "HaulerId": 1
# }))
#     # res= req.headers
#     # log.info(res)
#     print(req)
#     print(req.status_code)


@pytest.mark.ticket_maybe
def test_ticket_maybe(base_url):
    request = sess.post(url=f'{base_url}/ticket',
                        headers={
                            'Accept': '*/*',
                            'Content-Type': 'application/json',
                            'Cookie': get_cookie_headers()
                        },
                        data=json.dumps({

    "TicketTypeId": 2,
    "OperatorId": 1,
    "VehicleId": 3,
    "TrailerId": 1,
    "ManifestNumber": "1234",
    "OffloadTicketId": None,
    "WorkOrderId": None,
    "LoadTypeId": 6,
    "SourceTank": None,
    "SourceTankId": None,
    "SourceOutletId": 2,
    "SourceWellPadId": None,
    "SourceVolume": 55,
    "DestinationTank": None,
    "DestinationTankId": None,
    "DestinationOutletId": 33,
    "DestinationWellPadId": None,
    "DestinationVolume": 55,
    "TotalNetVolume": None,
    "CorrectedVolume": None,
    "ObservedGravity": None,
    "BasicSedimentAndWater": None,
    "CorrectedGravity": None,
    "ObservedTemperature": None,
    "StartDate": "2022/12/19 15:33:43-05:00",
    "EndDate": "2022/12/20 15:33:43-05:00",
    "Flags": [],
    "Tolls": [],
    "Rerouted": False,
    "TicketStatusId": 3,
    "IntendedDestinationOutletId": None,
    "IntendedDestinationWellPadId": None,
    "IntendedDestinationTankId": None
}))

    resp = request.headers
    rh = dict(resp)

    loc = rh['Location']
    ticket_id = loc[-6:]

    log.info(ticket_id)
    print(ticket_id)


# @pytest.mark.do_headers_work
# def test_do_headers_work(default_headers,base_url):
#     t = Tickets.create_ticket(default_headers,base_url)
#     print(t)





