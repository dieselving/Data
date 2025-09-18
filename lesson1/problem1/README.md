# Problem 1: File Organization

## Objective
Write a Python script to organize the messy files in the `messy_data` folder into properly structured directories based on file types.

## Current Situation
The `messy_data` folder contains various file types mixed together:
- JSON files (`.json`)
- CSV files (`.csv`) 
- Text files (`.txt`)
- Image files (`.jpg`, `.png`, `.gif`)

## Task
Create a Python script called `organize_files.py` that:

1. **Scans** the `messy_data` folder
2. **Creates** appropriate subdirectories:
   - `json_files/` for JSON files
   - `csv_files/` for CSV files  
   - `text_files/` for TXT files
   - `images/` for image files
3. **Moves** each file to its corresponding directory
4. **Prints** a summary of what was organized

## Requirements
- Use the `pathlib` module for file operations
- Handle file extensions case-insensitively (`.JSON` should be treated same as `.json`)
- Create directories only if they don't already exist
- Print the number of files moved to each directory
- Handle any potential errors gracefully

## Expected Output Structure
```
messy_data/
├── json_files/
│   ├── users.json
│   ├── products.json
│   └── config.json
├── csv_files/
│   ├── sales.csv
│   ├── employees.csv
│   └── inventory.csv
├── text_files/
│   ├── readme.txt
│   ├── notes.txt
│   └── log.txt
└── images/
    ├── photo1.jpg
    ├── chart.png
    └── diagram.gif
```

## Bonus Challenge
Extend your script to also handle:
- Creating a summary report in `organization_report.txt`
- Handling unknown file types (create an `other_files/` directory)
- Adding timestamp to the report

## Testing
Run your script and verify that all files are properly organized into their respective folders.