import sqlite3
import createtable, adddata as add, updatedata as update, deletedata as delete, generalSQL as gen

''' THE MAIN PYTHON PROGRAM
    Here defines the function for main program

'''
# function for create table
def create():
    createtable.create_table()

# function for adding preset data
def preset():
    add.predefined_data()

# main menu function
def main_menu():
    # Hardcoded terminal width
    terminal_width = 80

    # Text to center
    menu_header = "MAIN MENU"

    # Calculate spaces to center the text
    padding = (terminal_width - len(menu_header)) // 2

    # Print the menu with centered "MAIN MENU"
    print("\nWelcome to the main menu of the SafeDrive Insurance System")
    print("=" * terminal_width)
    print(" " * padding + menu_header)
    print("=" * terminal_width)
    print("\nSelect an option:")
    print("1. Add Data")
    print("2. Delete Data")
    print("3. Update Data")
    print("4. Show all tables")
    print("5. Access SQL command interface")
    print("6. Exit")

    try:
        choice = int(input("\nEnter the number of your choice: "))

        # Handle the options based on user input
        if choice == 1:
            add_menu()
        elif choice == 2:
            delete_menu()
        elif choice == 3:
            update_menu()
        elif choice == 4:
            gen.show_all()
            return main_menu()
        elif choice == 5:
            sql_cmd()
            return main_menu()
        elif choice == 6:
            print("\nExiting the system. Goodbye!")
            gen.close()
            return  # Exit the program
        else:
            print("\nInvalid choice! Please select a valid option.")
            main_menu()  # Recursively call the menu if the input is invalid
    except ValueError:
        print("\nInvalid input! Please enter a number.")
        main_menu()  # Recursively call the menu if input is not a number

def add_menu():
    # Hardcoded terminal width
    terminal_width = 80

    # Text to center
    menu_header = "ADD DATA MENU"

    # Calculate spaces to center the text
    padding = (terminal_width - len(menu_header)) // 2
    padding2 = (terminal_width - len("Please select which data to be added")) // 2

    # Print the menu with centered "ADD DATA MENU"
    print(" " * padding + menu_header)
    print("=" * terminal_width)
    print(" " * padding2 + "Please select which data to be added")
    print("=" * terminal_width)

    # Option menu with choices
    print("1. Add Policyholder")
    print("2. Add Policy")
    print("3. Add Vehicle")
    print("4. Add Coverage Details")
    print("5. Add Comprehensive Policy")
    print("6. Add Third-party Policy")
    print("7. Add Personal Purpose Policy")
    print("8. Add Commercial Purpose Policy")
    print("9. Add Policy Type")
    print("10. Add Policy Purpose")
    print("Type 'back' to return to the Main Menu.")

    # User input for menu selection
    choice = input("Enter your choice (or 'back' to exit): ").strip().lower()

    # Handle user selection
    if choice == "1":
        add.add_policyholder()
        return add_menu()
    elif choice == "2":
        add.add_policy()
        return add_menu()
    elif choice == "3":
        add.add_vehicle()
        return add_menu()
    elif choice == "4":
        add.add_coverage()
        return add_menu()
    elif choice == "5":
        add.add_compPolicy()
        return add_menu()
    elif choice == "6":
        add.add_3PPolicy()
        return add_menu()
    elif choice == "7":
        add.add_personalPolicy()
        return add_menu()
    elif choice == "8":
        add.add_commercialPolicy()
        return add_menu()
    elif choice == "9":
        add.add_policyType()
        return add_menu()
    elif choice == "10":
        add.add_policyPurpose()
        return add_menu()
    elif choice == "back":
        print("Exiting to Main Menu...")
        return main_menu()  # Exit the menu and return to main menu
    else:
        print("Invalid choice. Please select a valid option.")
        return add_menu()  # Loop again if input is invalid

