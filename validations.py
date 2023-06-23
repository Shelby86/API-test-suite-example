from Helpers.db_helper import DBHelper
import pyodbc


def db():
    server = 'geminishaledev01.database.windows.net'
    database = 'GeminiShale'
    username = 'QA Automation'
    password = '3K8V999CreIYZoY'
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';ENCRYPT=yes;UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    return cursor

id = 1568933

# Get the main ticket rate and type
query = f"""SET NOCOUNT ON SET ANSI_WARNINGS OFF exec getticketrate {id};"""
sql = DBHelper.query_runner_as_dict(db=db(),query=query)

rate = sql['results'][0]['Rate']
cost_type = sql['results'][0]['CostTypeId']

print(cost_type)

# Get the main ticket time and barrels
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
    t.id = 1568933
    AND tca.enabled = 1
GROUP BY TicketId
ORDER BY TicketId"""

sql = DBHelper.query_runner_as_dict(db=db(),query=query)


# round all the value to decimel place 1 for asserts
ticket_time = round(sql['results'][0]['Ticket bill. time'],1)
bbls = round(sql['results'][0]['Sum of Bbls'],1)
db_ticket_cost = round(sql['results'][0]['Ticket Cost'],1)
npt_cost = round(sql['results'][0]['NPT Cost'],1)
npt_time = round(sql['results'][0]['NPT bill. time'],1)

# Write an if / else statement to calculate either the rate * bbls or rate * time

if cost_type == 1:
    total = rate * bbls
elif cost_type == 3:
    total = rate * ticket_time
else:
    print('That rate type has not been coded \n'
          'Please run the QUERY: \n'
          'SELECT Id, NAME, Description FROM dbo.CostType')

total = round(total,1)

# Verify the rate * cost type against the ticket total in the DB
assert float(total) == float(db_ticket_cost)

# Get the rate and cost type of the npt ticket
query = f"""SET NOCOUNT ON exec getnptrate 556743"""
sql = DBHelper.query_runner_as_dict(db=db(),query=query)

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

npt_total = round(npt_total,1)

assert float(npt_total) == float(npt_cost)

# Now add in the well head cost allication and you are done!



