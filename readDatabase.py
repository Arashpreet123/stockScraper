import pyodbc
import csv
from datetime import date

connection = pyodbc.connect(
    'DRIVER={ODBC DRIVER 17 for SQL Server};'
    'SERVER=MSI;'
    'DATABASE=stocks;'
    'Trusted_connection=yes;'
)

# cursor = connection.cursor()

try:
    with connection.cursor() as cursor:
        # Read data from database
        sql = "SELECT * FROM stockData"
        cursor.execute(sql)

        # Fetch all rows
        rows = cursor.fetchall()

        # Print results
        for row in rows:
            print(row)
finally:
    connection.close()