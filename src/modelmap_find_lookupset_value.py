#moelmap_postgres_etl.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- Database 1 Connection and Data Fetch ---
db_name1 = 'test_etl_db1'
db_connectionstring1 = 'postgresql://postgres:Welcome123@localhost:5432/'
engine1 = create_engine(db_connectionstring1 + db_name1)
Session1 = sessionmaker(bind=engine1)
session1 = Session1()

def find_lookupsetid(var_set_id, var_rightattribue):
    set_id = var_set_id
    rightattribute = var_rightattribue

    queryselect = text("""
            SELECT leftattribute,transform_lookupset from st_mapping_set_detail_v3
            WHERE set_id=:set_id and rightattribute=:rightattribute
            """)

    value_set_id = None # Initialize to None in case of an error or no result

    try:
        result_select = session1.execute(queryselect, {
                'set_id': set_id,
                'rightattribute': rightattribute
            })
        result1 = result_select.fetchone()

        if result1: # Check if a result was actually returned
            print(result1)
            print(result1[1])
            value_set_id = result1[1]
        else:
            print(f"No lookup set found for set_id='{set_id}' and rightattribute='{rightattribute}'")

    except Exception as e:
        print(f"An error occurred during data processing or insertion: {e}")
    finally:
        # It's generally good practice to manage session closing outside the function
        # if the session is passed in or meant to be long-lived for a transaction.
        # If this function creates its own session, then session1.close() here is fine.
        # Given your previous context, session1 seems to be managed at a higher level.
        print("Function execution finished.") # Renamed for clarity

    return value_set_id # This line makes value_set_id the return value

# Now, when you call the function, the returned value will be stored in lookupset_id
lookupset_id = find_lookupsetid('set1','item_type_name')

# You can then use lookupset_id in your next function or further processing
print(f"The lookup set ID obtained is: {lookupset_id}")

#set_id='set2'
#set_id=lookupset_id
l#eftattributevalue='laptop'

def find_lookupvalue(var_valset_id, var_leftattributevalue):
    set_id=var_valset_id
    leftattributevalue=var_leftattributevalue

    queryselect2 = text("""
            SELECT rightattributevalue from st_mapping_set_detail_v3  
            WHERE  set_id=:set_id and leftattributevalue=:leftattributevalue
            """)

    try:
        result_select2 = session1.execute(queryselect2, {
                'set_id': set_id,
                'leftattributevalue': leftattributevalue
            })
        result3=result_select2.fetchone()
        print(result3)
    except Exception as e:
        print(f"An error occurred during data processing or insertion: {e}")
    finally:
        session1.close()
        print("second sessions closed.")    
    return result3 # This line makes value_set_id the return value

lookupvalue= find_lookupvalue(lookupset_id,'laptop')