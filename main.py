import requests

r = requests.get(
    "https://phl.carto.com/api/v2/sql",
    params={"q": "SELECT * FROM violations WHERE violationdate >=  '2025-01-01T00:00:00Z'"}
)
print(r.text)
