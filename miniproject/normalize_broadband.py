#FDI mini project: Disaster Resilience Index/Digital Quity Index
#Lingyue Wang
#06/11/2026

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "original_broadband_data.json"
WEIGHTS_FILE = BASE_DIR / "weights.json"
OUTPUT_FILE = BASE_DIR / "weighted_normalized_broadband_data.json"

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
        return float(value[:-1]) / 100.0

    return float(value)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_json(INPUT_FILE)
    weights = load_json(WEIGHTS_FILE)

    regions = data["regions"]

    # Check weights
    missing_weights = [m for m in BENEFIT_METRICS + COST_METRICS if m not in weights]
    if missing_weights:
        raise ValueError(f"Missing weights for: {missing_weights}")

    weight_sum = sum(weights[m] for m in BENEFIT_METRICS + COST_METRICS)
    if abs(weight_sum - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1. Current sum = {weight_sum}")

    # Compute max values for benefit metrics
    max_values = {}
    for metric in BENEFIT_METRICS:
        values = [parse_percent(region[metric]) for region in regions]
        max_values[metric] = max(values)

    # Compute min values for cost metrics
    min_values = {}
    for metric in COST_METRICS:
        values = [parse_percent(region[metric]) for region in regions]
        min_values[metric] = min(values)

    output_regions = []

    for region in regions:
        region_name = region["name"]
        normalized = {}
        weighted = {}

        # Normalize benefit metrics
        for metric in BENEFIT_METRICS:
            actual = parse_percent(region[metric])
            norm = actual / max_values[metric] if max_values[metric] != 0 else 0.0
            normalized[metric] = round(norm, 4)
            weighted[metric] = round(norm * weights[metric], 4)

        # Normalize cost metrics
        for metric in COST_METRICS:
            actual = parse_percent(region[metric])
            denom = 1.0 - min_values[metric]
            norm = (1.0 - actual) / denom if denom != 0 else 0.0
            normalized[metric] = round(norm, 4)
            weighted[metric] = round(norm * weights[metric], 4)

        index_value = sum(weighted[m] for m in BENEFIT_METRICS + COST_METRICS)

        output_regions.append({
            "name": region_name,
            "normalized": normalized,
            "weighted": weighted,
            "index": round(index_value, 4)
        })

    output = {
        "weights": weights,
        "regions": output_regions
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"Weighted normalized data written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
