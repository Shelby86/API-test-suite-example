import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets


@pytest.mark.driver_milk_run_tickets
class TestDriverMilkRunTickets:

    ticket_types = FO.open_json_file(file_name='Data/ticket_types.json')
    # Keep destination the same
    # Change the source
    load_type = FO.open_json_file(file_name='Data/load_types.json')

    @pytest.mark.test_milk_run_simple
    def test_milk_run_simple(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = self.ticket_types['driver_ticket']
        ticket = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Second Ticket
        # Do I have to attach the ID of the old ticket somewhere ?
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = self.ticket_types['driver_milk_run']
        ticket_file['SourceOutletId'] = 41
        ticket_file['AssociatedTicketId'] = ticket
        second_ticket = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Assert tickets are found, types are correct
        # Not sure how to verify they are connected

        sql_query = f"""SELECT Id, TicketTypeId, Enabled
                                FROM dbo.ticket
                                WHERE Id = {ticket}"""
        db_value = DB.query_runner_as_dict(db=db, query=sql_query)

        assert db_value['results'][0]['TicketTypeId'] == self.ticket_types['driver_ticket']
        assert db_value['results'][0]['Enabled'] == True

        # Assert the same for second ticket
        sql_query = f"""SELECT Id, TicketTypeId, Enabled, AssociatedTicketId
                                        FROM dbo.ticket
                                        WHERE Id = {second_ticket}"""
        db_value = DB.query_runner_as_dict(db=db, query=sql_query)

        assert db_value['results'][0]['TicketTypeId'] == self.ticket_types['driver_milk_run']
        assert db_value['results'][0]['Enabled'] == True
        assert db_value['results'][0]['AssociatedTicketId'] == int(ticket)


    def test_milk_run_prod_to_prod(self,default_headers,base_url,db):
        pass


    def test_milk_run_completion_flowback(self):
        pass

    def test_milk_run_facilities_fresh(self):
        pass

    def test_milk_run_drilling_fresh(self):
        pass


    def test_delete_milk_run(self):
        pass


