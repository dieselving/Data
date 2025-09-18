# Problem 2: Data Cleaning

## Objective
Clean the messy `dirty_customer_data.csv` file by fixing various data quality issues and create a clean, standardized dataset.

## Current Issues
The CSV file contains multiple data quality problems:
- **Missing values** in various columns
- **Inconsistent name formatting** (mixed case)
- **Invalid email addresses** 
- **Non-numeric age values** (text instead of numbers)
- **Inconsistent phone number formats**
- **Non-numeric salary values** (text instead of numbers)
- **Inconsistent date formats** 
- **Duplicate rows**

## Task
Create a Python script called `clean_data.py` that:

1. **Loads** the dirty CSV file using pandas
2. **Handles missing values** appropriately:
   - Remove rows with missing customer_id
   - Fill or remove other missing values as appropriate
3. **Standardizes text data**:
   - Convert names to Title Case
   - Convert emails to lowercase
   - Remove invalid email addresses
4. **Cleans numeric data**:
   - Convert age to integers (handle text values)
   - Convert salary to float (handle text values)
5. **Standardizes phone numbers** to format: `(XXX) XXX-XXXX`
6. **Standardizes dates** to format: `YYYY-MM-DD`
7. **Removes duplicate rows**
8. **Saves** the cleaned data to `cleaned_customer_data.csv`

## Requirements
- Use pandas for data manipulation
- Handle errors gracefully (don't crash on invalid data)
- Print summary statistics before and after cleaning
- Document your cleaning decisions with comments

## Data Cleaning Guidelines

### Phone Numbers
Convert various formats to `(XXX) XXX-XXXX`:
- `123-456-7890` → `(123) 456-7890`
- `5551234567` → `(555) 123-4567`
- `123.456.7890` → `(123) 456-7890`

### Dates
Convert various formats to `YYYY-MM-DD`:
- `2023/02/20` → `2023-02-20`
- `15-03-2023` → `2023-03-15`
- `May 30, 2023` → `2023-05-30`

### Age and Salary
- Convert text numbers to numeric values
- Remove or handle invalid entries appropriately

## Testing Your Solution
After creating your cleaning script, test it using:
```bash
python validate_problem2.py cleaned_customer_data.csv
```

The validation script will check if your cleaned data meets all requirements and provide detailed feedback.

## Expected Output
Your cleaned CSV should have:
- No duplicate rows
- All customer_ids present and valid
- Names in Title Case
- Valid email addresses in lowercase
- Numeric ages and salaries
- Standardized phone numbers
- Standardized date formats

## Bonus Challenges
1. Create a data quality report showing what was cleaned
2. Handle edge cases like international phone numbers
3. Add data validation rules for future data imports