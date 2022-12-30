import pytest
from Endpoints.tickets import Tickets
from Helpers.file_opener import FileOpener as FO
from Helpers.db_helper import DBHelper as DB


class TestTickets():


    @pytest.mark.create_basic_ticket
    def test_create_ticket(self,default_headers,db,base_url):
        file = FO.open_file(file_name='ticket.json')

        ticket = Tickets.create_ticket(default_headers=default_headers,base_url=base_url,file=file)

        assert ticket, 'Ticket was not created'

        # to do get the sql query to get the ticket id
        sql_query = """SELECT Id
                        FROM dbo.ticket
                        WHERE Id = 782926"""
        db_value = DB.query_runner_as_dict(db=db,query=sql_query)

        assert db_value, 'Ticket was not found in the Database'
    
    # @pytest.mark.delete_basic_ticket
    # def delete_basic_ticket():
    #     file = FO.open_file(file_name='tests/Data/ticket.json')
    #     ticket = Tickets.create_ticket(file=file)
    #
    #     assert ticket, 'Ticket was not created'
    #
    #     deleted = Tickets.delete_ticket(ticket_id=ticket)
    #
    #     print(deleted)
    #
    # @pytest.mark.headers
    # def test_headers(self,default_headers):
    #     print(default_headers)

        




    