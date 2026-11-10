"""
    Extracts tasks with desired type and shard count from original data JSON file and saves them to a new JSON file.
"""

import json
from pathlib import Path


script_dir = Path(__file__).resolve().parent
input_file = script_dir.parent / "data" / "sharded_instructions_600.json"
output_file = script_dir / "gsm8k_filtered_6shards.json"

wanted_type = "math"
wanted_shard_count = 6

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

filtered_data = []

for item in data:
    if item.get("task") == wanted_type and len(item.get("shards", [])) == wanted_shard_count:
        filtered_data.append(item)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=2)

print(f"Saved {len(filtered_data)} matching entries to {output_file}")