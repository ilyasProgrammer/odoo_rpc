import pyodbc
import pandas as pd
import numpy as np

server = '*'
database = '*'
username = '*'
password = '*'
cnxn = pyodbc.connect('DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

df = pd.read_sql_query('select * from dbo.com', cnxn)

# Check if no current transaction
if not bool(df['ERP'].values[0]):
    # Request for new transaction
    cursor.execute("UPDATE dbo.com SET ERP = 1")
    cnxn.commit()
else:
    pass  # Busy. return
df = pd.read_sql_query('select * from dbo.com', cnxn)

# Check if transaction active and Vault not writing
if bool(df['ERP'].values[0]) and not bool(df['Vault'].values[0]):
    cursor.execute("INSERT INTO dbo.Item (ItemNum, Title, ItemTypId, LfCycDefId, LfCycStateId, UnitId) "
                   "VALUES (1234,'TEST INSERT ITEM',15,1,1,22)")
    cnxn.commit()

# Increment export counter
df = pd.read_sql_query('select ExportCounter from dbo.TransferInfoErp', cnxn)
new_cnt_val = df['ExportCounter'].values[0] + 1
cursor.execute("UPDATE dbo.TransferInfoErp SET ExportCounter = %s" % new_cnt_val)
cnxn.commit()


# Close transaction
cursor.execute("UPDATE dbo.com SET ERP = 0")
cnxn.commit()
