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

hauler_imp = FO.open_json_file(file_name='Data/impersonate_hauler')
ticket_file = FO.open_json_file(file_name='Data/range.json')
ticket_file['LoadTypeId'] = 1
npt_file = FO.open_json_file(file_name="Data/principle_range_npt.json")
toll = FO.open_json_file(file_name="Data/toll.json")
operator_imp = FO.open_json_file(file_name='Data/impersonate_operator.json')
cost_file = FO.open_json_file(file_name="Data/cost_assignment.json")
approve_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')

class TestRangePrincipleComp:


    @pytest.mark.auth_test_comp
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


    @pytest.mark.range_npt_comp
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

    @pytest.mark.range_principle_toll_comp
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



    @pytest.mark.approve_ticket_comp
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


    @pytest.mark.approve_npt_ticket_comp
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


    @pytest.mark.approve_ticket_as_operator_comp
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

    @pytest.mark.approve_npt_ticket_as_an_operator_comp
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

    @pytest.mark.assign_cost_comp
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

        # DB Verifications
        # status 11
        query = f"""
                SELECT Id, TicketStatusId
                FROM dbo.ticket
                WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 11

    @pytest.mark.assign_cost_with_npt_comp
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

    @pytest.mark.cost_assign_review_npt_comp
    def test_cost_assign_review_with_npt(self,base_url,default_headers,db):
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

        approve_cost_file['Tickets'][0] = id
        cost_review = CostAssignmentReview.approve_cost(base_url,default_headers,cookie=imp_operator,
                                                        file=approve_cost_file)

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

    @pytest.mark.review_cost_comp
    def test_review_cost(self,base_url,default_headers,db):
        impersonate = Auth.impoersonate(base_url, default_headers, file=hauler_imp)
        # create ticket as hauler
        ticket = Tickets.create_ticket(base_url, cookie=impersonate, file=ticket_file)
        id = ticket['data']
        approved = Tickets.approve_ticket(base_url, cookie=impersonate, id=id)
        assert approved['status_code'] == 200
        # Impersonate Operator
        imp_operator = Auth.impoersonate(base_url, default_headers, file=operator_imp)
        # Approve Ticket as an Operator
        approved = Tickets.approve_ticket(base_url, cookie=imp_operator, id=id)
        assert approved['status_code'] == 200
        # Assert DB validation Ticket is in cost assignment
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

















