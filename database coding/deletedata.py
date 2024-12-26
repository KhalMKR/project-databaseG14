import sqlite3
from datetime import datetime
''' deletedata.py
    Here defines the delete funtion for
    the database

'''
# define connection and cursor
connect = sqlite3.connect('insurance.db')

c = connect.cursor()

# function for deleting policyholder and all data associated with it
def delete_policyholder():
    try:
        # Display all available policyholders
        print("Available Policyholders:")
        c.execute("SELECT policyholder_id, full_name FROM policyholder")
        policyholders = c.fetchall()

        if not policyholders:
            print("No policyholders found.")
            return

        for ph in policyholders:
            print(f"ID: {ph[0]}, Name: {ph[1]}")  # Show the ID and name

        # Ask the user to select a policyholder to delete
        policyholder_id = int(input("Enter the Policyholder ID to delete: "))

        # Check if the policyholder exists
        c.execute("SELECT COUNT(*) FROM policyholder WHERE policyholder_id = ?", (policyholder_id,))
        exists = c.fetchone()[0]

        if exists:
            # Delete the policyholder (and any related policies due to cascading delete)
            c.execute("DELETE FROM policyholder WHERE policyholder_id = ?", (policyholder_id,))
            connect.commit()
            print(f"Policyholder with ID {policyholder_id} deleted successfully!")
        else:
            print("Policyholder ID not found. Please enter a valid ID.")

    except ValueError:
        print("Invalid input. Please enter a valid Policyholder ID.")

