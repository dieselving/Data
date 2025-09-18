#!/usr/bin/env python3
"""
merge_customers.py
Merge Q1 and Q2 customer datasets, handle duplicates & conflicts,
and produce merged_customers.csv with a merge report.
"""

import pandas as pd
from datetime import datetime

Q1_FILE = "customers_q1.csv"
Q2_FILE = "customers_q2.csv"
OUTPUT_FILE = "merged_customers.csv"
REPORT_FILE = "merge_report.txt"


def merge_customers():
    # Load both CSVs
    q1 = pd.read_csv(Q1_FILE)
    q2 = pd.read_csv(Q2_FILE)

    # Ensure consistent column names (strip spaces, lowercase)
    q1.columns = q1.columns.str.strip().str.lower()
    q2.columns = q2.columns.str.strip().str.lower()

    # Add a source column for debugging/reporting
    q1["source"] = "Q1"
    q2["source"] = "Q2"

    # Combine datasets
    combined = pd.concat([q1, q2], ignore_index=True)

    # Drop exact duplicates (all columns identical)
    combined = combined.drop_duplicates()

    # Prepare report stats
    report_lines = []
    report_lines.append("Customer Merge Report")
    report_lines.append("=" * 40)

    unique_customers_before = combined["customer_id"].nunique()
    report_lines.append(f"Unique customers before deduplication: {unique_customers_before}")

    # Conflict resolution
    resolved_rows = []
    conflicts = []

    for cid, group in combined.groupby("customer_id"):
        if len(group) == 1:
            # Only one record → keep as is
            resolved_rows.append(group.iloc[0].to_dict())
        else:
            # Conflict case (appears in both quarters)
            q1_row = group[group["source"] == "Q1"].iloc[0] if "Q1" in group["source"].values else None
            q2_row = group[group["source"] == "Q2"].iloc[0] if "Q2" in group["source"].values else None

            # Start with Q2 data (latest)
            merged = q2_row.to_dict() if q2_row is not None else {}

            # If Q1 exists, resolve conflicts
            if q1_row is not None:
                # Combine purchases
                try:
                    merged["total_purchases"] = float(q1_row["total_purchases"]) + float(q2_row["total_purchases"])
                except Exception:
                    merged["total_purchases"] = q2_row["total_purchases"]

                # Earliest registration date
                try:
                    d1 = pd.to_datetime(q1_row["registration_date"], errors="coerce")
                    d2 = pd.to_datetime(q2_row["registration_date"], errors="coerce")
                    merged["registration_date"] = min(d1, d2).strftime("%Y-%m-%d")
                except Exception:
                    merged["registration_date"] = q2_row["registration_date"]

                # Log conflicts if other columns differ
                for col in group.columns:
                    if col not in ["customer_id", "total_purchases", "registration_date", "source"]:
                        if pd.notna(q1_row[col]) and pd.notna(q2_row[col]) and q1_row[col] != q2_row[col]:
                            conflicts.append((cid, col, q1_row[col], q2_row[col]))

            resolved_rows.append(merged)

    # Create final dataframe
    merged_df = pd.DataFrame(resolved_rows)

    # Drop "source" column if present
    if "source" in merged_df.columns:
        merged_df = merged_df.drop(columns=["source"])

    # Save merged result
    merged_df.to_csv(OUTPUT_FILE, index=False)

    # Report summary
    unique_customers_after = merged_df["customer_id"].nunique()
    report_lines.append(f"Unique customers after deduplication: {unique_customers_after}")
    report_lines.append(f"Total rows in final dataset: {len(merged_df)}")

    # Purchase totals
    try:
        total_before = combined["total_purchases"].astype(float).sum()
        total_after = merged_df["total_purchases"].astype(float).sum()
        report_lines.append(f"Total purchases before merging: {total_before}")
        report_lines.append(f"Total purchases after merging: {total_after}")
    except Exception:
        report_lines.append("Purchase totals could not be fully calculated due to invalid data.")

    # Conflict details
    report_lines.append("\nConflicts Resolved:")
    if conflicts:
        for cid, col, val1, val2 in conflicts:
            report_lines.append(f"Customer {cid}: Column '{col}' -> Q1='{val1}', Q2='{val2}' (Q2 kept)")
    else:
        report_lines.append("No conflicting data found.")

    # Save report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        f.write("\nGenerated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("\n--- Merge Completed ---")
    print(f"Final dataset saved to {OUTPUT_FILE}")
    print(f"Merge report saved to {REPORT_FILE}")


if __name__ == "__main__":
    merge_customers()
