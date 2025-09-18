#!/usr/bin/env python3
"""
Validation script for Problem 3: Checks if the merged CSV is properly deduplicated
"""

import pandas as pd
import sys
from pathlib import Path

def validate_merged_data(file_path):
    """Validate the merged and deduplicated customer data"""
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Load original files for comparison
    try:
        q1 = pd.read_csv(Path(file_path).parent / "customers_q1.csv")
        q2 = pd.read_csv(Path(file_path).parent / "customers_q2.csv")
    except Exception as e:
        print(f"❌ Error reading original files: {e}")
        return False
    
    errors = []
    warnings = []
    
    # Check required columns
    required_columns = ['customer_id', 'name', 'email', 'city', 'registration_date', 'total_purchases']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
    
    # Check for duplicates based on customer_id
    if df['customer_id'].duplicated().any():
        duplicate_ids = df[df['customer_id'].duplicated()]['customer_id'].tolist()
        errors.append(f"Found duplicate customer_ids: {duplicate_ids}")
    
    # Check if all unique customers are present
    expected_unique_customers = pd.concat([q1, q2])['customer_id'].unique()
    actual_customers = df['customer_id'].unique()
    missing_customers = set(expected_unique_customers) - set(actual_customers)
    extra_customers = set(actual_customers) - set(expected_unique_customers)
    
    if missing_customers:
        errors.append(f"Missing customers: {sorted(missing_customers)}")
    if extra_customers:
        warnings.append(f"Extra customers not in original data: {sorted(extra_customers)}")
    
    # Check data consistency for overlapping customers
    overlapping_ids = set(q1['customer_id']) & set(q2['customer_id'])
    for customer_id in overlapping_ids:
        q1_row = q1[q1['customer_id'] == customer_id].iloc[0]
        q2_row = q2[q2['customer_id'] == customer_id].iloc[0]
        merged_row = df[df['customer_id'] == customer_id].iloc[0]
        
        # Check if basic info is consistent (name, email should be the same)
        if q1_row['name'] == q2_row['name']:
            if merged_row['name'] != q1_row['name']:
                warnings.append(f"Customer {customer_id}: name mismatch in merged data")
        
        if q1_row['email'] == q2_row['email']:
            if merged_row['email'] != q1_row['email']:
                warnings.append(f"Customer {customer_id}: email mismatch in merged data")
    
    # Check total number of rows
    expected_min_rows = len(expected_unique_customers)
    if len(df) < expected_min_rows:
        errors.append(f"Too few rows: {len(df)}, expected at least {expected_min_rows}")
    elif len(df) > expected_min_rows:
        warnings.append(f"More rows than expected: {len(df)}, expected {expected_min_rows}")
    
    # Print results
    print(f"\n📊 Validation Results for {Path(file_path).name}")
    print(f"{'='*50}")
    print(f"Total rows in merged file: {len(df)}")
    print(f"Unique customers expected: {len(expected_unique_customers)}")
    print(f"Unique customers in merged file: {len(df['customer_id'].unique())}")
    print(f"Original Q1 customers: {len(q1)}")
    print(f"Original Q2 customers: {len(q2)}")
    print(f"Overlapping customers: {len(overlapping_ids)}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("\n✅ All checks passed! Great job on the merge and deduplication!")
        return True
    elif not errors:
        print("\n✅ No errors found, but there are some warnings to consider.")
        return True
    else:
        print("\n❌ Please fix the errors above and try again.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_problem3.py <merged_csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    success = validate_merged_data(file_path)
    sys.exit(0 if success else 1)
