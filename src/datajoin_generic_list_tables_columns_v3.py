from sqlalchemy import Table, create_engine, MetaData, delete
from sqlalchemy.orm import sessionmaker
db_name='alm'  
#db_name='datajoin'  
#db_name='datasum'
db_connectionstring='postgresql://postgres:Welcome123@localhost:5432/'
#engine1 = create_engine('postgresql://postgres:Welcome123@localhost:5432/datasum')
#engine1 = create_engine('postgresql://postgres:Welcome123@localhost:5432/datajoin')
engine1 = create_engine(db_connectionstring+db_name)
metadata1 = MetaData()
metadata1.reflect(bind=engine1)
#db_name='datasum'  
#db_name='datajoin'  
example_table2 = Table('st_schema_attribute', metadata1, autoload_with=engine1) 
Session = sessionmaker(bind=engine1)
session = Session()
delete_statement = delete(example_table2)
session.execute(delete_statement)
session.commit()
print("All rows deleted successfully!")

tables1 = metadata1.tables.keys()
table_list1 = list(tables1)
#print(table_list)
# Print the list of tables
print("Tables in the database:")
for table1 in table_list1:
    print(table1)
    table_name = table1
    #db_name='datasum'  
    #engine = create_engine('postgresql://postgres:Welcome123@localhost:5432/datasum')
    engine = create_engine(db_connectionstring+db_name)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)
    example_table = Table('st_schema_attribute', metadata, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    column_types = {column.name: column.type for column in table.columns}
    #print("Column data types in the table:")
    for column_name, column_type in column_types.items():
        #print(f"{column_name}: {column_type}")
        schema_attribute_key=db_name+"|"+table_name+"|"+column_name
        schema_table_key=db_name+"|"+table_name
        data = schema_attribute_key+","+schema_table_key+","+table_name+","+column_name+","+str(column_type)
        #print(data)
        data_list = data.split(",")
        #print(data_list)
        insert_statement = example_table.insert().values(schema_attribute_key=data_list[0], schema_table_key=data_list[1], tablename=data_list[2], tableattribute=data_list[3], data_type=data_list[4])
        #print(insert_statement)
        session.execute(insert_statement)
        session.commit()
        