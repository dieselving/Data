import pandas as pd
import os
import re
from pathlib import Path

# PII字段常见关键词
PII_KEYWORDS = ['name', 'email', 'ssn', 'phone', 'address', 'credit_card', 'dob', 'date_of_birth']

def detect_pii(columns):
    """检测潜在PII字段"""
    return [col for col in columns if any(kw in col.lower() for kw in PII_KEYWORDS)]

def profile_csv(file_path):
    """分析单个CSV文件"""
    df = pd.read_csv(file_path)
    report = {
        'file': str(file_path),
        'columns': [],
        'pii_fields': detect_pii(df.columns)
    }
    for col in df.columns:
        col_info = {
            'name': col,
            'dtype': str(df[col].dtype),
            'nulls': int(df[col].isnull().sum()),
            'unique': int(df[col].nunique()),
        }
        # 基本统计（仅数值型）
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info['min'] = df[col].min()
            col_info['max'] = df[col].max()
            col_info['mean'] = df[col].mean()
        report['columns'].append(col_info)
    return report

def scan_directory(data_dir):
    """扫描目录下所有CSV文件"""
    reports = []
    for csv_file in Path(data_dir).glob('*.csv'):
        try:
            reports.append(profile_csv(csv_file))
        except Exception as e:
            print(f"文件 {csv_file} 处理失败: {e}")
    return reports

if __name__ == "__main__":
      # 指定数据目录
    data_dir = "sample_data"
    discovery_results = scan_directory(data_dir)
    # 生成发现报告
    pd.DataFrame(discovery_results).to_json("discovery_report.json", orient="records", force_ascii=False, indent=2)
    print("数据发现报告已生成：discovery_report.json")