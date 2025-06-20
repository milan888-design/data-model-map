#moelmap_postgres_etl.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- Database 1 Connection and Data Fetch ---
db_name1 = 'test_etl_db1'
db_connectionstring1 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine1 = create_engine(db_connectionstring1 + db_name1)
Session1 = sessionmaker(bind=engine1)
session1 = Session1()

# --- Database 2 Connection and insert ---
db_name2 = 'test_etl_db2'
db_connectionstring2 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine2 = create_engine(db_connectionstring2 + db_name2)
Session_insert = sessionmaker(bind=engine2)
session_insert = Session_insert()

leftdatabase=db_name1
lefttable='sales_order'
rightdatabase=db_name2
righttable='sales_txn'
maptype='schema to schema'
select set_id 
from st_mapping_set_v3
Where leftdatabase='test_etl_db1'
 and lefttable='sales_order'
 And rightdatabase='test_etl_db2' 
 and righttable='sales_txn'
And maptype='schema to schema'

queryselect = text("""
        SELECT  set_id from st_mapping_set_v3 
        WHERE  leftdatabase=:leftdatabase and lefttable=:lefttable and rightdatabase=:rightdatabase and righttable=:righttable and maptype=:maptype
        """)

queryinsert = text("""
        INSERT INTO sales_txn (id,txn_type,description,item_type_name,customer_id,qty,txn_date)
        VALUES (:id, :txn_type, :description, :item_type_name, :customer_id, :qty, :txn_date)
        """)

select_statement1 = text('SELECT order_id,order_type,description,product_type_name,customer_id,quantity,order_date FROM sales_order')




try:
    result = session1.execute(select_statement1)
    results1 = result.fetchall()

    for row in results1:
        # The problematic line was here.
        # You can print the whole row for debugging like this:
        print(row) # This will print the entire Row object
        # Or print specific columns:
        # print(f"Order ID: {row.order_id}, Type: {row.order_type}")

        id = row.order_id
        txn_type = row.order_type
        description = row.description
        item_type_name = row.product_type_name # This maps to product_type_name from sales_order
        customer_id = row.customer_id
        qty = row.quantity
        txn_date = row.order_date

        result_insert = session_insert.execute(queryinsert, {
            'id': id,
            'txn_type': txn_type,
            'description': description,
            'item_type_name': item_type_name, # Ensure your sales_txn table's item_type_name maps to product_type_name from sales_order
            'customer_id': customer_id,
            'qty': qty,
            'txn_date': txn_date
        })
        session_insert.commit()

except Exception as e:
    # It's good practice to rollback the session_insert if an error occurs during the loop
    # before closing, to ensure no partial inserts are committed.
    session_insert.rollback()
    print(f"An error occurred during data processing or insertion: {e}")
finally:
    session1.close()
    session_insert.close()
    print("All sessions closed.")