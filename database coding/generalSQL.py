import sqlite3

''' generalSQL.py
    Here defines the general functionality
    of the SQL program used in the program

'''
# define connection and cursor
connect = sqlite3.connect('insurance.db')

c = connect.cursor()

def enable_FK():
    c.execute('PRAGMA foreign_keys = ON;')


def execute_comm(sql):
    try:
        # Assuming 'c' is the cursor object and 'conn' is the connection object
        c.execute(sql)

        # If it's a SELECT query, fetch the data and return it
        if sql.strip().upper().startswith("SELECT"):
            result = c.fetchall()  # Fetch all rows from the result
            return result

        # If not a SELECT query, just print success message
        print("SQL command executed successfully.")

    except sqlite3.Error as e:
        # Print the error directly if something goes wrong
        print(f"An error occurred: {e}")
        connect.rollback()  # Rollback the transaction if an error occurs
        return None

def show_all():
    try:
        # Execute the query to get all tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Fetch all tables
        tables = c.fetchall()

        # Loop through each table
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")
            print("-" * 114)

            # Retrieve column names for the table
            c.execute(f"PRAGMA table_info({table_name});")
            columns = c.fetchall()
            column_names = [column[1] for column in columns]  # Extract column names

            # Dynamically create the format string based on the number of columns
            format_string = " | ".join([f"{{:<20}}"] * len(column_names))  # Add separator ' | '

            # Display column headers with separators
            print(format_string.format(*column_names) + " |")  # Add pipe at the end of the header
            print("-" * 114)

            # Query to select all data from the table
            c.execute(f"SELECT * FROM {table_name}")

            # Fetch all rows of data
            rows = c.fetchall()

            # Print the data inside the table
            if rows:
                for row in rows:
                    print(format_string.format(*row) + " |")  # Add pipe at the end of each row
            else:
                print("No data in this table.")

            print("\n" + "=" * 114 + "\n")  # Separator between tables

    except sqlite3.Error as e:
        print(f"Error: {e}")


def close():
    connect.close()

