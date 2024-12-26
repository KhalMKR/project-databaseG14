import sqlite3
from datetime import datetime
''' updatedata.py
    Here defines the functions for updating
    data in the database

'''
# define connection and cursor
connect = sqlite3.connect('insurance.db')

c = connect.cursor()

def upd_policyholder():
    try:
        # Fetch all available policyholders
        c.execute("SELECT policyholder_id, full_name, contact_details, dob, driving_license FROM policyholder")
        policyholders = c.fetchall()

        if not policyholders:
            print("No policyholders available to update.")
            return

        # Display available policyholders
        print("Available Policyholders:")
        print(f"{'Policyholder ID':<20} {'Name':<25} {'Phone':<20} {'DOB':<15} {'License Status'}")
        print("-" * 85)

        for policyholder in policyholders:
            print(f"{policyholder[0]:<20} {policyholder[1]:<25} {policyholder[2]:<20} {policyholder[3]:<15} {policyholder[4]}")

        print("-" * 85)

        # Prompt the user to select a policyholder by ID
        policyholder_id = input("Enter the Policyholder ID to update: ")

        # Verify the policyholder exists
        c.execute("SELECT policyholder_id FROM policyholder WHERE policyholder_id = ?", (policyholder_id,))
        if c.fetchone() is None:
            print("Invalid Policyholder ID. No changes made.")
            return

        # Ask the user for new details for the selected policyholder
        new_name = input("Enter the new Policyholder Name: ")
        new_phone = input("Enter the new Phone Number: ")

        # Validate and convert Date of Birth (DD-MM-YYYY)
        while True:
            dob_str = input("Enter the new Date of Birth (DD-MM-YYYY): ")
            try:
                new_dob = datetime.strptime(dob_str, "%d-%m-%Y").date()  # Convert to date object
                break  # Exit the loop if the date is valid
            except ValueError:
                print("Invalid date format. Please enter the date in DD-MM-YYYY format.")

        new_status = input("Enter the new Status (D, DA, etc.): ")

        # Update the policyholder in the database
        c.execute('''
            UPDATE policyholder
            SET full_name = ?, contact_details = ?, dob = ?, driving_license = ?
            WHERE policyholder_id = ?
        ''', (new_name, new_phone, new_dob, new_status, policyholder_id))

        # Commit the changes
        connect.commit()

        print(f"Policyholder with ID {policyholder_id} has been successfully updated.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")

def upd_policy():
    try:
        # Fetch all available policies
        c.execute('SELECT policy_number, start_date, end_date, premium_amount, policyholder_id FROM policy')
        policies = c.fetchall()

        if not policies:
            print("No policies available to update.")
            return

        # Display available policies
        print("Available Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10} {'Policyholder ID'}")
        print("-" * 65)

        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10} {policy[4]}")

        print("-" * 65)

        # Prompt the user to select a policy number to update
        policy_number = input("Enter the Policy Number to update: ")

        # Validate if the entered policy_number exists
        c.execute("SELECT 1 FROM policy WHERE policy_number = ?", (policy_number,))
        if not c.fetchone():
            print("Invalid Policy Number. No changes made.")
            return

        # Ask for the new policy details
        new_start_date = input("Enter the new Start Date (DD-MM-YYYY): ")
        new_end_date = input("Enter the new End Date (DD-MM-YYYY): ")
        new_premium = float(input("Enter the new Premium: "))

        # Update the policy details in the database
        c.execute('''
            UPDATE policy
            SET start_date = ?, end_date = ?, premium_amount = ?
            WHERE policy_number = ?
        ''', (new_start_date, new_end_date, new_premium, policy_number))

        # Commit the changes
        connect.commit()

        print(f"Policy with Policy Number {policy_number} has been successfully updated.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")

