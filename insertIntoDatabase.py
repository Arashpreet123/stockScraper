import pyodbc
import csv
from datetime import date

connection = pyodbc.connect(
    'DRIVER={ODBC DRIVER 17 for SQL Server};'
    'SERVER=MSI;'
    'DATABASE=stocks;'
    'Trusted_connection=yes;'
)

cursor = connection.cursor()

csv_file = 'uci_datasets.csv'

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    # print(date.today())
    # exit
    for row in reader:
        print(f"Processing row: {row}")
            
        pe_ratio = float(row[3].strip()) 
        print(row[4])
        if row[4] == '--':
            dividend_yield = 0
        else:
            dividend_yield = row[4].split(' ')[0].strip()

        row[5] = row[5].replace('%', '').strip() 
        row[5] = float(row[5])

        cursor.execute('''
            INSERT INTO stockData (stockName, livePrice, dayChange, peRatio, yield, ROI, EPS, stockDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row[0],  # Stock Name
            float(row[1]),  # Live Price
            float(row[2]),  # Day Change
            pe_ratio,  # PE Ratio
            dividend_yield,  # Forward Dividend
            row[5],  # ROI
            float(row[6]),  # EPS
            # date.today()
        ))

connection.commit()
connection.close()

print("Finished importing data")