def delete_menu():
    # Hardcoded terminal width
    terminal_width = 80

    # Text to center
    menu_header = "DELETE DATA MENU"

    # Calculate spaces to center the text
    padding = (terminal_width - len(menu_header)) // 2
    padding2 = (terminal_width - len("Please select which data to be deleted")) // 2

    # Print the menu with centered "MAIN MENU"
    print(" " * padding + menu_header)
    print("=" * terminal_width)
    print(" " * padding2 + "Please select which data to be deleted")
    print("WARNING!!! : DELETING A ROW OF DATA WILL DELETE ALL ASSOCIATED DATA WITH THAT ROW")
    print("=" * terminal_width)

    # Option menu with choices
    print("1. Delete Policyholder")
    print("2. Delete Policy")
    print("3. Delete Vehicle")
    print("4. Delete Coverage Details")
    print("5. Delete Comprehensive Policy")
    print("6. Delete Third-party Policy")
    print("7. Delete Personal Purpose Policy")
    print("8. Delete Commercial Purpose Policy")
    print("9. Delete Policy Type")
    print("10. Delete Policy Purpose")
    print("Type 'back' to return to the Main Menu.")

    # User input for menu selection
    choice = input("Enter your choice (or 'back' to exit): ").strip().lower()

    # Handle user selection
    if choice == "1":
        delete.delete_policyholder()
        return delete_menu()
    elif choice == "2":
        delete.delete_policy()
        return delete_menu()
    elif choice == "3":
        delete.delete_vehicle()
        return delete_menu()
    elif choice == "4":
        delete.delete_coverage()
        return delete_menu()
    elif choice == "5":
        delete.delete_compPolicy()
        return delete_menu()
    elif choice == "6":
        delete.delete_3PPolicy()
        return delete_menu()
    elif choice == "7":
        delete.delete_personalPolicy()
        return delete_menu()
    elif choice == "8":
        delete.delete_commercialPolicy()
        return delete_menu()
    elif choice == "9":
        delete.delete_policyType()
        return delete_menu()
    elif choice == "10":
        delete.delete_policyPurpose()
        return delete_menu()
    elif choice == "back":
        print("Exiting To Main Menu...")
        return main_menu()  # Exit the menu
    else:
        print("Invalid choice. Please select a valid option.")
        return delete_menu()

def update_menu():
    # Hardcoded terminal width
    terminal_width = 80

    # Text to center
    menu_header = "UPDATE DATA MENU"

    # Calculate spaces to center the text
    padding = (terminal_width - len(menu_header)) // 2
    padding2 = (terminal_width - len("Please select which data to be updated")) // 2

    # Print the menu with centered "ADD DATA MENU"
    print(" " * padding + menu_header)
    print("=" * terminal_width)
    print(" " * padding2 + "Please select which data to be updated")
    print("=" * terminal_width)

    # Option menu with choices
    print("1. Update Policyholder")
    print("2. Update Policy")
    print("3. Update Vehicle")
    print("4. Update Coverage Details")
    print("5. Update Comprehensive Policy")
    print("6. Update Third-party Policy")
    print("7. Update Personal Purpose Policy")
    print("8. Update Commercial Purpose Policy")
    print("9. Update Policy Type")
    print("10. Update Policy Purpose")
    print("Type 'back' to return to the Main Menu.")

    # User input for menu selection
    choice = input("Enter your choice (or 'back' to exit): ").strip().lower()

    # Handle user selection
    if choice == "1":
        update.upd_policyholder()
        return update_menu()
    elif choice == "2":
        update.upd_policy()
        return update_menu()
    elif choice == "3":
        update.upd_vehicle()
        return update_menu()
    elif choice == "4":
        update.upd_coverage()
        return update_menu()
    elif choice == "5":
        update.upd_compPolicy()
        return update_menu()
    elif choice == "6":
        update.upd_3PPolicy()
        return update_menu()
    elif choice == "7":
        update.upd_personalPolicy()
        return update_menu()
    elif choice == "8":
        update.upd_commercialPolicy()
        return update_menu()
    elif choice == "9":
        update.upd_policyType()
        return update_menu()
    elif choice == "10":
        update.upd_policyPurpose()
        return update_menu()
    elif choice == "back":
        print("Exiting to Main Menu...")
        return main_menu()  # Exit the menu and return to main menu
    else:
        print("Invalid choice. Please select a valid option.")
        return update_menu()  # Loop again if input is invalid

# function for allowing user to use the SQL command line
def sql_cmd():
    # Asks for input in the form of SQL command
    sqlcmd = input("Input SQL commands: ").strip()

    # Execute the SQL command via the execute_comm function and get the result
    result = gen.execute_comm(sqlcmd)

    # If the result is not None (for SELECT queries), print the data
    if result:
        for row in result:
            print(row)  # Print each row of the result
    else:
        print("No data to display.")

# startup
if __name__ == "__main__":
    # start up the database
    gen.enable_FK()
    create()
    preset()
    main_menu()

