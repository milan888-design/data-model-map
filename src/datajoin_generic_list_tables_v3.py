from sqlalchemy import Table, create_engine, MetaData, delete
from sqlalchemy.orm import sessionmaker
db_name='test_etl_db1' 
db_connectionstring='postgresql://postgres:pass@localhost:5432/'
engine1 = create_engine(db_connectionstring+db_name)
metadata1 = MetaData()
metadata1.reflect(bind=engine1)

example_table1 = Table('st_schema_table', metadata1, autoload_with=engine1) 
Session = sessionmaker(bind=engine1)
session = Session()
delete_statement = delete(example_table1)
session.execute(delete_statement)
session.commit()
print("All rows deleted successfully!")

tables1 = metadata1.tables.keys()
table_list1 = list(tables1)
#print(table_list)
# Print the list of tables
print("Tables in the database:")
for table1 in table_list1:
    #print(table1)
    table_name = table1
    engine = create_engine(db_connectionstring+db_name)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)
    example_table = Table('st_schema_table', metadata, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    #column_types = {column.name: column.type for column in table.columns}
    #print("Column data types in the table:")
    schema_table_key=db_name+"|"+table_name
    schema_key=db_name
    data = schema_table_key+","+schema_key+","+table_name
    #print(data)
    data_list = data.split(",")
    #print(data_list)
    insert_statement = example_table.insert().values(schema_table_key=data_list[0], schema_key=data_list[1], tablename=data_list[2])
    #print(insert_statement)
    session.execute(insert_statement)
    session.commit()
    