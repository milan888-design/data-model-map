#moelmap_postgres_etl.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- Database 1 Connection and Data Fetch ---
db_name1 = 'test_etl_db1'
db_connectionstring1 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine1 = create_engine(db_connectionstring1 + db_name1)
Session1 = sessionmaker(bind=engine1)
session1 = Session1()

leftdatabase='test_etl_db1'
lefttable='sales_order'
rightdatabase='test_etl_db2'
righttable='sales_txn'
maptype='schema to schema'

queryselect = text("""
        SELECT  set_id from st_mapping_set_v3 
        WHERE  leftdatabase=:leftdatabase and lefttable=:lefttable and rightdatabase=:rightdatabase and righttable=:righttable and maptype=:maptype
        """)


try:
    result_select = session1.execute(queryselect, {
            'leftdatabase': leftdatabase,
            'lefttable': lefttable,
            'rightdatabase': rightdatabase,
            'righttable': righttable,
            'maptype': maptype
        })
    result1=result_select.fetchone()
    print(result1)
except Exception as e:
    print(f"An error occurred during data processing or insertion: {e}")
finally:
    session1.close()
    print("All sessions closed.")