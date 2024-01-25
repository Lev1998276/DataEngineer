## /AppDev/CEDL/etl/SrcFiles/lg/visit

#exjson1.py
import csv
import json

csv_file_path = 'sample.csv'
json_file_path = 'output.json'

# Read CSV and convert to a list of dictionaries
csv_data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_data.append(row)

# Write JSON data to a file
with open(json_file_path, 'w') as json_file:
    json.dump(csv_data, json_file, indent=2)
    
# Read JSON from file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Convert data to JSON-formatted string
json_string = json.dumps(json_data, indent=2)

# Print JSON to the terminal
print(json_string)
print("\n")
print(f"Data has been read from {csv_file_path} and written to {json_file_path}.")





##exjson2.py
import json
import requests

# API endpoint URL for testing (JSONPlaceholder)
api_url = 'https://jsonplaceholder.typicode.com/posts'

# Path to the JSON file
json_file_path = 'output.json'

try:
    # Read JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Make a POST request with JSON data
    response = requests.post(api_url, json=json_data)

    # Check the response status
    response.raise_for_status()

    print('JSON data successfully sent to the test API.')
    print('Response:')
    print(response.json())

except FileNotFoundError:
    print(f'Error: JSON file not found at {json_file_path}')

except json.JSONDecodeError:
    print(f'Error: Unable to decode JSON data from {json_file_path}')

except requests.RequestException as e:
    print(f'Error sending JSON data to the test API: {e}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')



# SNIPPET TO ADD TOTAL  NUMBER OF POSTS SUCCESSFULLY DEPOSITED IN THE API 
#exjson3.py

import json
import requests

# API endpoint URL for testing (JSONPlaceholder)
api_url = 'https://jsonplaceholder.typicode.com/posts'

# Path to the JSON file
json_file_path = 'output.json'

total_records_sent = 0  # Initialize the counter

try:
    # Read JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

        # Check if there are records to send
        if isinstance(json_data, list):
            total_records_sent = len(json_data)

            # Make a POST request for each record in JSON data
            for record in json_data:
                response = requests.post(api_url, json=record)
                response.raise_for_status()

        else:
            print(f'Error: JSON data is not a list. Unable to send records.')

    print(f'{total_records_sent} record(s) successfully sent to the test API.')

except FileNotFoundError:
    print(f'Error: JSON file not found at {json_file_path}')

except json.JSONDecodeError:
    print(f'Error: Unable to decode JSON data from {json_file_path}')

except requests.RequestException as e:
    print(f'Error sending JSON data to the test API: {e}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')




#CHECK THE DATA IS POSTED IN API 
#exjson4.py

import json
import requests

# API endpoint URL for testing (JSONPlaceholder)
api_url = 'https://jsonplaceholder.typicode.com/posts'

# Path to the JSON file
json_file_path = 'output.json'

total_records_sent = 0  # Initialize the counter

try:
    # Read JSON data from file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

        # Check if there are records to send
        if isinstance(json_data, list):
            total_records_sent = len(json_data)

            # Make a POST request for each record in JSON data
            for record in json_data:
                response = requests.post(api_url, json=record)
                response.raise_for_status()

            # Verify the data by making a GET request
            get_response = requests.get(api_url)
            get_response.raise_for_status()

            # Compare the posted data with the retrieved data
            retrieved_data = get_response.json()
            
            print(f"json data - > {json_data}")
            print("\n")
            print(f"retrieved_data - > {retrieved_data}")
            print("\n")

            if json_data == retrieved_data:
                print(f'{total_records_sent} record(s) successfully sent to the test API and verified.')
            else:
                print('Error: Retrieved data does not match the posted data.')

        else:
            print(f'Error: JSON data is not a list. Unable to send or verify records.')

except FileNotFoundError:
    print(f'Error: JSON file not found at {json_file_path}')

except json.JSONDecodeError:
    print(f'Error: Unable to decode JSON data from {json_file_path}')

except requests.RequestException as e:
    print(f'Error sending or verifying JSON data to the test API: {e}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')



#VALIDATE JSON DATA AGAINSTS CSV FILE
#exjson5.py


import json
import csv

def read_json_file(json_file_path):
    """Read JSON data from a file."""
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)

def read_csv_file(csv_file_path):
    """Read data from a CSV file."""
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def validate_json_against_csv(json_data, csv_data):
    """Validate JSON data against CSV data."""
    # Assuming both JSON and CSV data are lists of dictionaries
    return json_data == csv_data

