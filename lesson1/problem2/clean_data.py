#!/usr/bin/env python3
"""
clean_data.py
Clean dirty_customer_data.csv by fixing missing values, standardizing formats,
and producing cleaned_customer_data.csv.
"""

import os
import pandas as pd
import re
from datetime import datetime

INPUT_FILE = "dirty_customer_data.csv"
OUTPUT_FILE = "cleaned_customer_data.csv"
REPORT_FILE = "data_quality_report.txt"


# ---------- Helper Functions ----------

def clean_name(name):
    """Convert to Title Case.----将输入转换为首字母大写的形式(Title Case)"""
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
    if pd.isnull(age):
        return None
    if isinstance(age, str):
        age = age.strip().lower()
        if age.isdigit():
            return int(age)
        text2num = {
            'twenty-seven': 27, 'thirty-five': 35, 'forty-five': 45, 'twenty-two': 22,
            'twenty-five': 25, 'thirty': 30, 'twenty-nine': 29, 'thirty-three': 33,
            'forty-one': 41, 'twenty-eight': 28, 'thirty-one': 31
        }
        return text2num.get(age, None)
    try:
        return int(age)
    except Exception:
        return None


def clean_salary(salary):
    """Convert salary to float if valid, else None."""
    if pd.isnull(salary):
        return None
    if isinstance(salary, str):
        salary = salary.replace(',', '').replace('$', '').strip().lower()
        if salary.isdigit():
            return float(salary)
        if salary == 'sixty thousand':
            return 60000.0
    try:
        return float(salary)
    except Exception:
        return None


def clean_phone(phone):
    """Standardize phone number to (XXX) XXX-XXXX format."""
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return None  # invalid phone number


def clean_date(date):
    """Standardize dates to YYYY-MM-DD format."""
    if pd.isna(date):
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%B %d, %Y", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(date), fmt).strftime("%Y-%m-%d")
        except Exception:
            continue
    try:
        return pd.to_datetime(date, errors='coerce').strftime("%Y-%m-%d")
    except Exception:
        return None


# ---------- Main Cleaning Pipeline ----------

def generate_quality_report(df, filename, before_stats, after_stats):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("数据质量报告\n")
        f.write("="*30 + "\n")
        f.write("清洗前统计信息:\n")
        f.write(str(before_stats) + "\n\n")
        f.write("清洗后统计信息:\n")
        f.write(str(after_stats) + "\n\n")
        f.write(f"总记录数: {len(df)}\n\n")
        for col in df.columns:
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            f.write(f"字段: {col}\n")
            f.write(f"  缺失值数量: {null_count}\n")
            f.write(f"  唯一值数量: {unique_count}\n")
            if pd.api.types.is_numeric_dtype(df[col]):
                f.write(f"  最小值: {df[col].min()}\n")
                f.write(f"  最大值: {df[col].max()}\n")
                f.write(f"  均值: {df[col].mean()}\n")
                f.write(f"  标准差: {df[col].std()}\n")
            f.write("\n")


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(BASE_DIR, 'dirty_customer_data.csv')
    output_path = os.path.join(BASE_DIR, 'cleaned_customer_data.csv')
    report_path = os.path.join(BASE_DIR, 'data_quality_report.txt')

    df = pd.read_csv(input_path)

    print("清洗前统计：")
    before_stats = df.describe(include='all')
    print(df.info())
    print(before_stats)

    # 1. 移除customer_id缺失的行
    df = df[df['customer_id'].notnull()]

    # 2. 处理缺失值
    df['name'] = df['name'].fillna('')
    df['email'] = df['email'].fillna('')
    df['age'] = df['age'].apply(clean_age)
    df['salary'] = df['salary'].apply(clean_salary)
    df['phone'] = df['phone'].apply(clean_phone)
    df['join_date'] = df['join_date'].apply(clean_date)

    # 3. 标准化文本
    df['name'] = df['name'].apply(lambda x: x.title() if isinstance(x, str) else x)
    df['email'] = df['email'].apply(valid_email) # type: ignore

    # 4. 移除无效email
    df = df[df['email'].notnull()]

    # 5. 移除重复行
    df = df.drop_duplicates()

    # 6. 保存清洗后的数据
    df.to_csv(output_path, index=False)

    print("清洗后统计：")
    after_stats = df.describe(include='all')
    print(df.info())
    print(after_stats)

    # 7. 生成数据质量报告
    generate_quality_report(df, report_path, before_stats, after_stats)

    print(f"\nCleaned data saved to {OUTPUT_FILE}")
    print(f"Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    main()
