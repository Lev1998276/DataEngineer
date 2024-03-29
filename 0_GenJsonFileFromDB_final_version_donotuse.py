import os
import snowflake.connector
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import csv
import json

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

CEDL_HOME = os.environ['CEDL_HOME']
nexus_connectionProfile = CEDL_HOME + '/etc/.sf.nexus.profile'
s3_connectionProfile = CEDL_HOME + '/etc/.s3_connection_profile'


def create_snowflake_connection():
    try:
        pathExist = os.path.exists(nexus_connectionProfile)
        if (not pathExist):
            print('The profile {} doesn''t exist'.format(nexus_connectionProfile))
            exit(1)
        profileFile = open(nexus_connectionProfile)
        for line in profileFile:
            if (line.split('=')[0] == 'snowflakeAccount'):
                snowflakeAccount = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeUsername'):
                snowflakeUsername = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakePassword'):
                snowflakePassword = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeRole'):
                snowflakeRole = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeDBName'):
                snowflakeDBName = line.split('=')[1].replace('\n', '')
            elif (line.split('=')[0] == 'snowflakeWarehouse'):
                snowflakeWarehouse = line.split('=')[1].replace('\n', '')
            else:
                pass
        profileFile.close()
        if (len(snowflakeAccount) == 0 or len(snowflakeUsername) == 0 or len(snowflakePassword) == 0 or len(
                snowflakeRole) == 0 or len(snowflakeDBName) == 0 or len(snowflakeWarehouse) == 0):
            print('some parameters are missing from {}'.format(nexus_connectionProfile))
            exit(1)
        conn = snowflake.connector.connect(user=snowflakeUsername, password=snowflakePassword, account=snowflakeAccount,
                            warehouse=snowflakeWarehouse, database=snowflakeDBName)
        print("connected to SNOWFLAKE Database.")
    except snowflake.connector.Error as e:
        print('Error connecting to SNOWFLAKE Database - {}'.format(e))
        exit(1)
    return conn
    
    
#get the json data from the database     
def get_json_data(conn):
    try:
        sf_cur = sf_conn.cursor()
        query = '''
                
       SELECT 'tx_hx_hosp'     AS AutomationKey,
               'ADD'            AS FormMode,
               NULL             AS KeyValue,
               D.sponsor_mrn    AS "Link to Person",
               CASE
                 WHEN Trim(Upper(D.facility_type)) = 'HHA' THEN 'Post Acute-Home Care'
                 WHEN Trim(Upper(D.facility_type)) = 'HOSPICE' THEN 'Post Acute-Hospice'
                 WHEN Trim(Upper(D.facility_type)) = 'IRF' THEN 'Post Acute-IRF'
                 WHEN Trim(Upper(D.facility_type)) = 'LTACH' THEN
                 'Post Acute-Long Term Care'
                 WHEN Trim(Upper(D.facility_type)) = 'SNF' THEN 'Post Acute-SNF'
                 WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                      AND Trim(Upper(D.setting)) = 'OBSERVATION' THEN 'Observation'
                 WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                      AND Trim(Upper(D.setting)) = 'EMERGENCY' THEN 'ED/ER'
                 WHEN Trim(Upper(D.facility_type)) = 'HOSPITAL'
                      AND Trim(Upper(D.setting)) = 'INPATIENT' THEN 'Inpatient'
               END              AS "Treatment History Type",
               D.status_date
               || ' '
               || D.status_time AS "Admission Date",
               NULL             AS "Discharge Date",
               D.facility       AS "Facility Name",
               'CAREPORT'       AS SOURCE,
               NULL             AS Type,
               NULL             AS Agency
        FROM   nexus.dw_owner.careport_daily_event D
        WHERE  D.sponsor_mrn = '10033814'
               AND Trim(Upper(D.status)) NOT IN ('DISCHARGED - CANCELLED', 'ADMITTED - CANCELLED', 'SETTING CHANGED - CANCELLED' );
                '''
        sf_cur.execute(query,)
        result = sf_cur.fetchall()

        if sf_cur.rowcount == 0:
            print('No Data available')
            exit(1)
        else:
            print("Query was executed successfully")
    except Exception as e:
        print('Error getting query details: {}'.format(e))
        exit(1)
    return  result
    
 
#Convert data from the query to csv file 
def write_tuples_to_csv(data, file_path, header=None):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write the header if provided
            if header:
                csv_writer.writerow(header)

            csv_writer.writerows(data)

        print(f'The data has been written to {file_path}')
    except Exception as e:
        print(f'Error writing to CSV: {e}')


def read_csv(file_path):
    """
    Read data from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - headers (list): List of column headers.
    - data (list): List of rows as dictionaries.
    """
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        headers = csv_reader.fieldnames
        data = [row for row in csv_reader]

    return headers, data




def convert_to_json_structure(csv_data):
    """
    Convert CSV data to the specified JSON structure.

    Parameters:
    - csv_data (list): List of rows as dictionaries.

    Returns:
    - json_data (dict): JSON structure.
    """
    json_data = {
        "AutomationKey": 'tx_hx_hosp',
        "FormMode": 'ADD',
        "KeyValue": None,
        "FormLines": [],
        "SubData": []
    }
    
    print("\n")
    print("\n")
    print(f"Headers = > {csv_data[0]}")
    print("\n")
    print("\n")

    for row in csv_data:
        print(row)
        form_line = [
            {"Caption": header, "value": row.get(header, "")} for header in csv_data[0]
        ]
        json_data["FormLines"].append(form_line)

    return json_data

# Example usage
csv_file_path = 'output.csv'
headers, csv_data = read_csv(csv_file_path)

# Convert to the specified JSON structure
json_data = convert_to_json_structure(csv_data)

# Update the KeyValue in the JSON structure
json_data["KeyValue"] = csv_data[0]["KeyValue"]

# Print the resulting JSON data

print(json.dumps(json_data,indent = 4))