# Replace these paths with the paths to your actual JSON and CSV files
json_file_path = 'output.json'
csv_file_path = 'sample.csv'

try:
    # Read JSON data
    json_data = read_json_file(json_file_path)

    # Read CSV data
    csv_data = read_csv_file(csv_file_path)

    # Validate JSON against CSV
    if validate_json_against_csv(json_data, csv_data):
        print('JSON data matches CSV data.')
    else:
        print('Error: JSON data does not match CSV data.')

except FileNotFoundError as file_err:
    print(f'Error: {file_err}')

except json.JSONDecodeError as json_err:
    print(f'Error decoding JSON: {json_err}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')


## HOW TO CREATE JSON FILE AND UPDATE IT ACCORDINGLY

json_data = {'users': [], 'orders': []}


user_dict = {
            'user_id': 111,
            'username': 'lev',
            'email': 'lg@examplecom'
        }
		
		
order_dict = {
            'order_id': 7777,
            'user_id': 'lev',
            'product_name': 'laptop',
            'order_date': '2024-05-13'
        }
		
json_data['users'].append(user_dict)
json_data['orders'].append(order_dict)



# EXPECTED JSON FILE 
#exjson5.py

import json

#json_data = {'AutomationKey': None, 'FormMode': None, 'KeyValue':None, 'Users':[]}
#>>> json_data['AutomationKey'] = '123456'
#>>> json_data['FormMode'] = 'xx'
#>>> json_data['KeyValue'] = 222
#>>> json_data['users']= ['1','2','3','4','5']




# Create a dictionary representing the JSON structure
json_data = {
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": None,
    "FormLines": [
        {"Caption": "Link to Person", "value": ""},
        {"Caption": "Treatment History Type", "value": ""},
        {"Caption": "Hospitalization Type", "value": ""},
        {"Caption": "Key", "value": ""},
        {"Caption": "Admission Date", "value": ""},
        {"Caption": "Discharge Date", "value": ""},
        {"Caption": "Facility Name", "value": ""},
        {"Caption": "Source", "value": ""},
        {"Caption": "Health Plan Identifier", "value": ""},
        {"Caption": "Health Plan Code", "value": ""},
        {"Caption": "Health Plan Member ID", "value": ""},
        {"Caption": "Health Plan Name", "value": ""},
        {"Caption": "Health Plan Type", "value": ""},
        {"Caption": "Health Plan Start Date", "value": ""},
        {"Caption": "Health Plan End Date", "value": ""},
        {"Caption": "Contact Person", "value": ""},
        {"Caption": "Admission Diagnosis", "value": ""},
        {"Caption": "Discharge Diagnosis", "value": ""},
        {"Caption": "Date Last Updated", "value": ""},
        {"Caption": "Type", "value": ""},
        {"Caption": "Agency", "value": ""}
    ],
    "SubData": []
}

# Convert the dictionary to a JSON string with indentation for better readability
json_string = json.dumps(json_data, indent=2)

# Print the resulting JSON string
print(json_string)


###############################################################################################

## EXPECTED JSON FILE 
#exjson6.py

import json

# Define the JSON structure
json_data = {
    "AutomationKey": None,
    "FormMode": None,
    "KeyValue": None,
    "FormLines": [
        {"Link to Person": None},
        {"Treatment History Type": None},
        {"Hospitalization Type": None},
        {"Key": None},
        {"Admission Date": None},
        {"Discharge Date": None},
        {"Facility Name": None},
        {"Source": None},
        {"Health Plan Identifier": None},
        {"Health Plan Code": None},
        {"Health Plan Member ID": None},
        {"Health Plan Name": None},
        {"Health Plan Type": None},
        {"Health Plan Start Date": None},
        {"Health Plan End Date": None},
        {"Contact Person": None},
        {"Admission Diagnosis": None},
        {"Discharge Diagnosis": None},
        {"Date Last Updated": None},
        {"Type": None},
        {"Agency": None}
    ],
    "SubData": []
}

# Specify the path to the JSON file
json_file_path = 'output.json'

# Write the JSON structure to the file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=2)

print(f'Data successfully written to {json_file_path}')


##############################################################################################


