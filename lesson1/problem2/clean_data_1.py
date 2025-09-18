#!/usr/bin/env python3
"""
clean_data.py  — Improved cleaning for numeric-words, phones, dates, emails, etc.
- Adds text->number parsing (e.g. "sixty thousand" -> 60000)
- Keeps counters to report how many conversions succeeded/failed
- Uses pandas and pathlib; no external packages required
- 改进了对数字单词、电话、日期、电子邮件等的清理 - 添加文本>数字解析（例如“六万” -> 60000） - 保留计数器以报告成功失败的转换次数
"""

import re
from datetime import datetime
from pathlib import Path
import pandas as pd

INPUT_FILE = "dirty_customer_data.csv"
OUTPUT_FILE = "cleaned_customer_data_1.csv"
REPORT_FILE = "data_quality_report_1.txt"

# Global counters for reporting 用于报告的全局计数器
STATS = {
    "rows_before": 0,
    "rows_after": 0,
    "salary_numeric_parsed": 0,
    "salary_text_parsed": 0,
    "salary_failed": 0,
    "age_numeric_parsed": 0,
    "age_text_parsed": 0,
    "age_failed": 0,
    "phone_parsed_us": 0,
    "phone_parsed_intl": 0,
    "phone_failed": 0,
    "date_parsed": 0,
    "date_failed": 0,
    "invalid_emails_removed": 0
}


