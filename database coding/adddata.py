import sqlite3
from datetime import datetime
''' adddata.py
    Here defines the function for adding
    data into the database

'''
# define connection and cursor
connect = sqlite3.connect('insurance.db')

c = connect.cursor()

def are_all_tables_empty(tables):
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table};")
        count = c.fetchone()[0]
        if count > 0:
            return False  # If any table is not empty, return False
    return True  # If all tables are empty, return True

def predefined_data():
    # List of tables to check
    tables = [
        "policyholder", "policy", "policy_type", "coverage_details",
        "vehicle", "comprehensive_policy", "third_party_policy",
        "policy_purpose", "personal_purpose", "commercial_purpose"
    ]

    # Check if all tables are empty
    if are_all_tables_empty(tables):
        # Insert data into policyholder table
        c.execute('''INSERT INTO policyholder VALUES 
                    (1, "Khalish", "01129180129", "2004-08-09", "D"),
                    (2, "Norman", "01789319292", "2004-11-09", "DA"),
                    (3, "Afiq", "01644299733", "2004-08-07", "D")''')

        # Insert data into policy table
        c.execute('''INSERT INTO policy VALUES
                     (101, "2025-01-01", "2027-01-01", 320.00, 1),
                     (102, "2024-05-04", "2026-05-06", 270.00, 2),
                     (103, "2022-11-28", "2024-12-02", 440.00, 3)''')

        # Insert data into policy_type table
        c.execute('''INSERT INTO policy_type VALUES
                    (1, "Comprehensive Policy", "Standard Laws"),
                    (2, "Third-party Policy", "Standard Laws")''')

        # Insert data into coverage_details table
        c.execute('''INSERT INTO coverage_details VALUES
                    (101, 1, "Single-car"),
                    (102, 2, "Multi-car"),
                    (103, 2, "Multi-car")''')

        # Insert data into vehicle table
        c.execute('''INSERT INTO vehicle VALUES
                    (101, "QAA1051", "MPV"),
                    (102, "WXY2256", "SUV"),
                    (103, "QM4014B", "Sedan")''')

        # Insert data into comprehensive_policy table
        c.execute('''INSERT INTO comprehensive_policy VALUES
                    (101, 500.00, "Accidental Damage"),
                    (102, 300.00, "Theft Protection"),
                    (103, 200.00, "Windshield Coverage")''')

        # Insert data into third_party_policy table
        c.execute('''INSERT INTO third_party_policy VALUES
                    (101, 1000000.00),
                    (102, 1500000.00),
                    (103, 1200000.00)''')

        # Insert data into policy_purpose table
        c.execute('''INSERT INTO policy_purpose VALUES
                    (1, "Personal", "Driver Age 21+"),
                    (2, "Commercial", "Business Vehicle")
                    ''')

        # Insert data into personal_purpose table
        c.execute('''INSERT INTO personal_purpose VALUES
                    (102, "No Restrictions")
                    ''')

        # Insert data into commercial_purpose table
        c.execute('''INSERT INTO commercial_purpose VALUES
                    (101, "Taxi Business"),
                    (103, "Parcel Delivery")''')
    else:
        print("Some tables already have data, skipping insertion.")

    connect.commit()

def add_policyholder():
    try:

        # Get the highest existing policyholder_id
        c.execute('SELECT MAX(policyholder_id) FROM policyholder')
        result = c.fetchone()
        next_id = result[0] + 1 if result[0] is not None else 4  # Start from 4 if no data exists

        # Ask for user input for the policyholder
        name = input("Enter Policyholder Name: ")
        phone = input("Enter Phone Number: ")
        # Validate and convert Date of Birth (DD-MM-YYYY)
        while True:
            dob_str = input("Enter Date of Birth (DD-MM-YYYY): ")
            try:
                dob = datetime.strptime(dob_str, "%d-%m-%Y").date()  # Convert to date object
                break  # Exit the loop if the date is valid
            except ValueError:
                print("Invalid date format. Please enter the date in DD-MM-YYYY format.")

        status = input("Enter Status (D, DA, etc.): ")

        # Insert the policyholder data into the table with the auto-assigned ID
        c.execute('''INSERT INTO policyholder (policyholder_id, full_name, contact_details, dob, driving_license) 
                     VALUES (?, ?, ?, ?, ?)''', (next_id, name, phone, dob, status))

        # Commit changes
        connect.commit()

        print(f"Policyholder added successfully with ID {next_id}!")

    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")