AutomationKey,FormMode,KeyValue,Link to Person,Treatment History Type,Hospitalization Type,Key,Admission Date,Discharge Date,Facility Name,Source,Health Plan Identifier,Health Plan Code,Health Plan Member ID,Health Plan Name,Health Plan Type,Health Plan Start Date,Health Plan End Date,Contact Person,Admission Diagnosis,Discharge Diagnosis,Date Last Updated,Type,Agency
tx_hx_hosp,ADD,1234,John Doe,Physical Therapy,Inpatient,ABC123,2022-01-15,2022-02-01,General Hospital,Referral,123456,HP001,987654,Blue Cross,Health Maintenance Organization,2022-01-01,2023-01-01,Dr. Smith,Chest Pain,Recovery,2022-02-01,TypeA,XYZ Agency




import csv
import json

# Specify the path to the CSV file
csv_file_path = 'myev.csv'  # Replace with the actual path to your CSV file

# Read CSV data and convert to a list of dictionaries
csv_data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_data.append(row)

# Extract values from the first row (assuming headers are present)
json_values = {key: value for key, value in csv_data[0].items()}

# Create the JSON structure with loaded values
json_data = {
    "AutomationKey": json_values.get("AutomationKey"),
    "FormMode": json_values.get("FormMode"),
    "KeyValue": json_values.get("KeyValue"),
    "FormLines": [
        {key: json_values.get(key)} for key in json_values.keys() if key not in ["AutomationKey", "FormMode", "KeyValue"]
    ],
    "SubData": []
}

# Print the resulting JSON structure
print(json.dumps(json_data, indent=2))



###################################################

myev.csv
AutomationKey,FormMode,KeyValue,Link to Person,Treatment History Type,Hospitalization Type,Key,Admission Date,Discharge Date,Facility Name,Source,Health Plan Identifier,Health Plan Code,Health Plan Member ID,Health Plan Name,Health Plan Type,Health Plan Start Date,Health Plan End Date,Contact Person,Admission Diagnosis,Discharge Diagnosis,Date Last Updated,Type,Agency
tx_hx_hosp,ADD,1234,John Doe,Physical Therapy,Inpatient,ABC123,2022-01-15,2022-02-01,General Hospital,Referral,123456,HP001,987654,Blue Cross,Health Maintenance Organization,2022-01-01,2023-01-01,Dr. Smith,Chest Pain,Recovery,2022-02-01,TypeA,XYZ Agency
tx_hx_hosp,UPDATE,5678,Jane Smith,Occupational Therapy,Outpatient,XYZ789,2022-02-10,2022-03-01,City Clinic,Self-Referral,654321,HP002,876543,Aetna,Preferred Provider Organization,2022-02-01,2023-02-01,Dr. Johnson,Back Pain,Improved,2022-03-01,TypeB,ABC Agency
tx_hx_hosp,DELETE,9012,Bob Johnson,Cardiac Rehabilitation,Inpatient,DEF456,2022-03-20,2022-04-05,Regional Medical Center,Referral,987654,HP003,765432,Cigna,Exclusive Provider Organization,2022-03-01,2023-03-01,Dr. Davis,Heart Disease,Stable,2022-04-05,TypeC,PQR Agency
tx_hx_hosp,ADD,3456,Alice Miller,Speech Therapy,Outpatient,GHI789,2022-04-05,2022-04-20,Community Hospital,Self-Referral,789012,HP004,654321,UnitedHealthcare,Point of Service,2022-04-01,2023-04-01,Dr. White,Speech Disorder,Resolved,2022-04-20,TypeD,MNO Agency
tx_hx_hosp,UPDATE,7890,Michael Brown,Physical Therapy,Inpatient,JKL012,2022-05-15,2022-06-01,Metro Health Center,Referral,890123,HP005,543210,Humana,Health Maintenance Organization,2022-05-01,2023-05-01,Dr. Wilson,Joint Pain,Improved,2022-06-01,TypeE,XYZ Agency


import csv
import json

# Specify the path to the CSV file
csv_file_path = 'myev.csv'  # Replace with the actual path to your CSV file

# Read CSV data and convert to a list of dictionaries
csv_data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_data.append(row)

# Create the JSON structure with loaded values
json_data = {
    "AutomationKey": None,
    "FormMode": None,
    "KeyValue": None,
    "FormLines": [
        {key: row.get(key) for key in row.keys() if key not in ["AutomationKey", "FormMode", "KeyValue"]}
    ] for row in csv_data,
    "SubData": []
}

# Print the resulting JSON structure
print(json.dumps(json_data, indent=2))

