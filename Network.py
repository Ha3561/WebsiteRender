import pymysql 
import openpyxl 



# Establish connection
try:
    connection = pymysql.connect(
        host='localhost',
        user='Ha',
        password='TanmaySushmi1408',
        database='network'
    )
    #if connection.open:
       # print("Connected to MySQL database") 
    cursor = connection.cursor()

    # Define the CREATE TABLE query
    create_table_query = """
     CREATE TABLE network (
    Person TEXT,
    First TEXT,
    Last TEXT,
    Birthdate DATE,
    Location TEXT,
    `Group` TEXT,  -- Using backticks to escape reserved keyword
    Contact BIGINT,
    Position TEXT,
    DateOfLastContact DATE
);

    """

    # Execute the CREATE TABLE query
    cursor.execute(create_table_query)

    print("Table created successfully!")

    # Commit the changes (if you're in a transactional database)
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()

except pymysql.Error as e:
    print("Error connecting to MySQL database:", e)
