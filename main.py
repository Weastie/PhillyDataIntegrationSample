import requests
import urllib.parse
import time

print("Script started")

def write_analysis(analysis):
    with open('analysis.txt', 'a+') as f:
        print(f"Wrote analysis: {analysis}")
        f.write(analysis + "\n\n")

# Count of service Requests associated with L&I
r1 = requests.get(
    "https://phl.carto.com/api/v2/sql",
    params={"q": "SELECT (SELECT COUNT(*) FROM public_cases_fc WHERE agency_responsible = 'License & Inspections' AND requested_datetime >= '2025-01-01') as num_cases, (SELECT COUNT(*) FROM public_cases_fc WHERE requested_datetime >= '2025-01-01') as total_cases"}
)
r1_json = r1.json()
write_analysis(f"Since the beginning of 2025, {r1_json['rows'][0]['num_cases']} out of {r1_json['rows'][0]['total_cases']} service requests were associated with Licenses & Inspections")

# Dump of service requests, to find related violations
r2 = requests.get(
    "https://phl.carto.com/api/v2/sql",
    params={"q": "SELECT service_request_id, address, requested_datetime FROM public_cases_fc WHERE agency_responsible = 'License & Inspections' AND requested_datetime >= '2025-01-01'"}
)
service_requests = r2.json()['rows']
total_requests = 0
matching_violations = []
for row in service_requests:
    if row['address']:
        # Use urllib.parse.quote to urlencode the address, replacing any special characters with their hex encoding
        opa_lookup = requests.get(f"https://api.phila.gov/ais/v2/search/{urllib.parse.quote(row['address'])}")
        # Some addresses don't seem to have an `opa_account_num`, so we will leave them out of our data analysis
        if opa_lookup.headers['Content-Type'] == 'application/json' and 'features' in opa_lookup.json() and 'opa_account_num' in opa_lookup.json()['features'][0]['properties']:
            # Keep count of the number of requests that we go through, so we can log progress
            total_requests += 1
            if total_requests % 100 == 0:
                print(f"Analysis {(100 * total_requests / len(service_requests)):.2f}% done")
            opa_account_num = opa_lookup.json()['features'][0]['properties']['opa_account_num']
            # Find violations with matching OPA numbers, where casecreatedstart is within one month of the service request date
            # Performance enhanccement idea: Get all cases up front, so we don't need a request for each one
            violation_lookup = requests.get(
                "https://phl.carto.com/api/v2/sql",
                params={"q": f"SELECT casecreateddate, casestatus, violationstatus, casecompleteddate FROM violations WHERE opa_account_num = '{opa_account_num}' AND casecreateddate >= '{row['requested_datetime']}' AND casecreateddate <= ('{row['requested_datetime']}'::date + INTERVAL '1 month')"}
            )
            if len(violation_lookup.json()['rows']) >= 1:
                matching_violations.append(violation_lookup.json()['rows'])

write_analysis(f"Since the beginning of 2025, {len(matching_violations)} out of {len(service_requests)}, or {(100 * len(matching_violations)/len(service_requests)):.2f}% of service requests resulted in the issuance of a code violation.")

num_closed_violations = 0
for matching_violation in matching_violations:
    # For service requests with multiple matching violations, only report they are completed if all violations are closed
    num_completed = 0
    for v in matching_violation:
        if v['casestatus'] == 'CLOSED':
            num_completed += 1
    if num_completed == len(matching_violation):
        num_closed_violations += 1

write_analysis(f"Since the beginning of 2025, {num_closed_violations} of the {len(matching_violations)}, or {100 * (num_closed_violations/len(matching_violations)):.2f}% of violations from service requests were marked as closed")
print('done')