def upd_coverage():
    try:
        # Fetch and display available policies
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
        policy_number = int(input("Enter Policy Number to update coverage: "))

        # Validate if the entered policy_number exists
        c.execute("SELECT 1 FROM policy WHERE policy_number = ?", (policy_number,))
        if not c.fetchone():
            print("Invalid Policy Number. Please try again.")
            return

        # Fetch existing coverage details for the selected policy
        c.execute("SELECT coverage_id, coverage_type FROM coverage_details WHERE policy_number = ?", (policy_number,))
        existing_coverage = c.fetchall()

        if not existing_coverage:
            print(f"No coverage details found for Policy Number {policy_number}.")
            return

        print(f"Existing Coverage Details for Policy Number {policy_number}:")
        print(f"{'Coverage ID':<15} {'Coverage Type':<15}")
        print("-" * 30)
        for coverage in existing_coverage:
            print(f"{coverage[0]:<15} {coverage[1]:<15}")
        print("-" * 30)

        # Ask the user to select the coverage to update
        coverage_id = int(input("Enter the Coverage ID to update: "))

        # Validate if the selected coverage_id exists for the policy
        c.execute("SELECT 1 FROM coverage_details WHERE policy_number = ? AND coverage_id = ?",
                  (policy_number, coverage_id))
        if not c.fetchone():
            print("Invalid Coverage ID for the selected Policy Number. Please try again.")
            return

        # Ask user to input new coverage type
        coverage_type = input("Enter new Coverage Type ('Single-car' or 'Multi-car'): ")

        # Validate coverage_type input
        if coverage_type == 'Single-car':
            new_coverage_id = 1
        elif coverage_type == 'Multi-car':
            new_coverage_id = 2
        else:
            print("Invalid Coverage Type. Please enter 'Single-car' or 'Multi-car'.")
            return

        # Update coverage details in the database
        c.execute('''
            UPDATE coverage_details
            SET coverage_id = ?, coverage_type = ?
            WHERE policy_number = ? AND coverage_id = ?
        ''', (new_coverage_id, coverage_type, policy_number, coverage_id))

        # Commit changes
        connect.commit()

        print(f"Coverage for Policy Number {policy_number} updated successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")

def upd_vehicle():
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
        policy_number = int(input("Enter the Policy Number to update the vehicle: "))

        # Validate if the selected policy_number exists
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. Please try again.")
            return

        # Fetch existing vehicles for the selected policy
        c.execute("SELECT vehicle_registration, vehicle_type FROM vehicle WHERE policy_number = ?", (policy_number,))
        vehicles = c.fetchall()

        if not vehicles:
            print(f"No vehicles found for Policy Number {policy_number}.")
            return

        # Display the existing vehicles for the selected policy
        print(f"Existing Vehicles for Policy Number {policy_number}:")
        print(f"{'Registration Number':<20} {'Vehicle Type'}")
        print("-" * 40)
        for vehicle in vehicles:
            print(f"{vehicle[0]:<20} {vehicle[1]}")
        print("-" * 40)

        # Ask the user to select a vehicle to update by its registration number
        vehicle_registration = input("Enter the Vehicle Registration Number to update: ")

        # Validate if the entered vehicle registration exists for the selected policy
        c.execute("SELECT vehicle_registration FROM vehicle WHERE policy_number = ? AND vehicle_registration = ?",
                  (policy_number, vehicle_registration))
        if c.fetchone() is None:
            print("Invalid Vehicle Registration Number. Please try again.")
            return

        # Ask the user to enter a new vehicle registration number
        new_registration = input("Enter the new Vehicle Registration Number: ")

        # Ask the user to select the vehicle type
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

        new_vehicle_type = vehicle_types[vehicle_type_choice]

        # Update the vehicle data in the database
        c.execute('''UPDATE vehicle
                     SET vehicle_registration = ?, vehicle_type = ?
                     WHERE policy_number = ? AND vehicle_registration = ?''',
                  (new_registration, new_vehicle_type, policy_number, vehicle_registration))

        # Commit the changes
        connect.commit()

        print(f"Vehicle with registration number {vehicle_registration} updated successfully to {new_registration}.")

    except ValueError as e:
        print(f"Invalid input. Please make sure the data is entered correctly. Error: {e}")
    except sqlite3.Error as e:
        print(f"Error: {e}")

