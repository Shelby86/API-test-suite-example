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


hauler_imp = FO.open_json_file(file_name='Data/impersonate_hauler')
ticket_file = FO.open_json_file(file_name='Data/range.json')
npt_file = FO.open_json_file(file_name="Data/principle_range_npt.json")
toll = FO.open_json_file(file_name="Data/toll.json")
operator_imp = FO.open_json_file(file_name='Data/impersonate_operator.json')
cost_file = FO.open_json_file(file_name="Data/cost_assignment.json")
approve_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')

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


    @pytest.mark.approve_ticket_as_operator
    def test_approve_ticket_as_operator(self,base_url,default_headers,db):
        # impersonate hauler
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        # approve ticket as hauler
        id = ticket['data']
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # impersonate operator
        imp_operator = Auth.impoersonate(base_url,default_headers,file=operator_imp)
        # approve ticket as operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200

        # DB Verification
        query = f"""
                SELECT Id, TicketStatusId
                FROM dbo.Ticket
                WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 8

    @pytest.mark.approve_npt_ticket_as_an_operator
    def test_approve_ticket_with_npt_as_oprtator(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Create NPT ticket
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200

        # DB Verifications
        query = f"""
                SELECT Id, TicketStatusId, TicketId
                FROM dbo.NonProductiveTimeTicket
                WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 8
        assert sql['results'][0]['TicketId'] == id

    @pytest.mark.assign_cost
    def test_assign_cost(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost as Operator
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url,cookie=imp_operator,file=cost_file)
        assert cost == 200
        time.sleep(2)
        # DB Verifications
        # status 11
        query = f"""
                SELECT Id, TicketStatusId
                FROM dbo.ticket
                WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11

    @pytest.mark.assign_cost_with_npt
    def test_assign_cost_with_npt_ticket(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Create NPT ticket
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert cost == 200
        time.sleep(2)
        # DB Verifications
        # status 11
        query = f"""
                       SELECT Id, TicketStatusId
                        FROM dbo.ticket
                        WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11

        query = f"""
                        SELECT Id, TicketStatusId, TicketId
                        FROM dbo.NonProductiveTimeTicket
                        WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 11

    @pytest.mark.cost_assign_review_npt
    def test_cost_assign_review_with_npt(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Create NPT ticket
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert cost == 200
        approve_cost_file['Tickets'][0] = id
        cost_review = CostAssignmentReview.approve_cost(base_url,default_headers,cookie=imp_operator,
                                                        file=approve_cost_file)
        assert cost_review == 200

        # DB Verifications
        query = f"""
                       SELECT Id, TicketStatusId
                       FROM dbo.ticket
                       WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

        query = f"""
                                SELECT Id, TicketStatusId, TicketId
                                FROM dbo.NonProductiveTimeTicket
                                WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

    @pytest.mark.review_cost
    def test_review_cost(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Create NPT ticket
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert cost == 200
        approve_cost_file['Tickets'][0] = id
        cost_review = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                        file=approve_cost_file)
        assert cost_review == 200

        # DB Verifications
        query = f"""
                              SELECT Id, TicketStatusId
                              FROM dbo.ticket
                              WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16


    @pytest.mark.pend_hauler_inv_npt_toll
    def test_pend_hauler_inv_npt_toll(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        # Create NPT ticket
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        # Add the toll
        toll['TicketId'] = ticket['data']
        pay_the_toll_troll = Toll.create_toll(base_url, cookie=impersonate, file=toll)
        # Verify the toll
        query = f"""
                        SELECT Id, TicketId, Price
                        FROM dbo.TicketToll
                        WHERE TicketId = {id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketId'] == id
        assert sql['results'][0]['Price'] == 10.00

        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert cost == 200

        # Pause and Verify status 11 in the DB
        time.sleep(2)
        query = f"""
                               SELECT Id, TicketStatusId
                                FROM dbo.ticket
                                WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11

        query = f"""
                                SELECT Id, TicketStatusId, TicketId
                                FROM dbo.NonProductiveTimeTicket
                                WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11
        #Approve cost
        print(id)
        approve_cost_file['Tickets'][0] = id
        cost_review = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                        file=approve_cost_file)
        assert cost_review == 200

        # DB Verifications
        query = f"""
                              SELECT Id, TicketStatusId
                              FROM dbo.ticket
                              WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

        query = f"""
                                       SELECT Id, TicketStatusId, TicketId
                                       FROM dbo.NonProductiveTimeTicket
                                       WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

    @pytest.mark.pend_hauler_inv_npt
    def test_pend_hauler_inv_npt(self, base_url, default_headers, db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        print(id)
        # Create NPT ticket
        npt_file['TicketId'] = ticket['data']
        npt_ticket = Tickets.create_npt_ticket(base_url, file=npt_file, cookie=impersonate)
        npt_id = npt_ticket['data']
        # Approve Ticket as a Hauler
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assign Cost
        cost_file['TicketIds'][0] = id
        cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert cost == 200

        # Pause and Verify status 11 in the DB
        time.sleep(2)
        query = f"""
                                   SELECT Id, TicketStatusId
                                    FROM dbo.ticket
                                    WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11

        query = f"""
                                    SELECT Id, TicketStatusId, TicketId
                                    FROM dbo.NonProductiveTimeTicket
                                    WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11
        # Approve cost
        approve_cost_file['Tickets'][0] = id
        cost_review = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                        file=approve_cost_file)
        assert cost_review == 200

        # DB Verifications
        query = f"""
                                  SELECT Id, TicketStatusId
                                  FROM dbo.ticket
                                  WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

        query = f"""
                                           SELECT Id, TicketStatusId, TicketId
                                           FROM dbo.NonProductiveTimeTicket
                                           WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16

        # get the ticket details
        sql= DB.get_db_ticket_details(db,ticket_id=id)
        ticket_time = round(sql['results'][0]['Ticket bill. time'], 1)
        bbls = round(sql['results'][0]['Sum of Bbls'], 1)
        db_ticket_cost = round(sql['results'][0]['Ticket Cost'], 1)
        npt_cost = round(sql['results'][0]['NPT Cost'], 1)
        npt_time = round(sql['results'][0]['NPT bill. time'], 1)

        # Get the main ticket rate and cost type total
        calculated_total = DB.get_main_ticket_calculated_cost(db,ticket_id=id,bbls=bbls,
                                                              ticket_time=ticket_time)

        assert float(calculated_total) == float(db_ticket_cost)

        # Get the npt calculated total
        npt_calculated_total = DB.get_npt_ticket_total(db,bbls,npt_time,npt_id)

        assert float(npt_calculated_total) == float(npt_cost)

        # Verify the Well head percent and total
        # Json file Values
        pct_0910130332 = 0.30
        pct_0910130112_1 = 0.20
        pct_0910130112_2 = 0.30
        pct_0910130110 = 0.20

        ticket_pcts = DB.get_ticket_well_head_pct(db,ticket_id=id)
        print(ticket_pcts)

        # assert float(pct_0910130332) == ticket_pcts['db_pct_0910130332']
        # assert float(pct_0910130112_1) == ticket_pcts['db_pct_0910130112_1']
        # assert float(pct_0910130112_2) == ticket_pcts['db_pct_0910130112_2']
        # assert float(pct_0910130110) == ticket_pcts['db_pct_0910130110']

        # Verify the npt ticket pcts
        npt_pcts = DB.get_npt_pcts_prod(db,npt_id)





























