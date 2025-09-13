#!/usr/bin/env python3
import sys
print("Testing TEF-2025 environment...")
print(f"Python version: {sys.version}")

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except Exception as e:
    print(f"✗ pandas error: {e}")

try:
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except Exception as e:
    print(f"✗ matplotlib error: {e}")

try:
    import yaml
    print("✓ pyyaml imported successfully")
except Exception as e:
    print(f"✗ pyyaml error: {e}")

print("✅ Environment test complete!")

# Test CSV loading
try:
    df = pd.read_csv('inputs/results.csv')
    print(f"✓ CSV loaded: {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ CSV loading error: {e}")
