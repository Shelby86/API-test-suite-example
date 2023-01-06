import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets


class TestDriverAltTickets:

    load_types = FO.open_json_file(file_name='Data/load_types.json')

    @pytest.mark.driver_alt
    def test_driver_alt(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = 6
        alt_ticket = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Assert alt ticket in the DB
        sql = f"""SELECT  TicketId
        FROM audit.Ticket
        WHERE TicketId = {alt_ticket}"""
        db_ticket = DB.query_runner_as_dict(db,query=sql)
        
        assert db_ticket['results'][0]['TicketId']

    @pytest.mark.driver_alt_load_type_prod_prod
    def test_driver_alt_load_type_prod_prod(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = 6
        ticket_file['LoadTypeId'] = self.load_types['prod_prod']

        ticket_id = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Assert ticket in the DB
        sql = f"""SELECT  TicketId,TicketTypeId,LoadTypeId
                FROM audit.Ticket
                WHERE TicketId = {ticket_id}"""

        db_ticket = DB.query_runner_as_dict(db,query=sql)
        assert db_ticket['results'][0]['TicketTypeId'] == 6
        assert db_ticket['results'][0]['LoadTypeId'] == self.load_types['prod_prod']

    @pytest.mark.driver_alt_load_type_comp_flo
    def test_driver_alt_load_type_comp_flo(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = 6
        ticket_file['LoadTypeId'] = self.load_types['comp_flo']

        ticket_id = Tickets.create_ticket(default_headers, base_url, file=ticket_file)

        # Assert ticket in the DB
        sql = f"""SELECT  TicketId,TicketTypeId,LoadTypeId
                        FROM audit.Ticket
                        WHERE TicketId = {ticket_id}"""

        db_ticket = DB.query_runner_as_dict(db, query=sql)
        assert db_ticket['results'][0]['TicketTypeId'] == 6
        assert db_ticket['results'][0]['LoadTypeId'] == self.load_types['comp_flo']

    @pytest.mark.driver_alt_facilities_fresh
    def test_driver_alt_facilities_fresh(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = 6
        ticket_file['LoadTypeId'] = self.load_types['facilities_fresh']

        ticket_id = Tickets.create_ticket(default_headers, base_url, file=ticket_file)

        # Assert ticket in the DB
        sql = f"""SELECT  TicketId,TicketTypeId,LoadTypeId
                                FROM audit.Ticket
                                WHERE TicketId = {ticket_id}"""

        db_ticket = DB.query_runner_as_dict(db, query=sql)
        assert db_ticket['results'][0]['TicketTypeId'] == 6
        assert db_ticket['results'][0]['LoadTypeId'] == self.load_types['facilities_fresh']

    @pytest.mark.driver_alt_load_type_drilling_fetch
    def test_driver_alt_load_type_drilling_fetch(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = 6
        ticket_file['LoadTypeId'] = self.load_types['drilling_fetch']

        ticket_id = Tickets.create_ticket(default_headers, base_url, file=ticket_file)

        # Assert ticket in the DB
        sql = f"""SELECT  TicketId,TicketTypeId,LoadTypeId
                                        FROM audit.Ticket
                                        WHERE TicketId = {ticket_id}"""

        db_ticket = DB.query_runner_as_dict(db, query=sql)
        assert db_ticket['results'][0]['TicketTypeId'] == 6
        assert db_ticket['results'][0]['LoadTypeId'] == self.load_types['drilling_fetch']


