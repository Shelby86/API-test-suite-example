import pytest
from Endpoints.tickets import Tickets
from Helpers.file_opener import FileOpener as FO
from Helpers.auth import Auth


class TestRangeTickets():

    base_ticket = FO.open_json_file(file_name='Data/ticket.json')

    @pytest.mark.create_principle_range_ticket
    def test_create_principle_range_ticket(self,principle_headers,base_url):
        data = self.base_ticket
        ticket = Tickets.create_ticket(headers=principle_headers,base_url=base_url,
                                       file_name=data)
        print(ticket)

