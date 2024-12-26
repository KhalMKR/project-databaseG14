import sqlite3
''' createtable.py
    Here defines the table creation(will only happen once)
    for the database

'''
# define connection and cursor
connect = sqlite3.connect('insurance.db')

c = connect.cursor()


# define tables in the database

# policyholder
def create_table():
    # policyholder
    c.execute('''
    CREATE TABLE IF NOT EXISTS policyholder (
        policyholder_id INTEGER PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        contact_details VARCHAR(40),
        dob DATE,
        driving_license CHAR(3) CHECK (driving_license IN ('D', 'DA'))
    )
    ''')

    # policy
    c.execute('''
    CREATE TABLE IF NOT EXISTS policy (
        policy_number INTEGER PRIMARY KEY,
        start_date DATE,
        end_date DATE,
        premium_amount FLOAT CHECK (premium_amount >= 0),
        policyholder_id INTEGER NOT NULL,
        FOREIGN KEY (policyholder_id) REFERENCES policyholder (policyholder_id) ON DELETE CASCADE
    )
    ''')

    # coverage_details
    c.execute('''
    CREATE TABLE IF NOT EXISTS coverage_details (
        policy_number INTEGER NOT NULL,
        coverage_id INTEGER NOT NULL,
        coverage_type VARCHAR(15) CHECK (coverage_type IN ('Single-car', 'Multi-car')),
        PRIMARY KEY (policy_number, coverage_id),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    # vehicle
    c.execute('''
    CREATE TABLE IF NOT EXISTS vehicle (
        policy_number INTEGER NOT NULL,
        vehicle_registration VARCHAR(15) NOT NULL,
        vehicle_type VARCHAR(10) CHECK (vehicle_type IN ('Sedan', 'SUV', 'Truck', 'MPV')),
        PRIMARY KEY (policy_number, vehicle_registration),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    # policy_type
    c.execute('''
    CREATE TABLE IF NOT EXISTS policy_type (
        policy_type_id INTEGER PRIMARY KEY,
        type_name VARCHAR(20) NOT NULL,
        applicable_laws VARCHAR(50)
    )
    ''')

    # comprehensive_policy
    c.execute('''
    CREATE TABLE IF NOT EXISTS comprehensive_policy (
        policy_number INTEGER PRIMARY KEY,
        deductible FLOAT CHECK (deductible >= 0),
        special_coverage VARCHAR(50),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    # third-party_policy
    c.execute('''
    CREATE TABLE IF NOT EXISTS third_party_policy (
        policy_number INTEGER PRIMARY KEY,
        liability_limit FLOAT CHECK (liability_limit >= 0),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    # policy_purpose
    c.execute('''
    CREATE TABLE IF NOT EXISTS policy_purpose (
        purpose_id INTEGER PRIMARY KEY,
        purpose_type VARCHAR(30) NOT NULL,
        eligibility_criteria VARCHAR(50)
    )
    ''')

    # personal_purpose
    c.execute('''
    CREATE TABLE IF NOT EXISTS personal_purpose (
        policy_number INTEGER PRIMARY KEY,
        driver_restrictions VARCHAR(30),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    # commercial_purpose
    c.execute('''
    CREATE TABLE IF NOT EXISTS commercial_purpose (
        policy_number INTEGER PRIMARY KEY,
        business_use_details VARCHAR(30),
        FOREIGN KEY (policy_number) REFERENCES policy (policy_number) ON DELETE CASCADE
    )
    ''')

    connect.commit()



