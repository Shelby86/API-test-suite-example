print(4)
import pyodbc


server = 'geminishaledev01.database.windows.net' 
database = 'GeminiShale' 
username = 'Automation' 
password = '0lIvquRHSRe2cvYkNiFG' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("""
            SELECT TOP (10) Account
            FROM audit.AccountCode
            """)
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()

