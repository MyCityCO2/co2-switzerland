import csv
import yaml

fields = {
'uid_label' : 'Label',
    'uid_city' : 'City',
    'result' : 'Result',
    'currency' : 'Currency',
    'chart_of_account' : 'Account',
    'country_iso' : 'ISO'
}

with open('output.csv', 'w', newline='') as f_output:
    csv_output = csv.DictWriter(f_output, fieldnames=fields.values())
    csv_output.writeheader()

    for filename in ['log.yml']:
        with open(filename) as f_input:
            for row_yaml in yaml.safe_load(f_input):
                row_csv = {fields[key] : value for key, value in row_yaml.items()}
                csv_output.writerow(row_csv)