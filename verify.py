"""Recompute the monthly and Kamchatka counts from the supplied USGS query."""
import csv
import math
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2025-01-01&endtime=2025-12-31T23:59:59.999&minmagnitude=5.5&eventtype=earthquake"
SNAPSHOT = Path(__file__).with_name("usgs-2025-m55.csv")


def great_circle_km(a, b):
    lat_a, lat_b = map(math.radians, (float(a["latitude"]), float(b["latitude"])))
    delta_lon = math.radians(float(b["longitude"]) - float(a["longitude"]))
    h = math.sin((lat_b-lat_a)/2)**2 + math.cos(lat_a)*math.cos(lat_b)*math.sin(delta_lon/2)**2
    return 2 * 6371.0088 * math.asin(math.sqrt(min(1, h)))


if not SNAPSHOT.exists():
    with urlopen(URL, timeout=30) as response:
        SNAPSHOT.write_bytes(response.read())
with SNAPSHOT.open(newline="") as stream:
    rows = list(csv.DictReader(stream))
required = ("id", "time", "latitude", "longitude", "mag")
complete = [row for row in rows if all(row[key] for key in required)]
events = {row["id"]: row for row in complete}
monthly = Counter(datetime.fromisoformat(row["time"]).strftime("%Y-%m") for row in events.values())
mainshock = events["us6000qw60"]
near = [
    row for row in events.values()
    if "2025-07-30" <= row["time"] < "2025-08-01" and great_circle_km(mainshock,row) <= 500
]
for month, count in sorted(monthly.items()):
    print(month, count)
print("Rows:", len(rows), "| Missing required fields:", len(rows) - len(complete))
print("Distinct IDs:", len(events), "| Median month:", statistics.median(monthly.values()))
print("500 km group:", len(near), "| July excluding group:", monthly["2025-07"] - len(near))
