import requests

# Service Requests
r1 = requests.get(
    "https://phl.carto.com/api/v2/sql",
    params={"q": "SELECT (SELECT COUNT(*) FROM public_cases_fc WHERE agency_responsible = 'License & Inspections' AND requested_datetime >= '2025-01-01') as num_cases, (SELECT COUNT(*) FROM public_cases_fc WHERE requested_datetime >= '2025-01-01') as total_cases"}
)
r1_json = r1.json()
print(f"Since the beginning of the 2025, {r1_json['rows'][0]['num_cases']} out of {r1_json['rows'][0]['total_cases']} service requests were associated with Licenses & Inspections")

# L&I
#r = requests.get(
#    "https://phl.carto.com/api/v2/sql",
#    params={"q": "SELECT * FROM violations WHERE violationdate >= '2025-01-01T00:00:00Z'"}
#)
#print(r.text)
