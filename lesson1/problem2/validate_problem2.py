#!/usr/bin/env python3
"""
Validation script for Problem 2: Checks if the cleaned CSV meets requirements
"""

import pandas as pd
import re
import sys
from pathlib import Path

def validate_cleaned_data(file_path):
    """Validate the cleaned customer data"""
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    errors = []
    warnings = []
    
    # Check required columns
    required_columns = ['customer_id', 'name', 'email', 'age', 'phone', 'salary', 'join_date']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
    
    # Check for duplicates
    if df.duplicated().any():
        errors.append(f"Found {df.duplicated().sum()} duplicate rows")
    
    # Check customer_id
    if df['customer_id'].isnull().any():
        errors.append("customer_id column contains null values")
    
    # Check name formatting (should be title case)
    for idx, name in df['name'].items():
        if pd.notna(name) and name != name.title():
            warnings.append(f"Row {idx}: name not in title case: '{name}'")
    
    # Check email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    for idx, email in df['email'].items():
        if pd.notna(email) and not re.match(email_pattern, str(email).lower()):
            errors.append(f"Row {idx}: invalid email format: '{email}'")
    
    # Check age (should be numeric)
    if not pd.api.types.is_numeric_dtype(df['age']):
        errors.append("age column is not numeric")
    
    # Check phone format (should be standardized)
    phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    for idx, phone in df['phone'].items():
        if pd.notna(phone) and not re.match(phone_pattern, str(phone)):
            warnings.append(f"Row {idx}: phone not in standard format: '{phone}'")
    
    # Check salary (should be numeric)
    if not pd.api.types.is_numeric_dtype(df['salary']):
        errors.append("salary column is not numeric")
    
    # Check join_date format (should be YYYY-MM-DD)
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    for idx, date in df['join_date'].items():
        if pd.notna(date) and not re.match(date_pattern, str(date)):
            errors.append(f"Row {idx}: join_date not in YYYY-MM-DD format: '{date}'")
    
    # Print results
    print(f"\n📊 Validation Results for {Path(file_path).name}")
    print(f"{'='*50}")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings[:5]:  # Show first 5 warnings
            print(f"  - {warning}")
        if len(warnings) > 5:
            print(f"  ... and {len(warnings) - 5} more warnings")
    
    if not errors and not warnings:
        print("\n✅ All checks passed! Great job!")
        return True
    elif not errors:
        print("\n✅ No errors found, but there are some warnings to address.")
        return True
    else:
        print("\n❌ Please fix the errors above and try again.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_problem2.py <cleaned_csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    success = validate_cleaned_data(file_path)
    sys.exit(0 if success else 1)
