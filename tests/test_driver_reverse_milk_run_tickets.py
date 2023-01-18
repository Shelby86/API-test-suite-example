import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets



class TestDriverReverseMilkRun:

    # Keep the source the same
    # Change the volume on the drop off
    # Change the destination for the remaining drop off
    load_types = FO.open_json_file(file_name='Data/load_types.json')
    ticket_types = FO.open_json_file(file_name='Data/ticket_types.json')

    @pytest.mark.reverse_milk_run_simple
    def test_reverse_milk_run(self,base_url,default_headers,db):
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = self.ticket_types['driver_ticket']
        ticket_file['DestinationVolume'] = 35
        ticket_file['DestinationOutletId'] = 93
        ticket_file['IntendedDestinationOutletId'] = 93
        ticket = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Second Ticket
        ticket_file = FO.open_json_file(file_name='Data/ticket.json')
        ticket_file['TicketTypeId'] = self.ticket_types['driver_reverse_milk_run']
        ticket_file['DestinationWellPadId'] = 974
        ticket_file['SourceVolume'] = 20
        ticket_file['DestinationVolume'] = 20
        ticket_file['IntendedDestinationOutletId'] = 93
        ticket_file['AssociatedTicketId'] = ticket
        second_ticket = Tickets.create_ticket(default_headers,base_url,file=ticket_file)

        # Assert First Ticket in the db
        # Can add other verifications
        sql_query = f"""SELECT Id, TicketTypeId, Enabled
                                       FROM dbo.ticket
                                       WHERE Id = {ticket}"""
        db_value = DB.query_runner_as_dict(db=db, query=sql_query)

        assert db_value['results'][0]['TicketTypeId'] == self.ticket_types['driver_ticket']
        assert db_value['results'][0]['Enabled'] == True

        # Assert second ticket in DB
        sql_query = f"""SELECT Id, TicketTypeId, Enabled, AssociatedTicketId
                                                FROM dbo.ticket
                                                WHERE Id = {second_ticket}"""
        db_value = DB.query_runner_as_dict(db=db, query=sql_query)

        assert db_value['results'][0]['TicketTypeId'] == self.ticket_types['driver_reverse_milk_run']
        assert db_value['results'][0]['Enabled'] == True
        assert db_value['results'][0]['AssociatedTicketId'] == int(ticket)



