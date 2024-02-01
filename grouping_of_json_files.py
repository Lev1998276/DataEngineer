import json

# Sample list
l1 = [{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033814",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": ""
        },
        {
            "Caption": "Link to Person",
            "value": "10033814"
        },
        
    ],
    "SubData": []
},
{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033815",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": ""
        },
        {
            "Caption": "Link to Person",
            "value": "10033815"
        }
    ],
    "SubData": []
},
{
    "AutomationKey": "tx_hx_hosp",
    "FormMode": "ADD",
    "KeyValue": "10033814",
    "FormLines": [
        {
            "Caption": "FormMode",
            "value": "ADD"
        },
        {
            "Caption": "KeyValue",
            "value": "12"
        },
        {
            "Caption": "Link to Person",
            "value": "10033814"
        },
        
    ],
    "SubData": []
}
]

# Group records by KeyValue
grouped_records = {}
for record in l1:
    key_value = record["KeyValue"]
    if key_value not in grouped_records:
        grouped_records[key_value] = []
    grouped_records[key_value].append(record)

# Create JSON files for each KeyValue group
for key_value, records in grouped_records.items():
    file_name = f"{key_value}.json"
    with open(file_name, "w") as json_file:
        json.dump(records, json_file, indent=2)

print("JSON files created successfully.")