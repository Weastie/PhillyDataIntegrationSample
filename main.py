import requests
import urllib.parse

# Service Requests associated with L&I
#r1 = requests.get(
#    "https://phl.carto.com/api/v2/sql",
#    params={"q": "SELECT (SELECT COUNT(*) FROM public_cases_fc WHERE agency_responsible = 'License & Inspections' AND requested_datetime >= '2025-01-01') as num_cases, (SELECT COUNT(*) FROM public_cases_fc WHERE requested_datetime >= '2025-01-01') as total_cases"}
#)
#r1_json = r1.json()
#print(f"Since the beginning of the 2025, {r1_json['rows'][0]['num_cases']} out of {r1_json['rows'][0]['total_cases']} service requests were associated with Licenses & Inspections")

# 
r2 = requests.get(
    "https://phl.carto.com/api/v2/sql",
    params={"q": "SELECT service_request_id, address FROM public_cases_fc WHERE agency_responsible = 'License & Inspections' AND requested_datetime >= '2025-01-01'"}
)
# print(r2.json())
for row in r2.json()['rows']:
    # Use urllib.parse.quote to urlencode the address, replacing any special characters with their hex encoding
    opa_lookup = requests.get(f"https://api.phila.gov/ais/v2/search/{urllib.parse.quote(row['address'])}")
    opa_account_num = opa_lookup.json()['features'][0]['properties']['opa_account_num']
    print(opa_account_num)
    break


# L&I
#r = requests.get(
#    "https://phl.carto.com/api/v2/sql",
#    params={"q": "SELECT * FROM violations WHERE violationdate >= '2025-01-01T00:00:00Z'"}
#)
#print(r.text)
