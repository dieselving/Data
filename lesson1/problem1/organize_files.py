#!/usr/bin/env python3
"""
organize_files.py
Organize files in messy_data/ into structured subdirectories by file type.
"""

from pathlib import Path
import shutil
from datetime import datetime

# Define source folder
BASE_DIR = Path("messy_data")

# Define destination folders
DEST_DIRS = {
    "json": BASE_DIR / "json_files",
    "csv": BASE_DIR / "csv_files",
    "txt": BASE_DIR / "text_files",
    "images": BASE_DIR / "images",
    "other": BASE_DIR / "other_files",  # for unknown types
}

# Supported image extensions
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif"}


def organize_files():
    if not BASE_DIR.exists():
        print(f"Source folder {BASE_DIR} does not exist.")
        return

    # Create subdirectories if not exist 创建子目录（如果不存在）
    for folder in DEST_DIRS.values():
        folder.mkdir(exist_ok=True)

    summary = {k: 0 for k in DEST_DIRS.keys()}  # count files moved 计算移动的文件

    for file in BASE_DIR.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            try:
                if ext == ".json":
                    shutil.move(str(file), DEST_DIRS["json"] / file.name)
                    summary["json"] += 1
                elif ext == ".csv":
                    shutil.move(str(file), DEST_DIRS["csv"] / file.name)
                    summary["csv"] += 1
                elif ext == ".txt":
                    shutil.move(str(file), DEST_DIRS["txt"] / file.name)
                    summary["txt"] += 1
                elif ext in IMAGE_EXTS:
                    shutil.move(str(file), DEST_DIRS["images"] / file.name)
                    summary["images"] += 1
                else:
                    shutil.move(str(file), DEST_DIRS["other"] / file.name)
                    summary["other"] += 1
            except Exception as e:
                print(f"Error moving {file.name}: {e}")

    # Print summary 打印摘要
    print("\n--- File Organization Summary ---")
    for k, v in summary.items():
        print(f"{k.capitalize()} files moved: {v}")

    # Write report with timestamp 编写报告
    report_file = BASE_DIR / "organization_report.txt"
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(f"\nReport generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for k, v in summary.items():
            f.write(f"{k.capitalize()} files moved: {v}\n")
        f.write("-" * 40 + "\n")


if __name__ == "__main__":
    organize_files()
