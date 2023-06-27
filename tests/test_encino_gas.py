import time

import pytest
from Helpers.db_helper import DBHelper as DB
from Helpers.file_opener import FileOpener as FO
from Endpoints.tickets import Tickets
import json
from Helpers.auth import Auth
import logging as log
from Endpoints.toll import Toll
from Endpoints.assign_cost import AssignCost
from Endpoints.cost_assignment_review import CostAssignmentReview
from time import sleep
from Endpoints.Impersonate.impersonate import Impersonate

class TestEncinoGas:


    ticket_52 = FO.open_json_file(file_name='Data/ticket_1450452.json')
    ticket_71 = FO.open_json_file(file_name='Data/ticket_1450671.json')
    ticket_31 = FO.open_json_file(file_name="Data/ticket_1450731.json")
    ticket_63 = FO.open_json_file(file_name='Data/ticket_1450763.json')
    ticket_26 = FO.open_json_file(file_name="Data/ticket_1451826.json")
    ticket_47 = FO.open_json_file(file_name='Data/ticket_1451847.json')
    ticket_50 = FO.open_json_file(file_name="Data/ticket_1451850.json")
    ticket_98 = FO.open_json_file(file_name="Data/ticket_1451898.json")
    ticket_06 = FO.open_json_file(file_name="Data/ticket_1451906.json")
    ticket_73 = FO.open_json_file(file_name="Data/ticket_1451973.json")
    ticket_files = [ticket_52, ticket_71, ticket_31, ticket_63, ticket_26, ticket_47, ticket_50, ticket_98,
                    ticket_06, ticket_73]

    hauler = FO.open_json_file(file_name='Data/impersonate_hauler')
    hauler['HaulerId'] = 26
    operator_imp = FO.open_json_file(file_name='Data/operator_encino.json')


    npt_file = FO.open_json_file(file_name="Data/npt_ticket_encino_gas.json")

    @pytest.mark.encino_gas_invoice
    # npt not working
    def test_encino_gas_invoice(self,db,base_url,default_headers):
        ticket_ids = []
        npt_ids = []
        for file in self.ticket_files:
            # Impersonate Hauler
            imp_hauler = Auth.impoersonate(base_url,default_headers,file=self.hauler)
            # Create the ticket
            ticket = Tickets.create_ticket(base_url,cookie=imp_hauler,file=file)
            id = ticket['data']
            assert ticket['status_code'] == 201
            # gather the ticket ids in a list here
            ticket_ids.append(id)
            # Create npt
            self.npt_file['TicketId'] = id
            npt_ticket = Tickets.create_npt_ticket(base_url,file=self.npt_file,cookie=imp_hauler)
            npt_id = npt_ticket['data']
            # approve ticket
            approved = Tickets.approve_ticket(base_url,cookie=imp_hauler,id=id)

            # Approve npt
            # npt_approved = Tickets.approve_npt_ticket(base_url,id-npt_id,cookie=imp_hauler)
            # print(npt_approved)
            # Change the values in the not file to match the ticket file

            # self.npt_file['DriverId'] == file['']

            # # gather npt ids in a list here
            #
            # # Approve ticket as a Hauler
            # approved = Tickets.approve_ticket(base_url,cookie=imp_hauler,id=id)
            # assert approved['status_code'] == 200
            # # verify the ticket status is in operator review
            # # Approve NPT
            query = f"""
                                               SELECT Id, TicketStatusId
                                                FROM dbo.ticket
                                                WHERE Id = {id}"""
            sql = DB.query_runner_as_dict(db, query=query)
            assert sql['results'][0]['TicketStatusId'] == 5

            query = f"""
                                                SELECT Id, TicketStatusId, TicketId
                                                FROM dbo.NonProductiveTimeTicket
                                                WHERE Id = {npt_id}"""

            sql = DB.query_runner_as_dict(db, query=query)

            assert sql['results'][0]['TicketStatusId'] == 5

        #     # Impersonate_operator
        #     operator_cookie = Impersonate.impersonate_hauler(base_url,default_headers,file=self.operator_imp)
        #     # Approve cost as Operator
        #     approved = Tickets.approve_ticket(base_url,cookie=operator_cookie,id=id)
        #     assert approved['status_code'] == 200
        #     time.sleep(2)
        #     # Verify Ticket Status is assign cost
        #     query = f"""
        #                                                   SELECT Id, TicketStatusId
        #                                                    FROM dbo.ticket
        #                                                    WHERE Id = {id}"""
        #     sql = DB.query_runner_as_dict(db, query=query)
        #     assert sql['results'][0]['TicketStatusId'] == 8
        #     time.sleep(2)
        #
        #     query = f"""
        #                                                    SELECT Id, TicketStatusId, TicketId
        #                                                    FROM dbo.NonProductiveTimeTicket
        #                                                    WHERE Id = {npt_id}"""
        #
        #     sql = DB.query_runner_as_dict(db, query=query)
        #     assert sql['results'][0]['TicketStatusId'] == 8
        #     # Assign cost
        #     # Get the detsils of the cost assignment per id
        #     query = f"""select Top 10 Id from Ticket where InvoiceID=24049;"""
        #     sql = DB.query_runner_as_dict(db, query)
        #     ids = []
        #     ticket_details = DB.get_db_ticket_details(db,ticket_id=id)
        # print(ticket_details)


        # Complete Cost in a batch
        # Verify cost

    @pytest.mark.ticket_52
    def test_file_52(self,base_url,default_headers,db):
        # Impersonate Hauler
        imp_hauler = Auth.impoersonate(base_url, default_headers, file=self.hauler)
        # Create the ticket
        ticket = Tickets.create_ticket(base_url, cookie=imp_hauler, file=self.ticket_52)
        id = ticket['data']
        assert ticket['status_code'] == 201
        # gather the ticket ids in a list here
        # Create npt
        self.npt_file['TicketId'] = id
        npt_ticket = Tickets.create_npt_ticket(base_url, file=self.npt_file, cookie=imp_hauler)
        npt_id = npt_ticket['data']
        # approve ticket
        approved = Tickets.approve_ticket(base_url, cookie=imp_hauler, id=id)
        # Verify status
        query = f"""
                                                       SELECT Id, TicketStatusId
                                                        FROM dbo.ticket
                                                        WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 5

        query = f"""
                                                        SELECT Id, TicketStatusId, TicketId
                                                        FROM dbo.NonProductiveTimeTicket
                                                        WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 5

        # impersonate operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=self.operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200

        # Verify tickets are in assign cost
        query = f"""
                                                               SELECT Id, TicketStatusId
                                                                FROM dbo.ticket
                                                                WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 8

        query = f"""
                                                                SELECT Id, TicketStatusId, TicketId
                                                                FROM dbo.NonProductiveTimeTicket
                                                                WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 8

        # Assign cost
        ticket_details = DB.get_db_ticket_details(db,ticket_id=1450452)
        print(ticket_details)

