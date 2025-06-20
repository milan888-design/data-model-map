from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from fuzzywuzzy import fuzz

ratio_limit = 50
mapby = 'fuzzywuzzy'
set_id = 'set2'

# --- Database 1 Connection and Data Fetch ---
db_name1 = 'test_etl_db1'
db_connectionstring1 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine1 = create_engine(db_connectionstring1 + db_name1)
Session1 = sessionmaker(bind=engine1) # Use different Session name to avoid confusion
session1 = Session1()

select_statement1 = text('SELECT product_type_name FROM product_type')
try:
    result = session1.execute(select_statement1)
    results1 = result.fetchall()
    results_list1 = [list(row) for row in results1]
    lower_list1 = [item.lower() for sublist in results_list1 for item in sublist if isinstance(item, str)]
except Exception as e:
    print(f"An error occurred during DB1 data retrieval: {e}")
finally:
    session1.close()

# --- Database 2 Connection and Data Fetch ---
db_name2 = 'test_etl_db2'
db_connectionstring2 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine2 = create_engine(db_connectionstring2 + db_name2)
Session2 = sessionmaker(bind=engine2) # Use different Session name
session2 = Session2()

select_statement2 = text('SELECT item_type_name FROM item_type')
try:
    result2 = session2.execute(select_statement2)
    results2 = result2.fetchall()
    results_list2 = [list(row) for row in results2]
    lower_list2 = [item.lower() for sublist in results_list2 for item in sublist if isinstance(item, str)]
except Exception as e:
    print(f"An error occurred during DB2 data retrieval: {e}")
finally:
    session2.close()

print(lower_list1)
print(lower_list2)

# --- Process and Insert Data ---
# Re-establish session for engine1 for inserts
Session_insert = sessionmaker(bind=engine1)
session_insert = Session_insert()

print("Pairs with fuzz.ratio higher than 50:")
try:
    for value1_orig in lower_list1: # Use _orig to preserve original value for fuzzywuzzy
        for value2_orig in lower_list2:
            ratio = fuzz.ratio(value1_orig, value2_orig)
            if ratio > ratio_limit:
                # IMPORTANT: DO NOT replace single quotes here if using parameterized queries.
                # SQLAlchemy handles escaping automatically.
                # The .replace("#") lines are no longer needed and should be removed.
                # value1_processed = value1_orig.replace("'", "''") # This is how it would be done manually (double single quotes)
                # value2_processed = value2_orig.replace("'", "''") # But parameterized queries are better.

                # Define the INSERT statement with placeholders
                # Use named parameters like :param_name for clarity
                queryinsert = text("""
                    INSERT INTO st_mapping_set_detail_v3 (set_id, leftAttributevalue, rightAttributevalue, matchrating, mapby)
                    VALUES (:set_id, :left_attr_value, :right_attr_value, :match_rating, :map_by)
                """)

                # Execute the statement with a dictionary of parameters
                result_insert = session_insert.execute(queryinsert, {
                    'set_id': set_id,
                    'left_attr_value': value1_orig, # Use original values, SQLAlchemy will escape
                    'right_attr_value': value2_orig, # Use original values, SQLAlchemy will escape
                    'match_rating': ratio,
                    'map_by': mapby
                })

                # For INSERTs, you typically want to commit the transaction
                session_insert.commit()

                print(f"Inserted: '{value1_orig}' - '{value2_orig}', Ratio: {ratio}")

except Exception as e:
    print(f"An error occurred during insertion: {e}")
    session_insert.rollback() # Rollback on error
finally:
    session_insert.close()
    print("All operations completed and sessions closed.")