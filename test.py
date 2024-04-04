import pymysql

# Establish connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='TanmaySushmi1408',
                             database='test',
                             port=3306)

# Create cursor object 
#'
cursor = connection.cursor()

# Create table query
create_table_query = """
CREATE TABLE IF NOT EXISTS sample_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255)
)
"""

# Execute create table query
cursor.execute(create_table_query) 

insert_query = """
INSERT INTO sample_table (name, age, email)
VALUES (%s, %s, %s)
"""

# Define some random data
random_data = [
    ('John Doe', 30, 'john.doe@example.com'),
    ('Jane Smith', 25, 'jane.smith@example.com'),
    ('Michael Johnson', 35, 'michael.johnson@example.com')
]

# Execute the insert query for each row of random data
for data in random_data:
    cursor.execute(insert_query, data)

# Execute a sample select query
cursor.execute("SELECT * FROM sample_table")

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Commit the changes
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