def add_policy():
    try:
        # Get the highest existing policy_number
        c.execute("SELECT MAX(policy_number) FROM policy")
        result = c.fetchone()
        next_policy_number = result[0] + 1 if result[0] is not None else 101  # Start from 101 if no data exists

        # Display available policyholders
        print("Available Policyholders:")
        c.execute("SELECT policyholder_id, full_name FROM policyholder")
        policyholders = c.fetchall()

        if not policyholders:
            print("No policyholders available.")
            return

        for ph in policyholders:
            print(f"{ph[0]} - {ph[1]}")

        # Ask the user to choose a policyholder
        policyholder_id = int(input("Enter Policyholder ID: "))

        # Validate if the entered policyholder_id exists
        c.execute("SELECT 1 FROM policyholder WHERE policyholder_id = ?", (policyholder_id,))
        if not c.fetchone():
            print("Invalid Policyholder ID. Please try again.")
            return

        start_date = input("Enter Start Date (DD-MM-YYYY): ")
        end_date = input("Enter End Date (DD-MM-YYYY): ")
        premium = float(input("Enter Premium: "))

        # Insert the policy data with the automatically incremented policy_number
        c.execute('''INSERT INTO policy (policy_number, start_date, end_date, premium_amount, policyholder_id) 
                     VALUES (?, ?, ?, ?, ?)''', (next_policy_number, start_date, end_date, premium, policyholder_id))

        # Commit changes
        connect.commit()

        print(f"Policy with Policy Number {next_policy_number} added successfully!")

    except ValueError:
        print("Invalid input. Please make sure the data is entered correctly.")

def add_coverage():
    try:
        # Display available policies
        print("Available Policies:")
        c.execute("SELECT policy_number FROM policy")
        policies = c.fetchall()

        if not policies:
            print("No policies available.")
            return

        # Display policies
        for policy in policies:
            print(f"Policy Number: {policy[0]}")

        # Ask user to select a policy
        policy_number = int(input("Enter Policy Number to add coverage: "))

        # Validate if the entered policy_number exists
        c.execute("SELECT 1 FROM policy WHERE policy_number = ?", (policy_number,))
        if not c.fetchone():
            print("Invalid Policy Number. Please try again.")
            return

        # Ask user to input coverage type
        coverage_type = input("Enter Coverage Type ('Single-car' or 'Multi-car'): ")

        # Validate coverage_type input and map it to coverage_id
        if coverage_type == 'Single-car':
            coverage_id = 1
        elif coverage_type == 'Multi-car':
            coverage_id = 2
        else:
            print("Invalid Coverage Type. Please enter 'Single-car' or 'Multi-car'.")
            return

        # Insert coverage details into the database
        c.execute('''INSERT INTO coverage_details (policy_number, coverage_id, coverage_type) 
                     VALUES (?, ?, ?)''', (policy_number, coverage_id, coverage_type))

        # Commit changes
        connect.commit()

        print(f"Coverage with Coverage ID {coverage_id} and Coverage Type '{coverage_type}' added to Policy Number {policy_number} successfully!")

    except ValueError:
        print("Invalid input. Please make sure the data is entered correctly.")

