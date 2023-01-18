import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets

class TestDriverNptTickets:

    load_types = FO.open_json_file(file_name='Data/load_types.json')
    ticket_types = FO.open_json_file(file_name='Data/ticket_types.json')
    ticket_file = FO.open_json_file(file_name='Data/ticket.json')
    npt_ticket = FO.open_json_file(file_name='Data/npt_ticket.json')

    @pytest.mark.driver_billable_npt
    def test_driver_npt_billable(self,base_url,default_headers,db):
        # create a regular ticket
        data = self.ticket_file
        ticket = Tickets.create_ticket(default_headers=default_headers, base_url=base_url, file=data)

        # add the ticket number to the npt
        file = self.npt_ticket
        file['TicketId'] = ticket

        # create npt ticket
        npt_ticket = Tickets.create_npt_ticket(base_url=base_url, default_headers=default_headers,
                                               file=file)
        # assert the ticket was created in the db
        sql = f""" SELECT Id,TicketTypeId, Billable,TicketId
                    FROM dbo.NonProductiveTimeTicket
                    WHERE Id = {npt_ticket}"""

        # Assert ticket was found
        sql_npt = DB.query_runner_as_dict(db, query=sql)

        assert sql_npt['results'][0]['Id']
        assert sql_npt['results'][0]['Billable'] == True
        assert sql_npt['results'][0]['TicketTypeId'] == self.ticket_types['driver_npt']

    @pytest.mark.driver_non_billable_npt
    def test_driver_non_billable_npt(self,base_url,default_headers,db):
        # create a regular ticket
        data = self.ticket_file
        ticket = Tickets.create_ticket(default_headers=default_headers, base_url=base_url, file=data)

        # add the ticket number to the npt
        file = self.npt_ticket
        file['TicketId'] = ticket
        file['Billable'] = 0

        # create npt ticket
        npt_ticket = Tickets.create_npt_ticket(base_url=base_url, default_headers=default_headers,
                                               file=file)
        # assert the ticket was created in the db
        sql = f""" SELECT Id,TicketTypeId, Billable,TicketId
                            FROM dbo.NonProductiveTimeTicket
                            WHERE Id = {npt_ticket}"""

        # Assert ticket was found
        sql_npt = DB.query_runner_as_dict(db, query=sql)

        assert sql_npt['results'][0]['Id']
        assert sql_npt['results'][0]['Billable'] == False
        assert sql_npt['results'][0]['TicketTypeId'] == self.ticket_types['driver_npt']

