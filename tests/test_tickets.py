import json
import logging

import pytest
from Endpoints.tickets import Tickets
from Helpers.file_opener import FileOpener as FO
from Helpers.db_helper import DBHelper as DB


@pytest.mark.tickets
class TestTickets():

    @pytest.mark.create_basic_ticket
    def test_create_ticket(self,default_headers,db,base_url):
        data = FO.open_json_file(file_name='Data/ticket.json')
        ticket = Tickets.create_ticket(default_headers=default_headers,base_url=base_url,file=data)
        print(ticket)
        logging.info(ticket)

        # assert ticket, 'Ticket was not created'
        #
        # # to do get the sql query to get the ticket id
        # sql_query = f"""SELECT Id
        #                 FROM dbo.ticket
        #                 WHERE Id = {ticket}"""
        # db_value = DB.query_runner_as_dict(db=db,query=sql_query)
        #
        # assert db_value['results'][0]['Id'], 'Ticket was not found in the Database'

    @pytest.mark.delete_simple_ticket
    def test_delete_simple_ticket(self,default_headers,base_url,db):
        file = FO.open_json_file(file_name='Data/ticket.json')
        ticket = Tickets.create_ticket(default_headers=default_headers, base_url=base_url, file=file)
        deleted = Tickets.delete_ticket(default_headers,base_url,ticket_id=ticket)
        assert deleted['status_code'] == 200, f'Error deleting ticket. \nStatus is: {deleted["status_code"]}'

        # look at status in the db to confirm

        sql = f"""  SELECT Enabled,Id
                    FROM dbo.ticket
                    WHERE Id = {ticket}"""

        # Assert ticket is not found in the database
        db_res = DB.query_runner_as_dict(db,query=sql)
        print(db_res)
        assert db_res['results'][0]['Enabled'] == False

    @pytest.mark.create_npt_ticket
    def test_create_npt_ticket(self,default_headers,base_url,db):
        # create a regular ticket
        data = FO.open_json_file(file_name='Data/ticket.json')
        ticket = Tickets.create_ticket(default_headers=default_headers, base_url=base_url, file=data)

        # add the ticket number to the npt
        file = FO.open_json_file(file_name='Data/npt_ticket.json')
        file['TicketId'] = ticket

        # create npt ticket
        npt_ticket = Tickets.create_npt_ticket(base_url=base_url,default_headers=default_headers,
                                               file=file)
        # assert the ticket was created in the db
        sql = f""" SELECT Id
                    FROM dbo.NonProductiveTimeTicket
                    WHERE Id = {npt_ticket}"""

        # Assert ticket was found
        sql_npt = DB.query_runner_as_dict(db,query=sql)

        assert sql_npt['results'][0]['Id']

    @pytest.mark.delete_npt_ticket
    def test_delete_npt_ticket(self,base_url,default_headers,db):
        # create a regular ticket
        data = FO.open_json_file(file_name='Data/ticket.json')
        ticket = Tickets.create_ticket(default_headers=default_headers, base_url=base_url, file=data)

        # add the ticket number to the npt
        file = FO.open_json_file(file_name='Data/npt_ticket.json')
        file['TicketId'] = ticket

        # create npt ticket
        npt_ticket = Tickets.create_npt_ticket(base_url=base_url, default_headers=default_headers,
                                               file=file)

        # Delete Npt Ticket
        deleted_ticket = Tickets.delete_npt_ticket(base_url=base_url,default_headers=default_headers,
                                                   ticket_id=npt_ticket)

        assert deleted_ticket['status_code'] == 200, f'Ticket was not deleted.' \
                                                     f'\nStatus code: {deleted_ticket["status_code"]}'

        # Assert status is disabled in the DB
        sql = f"""SELECT Id,Enabled
                  FROM dbo.NonProductiveTimeTicket
                  WHERE Id = {npt_ticket}"""

        sql_ticket = DB.query_runner_as_dict(db,query=sql)

        assert sql_ticket['results'][0]['Enabled'] == False, "Ticket was not deleted in the DB"






















    


        




    