# -------- text -> number utility (supports up to billions) --------
def text_to_number(s):
    """
    Convert a textual number to numeric (e.g. "sixty thousand" -> 60000).
    Supports:
      - "sixty thousand", "one hundred and twenty five", "forty-two"
      - numeric-shorthand like "60k", "2.5M"
      - removes currency words like 'dollars', 'usd'
    Returns float or None if can't parse.
      - 将文本数字转换为数字（例如“六万”-> 60000）。支持：
      - “六万”、“一百二十五”、“四十二”
      - 数字简写，如“60k”、“2.5M”
      - 删除货币词，如“美元”、“美元”如果无法解析，则返回浮点或无。
    """
    if s is None:
        return None
    s0 = str(s).lower().strip()
    if s0 == "":
        return None

    # quick cleanup
    s0 = s0.replace(",", "")
    s0 = re.sub(r"\b(dollars?|usd|aud|gbp|eur)\b", "", s0)
    s0 = s0.strip()

    # handle numeric with k/m shorthand: 60k, 2.5M, $60k, 60k USD
    m = re.match(r"^([+-]?\d+(\.\d+)?)(\s*[kKmM])?$", s0)
    if m:
        base = float(m.group(1))
        suffix = (m.group(3) or "").strip().lower()
        if suffix == "k":
            return base * 1_000
        if suffix == "m":
            return base * 1_000_000
        return base

    # fallback: try to extract a plain float even if other text exists (e.g. "approx 60000")
    m2 = re.search(r"([+-]?\d+(\.\d+)?)", s0)
    if m2:
        return float(m2.group(1))

    # words -> number mapping
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19
    }
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }
    scales = {"hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000}

    words = re.split(r"[\s-]+", s0)  # split on spaces and hyphens
    current = 0
    total = 0
    for w in words:
        if w in units:
            current += units[w]
        elif w in tens:
            current += tens[w]
        elif w == "and":
            continue
        elif w in scales:
            scale = scales[w]
            if current == 0:
                current = 1
            current = current * scale
            total += current
            current = 0
        else:
            # unknown token — stop processing (keeps it conservative)
            return None
    total += current
    return float(total) if total != 0 else None


# -------- cleaning helper functions --------
def clean_name(name):
    if pd.isna(name):
        return None
    return str(name).strip().title()


def clean_email(email):
    if pd.isna(email):
        return None
    e = str(email).strip().lower()
    pattern = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    if re.match(pattern, e):
        return e
    STATS["invalid_emails_removed"] += 1
    return None


def clean_age(age):
    if pd.isna(age):
        STATS["age_failed"] += 1
        return None
    s = str(age).strip()
    # try numeric first
    try:
        val = int(float(re.sub(r"[^\d\.-]", "", s)))
        STATS["age_numeric_parsed"] += 1
        return val
    except Exception:
        pass
    # try text->number
    n = text_to_number(s)
    if n is not None:
        STATS["age_text_parsed"] += 1
        try:
            return int(n)
        except:
            return int(float(n))
    STATS["age_failed"] += 1
    return None


def clean_salary(salary):
    if pd.isna(salary):
        STATS["salary_failed"] += 1
        return None
    s = str(salary).strip()
    # try direct numeric extraction (strip $ and commas)
    s_digits = re.sub(r"[^\d\.\-kKmM]", "", s)  # keep numbers, dot, - and k/m
    # attempt float with k/m suffix
    try:
        m = re.match(r"^([+-]?\d+(\.\d+)?)([kKmM])?$", s_digits)
        if m:
            base = float(m.group(1))
            suffix = (m.group(3) or "").lower()
            if suffix == "k":
                STATS["salary_numeric_parsed"] += 1
                return base * 1_000
            if suffix == "m":
                STATS["salary_numeric_parsed"] += 1
                return base * 1_000_000
            STATS["salary_numeric_parsed"] += 1
            return base
    except Exception:
        pass

    # try text -> number (e.g. "sixty thousand")
    n = text_to_number(s)
    if n is not None:
        STATS["salary_text_parsed"] += 1
        return float(n)

    STATS["salary_failed"] += 1
    return None


def clean_phone(phone):
    if pd.isna(phone):
        STATS["phone_failed"] += 1
        return None
    s = str(phone)
    # remove common separators and wrappers
    digits = re.sub(r"[^\d+]", "", s)
    # if plus sign followed by digits -> keep plus
    digits_only = re.sub(r"\D", "", s)

    # US-style / NANP detection:
    if len(digits_only) == 10:
        STATS["phone_parsed_us"] += 1
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    if len(digits_only) == 11 and digits_only.startswith("1"):
        STATS["phone_parsed_us"] += 1
        d = digits_only[1:]
        return f"({d[:3]}) {d[3:6]}-{d[6:]}"
    # fallback: return international normalized format if possible
    if len(digits_only) > 10:
        STATS["phone_parsed_intl"] += 1
        return "+" + digits_only
    STATS["phone_failed"] += 1
    return None


def clean_date(val):
    if pd.isna(val):
        STATS["date_failed"] += 1
        return None
    # try pandas with multiple strategies: first default, then dayfirst
    for dayfirst in (False, True):
        try:
            dt = pd.to_datetime(val, errors="coerce", dayfirst=dayfirst, infer_datetime_format=True)
            if not pd.isna(dt):
                STATS["date_parsed"] += 1
                return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    STATS["date_failed"] += 1
    return None


# -------- main pipeline --------
def main():
    p = Path(INPUT_FILE)
    if not p.exists():
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(p)
    STATS["rows_before"] = len(df)

    # Drop rows missing customer_id
    if "customer_id" in df.columns:
        df = df.dropna(subset=["customer_id"])
    else:
        print("Warning: customer_id column not present; cannot enforce primary key.")

    # Apply cleaning functions; guard against missing columns
    if "name" in df.columns:
        df["name"] = df["name"].apply(clean_name)
    if "email" in df.columns:
        df["email"] = df["email"].apply(clean_email)
    if "age" in df.columns:
        df["age"] = df["age"].apply(clean_age)
    if "salary" in df.columns:
        df["salary"] = df["salary"].apply(clean_salary)
    if "phone" in df.columns:
        df["phone"] = df["phone"].apply(clean_phone)
    if "join_date" in df.columns:
        df["join_date"] = df["join_date"].apply(clean_date)

    # Remove duplicates
    df = df.drop_duplicates()
    STATS["rows_after"] = len(df)

    # Save cleaned file
    df.to_csv(OUTPUT_FILE, index=False)

    # Produce a short report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("Data Quality Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Input file: {INPUT_FILE}\n")
        f.write(f"Rows before: {STATS['rows_before']}\n")
        f.write(f"Rows after:  {STATS['rows_after']}\n\n")
        f.write("Conversion counts:\n")
        f.write(f"  salary_numeric_parsed: {STATS['salary_numeric_parsed']}\n")
        f.write(f"  salary_text_parsed:    {STATS['salary_text_parsed']}\n")
        f.write(f"  salary_failed:         {STATS['salary_failed']}\n")
        f.write(f"  age_numeric_parsed:    {STATS['age_numeric_parsed']}\n")
        f.write(f"  age_text_parsed:       {STATS['age_text_parsed']}\n")
        f.write(f"  age_failed:            {STATS['age_failed']}\n")
        f.write(f"  phone_parsed_us:       {STATS['phone_parsed_us']}\n")
        f.write(f"  phone_parsed_intl:     {STATS['phone_parsed_intl']}\n")
        f.write(f"  phone_failed:          {STATS['phone_failed']}\n")
        f.write(f"  date_parsed:           {STATS['date_parsed']}\n")
        f.write(f"  date_failed:           {STATS['date_failed']}\n")
        f.write(f"  invalid_emails_removed:{STATS['invalid_emails_removed']}\n\n")
        f.write("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

    print("Cleaning complete.")
    print(f"Cleaned data written to: {OUTPUT_FILE}")
    print(f"Report written to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
