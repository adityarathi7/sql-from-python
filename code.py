import psycopg2

def connect_to_postgres():
    # connect to the PostgreSQL database
    conn = psycopg2.connect(database="postgres")

    # create a cursor object
    cur = conn.cursor()
    return conn, cur

def create_department_table(cur):
    table_name = "department"
    cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
    table_exists = cur.fetchone()[0]

    # if the table exists, drop it
    if table_exists:
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()

    # create the departments table
    cur.execute(f"""CREATE TABLE {table_name} (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL)""")
    conn.commit()

def create_employees_table(cur):
    table_name = "employees"
    cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')")
    table_exists = cur.fetchone()[0]

    # if the table exists, drop it
    if table_exists:
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()

    # create the employees table
    cur.execute(f"""CREATE TABLE {table_name} (
                        id SERIAL PRIMARY KEY,
                        emp_name VARCHAR(50) NOT NULL,
                        emp_age INTEGER NOT NULL,
                        emp_email VARCHAR(50) NOT NULL UNIQUE,
                        department_id INTEGER NOT NULL REFERENCES department(id))""")
    conn.commit()

def insert_department_values(cur):
    # define the SQL query to insert values into the table
    sql = """INSERT INTO department (id, name)
             VALUES (%s, %s)"""

    # define the values to insert into the table
    values = [(100,"Sales"),
              (200,"Marketing"),
              (300,"Engineering")]

    # execute the SQL query with the values
    cur.executemany(sql, values)
    conn.commit()

def insert_employee_values(cur):
    # define the SQL query to insert values into the table
    sql = """INSERT INTO employees (id, emp_name, emp_age, emp_email, department_id)
             VALUES (%s, %s, %s, %s, %s)"""

    # define the values to insert into the table
    values = [(1,"Alice", 30, "alice@example.com", 100),
              (2,"Bob", 35, "bob@example.com", 200),
              (3,"Charlie", 25, "charlie@example.com", 100)]

    # execute the SQL query with the values
    cur.executemany(sql, values)
    conn.commit()

# establish connection to the database
conn, cur = connect_to_postgres()

# create department and employees tables
create_department_table(cur)
create_employees_table(cur)

# insert values into department and employees tables
insert_department_values(cur)
insert_employee_values(cur)

# close the cursor and the database connection
cur.close()
conn.close()
