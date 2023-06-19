import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets
import json
from Helpers.auth import Auth
import logging as log
from Endpoints.toll import Toll

hauler_imp = FO.open_json_file(file_name='Data/impersonate_hauler')
ticket_file = FO.open_json_file(file_name='Data/range.json')
npt_file = FO.open_json_file(file_name="Data/principle_range_npt.json")
toll = FO.open_json_file(file_name="Data/toll.json")

class TestRangePrinciple:


    @pytest.mark.auth_test
    def test_auths(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url,default_headers,file=hauler_imp)
        ticket = Tickets.create_ticket(base_url,cookie=impersonate,file=ticket_file)
        assert ticket['status_code'] == 201
        id =  ticket['data']

        # DB Verifications
        # Can add whatever verifications

        query = f"""
        SELECT Id
        FROM dbo.Ticket
        WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db,query=query)
        assert sql['results'][0]['Id']


    @pytest.mark.range_npt
    def test_npt_ticket(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        npt_file['TicketId'] = ticket['data']
        npt_ticket= Tickets.create_npt_ticket(base_url,file=npt_file,cookie=impersonate)
        npt_id = npt_ticket['data']
        assert ticket['status_code'] == 201
        assert ticket['data']

        # DB Asserts
        query = f"""
            SELECT Id, TicketId
            FROM dbo.NonProductiveTimeTicket
            WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['Id'] == npt_id
        assert sql['results'][0]['TicketId'] == ticket['data']

    @pytest.mark.range_principle_toll
    def test_range_prince(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        toll['TicketId'] = ticket['data']
        pay_the_toll_troll = Toll.create_toll(base_url,cookie=impersonate,file=toll)
        assert pay_the_toll_troll== 201
        id = ticket['data']

        # DB Verifications
        query = f"""
                SELECT Id, TicketId, Price
                FROM dbo.TicketToll
                WHERE TicketId = {id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketId'] == id
        assert sql['results'][0]['Price'] == 10.00



    @pytest.mark.approve_ticket
    def test_approve_ticket(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        ticket['TicketId'] = ticket['data']
        id = ticket['data']
        approved = Tickets.approve_ticket(base_url,cookie=impersonate,id=id)
        assert approved['status_code'] == 200

        # DB Verifications
        query = f"""
                SELECT TicketStatusId
                FROM dbo.Ticket
                WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 5


    @pytest.mark.approve_npt_ticket
    def test_approve_npt_ticket(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        id = ticket['data']
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # NPT ticket moves to the operator review when the parent ticket is approved

        # DB Verifications
        query = f"""
                SELECT Id, TicketStatusId
                FROM dbo.NonProductiveTimeTicket
                WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 5







