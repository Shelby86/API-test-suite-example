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

# When calculating rate * time, time = time/60/60. calculaed value and db values must be cast as a float

class TestEncinoGas:


    ticket_52 = FO.open_json_file(file_name='Data/ticket_1450452.json')
    ticket_39 = FO.open_json_file(file_name='Data/ticket_1454839.json')
    ticket_34 = FO.open_json_file(file_name="Data/invoice_files/ticket_34.json")
    ticket_53 = FO.open_json_file(file_name="Data/invoice_files/tickets/ticket_53.json")

    ticket_files = []

    hauler = FO.open_json_file(file_name='Data/impersonate_hauler')
    hauler['HaulerId'] = 26
    operator_imp = FO.open_json_file(file_name='Data/operator_encino.json')
    npt_file = FO.open_json_file(file_name="Data/npt_ticket_encino_gas.json")

    npt_39 = FO.open_json_file(file_name="Data/npt_1454839.json")
    npt_34 = FO.open_json_file(file_name="Data/invoice_files/npt_ticket_34.json")
    npt_53 = FO.open_json_file(file_name="Data/invoice_files/npt_tickets/npt_53.json")


    npt_files = []

    invoice = 24049

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
        print(id)
        assert ticket['status_code'] == 201
        approved = Tickets.approve_ticket(base_url, cookie=imp_hauler, id=id)
        # Verify status
        query = f"""
                                                       SELECT Id, TicketStatusId
                                                        FROM dbo.ticket
                                                        WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 5

        # query = f"""
        #                                                 SELECT Id, TicketStatusId, TicketId
        #                                                 FROM dbo.NonProductiveTimeTicket
        #                                                 WHERE Id = {npt_id}"""
        #
        # sql = DB.query_runner_as_dict(db, query=query)
        #
        # assert sql['results'][0]['TicketStatusId'] == 5

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

        # query = f"""
        #                                                         SELECT Id, TicketStatusId, TicketId
        #                                                         FROM dbo.NonProductiveTimeTicket
        #                                                         WHERE Id = {npt_id}"""
        #
        # sql = DB.query_runner_as_dict(db, query=query)
        #
        # assert sql['results'][0]['TicketStatusId'] == 8

        # Assign cost
        # cost_assignment_details = DB.get_ticket_well_head_pct_and_allocation_costs(db,ticket_id=1450452)
        cost_file = FO.open_json_file(file_name='Data/cost_assign_ticket_52.json')
        cost_file['TicketIds'][0] = id
        assign_cost = AssignCost.assign_cost(base_url,cookie=imp_operator,file=cost_file)
        assert assign_cost == 200

        # Verify ticket status and npt ticket status is in cost awaiting review
        time.sleep(2)
        query = f"""
                                                                      SELECT Id, TicketStatusId
                                                                       FROM dbo.ticket
                                                                       WHERE Id = {id}"""
        # sql = DB.query_runner_as_dict(db, query=query)
        # assert sql['results'][0]['TicketStatusId'] == 11
        #
        # query = f"""
        #                                                                SELECT Id, TicketStatusId, TicketId
        #                                                                FROM dbo.NonProductiveTimeTicket
        #                                                                WHERE Id = {npt_id}"""
        #
        # sql = DB.query_runner_as_dict(db, query=query)
        #
        # assert sql['results'][0]['TicketStatusId'] == 11

        # Complete Cost
        complete_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')
        complete_cost_file['Tickets'][0] = id
        completed_cost = CostAssignmentReview.approve_cost(base_url,default_headers,cookie=imp_operator,file=complete_cost_file)
        assert completed_cost == 200

        # Verify ticket status is in Pending Hauler Invoice
        time.sleep(2)
        query = f"""
                                                                              SELECT Id, TicketStatusId
                                                                               FROM dbo.ticket
                                                                               WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16
        #
        # query = f"""
        #                                                                        SELECT Id, TicketStatusId, TicketId
        #                                                                        FROM dbo.NonProductiveTimeTicket
        #                                                                        WHERE Id = {npt_id}"""
        #
        # sql = DB.query_runner_as_dict(db, query=query)
        #
        # assert sql['results'][0]['TicketStatusId'] == 16

        # Verify cost og the original ticket against the cost in the mimicked ticket
        query = f"""
                    SELECT TotalAmount
                    FROM dbo.Ticket
                    WHERE Id = {id}"""

        # New Ticket Details
        ticket_details = DB.get_db_ticket_details(db,ticket_id=id)
        total_amount = ticket_details['results'][0]['Ticket Cost']


        # Verify total pcts are 100
        pcts = DB.get_pcts(db,ticket_id=id)
        dec_pcts = []
        for entry in pcts['results']:
            dec_pct = entry['AllocationPercent']
            dec_pcts.append(dec_pct)

        pct_sum = sum(dec_pcts)
        pct_sum = round(pct_sum,3)
        assert pct_sum in (1.000, 0.999)

        # Total of BarrelAllocatedValue = DestinationVolume on Ticket
        barrel_allocated = DB.get_ticket_well_head_pct_and_allocation_costs(db,ticket_id=id)
        bbl_allocated_values = []
        for entry in barrel_allocated['results']:
            value = entry['BarrelAllocatedValue']
            bbl_allocated_values.append(value)

        bbl_sum = sum(bbl_allocated_values)
        bbl_sum = round(bbl_sum,2)

        query = f"""SELECT SourceVolume
                FROM dbo.Ticket
                WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db,query)

        assert sql['results'][0]['SourceVolume'] == bbl_sum

        # Total of CostAllocatedValue = Total Amount on Ticket
        details = DB.get_db_ticket_details(db,ticket_id=id)
        print(details)
        total_cost_allocation = details['results'][0]['Ticket CostAllocatedValue(C.A.V.)']
        query = f"""SELECT TotalAmount
                    FROM dbo.ticket
                    WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)
        ticket_total = sql['results'][0]['TotalAmount']

        # The 8th decibel place is different
        print(ticket_total)
        print(total_cost_allocation)

        # TicketRate x CostType = TotalAmount on Ticket
        sql = DB.get_db_ticket_details(db, ticket_id=id)
        ticket_time = sql['results'][0]['Ticket bill. time']
        bbls = sql['results'][0]['Sum of Bbls']
        db_ticket_cost = sql['results'][0]['Ticket Cost']

        # Get the main ticket rate and cost type total
        calculated_total = DB.get_main_ticket_calculated_cost(db, ticket_id=id, bbls=bbls,
                                                              ticket_time=ticket_time)
        ticket_total = round(ticket_total,3)
        assert round(calculated_total,3) == ticket_total




    @pytest.mark.ticket_39
    def test_ticket_1454839(self,db,base_url,default_headers):
        # Impersonate Hauler
        imp_hauler = Auth.impoersonate(base_url, default_headers, file=self.hauler)
        # Create the ticket
        ticket = Tickets.create_ticket(base_url, cookie=imp_hauler, file=self.ticket_39)
        id = ticket['data']
        print(id)
        self.npt_39['TicketId'] = id
        npt_ticket = Tickets.create_npt_ticket(base_url,file=self.npt_39,cookie=imp_hauler)
        npt_id = npt_ticket['data']
        assert ticket['status_code'] == 201
        approved = Tickets.approve_ticket(base_url, cookie=imp_hauler, id=id)
        # Verify status
        query = f"""
                                                               SELECT Id, TicketStatusId
                                                                FROM dbo.ticket
                                                                WHERE Id = {id}"""

        time.sleep(2)
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
        # cost_assignment_details = DB.get_ticket_well_head_pct_and_allocation_costs(db,ticket_id=1450452)
        cost_file = FO.open_json_file(file_name='Data/cost_assign_ticket_39')
        cost_file['TicketIds'][0] = id
        assign_cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert assign_cost == 200

        # Verify ticket status and npt ticket status is in cost awaiting review
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

        # Complete Cost
        complete_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')
        complete_cost_file['Tickets'][0] = id
        completed_cost = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                           file=complete_cost_file)
        assert completed_cost == 200

        # Verify ticket status is in Pending Hauler Invoice
        time.sleep(2)
        query = f"""
                                                                                                    SELECT Id, TicketStatusId
                                                                                                     FROM dbo.ticket
                                                                                                     WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16
        #
        query = f"""
                                                                                             SELECT Id, TicketStatusId, TicketId
                                                                                             FROM dbo.NonProductiveTimeTicket
                                                                                             WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 16

        # Verify cost og the original ticket against the cost in the mimicked ticket
        query = f"""
                                          SELECT TotalAmount
                                          FROM dbo.Ticket
                                          WHERE Id = {id}"""

        # New Ticket Details
        ticket_details = DB.get_db_ticket_details(db, ticket_id=id)
        total_amount = ticket_details['results'][0]['Ticket Cost']

        # Verify total pcts are 100
        pcts = DB.get_pcts(db, ticket_id=id)
        dec_pcts = []
        for entry in pcts['results']:
            dec_pct = entry['AllocationPercent']
            dec_pcts.append(dec_pct)

        pct_sum = sum(dec_pcts)
        # pct here = 0.99999000 not 1
        pct_sum = round(pct_sum,3)
        assert pct_sum in (1.000, 0.999)
        print(npt_id)

        # Total of BarrelAllocatedValue = DestinationVolume on Ticket
        barrel_allocated = DB.get_ticket_well_head_pct_and_allocation_costs(db, ticket_id=id)
        bbl_allocated_values = []
        for entry in barrel_allocated['results']:
            value = entry['BarrelAllocatedValue']
            bbl_allocated_values.append(value)

        bbl_sum = sum(bbl_allocated_values)
        bbl_sum = round(bbl_sum, 2)

        query = f"""SELECT SourceVolume
                                      FROM dbo.Ticket
                                      WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)

        assert sql['results'][0]['SourceVolume'] == bbl_sum

        # Total of CostAllocatedValue = Total Amount on Ticket
        details = DB.get_db_ticket_details(db, ticket_id=id)
        total_cost_allocation = details['results'][0]['Ticket CostAllocatedValue(C.A.V.)']
        query = f"""SELECT TotalAmount
                                          FROM dbo.ticket
                                          WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)
        ticket_total = sql['results'][0]['TotalAmount']

        # The 8th decibel place is different
        # print(ticket_total)
        # print(total_cost_allocation)

        # TicketRate x CostType = TotalAmount on Ticket
        sql = DB.get_db_ticket_details(db, ticket_id=id)
        ticket_time = sql['results'][0]['Ticket bill. time']
        bbls = sql['results'][0]['Sum of Bbls']
        db_ticket_cost = sql['results'][0]['Ticket Cost']

        # Get the main ticket rate and cost type total
        calculated_total = DB.get_main_ticket_calculated_cost(db, ticket_id=id, bbls=bbls,
                                                              ticket_time=ticket_time)
        ticket_total = round(ticket_total, 3)
        assert round(calculated_total, 3) == ticket_total

        # Query to get npt billable time and total amount
        query = f"""select TotalAmount,BillableTimeSeconds, Billable, ContractID
        from NonProductiveTimeTicket 
        where ID = {npt_id};"""

        sql = DB.query_runner_as_dict(db,query)
        billable_time = sql['results'][0]['BillableTimeSeconds']
        billable_time = billable_time/60/60
        total_amount = sql['results'][0]['TotalAmount']
        # The calculated rate of billable time * rate is giving a different amount then the npt billable time
        calculated_npt_total = DB.get_npt_ticket_total(db,bbls,npt_time=billable_time,npt_id=npt_id)
        calculated_npt_total = round(calculated_npt_total,3)
        calculated_npt_total = float(calculated_npt_total)
        total_amount = round(total_amount,3)
        total_amount = float(total_amount)

        assert calculated_npt_total == total_amount

    @pytest.mark.ticket_34
    def test_ticket_34(self,base_url,db,default_headers):
        original_ticket = 1453534
        well_head = 9309, "WIANDT 12-13-6 001H"
        account_area = 5, "CPLOE"
        account_code = 1001, "800-1038"
        # Allocation pct is all even with manual distribution
        # Impersonate Hauler
        imp_hauler = Auth.impoersonate(base_url, default_headers, file=self.hauler)
        # Create the ticket
        ticket = Tickets.create_ticket(base_url, cookie=imp_hauler, file=self.ticket_34)
        id = ticket['data']
        print(id)
        self.npt_34['TicketId'] = id
        npt_ticket = Tickets.create_npt_ticket(base_url, file=self.npt_34, cookie=imp_hauler)
        npt_id = npt_ticket['data']
        assert ticket['status_code'] == 201
        approved = Tickets.approve_ticket(base_url, cookie=imp_hauler, id=id)
        # Verify status
        query = f"""
                                                                       SELECT Id, TicketStatusId
                                                                        FROM dbo.ticket
                                                                        WHERE Id = {id}"""

        time.sleep(2)
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
        # cost_assignment_details = DB.get_ticket_well_head_pct_and_allocation_costs(db,ticket_id=1450452)
        cost_file = FO.open_json_file(file_name="Data/invoice_files/assign_cost_34.json")
        cost_file['TicketIds'][0] = id
        assign_cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert assign_cost == 200

        # Verify ticket status and npt ticket status is in cost awaiting review
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

        # Complete Cost
        complete_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')
        complete_cost_file['Tickets'][0] = id
        completed_cost = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                           file=complete_cost_file)
        assert completed_cost == 200

        # Verify ticket status is in Pending Hauler Invoice
        time.sleep(2)
        query = f"""
                                                                                                            SELECT Id, TicketStatusId
                                                                                                             FROM dbo.ticket
                                                                                                             WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16
        #
        query = f"""
                                                                                                     SELECT Id, TicketStatusId, TicketId
                                                                                                     FROM dbo.NonProductiveTimeTicket
                                                                                                     WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 16

        # Verify cost og the original ticket against the cost in the mimicked ticket
        query = f"""
                                                  SELECT TotalAmount
                                                  FROM dbo.Ticket
                                                  WHERE Id = {id}"""

        # New Ticket Details
        ticket_details = DB.get_db_ticket_details(db, ticket_id=id)
        total_amount = ticket_details['results'][0]['Ticket Cost']

        # Verify total pcts are 100
        pcts = DB.get_pcts(db, ticket_id=id)
        dec_pcts = []
        for entry in pcts['results']:
            dec_pct = entry['AllocationPercent']
            dec_pcts.append(dec_pct)

        pct_sum = sum(dec_pcts)
        # pct here = 0.99999000 not 1
        pct_sum = round(pct_sum, 3)
        assert pct_sum in (1.000, 0.999)
        print(npt_id)

        # Total of BarrelAllocatedValue = DestinationVolume on Ticket
        barrel_allocated = DB.get_ticket_well_head_pct_and_allocation_costs(db, ticket_id=id)
        bbl_allocated_values = []
        for entry in barrel_allocated['results']:
            value = entry['BarrelAllocatedValue']
            bbl_allocated_values.append(value)

        bbl_sum = sum(bbl_allocated_values)
        bbl_sum = round(bbl_sum, 2)

        query = f"""SELECT SourceVolume
                                              FROM dbo.Ticket
                                              WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)

        assert sql['results'][0]['SourceVolume'] == bbl_sum

        # Total of CostAllocatedValue = Total Amount on Ticket
        details = DB.get_db_ticket_details(db, ticket_id=id)
        total_cost_allocation = details['results'][0]['Ticket CostAllocatedValue(C.A.V.)']
        query = f"""SELECT TotalAmount
                                                  FROM dbo.ticket
                                                  WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)
        ticket_total = sql['results'][0]['TotalAmount']

        # The 8th decibel place is different
        # print(ticket_total)
        # print(total_cost_allocation)

        # TicketRate x CostType = TotalAmount on Ticket
        sql = DB.get_db_ticket_details(db, ticket_id=id)
        ticket_time = sql['results'][0]['Ticket bill. time']
        bbls = sql['results'][0]['Sum of Bbls']
        db_ticket_cost = sql['results'][0]['Ticket Cost']

        # Get the main ticket rate and cost type total
        calculated_total = DB.get_main_ticket_calculated_cost(db, ticket_id=id, bbls=bbls,
                                                              ticket_time=ticket_time)
        ticket_total = round(ticket_total, 3)
        assert round(calculated_total, 3) == ticket_total

        # Query to get npt billable time and total amount
        query = f"""select TotalAmount,BillableTimeSeconds, Billable, ContractID
                from NonProductiveTimeTicket 
                where ID = {npt_id};"""

        sql = DB.query_runner_as_dict(db, query)
        billable_time = sql['results'][0]['BillableTimeSeconds']
        billable_time = billable_time / 60 / 60
        total_amount = sql['results'][0]['TotalAmount']
        # The calculated rate of billable time * rate is giving a different amount then the npt billable time
        calculated_npt_total = DB.get_npt_ticket_total(db, bbls, npt_time=billable_time, npt_id=npt_id)
        calculated_npt_total = round(calculated_npt_total, 3)
        calculated_npt_total = float(calculated_npt_total)
        total_amount = round(total_amount, 3)
        total_amount = float(total_amount)

        assert calculated_npt_total == total_amount


    @pytest.mark.ticket_53
    def test_ticket_53(self,db,base_url,default_headers):
        # Impersonate Hauler
        imp_hauler = Auth.impoersonate(base_url, default_headers, file=self.hauler)
        # Create the ticket
        ticket = Tickets.create_ticket(base_url, cookie=imp_hauler, file=self.ticket_53)
        id = ticket['data']
        print(id)
        self.npt_53['TicketId'] = id
        npt_ticket = Tickets.create_npt_ticket(base_url, file=self.npt_53, cookie=imp_hauler)
        npt_id = npt_ticket['data']
        assert ticket['status_code'] == 201
        approved = Tickets.approve_ticket(base_url, cookie=imp_hauler, id=id)
        # Verify status
        query = f"""
                                                                               SELECT Id, TicketStatusId
                                                                                FROM dbo.ticket
                                                                                WHERE Id = {id}"""

        time.sleep(2)
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
        # cost_assignment_details = DB.get_ticket_well_head_pct_and_allocation_costs(db,ticket_id=1450452)
        cost_file = FO.open_json_file(file_name="Data/invoice_files/assign_cost_files/assign_cost_53.json")
        cost_file['TicketIds'][0] = id
        assign_cost = AssignCost.assign_cost(base_url, cookie=imp_operator, file=cost_file)
        assert assign_cost == 200

        # Verify ticket status and npt ticket status is in cost awaiting review
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

        # Complete Cost
        complete_cost_file = FO.open_json_file(file_name='Data/cost_assignment_review.json')
        complete_cost_file['Tickets'][0] = id
        completed_cost = CostAssignmentReview.approve_cost(base_url, default_headers, cookie=imp_operator,
                                                           file=complete_cost_file)
        assert completed_cost == 200

        # Verify ticket status is in Pending Hauler Invoice
        time.sleep(2)
        query = f"""
                                                                                                                    SELECT Id, TicketStatusId
                                                                                                                     FROM dbo.ticket
                                                                                                                     WHERE Id = {id}"""
        sql = DB.query_runner_as_dict(db, query=query)
        assert sql['results'][0]['TicketStatusId'] == 16
        #
        query = f"""
                                                                                                             SELECT Id, TicketStatusId, TicketId
                                                                                                             FROM dbo.NonProductiveTimeTicket
                                                                                                             WHERE Id = {npt_id}"""

        sql = DB.query_runner_as_dict(db, query=query)

        assert sql['results'][0]['TicketStatusId'] == 16

        # Verify cost og the original ticket against the cost in the mimicked ticket
        query = f"""
                                                          SELECT TotalAmount
                                                          FROM dbo.Ticket
                                                          WHERE Id = {id}"""

        # New Ticket Details
        ticket_details = DB.get_db_ticket_details(db, ticket_id=id)
        total_amount = ticket_details['results'][0]['Ticket Cost']

        # Verify total pcts are 100
        pcts = DB.get_pcts(db, ticket_id=id)
        dec_pcts = []
        for entry in pcts['results']:
            dec_pct = entry['AllocationPercent']
            dec_pcts.append(dec_pct)

        pct_sum = sum(dec_pcts)
        # pct here = 0.99999000 not 1
        pct_sum = round(pct_sum, 3)
        assert pct_sum in (1.000, 0.999)
        print(npt_id)

        # Total of BarrelAllocatedValue = DestinationVolume on Ticket
        barrel_allocated = DB.get_ticket_well_head_pct_and_allocation_costs(db, ticket_id=id)
        bbl_allocated_values = []
        for entry in barrel_allocated['results']:
            value = entry['BarrelAllocatedValue']
            bbl_allocated_values.append(value)

        bbl_sum = sum(bbl_allocated_values)
        bbl_sum = round(bbl_sum, 2)

        query = f"""SELECT SourceVolume
                                                      FROM dbo.Ticket
                                                      WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)

        assert sql['results'][0]['SourceVolume'] == bbl_sum

        # Total of CostAllocatedValue = Total Amount on Ticket
        details = DB.get_db_ticket_details(db, ticket_id=id)
        total_cost_allocation = details['results'][0]['Ticket CostAllocatedValue(C.A.V.)']
        query = f"""SELECT TotalAmount
                                                          FROM dbo.ticket
                                                          WHERE Id = {id}"""

        sql = DB.query_runner_as_dict(db, query)
        ticket_total = sql['results'][0]['TotalAmount']

        # The 8th decibel place is different
        # print(ticket_total)
        # print(total_cost_allocation)

        # TicketRate x CostType = TotalAmount on Ticket
        sql = DB.get_db_ticket_details(db, ticket_id=id)
        ticket_time = sql['results'][0]['Ticket bill. time']
        bbls = sql['results'][0]['Sum of Bbls']
        db_ticket_cost = sql['results'][0]['Ticket Cost']

        # Get the main ticket rate and cost type total
        calculated_total = DB.get_main_ticket_calculated_cost(db, ticket_id=id, bbls=bbls,
                                                              ticket_time=ticket_time)
        ticket_total = round(ticket_total, 3)
        assert round(calculated_total, 3) == ticket_total












