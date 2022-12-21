import logging

from Endpoints.tickets import Tickets
from Endpoints.auth import Auth
import logging as log
import pytest
from Helpers.db_utility import DBUtility as DB

class TestTickets():

    @pytest.mark.create_ticket
    def test_create_ticket(self,base_url,default_headers):
        ticket_number = Tickets.create_ticket(default_headers,base_url)
        log.info(ticket_number)
        print(ticket_number)

        assert ticket_number

    @pytest.mark.db_maybe
    def test_db_maybe(self,create_connection):
        sql = """
        SELECT DISTINCT AccountAreaId
        FROM audit.AccountArea"""

        sel = DB.execute_selection(create_connection=create_connection,sql=sql)

        log.info(sel)
        print(sel)








