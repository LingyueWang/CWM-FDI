#FDI mini project: Disaster Resilience Index/Digital Quity Index
#Lingyue Wang
#06/11/2026

import json
from pathlib import Path

INPUT_FILE = Path("original_broadband_data.json")
OUTPUT_FILE = Path("normalized_broadband_data.json")

# Higher = better
BENEFIT_METRICS = [
    "Gigabit-capable",
    "Full fibre",
    "Superfast",
    "5G coverage"
]

# Lower = better
COST_METRICS = [
    "Unable to get decent connection",
    "4G total not spots",
    "Voice and text total not spots"
]


def parse_percent(value):
    """
    Convert:
        '77%' -> 0.77
        '0.5%' -> 0.005
        '0.77' -> 0.77
    """
    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if value.endswith("%"):
        return float(value[:-1]) / 100

    return float(value)


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

regions = data["regions"]

# Calculate maxima for benefit metrics
max_values = {}

for metric in BENEFIT_METRICS:
    values = [parse_percent(region[metric]) for region in regions]
    max_values[metric] = max(values)

# Calculate minima for cost metrics
min_values = {}

for metric in COST_METRICS:
    values = [parse_percent(region[metric]) for region in regions]
    min_values[metric] = min(values)

normalized_regions = []

for region in regions:

    normalized = {
        "name": region["name"]
    }

    # Benefit metrics
    for metric in BENEFIT_METRICS:

        actual = parse_percent(region[metric])

        normalized[metric] = round(
            actual / max_values[metric],
            4
        )

    # Cost metrics
    for metric in COST_METRICS:

        actual = parse_percent(region[metric])

        normalized[metric] = round(
            (1 - actual) /
            (1 - min_values[metric]),
            4
        )

    normalized_regions.append(normalized)

output = {
    "regions": normalized_regions
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f"Normalized data written to: {OUTPUT_FILE}")
