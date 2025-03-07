# Import the pandas library for data processing and analysis
import pandas as pd
# Import the sqlite3 library for interacting with SQLite databases
import sqlite3

# Read customer data from the 'customer.csv' file and store it in a DataFrame
customers_df = pd.read_csv('customer.csv')
# Read order data from the 'orders.csv' file and store it in a DataFrame
orders_df = pd.read_csv('orders.csv')

# Use pandas' merge function to perform an inner join on the order data and customer data based on 'CustomerID'
merged_df = pd.merge(orders_df, customers_df, on='CustomerID', how='inner')

# Add a new column 'TotalAmount' to the merged DataFrame, calculating the total amount for each order
merged_df['TotalAmount'] = merged_df['Quantity'] * merged_df['Price']

# Determine the order status based on the order date. If the date starts with '2025-03', the status is 'New'; otherwise, it's 'Old'
merged_df['Status'] = merged_df['OrderDate'].apply(lambda d: 'New' if d.startswith('2025-03') else 'Old')

# Filter out order data where the total amount is greater than 5000
high_value_orders = merged_df[merged_df['TotalAmount'] > 5000]

# Connect to the SQLite database named 'ecommerce.db'
conn = sqlite3.connect('ecommerce.db')

# Define an SQL query statement to create a table named 'HighValueOrders'
create_table_query = '''
CREATE TABLE IF NOT EXISTS HighValueOrders (
    OrderID INTEGER,
    CustomerID INTEGER,
    Name TEXT,
    Email TEXT,
    Product TEXT,
    Quantity INTEGER,
    Price REAL,
    OrderDate TEXT,
    TotalAmount REAL,
    Status TEXT
)
'''
# Execute the SQL query to create the table
conn.execute(create_table_query)

# Write the high-value order data to the 'HighValueOrders' table in the database, replacing existing data if it exists
high_value_orders.to_sql('HighValueOrders', conn, if_exists='replace', index=False)

# Execute a SQL query to select all data from the 'HighValueOrders' table
result = conn.execute('SELECT * FROM HighValueOrders')
# Iterate over the query results and print each row
for row in result.fetchall():
    print(row)

# Close the database connection
conn.close()

# Print a message indicating that the ETL process has completed successfully
print("ETL process completed successfully!")