def upd_compPolicy():
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
        policy_number = input("Enter the Policy Number for the comprehensive policy to update: ")

        # Verify the selected policy exists
        c.execute("SELECT policy_number FROM policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. Please try again.")
            return

        # Check if the policy has an existing comprehensive policy
        c.execute("SELECT policy_number FROM comprehensive_policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print(f"No comprehensive policy found for Policy Number {policy_number}.")
            return

        # Fetch existing comprehensive policy details
        c.execute("SELECT deductible, special_coverage FROM comprehensive_policy WHERE policy_number = ?", (policy_number,))
        comp_policy = c.fetchone()

        # Display existing comprehensive policy details
        print(f"Existing Comprehensive Policy for Policy Number {policy_number}:")
        print(f"Deductible: {comp_policy[0]}")
        print(f"Special Coverage: {comp_policy[1]}")

        # Prompt the user to update deductible
        while True:
            try:
                deductible = float(input(f"Enter new Deductible (current: {comp_policy[0]}): "))
                if deductible < 0:
                    raise ValueError("Deductible cannot be negative.")
                break
            except ValueError as e:
                print(e)

        # Prompt the user to update special coverage
        special_coverage = input(f"Enter new Special Coverage (current: {comp_policy[1]}): ")

        # Update the comprehensive policy in the database
        c.execute('''
            UPDATE comprehensive_policy
            SET deductible = ?, special_coverage = ?
            WHERE policy_number = ?
        ''', (deductible, special_coverage, policy_number))

        # Commit the transaction
        connect.commit()

        print(f"Comprehensive policy for Policy Number {policy_number} updated successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def upd_3PPolicy():
    try:
        # Fetch all available third-party policies
        c.execute('''SELECT policy_number, liability_limit FROM third_party_policy''')
        policies = c.fetchall()

        # Check if any third-party policies exist
        if not policies:
            print("No third-party policies available to update.")
            return

        # Display available third-party policies
        print("Existing Third-party Policies:")
        print(f"{'Policy Number':<15} {'Liability Limit':<20}")
        print("-" * 35)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<20}")
        print("-" * 35)

        # Prompt the user to select a policy number to update
        policy_number = input("Enter the Policy Number to update the third-party policy: ")

        # Validate the selected policy exists in the third-party policies table
        c.execute("SELECT policy_number FROM third_party_policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. Please select a valid option.")
            return

        # Fetch the current liability limit for the selected policy
        c.execute("SELECT liability_limit FROM third_party_policy WHERE policy_number = ?", (policy_number,))
        current_limit = c.fetchone()[0]

        # Display the current liability limit
        print(f"Current Liability Limit: {current_limit}")

        # Prompt the user to enter a new liability limit
        while True:
            try:
                liability_limit = float(input(f"Enter new Liability Limit (current: {current_limit}): "))
                if liability_limit < 0:
                    raise ValueError("Liability limit must be non-negative.")
                break
            except ValueError as e:
                print(e)

        # Update the liability limit for the selected third-party policy
        c.execute('''
            UPDATE third_party_policy
            SET liability_limit = ?
            WHERE policy_number = ?
        ''', (liability_limit, policy_number))

        # Commit the transaction
        connect.commit()

        print(f"Third-party policy with Policy Number {policy_number} updated successfully.")

    except ValueError as e:
        print(f"Error: {e}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")

def upd_personalPolicy():
    try:
        # Fetch all personal purpose policies
        c.execute('''
            SELECT pp.policy_number, p.start_date, p.end_date, pp.driver_restrictions
            FROM personal_purpose pp
            JOIN policy p ON pp.policy_number = p.policy_number
        ''')
        personal_policies = c.fetchall()

        # Check if there are any personal policies
        if not personal_policies:
            print("No personal purpose policies available to modify.")
            return

        # Display available personal policies
        print("Personal Purpose Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Driver Restrictions':<30}")
        print("-" * 80)
        for policy in personal_policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<30}")
        print("-" * 80)

        # Prompt the user to select a policy number to modify
        policy_number = input("Enter the Policy Number to modify its personal purpose: ")

        # Verify the policy exists in the personal_purpose table
        c.execute("SELECT policy_number FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Prompt the user for the new driver restrictions
        new_restrictions = input("Enter new Driver Restrictions (leave blank to cancel): ").strip()
        if not new_restrictions:
            print("Modification canceled.")
            return

        # Update the personal purpose
        c.execute('''
            UPDATE personal_purpose 
            SET driver_restrictions = ?
            WHERE policy_number = ?
        ''', (new_restrictions, policy_number))
        connect.commit()

        print(f"Personal purpose for Policy Number {policy_number} successfully updated to '{new_restrictions}'.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def upd_commercialPolicy():
    try:
        # Fetch all policies with commercial purposes
        c.execute('''
            SELECT p.policy_number, p.start_date, p.end_date, p.premium_amount, cp.business_use_details
            FROM policy p
            JOIN commercial_purpose cp ON p.policy_number = cp.policy_number
        ''')
        policies = c.fetchall()

        # Check if there are any policies with commercial purposes
        if not policies:
            print("No policies with a commercial purpose to update.")
            return

        # Display available policies with commercial purpose
        print("Policies with Commercial Purpose:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10} {'Business Use'}")
        print("-" * 75)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10} {policy[4]}")
        print("-" * 75)

        # Prompt the user to select a policy number
        policy_number = input("Enter the Policy Number to update its commercial purpose: ")

        # Verify if the policy exists in the commercial_purpose table
        c.execute("SELECT policy_number FROM commercial_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("This policy does not have a commercial purpose assigned.")
            return

        # Prompt the user to enter new business use details
        new_business_use_details = input("Enter the new business use details: ")

        # Update the commercial purpose details
        c.execute('''
            UPDATE commercial_purpose
            SET business_use_details = ?
            WHERE policy_number = ?
        ''', (new_business_use_details, policy_number))

        # Commit the transaction
        connect.commit()

        print(f"Commercial purpose successfully updated for Policy Number {policy_number}.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def upd_policyType():
    try:
        # Display all available policy types
        c.execute("SELECT policy_type_id, type_name, applicable_laws FROM policy_type")
        policy_types = c.fetchall()

        if not policy_types:
            print("No policy types available to update.")
            return

        print("Available Policy Types:")
        print(f"{'Policy Type ID':<15} {'Type Name':<20} {'Applicable Laws'}")
        print("-" * 60)

        for policy_type in policy_types:
            print(f"{policy_type[0]:<15} {policy_type[1]:<20} {policy_type[2]}")

        print("-" * 60)

        # Prompt the user to select a policy type to update
        policy_type_id = input("Enter the Policy Type ID to update: ")

        # Verify the policy type exists
        c.execute("SELECT policy_type_id FROM policy_type WHERE policy_type_id = ?", (policy_type_id,))
        if c.fetchone() is None:
            print("Invalid Policy Type ID. No changes made.")
            return

        # Get the new details for the policy type
        new_type_name = input("Enter the new type name: ")
        new_applicable_laws = input("Enter the new applicable laws: ")

        # Update the policy type in the database
        c.execute('''
            UPDATE policy_type
            SET type_name = ?, applicable_laws = ?
            WHERE policy_type_id = ?
        ''', (new_type_name, new_applicable_laws, policy_type_id))

        # Commit the transaction
        connect.commit()

        print(f"Policy type with ID {policy_type_id} successfully updated.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def upd_policyPurpose():
    try:
        # Display all available policy purposes
        c.execute("SELECT purpose_id, purpose_type, eligibility_criteria FROM policy_purpose")
        policy_purposes = c.fetchall()

        if not policy_purposes:
            print("No policy purposes available to update.")
            return

        print("Available Policy Purposes:")
        print(f"{'Purpose ID':<15} {'Purpose Type':<20} {'Eligibility Criteria'}")
        print("-" * 60)

        for purpose in policy_purposes:
            print(f"{purpose[0]:<15} {purpose[1]:<20} {purpose[2]}")

        print("-" * 60)

        # Prompt the user to select a policy purpose to update
        purpose_id = input("Enter the Policy Purpose ID to update: ")

        # Verify the policy purpose exists
        c.execute("SELECT purpose_id FROM policy_purpose WHERE purpose_id = ?", (purpose_id,))
        if c.fetchone() is None:
            print("Invalid Policy Purpose ID. No changes made.")
            return

        # Get the new details for the policy purpose
        new_purpose_type = input("Enter the new purpose type: ")
        new_eligibility_criteria = input("Enter the new eligibility criteria: ")

        # Update the policy purpose in the database
        c.execute('''
            UPDATE policy_purpose
            SET purpose_type = ?, eligibility_criteria = ?
            WHERE purpose_id = ?
        ''', (new_purpose_type, new_eligibility_criteria, purpose_id))

        # Commit the transaction
        connect.commit()

        print(f"Policy purpose with ID {purpose_id} successfully updated.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
'''
def upd_policyholder():
def upd_policyholder():
def upd_policyholder():
    '''
