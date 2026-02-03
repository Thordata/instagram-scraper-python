import os
import json
import pandas as pd
from typing import List, Dict, Any

def save_to_json(data: Any, filename: str):
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON to: {filepath}")

def save_to_csv(data: List[Dict], filename: str):
    if not data or not isinstance(data, list):
        print("Warning: Data is not a list, skipping CSV save.")
        return
    
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"Saved CSV to: {filepath}")
