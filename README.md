# Data Cleanup Lessons

A comprehensive hands-on course for learning data cleaning, organization, and merging techniques using Python and Pandas.

## 📚 Course Overview

This repository contains practical exercises designed to teach essential data engineering skills through real-world scenarios. Students will work with messy, realistic datasets and learn to clean, organize, and merge data programmatically.

## 🎯 Learning Objectives

By completing these lessons, students will learn to:
- Organize files programmatically using Python
- Identify and fix common data quality issues
- Clean and standardize datasets using Pandas
- Merge overlapping datasets intelligently
- Handle data conflicts and deduplication
- Validate data cleaning results

## 📋 Prerequisites

- Basic Python knowledge
- Familiarity with file operations
- Understanding of CSV file format
- Python 3.7+ installed

## 🚀 Getting Started

### Setup
1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required packages:
   ```bash
   pip install pandas numpy
   ```

### Course Structure
Navigate to `lesson1/` to begin with the three progressive problems.

## 📂 Repository Structure

```
├── README.md              # This file
├── lesson1/               # Main lesson folder
│   ├── problem1/          # File Organization
│   │   ├── README.md      # Problem instructions
│   │   └── messy_data/    # Mixed file types to organize
│   ├── problem2/          # Data Cleaning
│   │   ├── README.md      # Problem instructions
│   │   ├── dirty_customer_data.csv
│   │   └── validate_problem2.py
│   └── problem3/          # Data Merging
│       ├── README.md      # Problem instructions
│       ├── customers_q1.csv
│       ├── customers_q2.csv
│       └── validate_problem3.py
├── .gitignore             # Git ignore rules
└── CLAUDE.md              # Generation documentation
```

## 🔧 Problems Overview

### Problem 1: File Organization
**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Skills**: File operations, pathlib, directory management

Organize a messy folder containing various file types (JSON, CSV, TXT, images) into properly structured directories.

**Key Learning**:
- File system navigation with Python
- Automated file organization
- Working with file extensions
- Directory creation and management

### Problem 2: Data Cleaning
**Difficulty**: Intermediate  
**Time**: 60-90 minutes  
**Skills**: Pandas, data validation, standardization

Clean a CSV file containing realistic data quality issues including missing values, formatting inconsistencies, and invalid entries.

**Data Issues to Fix**:
- Missing and null values
- Inconsistent name formatting
- Invalid email addresses
- Mixed data types
- Inconsistent phone formats
- Various date formats
- Duplicate rows

**Key Learning**:
- Data quality assessment
- Pandas data manipulation
- Data type conversion
- Pattern matching and regex
- Data standardization techniques

### Problem 3: Data Merging & Deduplication
**Difficulty**: Advanced  
**Time**: 90-120 minutes  
**Skills**: Data integration, conflict resolution, deduplication

Merge two CSV files with overlapping customer data, intelligently handle conflicts, and create a unified dataset.

**Challenges**:
- Identifying duplicate records
- Resolving data conflicts
- Combining related information
- Maintaining data integrity

**Key Learning**:
- Data merging strategies
- Conflict resolution logic
- Deduplication techniques
- Data validation after merging

## ✅ Validation & Testing

Each problem includes automated validation scripts to check your solutions:

```bash
# Problem 2 validation
python validate_problem2.py cleaned_customer_data.csv

# Problem 3 validation
python validate_problem3.py merged_customers.csv
```

The validation scripts provide detailed feedback on:
- Data format compliance
- Missing requirements
- Data quality issues
- Suggestions for improvement

## 🎓 Learning Path

**Recommended Order**:
1. Start with Problem 1 (File Organization)
2. Progress to Problem 2 (Data Cleaning)
3. Complete with Problem 3 (Data Merging)

Each problem builds upon skills from the previous one, creating a comprehensive learning experience.

## 💡 Tips for Success

1. **Read README files carefully** - Each problem has detailed instructions
2. **Test incrementally** - Don't try to solve everything at once
3. **Use validation scripts** - They provide immediate feedback
4. **Comment your code** - Explain your cleaning decisions
5. **Handle edge cases** - Real data is messy!

## 🔍 Common Challenges

- **File paths**: Use absolute paths or `pathlib` for cross-platform compatibility
- **Data types**: Always check and convert data types explicitly
- **Missing data**: Decide whether to fill, drop, or flag missing values
- **Duplicates**: Consider what makes a record truly duplicate
- **Validation**: Always validate your results with the provided scripts

## 📝 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python pathlib Guide](https://docs.python.org/3/library/pathlib.html)
- [Data Cleaning Best Practices](https://towardsdatascience.com/data-cleaning-with-python-and-pandas-detecting-missing-values-3e9c6ebcf78b)

## 🤝 Contributing

Found an issue or have suggestions for improvement? Feel free to:
- Open an issue describing the problem
- Suggest additional problems or challenges
- Contribute example solutions (in a separate branch)

## 📄 License

This educational content is provided for learning purposes. Feel free to use and modify for educational use.

---

**Happy Learning!** 🚀

*Remember: The best way to learn data cleaning is by getting your hands dirty with real, messy data.*