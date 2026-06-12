#FDI mini project: Digital Equity Index
#Lingyue Wang
#06/11/2026

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "original_broadband_data.json"
WEIGHTS_FILE = BASE_DIR / "weights.json"
NORMALIZED_OUTPUT_FILE = BASE_DIR / "normalized_broadband_data.json"
WEIGHTED_OUTPUT_FILE = BASE_DIR / "weighted_normalized_broadband_data.json"

# Benefit indicators: higher values are better, so keep the value as it is
BENEFIT_METRICS = [
    "Gigabit-capable",
    "Full fibre",
    "Superfast",
    "5G coverage",
]

# Cost indicators: lower values are better, so reverse using 1 - actual
COST_METRICS = [
    "Unable to get decent connection",
    "4G total not spots",
    "Voice and text total not spots",
]


def parse_percent(value):
    """
    Convert values like:
        '77%'  -> 0.77
        '0.5%' -> 0.005
        '0.77' -> 0.77
        0.77   -> 0.77
    """
    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if value.endswith("%"):
        return float(value[:-1].strip()) / 100.0

    num = float(value)
    return num if num <= 1.0 else num / 100.0


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def main():
    data = load_json(INPUT_FILE)
    weights = load_json(WEIGHTS_FILE)

    regions = data.get("regions", [])
    if not regions:
        raise ValueError("No regions found in original_broadband_data.json")

    all_metrics = BENEFIT_METRICS + COST_METRICS

    # Check that every metric has a weight
    missing_weights = [metric for metric in all_metrics if metric not in weights]
    if missing_weights:
        raise ValueError(f"Missing weights for: {missing_weights}")

    # Check that weights sum to 1
    weight_sum = sum(float(weights[m]) for m in all_metrics)
    if abs(weight_sum - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1. Current sum = {weight_sum}")

    normalized_regions = []
    weighted_regions = []

    for region in regions:
        region_name = region["name"]

        normalized_values = {}
        weighted_values = {}

        # Benefit indicators: normalized value = actual value
        for metric in BENEFIT_METRICS:
            actual = parse_percent(region[metric])
            norm = actual
            normalized_values[metric] = round(norm, 4)
            weighted_values[metric] = round(norm * float(weights[metric]), 4)

        # Cost indicators: normalized value = 1 - actual value
        for metric in COST_METRICS:
            actual = parse_percent(region[metric])
            norm = 1.0 - actual
            normalized_values[metric] = round(norm, 4)
            weighted_values[metric] = round(norm * float(weights[metric]), 4)

        index_value = sum(weighted_values[m] for m in all_metrics)

        normalized_regions.append({
            "name": region_name,
            "normalized": normalized_values
        })

        weighted_regions.append({
            "name": region_name,
            "normalized": normalized_values,
            "weighted": weighted_values,
            "index": round(index_value, 4)
        })

    save_json(NORMALIZED_OUTPUT_FILE, {
        "regions": normalized_regions
    })

    save_json(WEIGHTED_OUTPUT_FILE, {
        "weights": weights,
        "regions": weighted_regions
    })

    print(f"Normalized data written to: {NORMALIZED_OUTPUT_FILE}")
    print(f"Weighted data written to: {WEIGHTED_OUTPUT_FILE}")


if __name__ == "__main__":
    main()