def delete_policy():
    try:
        # Display all available policies
        c.execute("SELECT policy_number, start_date, end_date, premium_amount FROM policy")
        policies = c.fetchall()

        # Check if there are any policies to display
        if not policies:
            print("No policies available to delete.")
            return

        # Display the available policies
        print("Available Policies:")
        for policy in policies:
            print(f"Policy Number: {policy[0]}, Start Date: {policy[1]}, End Date: {policy[2]}, Premium: {policy[3]}")

        # Prompt user to select a policy number to delete
        policy_number = int(input("Enter the policy number of the policy you want to delete: "))

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete policy {policy_number}? (y/n): ").strip().lower()

        if confirm != "y":
            print("Policy deletion canceled.")
            return

        # First, delete from tables that reference policy_number
        c.execute("DELETE FROM coverage_details WHERE policy_number = ?", (policy_number,))
        c.execute("DELETE FROM vehicle WHERE policy_number = ?", (policy_number,))
        c.execute("DELETE FROM comprehensive_policy WHERE policy_number = ?", (policy_number,))
        c.execute("DELETE FROM third_party_policy WHERE policy_number = ?", (policy_number,))
        c.execute("DELETE FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        c.execute("DELETE FROM commercial_purpose WHERE policy_number = ?", (policy_number,))

        # Now, delete the policy itself
        c.execute("DELETE FROM policy WHERE policy_number = ?", (policy_number,))

        # Commit changes
        connect.commit()

        print(f"Policy with policy number {policy_number} and all related data deleted successfully!")

    except Exception as e:
        print(f"Error: {e}")

def delete_coverage():
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
        policy_number = int(input("Enter Policy Number to delete coverage: "))

        # Validate if the entered policy_number exists
        c.execute("SELECT 1 FROM policy WHERE policy_number = ?", (policy_number,))
        if not c.fetchone():
            print("Invalid Policy Number. Please try again.")
            return

        # Ask user to input coverage type to delete
        coverage_type = input("Enter Coverage Type to delete ('Single-car' or 'Multi-car'): ")

        # Validate coverage_type input and determine the coverage_id
        if coverage_type == 'Single-car':
            coverage_id = 1
        elif coverage_type == 'Multi-car':
            coverage_id = 2
        else:
            print("Invalid Coverage Type. Please enter 'Single-car' or 'Multi-car'.")
            return

        # Check if the coverage exists for the selected policy
        c.execute('''SELECT 1 FROM coverage_details 
                     WHERE policy_number = ? AND coverage_id = ?''', (policy_number, coverage_id))
        if not c.fetchone():
            print(f"No coverage found for Policy Number {policy_number} with Coverage Type '{coverage_type}'.")
            return

        # Ask for confirmation to delete
        confirm = input(f"Are you sure you want to delete the {coverage_type} coverage for Policy Number {policy_number}? (y/n): ").lower()
        if confirm != 'y':
            print("Coverage deletion canceled.")
            return

        # Delete the coverage from coverage_details table
        c.execute('''DELETE FROM coverage_details 
                     WHERE policy_number = ? AND coverage_id = ?''', (policy_number, coverage_id))

        # Commit changes
        connect.commit()

        print(f"Coverage with Coverage ID {coverage_id} and Coverage Type '{coverage_type}' for Policy Number {policy_number} deleted successfully!")

    except ValueError:
        print("Invalid input. Please make sure the data is entered correctly.")

def delete_vehicle():
    try:
        # Fetch all available vehicles with their policy_number and vehicle_registration
        c.execute("SELECT policy_number, vehicle_registration FROM vehicle")
        vehicles = c.fetchall()

        # Check if there are any vehicles available
        if not vehicles:
            print("No vehicles available to delete.")
            return

        # Display the available vehicles for selection
        print("Available Vehicles:")
        for vehicle in vehicles:
            print(f"Policy Number: {vehicle[0]}, Vehicle Registration: {vehicle[1]}")

        # Prompt the user to select a vehicle by its registration number
        vehicle_registration = input("Enter the Vehicle Registration Number to delete: ")

        # Validate if the selected vehicle_registration exists
        c.execute("SELECT vehicle_registration FROM vehicle WHERE vehicle_registration = ?", (vehicle_registration,))
        if c.fetchone() is None:
            print("Invalid Vehicle Registration. Please try again.")
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete the vehicle with registration number {vehicle_registration}? (y/n): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return

        # Delete the vehicle from the vehicle table
        c.execute("DELETE FROM vehicle WHERE vehicle_registration = ?", (vehicle_registration,))

        # Commit the changes
        connect.commit()

        print(f"Vehicle with registration number {vehicle_registration} deleted successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_compPolicy():
    try:
        # Fetch all available comprehensive policies
        c.execute('''
            SELECT cp.policy_number, p.start_date, p.end_date, p.premium_amount, cp.deductible, cp.special_coverage
            FROM comprehensive_policy cp
            JOIN policy p ON cp.policy_number = p.policy_number
        ''')
        policies = c.fetchall()

        # Check if there are any comprehensive policies available
        if not policies:
            print("No comprehensive policies available to delete.")
            return

        # Display comprehensive policies
        print("Available Comprehensive Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10} {'Deductible':<12} {'Special Coverage':<20}")
        print("-" * 90)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10} {policy[4]:<12} {policy[5]:<20}")
        print("-" * 90)

        # Prompt the user to select a policy to delete
        policy_number = input("Enter the Policy Number of the comprehensive policy to delete: ")

        # Verify the selected policy exists
        c.execute("SELECT policy_number FROM comprehensive_policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Delete the comprehensive policy
        c.execute("DELETE FROM comprehensive_policy WHERE policy_number = ?", (policy_number,))

        # Commit the transaction
        connect.commit()

        print(f"Comprehensive policy with Policy Number {policy_number} deleted successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_3PPolicy():
    try:
        # Fetch all available third-party policies
        c.execute('''
            SELECT tp.policy_number, p.start_date, p.end_date, p.premium_amount, tp.liability_limit
            FROM third_party_policy tp
            JOIN policy p ON tp.policy_number = p.policy_number
        ''')
        policies = c.fetchall()

        # Check if there are any third-party policies available
        if not policies:
            print("No third-party policies available to delete.")
            return

        # Display third-party policies
        print("Available Third-Party Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10} {'Liability Limit':<15}")
        print("-" * 80)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10} {policy[4]:<15}")
        print("-" * 80)

        # Prompt the user to select a policy to delete
        policy_number = input("Enter the Policy Number of the third-party policy to delete: ")

        # Verify the selected policy exists
        c.execute("SELECT policy_number FROM third_party_policy WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Delete the third-party policy
        c.execute("DELETE FROM third_party_policy WHERE policy_number = ?", (policy_number,))

        # Commit the transaction
        connect.commit()

        print(f"Third-party policy with Policy Number {policy_number} deleted successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_personalPolicy():
    try:
        # Fetch all policies with personal purposes
        c.execute('''
            SELECT pp.policy_number, p.start_date, p.end_date, pp.driver_restrictions
            FROM personal_purpose pp
            JOIN policy p ON pp.policy_number = p.policy_number
        ''')
        personal_policies = c.fetchall()

        # Check if there are any personal policies
        if not personal_policies:
            print("No personal purpose policies available to delete.")
            return

        # Display available personal policies
        print("Personal Purpose Policies:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Driver Restrictions':<30}")
        print("-" * 80)
        for policy in personal_policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<30}")
        print("-" * 80)

        # Prompt the user to select a policy number to delete
        policy_number = input("Enter the Policy Number to delete its personal purpose: ")

        # Verify the policy exists in the personal_purpose table
        c.execute("SELECT policy_number FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("Invalid Policy Number. No changes made.")
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete personal purpose for Policy Number {policy_number}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion canceled.")
            return

        # Delete the personal purpose
        c.execute("DELETE FROM personal_purpose WHERE policy_number = ?", (policy_number,))
        connect.commit()

        print(f"Personal purpose for Policy Number {policy_number} successfully deleted.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_commercialPolicy():
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
            print("No policies with a commercial purpose to delete.")
            return

        # Display available policies with commercial purpose
        print("Policies with Commercial Purpose:")
        print(f"{'Policy Number':<15} {'Start Date':<15} {'End Date':<15} {'Premium':<10} {'Business Use'}")
        print("-" * 75)
        for policy in policies:
            print(f"{policy[0]:<15} {policy[1]:<15} {policy[2]:<15} {policy[3]:<10} {policy[4]}")
        print("-" * 75)

        # Prompt the user to select a policy number
        policy_number = input("Enter the Policy Number to delete its commercial purpose: ")

        # Verify if the policy exists in the commercial_purpose table
        c.execute("SELECT policy_number FROM commercial_purpose WHERE policy_number = ?", (policy_number,))
        if c.fetchone() is None:
            print("This policy does not have a commercial purpose assigned.")
            return

        # Confirm deletion
        confirm = input(
            f"Are you sure you want to delete personal purpose for Policy Number {policy_number}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion canceled.")
            return

        # Delete the commercial purpose entry for the selected policy
        c.execute('''
            DELETE FROM commercial_purpose
            WHERE policy_number = ?
        ''', (policy_number,))

        # Commit the transaction
        connect.commit()

        print(f"Commercial purpose successfully deleted for Policy Number {policy_number}.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_policyType():
    try:
        # Display all available policy types
        c.execute("SELECT policy_type_id, type_name, applicable_laws FROM policy_type")
        policy_types = c.fetchall()

        if not policy_types:
            print("No policy types available to delete.")
            return

        print("Available Policy Types:")
        print(f"{'Policy Type ID':<15} {'Type Name':<20} {'Applicable Laws'}")
        print("-" * 60)

        for policy_type in policy_types:
            print(f"{policy_type[0]:<15} {policy_type[1]:<20} {policy_type[2]}")

        print("-" * 60)

        # Prompt user to select a policy type to delete
        policy_type_id = input("Enter the Policy Type ID to delete: ")

        # Verify the policy type exists
        c.execute("SELECT policy_type_id FROM policy_type WHERE policy_type_id = ?", (policy_type_id,))
        if c.fetchone() is None:
            print("Invalid Policy Type ID. No changes made.")
            return

        # Delete the selected policy type
        c.execute("DELETE FROM policy_type WHERE policy_type_id = ?", (policy_type_id,))

        # Commit the transaction
        connect.commit()

        print(f"Policy type with ID {policy_type_id} successfully deleted.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

def delete_policyPurpose():
    try:
        # Display all available policy purposes
        c.execute("SELECT purpose_id, purpose_type, eligibility_criteria FROM policy_purpose")
        policy_purposes = c.fetchall()

        if not policy_purposes:
            print("No policy purposes available to delete.")
            return

        print("Available Policy Purposes:")
        print(f"{'Purpose ID':<15} {'Purpose Type':<20} {'Eligibility Criteria'}")
        print("-" * 60)

        for purpose in policy_purposes:
            print(f"{purpose[0]:<15} {purpose[1]:<20} {purpose[2]}")

        print("-" * 60)

        # Prompt user to select a policy purpose to delete
        purpose_id = input("Enter the Policy Purpose ID to delete: ")

        # Verify the policy purpose exists
        c.execute("SELECT purpose_id FROM policy_purpose WHERE purpose_id = ?", (purpose_id,))
        if c.fetchone() is None:
            print("Invalid Policy Purpose ID. No changes made.")
            return

        # Delete the selected policy purpose
        c.execute("DELETE FROM policy_purpose WHERE purpose_id = ?", (purpose_id,))

        # Commit the transaction
        connect.commit()

        print(f"Policy purpose with ID {purpose_id} successfully deleted.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

