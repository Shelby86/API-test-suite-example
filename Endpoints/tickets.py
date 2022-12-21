import requests
from requests import Session
sess = Session()
import json

class Tickets():

    @staticmethod
    def create_ticket(default_headers,base_url):
        request = sess.post(url=f'{base_url}/ticket',
                            headers=default_headers,
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

        return ticket_id