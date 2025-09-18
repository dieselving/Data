#!/usr/bin/env python3
"""
clean_data.py
Clean dirty_customer_data.csv by fixing missing values, standardizing formats,
and producing cleaned_customer_data.csv.
"""

import pandas as pd
import re
from datetime import datetime

INPUT_FILE = "dirty_customer_data.csv"
OUTPUT_FILE = "cleaned_customer_data.csv"
REPORT_FILE = "data_quality_report.txt"


# ---------- Helper Functions ----------

def clean_name(name):
    """Convert to Title Case.----将输入转换为首字母大写的形式（Title Case）"""
    if pd.isna(name):
        return None
    return str(name).title().strip()


def clean_email(email):
    """Validate and normalize email addresses."""
    if pd.isna(email):
        return None
    email = str(email).strip().lower() #转换为小写
    pattern = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$" #标准化格式
    return email if re.match(pattern, email) else None


def clean_age(age):
    """Convert age to integer if valid, else None."""
    try:
        return int(float(str(age).strip()))
    except (ValueError, TypeError):
        return None


def clean_salary(salary):
    """Convert salary to float if valid, else None."""
    try:
        return float(str(salary).replace(",", "").replace("$", "").strip())
    #薪水转换为字符串，去除逗号和美元符号，然后将结果转换为浮点数
    except (ValueError, TypeError):
        return None


def clean_phone(phone):
    """Standardize phone number to (XXX) XXX-XXXX format."""
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return None  # invalid phone number


def clean_date(date):
    """Standardize dates to YYYY-MM-DD format."""
    if pd.isna(date):
        return None
    try:
        return pd.to_datetime(date, errors="coerce").strftime("%Y-%m-%d")
    except Exception:
        return None


# ---------- Main Cleaning Pipeline ----------

def main():
    # Load dataset
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"File {INPUT_FILE} not found.")
        return

    print("\n--- Data Summary Before Cleaning ---")
    print(df.info())
    print(df.head())

    # Remove rows with missing customer_id
    df = df.dropna(subset=["customer_id"])

    # Standardize text
    df["name"] = df["name"].apply(clean_name)
    df["email"] = df["email"].apply(clean_email)

    # Clean numeric data
    df["age"] = df["age"].apply(clean_age)
    df["salary"] = df["salary"].apply(clean_salary)

    # Standardize phone and date formats
    df["phone"] = df["phone"].apply(clean_phone)
    df["join_date"] = df["join_date"].apply(clean_date)

    # Handle missing values in other columns 处理其他列中的缺失值
    df = df.dropna(how="all")  # drop rows completely empty 删除完全为空的行

    # Remove duplicates 删除重复项
    df = df.drop_duplicates()

    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)

    print("\n--- Data Summary After Cleaning ---")
    print(df.info())
    print(df.head())

    # Bonus: Write data quality report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("Data Quality Report\n")
        f.write("=" * 40 + "\n")
        f.write(f"Rows after cleaning: {len(df)}\n")
        f.write(f"Missing values by column:\n{df.isna().sum()}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"\nCleaned data saved to {OUTPUT_FILE}")
    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
