#!/usr/bin/env python3
"""
TEF-2025 CSV Validation Script
Validates the structure and content of results.csv
"""

import pandas as pd
import sys
from pathlib import Path

def validate_csv(csv_path):
    """
    Validate the CSV file structure and content.
    
    Args:
        csv_path (str): Path to the CSV file
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_columns = [
        'protocol', 'family', 'scenario', 'tps', 'p95_latency_ms', 
        'finality_s', 'energy_wh_tx', 'committee_k', 'adversary_beta',
        'nakamoto_coef', 'gini', 'notes', 'source'
    ]
    
    numeric_columns = [
        'tps', 'p95_latency_ms', 'finality_s', 'energy_wh_tx',
        'committee_k', 'adversary_beta', 'nakamoto_coef', 'gini'
    ]
    
    try:
        # Load CSV
        df = pd.read_csv(csv_path)
        print(f"✓ Successfully loaded CSV with {len(df)} rows")
        
        # Check required columns
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            print(f"✗ Missing required columns: {missing_cols}")
            return False
        print("✓ All required columns present")
        
        # Check for empty rows
        empty_rows = df.isnull().all(axis=1).sum()
        if empty_rows > 0:
            print(f"⚠ Warning: {empty_rows} completely empty rows found")
        
        # Validate numeric columns
        for col in numeric_columns:
            if col in df.columns:
                non_numeric = df[col].apply(lambda x: pd.isna(x) or isinstance(x, (int, float)))
                if not non_numeric.all():
                    invalid_count = (~non_numeric).sum()
                    print(f"⚠ Warning: {invalid_count} non-numeric values in {col}")
        
        # Check for reasonable value ranges
        if 'tps' in df.columns:
            invalid_tps = df[(df['tps'] < 0) | (df['tps'] > 100000)]
            if len(invalid_tps) > 0:
                print(f"⚠ Warning: {len(invalid_tps)} rows with unrealistic TPS values")
        
        if 'gini' in df.columns:
            invalid_gini = df[(df['gini'] < 0) | (df['gini'] > 1)]
            if len(invalid_gini) > 0:
                print(f"⚠ Warning: {len(invalid_gini)} rows with Gini coefficient outside [0,1]")
        
        if 'adversary_beta' in df.columns:
            invalid_beta = df[(df['adversary_beta'] < 0) | (df['adversary_beta'] > 0.5)]
            if len(invalid_beta) > 0:
                print(f"⚠ Warning: {len(invalid_beta)} rows with adversary_beta outside [0,0.5]")
        
        # Summary
        print(f"\n📊 Data Summary:")
        print(f"   Protocols: {df['protocol'].nunique()} unique")
        print(f"   Families: {df['family'].value_counts().to_dict()}")
        print(f"   Scenarios: {df['scenario'].nunique()} unique")
        
        return True
        
    except FileNotFoundError:
        print(f"✗ CSV file not found: {csv_path}")
        return False
    except pd.errors.EmptyDataError:
        print("✗ CSV file is empty")
        return False
    except Exception as e:
        print(f"✗ Error validating CSV: {str(e)}")
        return False

def main():
    """Main validation function."""
    if len(sys.argv) != 2:
        print("Usage: python validate_csv.py <csv_file_path>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    print("🔍 TEF-2025 CSV Validation")
    print("=" * 40)
    
    if validate_csv(csv_path):
        print("\n✅ CSV validation passed")
        sys.exit(0)
    else:
        print("\n❌ CSV validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
