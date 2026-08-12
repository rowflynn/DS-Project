import pandas as pd
import psycopg2
import json


df = pd.read_csv('healthcare_dataset.csv') # Read csv file

# Format csv data for database entry
df["Name"] = df["Name"].str.title()
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])


# Connect to database
conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="healthcare",
        user="rflynn",
        password="yourpassword"
    )
cur = conn.cursor()

# Create database tables
def make_tables():
    createCmdPatient = """ CREATE TABLE IF NOT EXISTS patients (
        patient_id SERIAL PRIMARY KEY,
        patient_name VARCHAR(255) NOT NULL,
        patient_age INTEGER NOT NULL,
        patient_gender VARCHAR(50) NOT NULL,
        patient_blood_type VARCHAR(10) NOT NULL
    )
    """
    cur.execute(createCmdPatient)
    
    createCmdDoctor = """ CREATE TABLE IF NOT EXISTS doctors (
        doctor_id SERIAL PRIMARY KEY,
        doctor_name VARCHAR(255) UNIQUE NOT NULL
    )
    """
    cur.execute(createCmdDoctor)
        
    createCmdHospital = """ CREATE TABLE IF NOT EXISTS hospitals (
        hospital_id SERIAL PRIMARY KEY,
        hospital_name VARCHAR(255) UNIQUE NOT NULL
    )
    """
    cur.execute(createCmdHospital)
    
    createCmdInsuranceProvider = """ CREATE TABLE IF NOT EXISTS insurance_providers (
        insurance_id SERIAL PRIMARY KEY,
        provider_name VARCHAR(255) UNIQUE NOT NULL
    )
    """
    cur.execute(createCmdInsuranceProvider)
    
    createCmdCondition = """ CREATE TABLE IF NOT EXISTS conditions (
        condition_id SERIAL PRIMARY KEY,
        condition_name VARCHAR(255) UNIQUE NOT NULL
    )
    """
    cur.execute(createCmdCondition)
    
    createCmdMedication = """ CREATE TABLE IF NOT EXISTS medications (
        medication_id SERIAL PRIMARY KEY,
        medication_name VARCHAR(255) UNIQUE NOT NULL
    )
    """
    cur.execute(createCmdMedication)
    
    createCmdAdmission = """ CREATE TABLE IF NOT EXISTS admissions (
        admission_id SERIAL PRIMARY KEY,
        
        patient_id INTEGER REFERENCES patients(patient_id),
        doctor_id INTEGER REFERENCES doctors(doctor_id),
        hospital_id INTEGER REFERENCES hospitals(hospital_id),
        insurance_id INTEGER REFERENCES insurance_providers(insurance_id),
        condition_id INTEGER REFERENCES conditions(condition_id),
        medication_id INTEGER REFERENCES medications(medication_id), 
        
        admission_date DATE NOT NULL,
        discharge_date DATE NOT NULL,
        admission_type VARCHAR(255) NOT NULL,
        test_results VARCHAR(255) NOT NULL,
        room_number INTEGER NOT NULL,
        billing_amount NUMERIC(12,2) NOT NULL
    )
    """
    cur.execute(createCmdAdmission)
      
# Add csv data to tables
def populate_tables():
    # Create unique lists
    unique_names = df.drop_duplicates(subset=["Name"])
    doctor_list = df['Doctor'].unique()
    hospital_list = df['Hospital'].unique()
    insurance_list = df['Insurance Provider'].unique()
    condition_list = df['Medical Condition'].unique()
    medication_list = df['Medication'].unique()

    # Populate tables
    for _, row in unique_names.iterrows(): 
        cur.execute(
            """
            INSERT INTO patients (patient_name, patient_age, patient_gender, patient_blood_type)
            VALUES (%s, %s, %s, %s)
            """,
            (row["Name"], row["Age"], row["Gender"], row["Blood Type"])
        )
    for doctor in doctor_list:
        cur.execute(
            """
            INSERT INTO doctors (doctor_name)
            VALUES (%s)
            """,
            (doctor,)    
        ) 
    for hospital in hospital_list:
        cur.execute(
            """
            INSERT INTO hospitals (hospital_name)
            VALUES (%s)
            """,
            (hospital,)    
        )
    for provider in insurance_list:
        cur.execute(
            """
            INSERT INTO insurance_providers (provider_name)
            VALUES (%s)
            """,
            (provider,)    
        )
    for condition in condition_list:
        cur.execute(
            """
            INSERT INTO conditions (condition_name)
            VALUES (%s)
            """,
            (condition,)    
        )
    for medication in medication_list:
        cur.execute(
            """
            INSERT INTO medications (medication_name)
            VALUES (%s)
            """,
            (medication,)    
        )


    # Create lookup tables
    cur.execute(
        """
        SELECT patient_id, patient_name
        FROM patients
        """
    )
    patient_map = {}
    for patient_id, patient_name in cur.fetchall():
        patient_map[patient_name] = patient_id

    cur.execute(
        """
        SELECT doctor_id, doctor_name
        FROM doctors
        """
    )
    doctor_map = {}
    for doctor_id, doctor_name in cur.fetchall():
        doctor_map[doctor_name] = doctor_id
        
    cur.execute(
        """
        SELECT hospital_id, hospital_name
        FROM hospitals
        """
    )
    hospital_map = {}
    for hospital_id, hospital_name in cur.fetchall():
        hospital_map[hospital_name] = hospital_id
        
    cur.execute(
        """
        SELECT insurance_id, provider_name
        FROM insurance_providers
        """
    )
    insurance_map = {}
    for insurance_id, provider_name in cur.fetchall():
        insurance_map[provider_name] = insurance_id

    cur.execute(
            """
            SELECT condition_id, condition_name
            FROM conditions
            """
        )
    condition_map = {}
    for condition_id, condition_name in cur.fetchall():
        condition_map[condition_name] = condition_id
        
    cur.execute(
            """
            SELECT medication_id, medication_name
            FROM medications
            """
        )
    medication_map = {}
    for medication_id, medication_name in cur.fetchall():
        medication_map[medication_name] = medication_id

    # Populate admissions table
    for _, row in df.iterrows(): 
        cur.execute(
            """
            INSERT INTO admissions (
                patient_id,
                doctor_id,
                hospital_id,
                insurance_id,
                condition_id,
                medication_id,
                
                admission_date,
                discharge_date,
                admission_type,
                test_results,
                room_number,
                billing_amount
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                patient_map[row['Name']],
                doctor_map[row['Doctor']],
                hospital_map[row['Hospital']],
                insurance_map[row['Insurance Provider']],
                condition_map[row['Medical Condition']],
                medication_map[row['Medication']],
                
                row['Date of Admission'],
                row['Discharge Date'],
                row['Admission Type'],
                row['Test Results'],
                row['Room Number'],
                row['Billing Amount']
            )
        )
    
    conn.commit()

def reset ():
    cur.execute(
    """
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    """
    )
    make_tables()
    populate_tables()
    

reset()