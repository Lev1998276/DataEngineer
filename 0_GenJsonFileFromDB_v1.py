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

 
 

sf_conn = create_snowflake_connection()


result = get_json_data(sf_conn)
print(type(result))
print(f"Values returned from the function - > {result}")


#Writing query output to csv file 
header_row = ['AutomationKey','FormMode','KeyValue','Link to Person','Treatment History','Admission Date','Discharge Date','Facility Name','Source','Type','Agency']
write_tuples_to_csv(result, 'output.csv',header_row)


#write the output from csv to json file 
# Specify the path to the CSV file
csv_file_path = 'output.csv' 

# Read CSV data and convert to a list of dictionaries
csv_data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_data.append(row)

key_value = csv_data[0]["KeyValue"]

# Extract headers for FormLines
headers = [key for key in csv_data[0].keys() if key not in ["AutomationKey", "FormMode", "KeyValue"]]

# Create the JSON structure with loaded values
json_data = {
    "AutomationKey": 'tx_hx_hosp',
    "FormMode": 'ADD',
    "KeyValue": key_value,
    "FormLines": [
        {header: row[header] for header in headers} for row in csv_data
    ],
    "SubData": []
}

# Print the resulting JSON structure
print(json.dumps(json_data, indent=2))



     