def add_vehicle():
    try:
        # Fetch all available policies from the policy table
        c.execute("SELECT policy_number FROM policy")
        policies = c.fetchall()

        # Check if there are any policies available
        if not policies:
            print("No policies available. Please add a policy first.")
            return

        # Display the available policy numbers for selection
        print("Available Policies:")
        for policy in policies:
            print(f"Policy Number: {policy[0]}")

        # Prompt the user to select a policy by its policy number
        policy_number = int(input("Enter the Policy Number to associate with the vehicle: "))

        # Validate if the selected policy_number exists
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. Please try again.")
            return

        # Prompt the user to enter the vehicle registration
        vehicle_registration = input("Enter the Vehicle Registration Number: ")

        # Prompt the user to select the vehicle type
        print("Select Vehicle Type:")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
        print("4. MPV")
        vehicle_type_choice = input("Enter the number corresponding to the vehicle type: ")

        # Map the user's choice to the vehicle type
        vehicle_types = {
            "1": "Sedan",
            "2": "SUV",
            "3": "Truck",
            "4": "MPV"
        }

        # Check if the choice is valid
        if vehicle_type_choice not in vehicle_types:
            print("Invalid choice. Please select a valid vehicle type.")
            return

        vehicle_type = vehicle_types[vehicle_type_choice]

        # Insert the vehicle data into the vehicle table
        c.execute('''INSERT INTO vehicle (policy_number, vehicle_registration, vehicle_type) 
                     VALUES (?, ?, ?)''', (policy_number, vehicle_registration, vehicle_type))

        # Commit the changes
        connect.commit()

        print(f"Vehicle with registration number {vehicle_registration} added successfully to policy {policy_number}.")

    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def add_compPolicy():
    try:
        # Fetch all available policies to ensure valid policy selection
        c.execute("SELECT policy_number FROM policy")
        policies = c.fetchall()

        # Check if any policies are available
        if not policies:
            print("No policies available. Please add a policy first.")
            return

        # Display available policies
        print("Available Policies:")
        for policy in policies:
            print(f"Policy Number: {policy[0]}")

        # Prompt the user to select a policy number
        policy_number = input("Enter the Policy Number for the comprehensive policy: ")

        # Verify the selected policy exists
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. Please try again.")
            return

        # Prompt the user to enter the deductible
        while True:
            try:
                deductible = float(input("Enter Deductible (must be >= 0): "))
                if deductible < 0:
                    raise ValueError("Deductible cannot be negative.")
                break
            except ValueError as e:
                print(e)

        # Prompt the user to enter the special coverage description
        special_coverage = input("Enter Special Coverage (optional): ")

        # Insert the comprehensive policy into the database
        c.execute('''
            INSERT INTO comprehensive_policy (policy_number, deductible, special_coverage)
            VALUES (?, ?, ?)
        ''', (policy_number, deductible, special_coverage))

        # Commit the transaction
        connect.commit()

        print(f"Comprehensive policy added successfully for Policy Number {policy_number}.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def add_3PPolicy():
    try:
        # Fetch all available policies to select from
        c.execute('''
            SELECT policy_number, start_date, end_date, premium_amount
            FROM policy
            WHERE policy_number NOT IN (SELECT policy_number FROM third_party_policy)
        ''')
        policies = c.fetchall()

        # Check if there are any available policies
        if not policies:
            print("No eligible policies available to add as a third-party policy.")
            return

        # Display available policies
        print("Available Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10}")
        print("-" * 60)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10}")
        print("-" * 60)

        # Prompt the user to select a policy number
        policy_number = input("Enter the Policy Number to add as a third-party policy: ")

        # Validate the selected policy exists and is eligible
        valid_policy = [p[0] for p in policies]
        if int(policy_number) not in valid_policy:
            print("Invalid Policy Number. Please select a valid option.")
            return

        # Prompt user to enter the liability limit
        liability_limit = float(input("Enter Liability Limit (must be non-negative): "))
        if liability_limit < 0:
            print("Liability limit must be non-negative.")
            return

        # Insert the third-party policy into the database
        c.execute('''
            INSERT INTO third_party_policy (policy_number, liability_limit)
            VALUES (?, ?)
        ''', (policy_number, liability_limit))

        # Commit the transaction
        connect.commit()

        print(f"Third-party policy with Policy Number {policy_number} added successfully.")

    except ValueError:
        print("Invalid input. Please enter the data in the correct format.")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def add_personalPolicy():
    try:
        # Fetch all available policies that do not have a commercial purpose
        c.execute('''
            SELECT p.policy_number, p.start_date, p.end_date, p.premium_amount
            FROM policy p
            LEFT JOIN commercial_purpose cp ON p.policy_number = cp.policy_number
            WHERE cp.policy_number IS NULL
        ''')
        policies = c.fetchall()

        # Check if there are any policies available
        if not policies:
            print("No policies available to assign a personal purpose (some policies already have a commercial purpose).")
            return

        # Display available policies
        print("Available Policies (without Commercial Purpose):")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10}")
        print("-" * 60)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10}")
        print("-" * 60)

        # Prompt the user to select a policy number
        policy_number = input("Enter the Policy Number to assign a personal purpose: ")

        # Verify the policy exists
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Check if the policy already has a personal purpose assigned
        c.execute("SELECT policy_number FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is not None:
            print("This policy already has a personal purpose assigned.")
            return

        # Prompt the user to enter driver restrictions
        driver_restrictions = input("Enter Driver Restrictions (e.g., 'No young drivers'): ")

        # Insert the new personal purpose into the table
        c.execute('''
            INSERT INTO personal_purpose (policy_number, driver_restrictions)
            VALUES (?, ?)
        ''', (policy_number, driver_restrictions))

        # Commit the transaction
        connect.commit()

        print(f"Personal purpose successfully assigned to Policy Number {policy_number}.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def add_commercialPolicy():
    try:
        # Fetch all policies to allow the user to select a policy, excluding those with a personal purpose
        c.execute('''
            SELECT p.policy_number, p.start_date, p.end_date
            FROM policy p
            LEFT JOIN personal_purpose pp ON p.policy_number = pp.policy_number
            WHERE pp.policy_number IS NULL
        ''')
        policies = c.fetchall()

        # Check if there are any policies available that don't have personal purpose
        if not policies:
            print("No policies available to associate with a commercial purpose (some policies already have a personal purpose).")
            return

        # Display all available policies
        print("Available Policies for Commercial Purpose (without personal purpose):")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15}")
        print("-" * 50)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15}")
        print("-" * 50)

        # Prompt user to select a policy number
        policy_number = input("Enter the Policy Number to associate with commercial purpose: ")

        # Check if the policy number is valid
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Check if the selected policy already has a personal purpose
        c.execute("SELECT 1 FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone():
            print("This policy already has a personal purpose and cannot be used for a commercial purpose.")
            return

        # Prompt the user for business use details
        business_use_details = input("Enter the business use details for this commercial policy: ")

        # Insert the data into the commercial_purpose table
        c.execute('''
            INSERT INTO commercial_purpose (policy_number, business_use_details)
            VALUES (?, ?)
        ''', (policy_number, business_use_details))
        connect.commit()

        print(f"Commercial purpose successfully added for Policy Number {policy_number}.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def add_policyType():
    try:
        # Get policy type details from the user
        type_name = input("Enter the policy type name: ")
        applicable_laws = input("Enter applicable laws for this policy type: ")

        # Insert the new policy type into the database
        c.execute('''
            INSERT INTO policy_type (type_name, applicable_laws)
            VALUES (?, ?)
        ''', (type_name, applicable_laws))

        # Commit the transaction
        connect.commit()

        print(f"Policy type '{type_name}' successfully added.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def add_policyPurpose():
    try:
        # Get policy purpose details from the user
        purpose_type = input("Enter the purpose type: ")
        eligibility_criteria = input("Enter eligibility criteria for this policy purpose: ")

        # Insert the new policy purpose into the database
        c.execute('''
            INSERT INTO policy_purpose (purpose_type, eligibility_criteria)
            VALUES (?, ?)
        ''', (purpose_type, eligibility_criteria))

        # Commit the transaction
        connect.commit()

        print(f"Policy purpose '{purpose_type}' successfully added.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
