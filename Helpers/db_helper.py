import struct

import pyodbc


class DBHelper:

    def query_runner_as_dict(db, query):
        cursor = db
        cursor.execute(query)

        return {'results':
                    [dict(zip([column[0] for column in cursor.description], row))
                     for row in cursor.fetchall()]}

    def query_runner_as_list(db, query):
        cursor = db
        cursor.execute(query)

        cursor.execute(query)
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()

        return row

    def get_db_ticket_details(db,ticket_id):
        query = f"""SELECT
            tca.TicketId,
            sum(DurationAllocatedValue) as 'Ticket DurationAllocatedValue(D.A.V.)',
            sum(BarrelAllocatedValue) as 'Sum of Bbls',
            (SELECT cast((t.BillableTimeSeconds / 60.00 / 60.00) as decimal(18,8)) FROM Ticket t where id = tca.TicketId) as 'Ticket bill. time' ,
            (SELECT CASE WHEN count(npt.ticketId) < 1 THEN 0 ELSE sum(nptca.DurationAllocatedValue) END FROM NonProductiveTimeTicketCostAllocation nptca JOIN NonProductiveTimeTicket npt on npt.id = nptca.NonproductiveTimeTicketId where npt.ticketId = tca.TicketId AND nptca.Enabled = 1 GROUP BY npt.TicketId) as 'NPT D.A.V',
            (SELECT CAST((sum(npt.BillabletimeSeconds) / 60.00 / 60.00) as decimal(18,8)) FROM NonproductiveTimeTicket npt JOIN Ticket t ON t.id = npt.ticketId where t.id = tca.ticketId AND npt.TicketStatusId != 4 AND npt.billable = 1 GROUP BY t.id) as 'NPT bill. time',
            sum(CostAllocatedValue) as 'Ticket CostAllocatedValue(C.A.V.)',
            (SELECT t.TotalAmount FROM Ticket t where id = tca.TicketId) as 'Ticket Cost' ,
            (SELECT sum(nptca.CostAllocatedValue) FROM NonProductiveTimeTicketCostAllocation nptca JOIN NonProductiveTimeTicket npt on npt.id = nptca.NonproductiveTimeTicketId where npt.ticketId = tca.TicketId AND nptca.Enabled = 1 GROUP BY npt.TicketId) as 'NPT C.A.V.',
            (SELECT sum(npt.TotalAmount) FROM NonproductiveTimeTicket npt JOIN Ticket t ON t.id = npt.ticketId where t.id = tca.ticketId GROUP BY t.id) as 'NPT Cost',
            (SELECT t.DestinationVolume FROM Ticket t where id = tca.TicketId) as 'Volume',
            (SELECT lt.Name FROM Ticket t JOIN LoadType lt on lt.id = t.LoadTypeId where t.id = tca.TicketId) as 'LoadType',
            (SELECT o.name FROM Ticket t JOIN Operator o on o.id = t.operatorId where t.id = tca.TicketId) as 'Operator',
            (SELECT h.name FROM Ticket t JOIN Hauler h on h.id = t.haulerId where t.id = tca.TicketId) as 'Hauler',
            (SELECT invoiceId FROM Ticket t where t.id = tca.TicketId) as 'InvoiceId',
            (SELECT ts.name FROM Ticket t JOIN TicketStatus ts ON ts.id = t.TicketStatusId where t.id = tca.TicketId) as 'TicketStatus',
            (SELECT tt.name FROM Ticket t LEFT join TicketType tt on tt.id = t.TicketTypeId where t.id = tca.TicketId) as 'Ticket Type',
            (SELECT cnr.Rate FROM Ticket t
                LEFT JOIN ContractRate cnr on cnr.id = t.ContractRateId
                    AND cnr.enabled = 1
                where t.id = tca.TicketId) as 'Ticket Rate'
        FROM TicketCostAllocation tca
        JOIN Ticket t on t.id = tca.TicketId
        WHERE 
            t.id = {ticket_id}
            AND tca.enabled = 1
        GROUP BY TicketId
        ORDER BY TicketId"""

        sql = DBHelper.query_runner_as_dict(db, query=query)

        return sql

    def get_main_ticket_calculated_cost(db,ticket_id,bbls,ticket_time):
        query = f"""SET NOCOUNT ON exec getticketrate {ticket_id};"""
        sql = DBHelper.query_runner_as_dict(db, query=query)

        rate = sql['results'][0]['Rate']
        cost_type = sql['results'][0]['CostTypeId']

        if cost_type == 1:
            total = rate * bbls
        elif cost_type == 3:
            total = rate * ticket_time
        else:
            print('That rate type has not been coded \n'
                  'Please run the QUERY: \n'
                  'SELECT Id, NAME, Description FROM dbo.CostType')

        total = round(total, 1)

        return total

    def get_npt_ticket_total(db,bbls,npt_time,npt_id):
        query = f"""SET NOCOUNT ON exec getnptrate 556743"""
        sql = DBHelper.query_runner_as_dict(db, query=query)

        npt_rate = sql['results'][0]['Rate']
        npt_cost_type = sql['results'][0]['']
        print(npt_rate)

        if npt_cost_type == 1:
            npt_total = bbls * npt_rate
        elif npt_cost_type == 3:
            npt_total = npt_time * npt_rate
        else:
            print('That rate type has not been coded \n'
                  'Please run the QUERY: \n'
                  'SELECT Id, NAME, Description FROM dbo.CostType')

        npt_total = round(npt_total, 1)

        return npt_total

    def get_ticket_well_head_pct_and_allocation_costs(db,ticket_id):
        query = f"""SELECT AFENumber, AllocationPercent, RoundedPercent, BarrelAllocatedValue
        from TicketCostAllocation
        WHERE TicketId = {ticket_id};"""

        sql = DBHelper.query_runner_as_dict(db, query=query)

        return sql

        # db_pct_0910130332 = round(sql['results'][0]['AllocationPercent'], 2)
        # db_pct_0910130112_1 = round(sql['results'][1]['AllocationPercent'], 2)
        # db_pct_0910130112_2 = round(sql['results'][2]['AllocationPercent'], 2)
        # db_pct_0910130110 = round(sql['results'][3]['AllocationPercent'], 2)
        #
        # data = {
        #     "db_pct_0910130332": db_pct_0910130332,
        #     "db_pct_0910130112_1": db_pct_0910130112_1,
        #     "db_pct_0910130112_2": db_pct_0910130112_2,
        #     "db_pct_0910130110": db_pct_0910130110
        # }
        #
        # return data

    def get_npt_pcts_prod(db,npt_id):
        query = f"""SELECT AllocationPercent, RoundedPercent, DurationAllocatedValue, CostAllocatedValue
        from NonProductiveTimeTicketCostAllocation
        WHERE NonProductiveTimeTicketId = {npt_id}"""
        sql = DBHelper.query_runner_as_dict(db, query=query)

        return sql





















