# Problem 1: Data Discovery and Classification

## Learning Objectives
- Understand data discovery principles and automated scanning techniques
- Implement data classification frameworks based on sensitivity and business impact
- Apply DAMA-DMBOK data governance principles to real-world datasets
- Create risk-based data categorization following regulatory requirements

## Background
Your organization has multiple data sources that need to be cataloged and classified according to their sensitivity level and business impact. As a Data Protection Officer (DPO), you must implement a systematic approach to discover, classify, and document all data assets according to GDPR and internal governance policies.

## Scenario
You've inherited a new data landscape with various datasets scattered across different systems. Your task is to:

1. **Discover** all data assets in the provided sample datasets
2. **Classify** data according to sensitivity levels (Public, Internal, Confidential, Restricted)
3. **Categorize** by business impact (Low, Medium, High, Critical)
4. **Document** findings in a structured data catalog

## Task Requirements

### Part A: Data Discovery (25 points)
Write a Python script that:
- Scans all provided CSV files in the `sample_data/` directory
- Identifies column names, data types, and basic statistics
- Detects potential PII (Personally Identifiable Information) fields
- Generates a discovery report with data profiling results

### Part B: Data Classification (35 points)
Implement a classification system that:
- Assigns sensitivity levels based on data content patterns
- Determines business impact scores using predefined criteria
- Applies GDPR Article 9 special category identification
- Creates classification tags for each dataset and column

### Part C: Data Catalog Creation (40 points)
Build a comprehensive data catalog that includes:
- Asset metadata (source, owner, last updated)
- Data lineage information (where data comes from/goes to)
- Quality metrics (completeness, validity, uniqueness)
- Compliance status (GDPR compliance, retention requirements)

## Deliverables
1. `data_discovery.py` - Discovery and profiling script
2. `data_classification.py` - Classification engine implementation
3. `data_catalog.json` - Structured catalog output
4. `classification_report.csv` - Summary of all classifications
5. `discovery_log.txt` - Detailed discovery process log

## Evaluation Criteria
- **Technical Implementation** (40%): Code quality, error handling, efficiency
- **Governance Compliance** (30%): Adherence to DAMA-DMBOK and GDPR principles
- **Documentation Quality** (20%): Clear documentation and metadata standards
- **Risk Assessment** (10%): Accuracy of sensitivity and impact classifications

## Getting Started
```bash
# Install required packages
pip install pandas numpy re json pathlib

# Run the discovery process
python data_discovery.py

# Generate classifications
python data_classification.py

# View results
cat data_catalog.json
```

## Resources
- [DAMA-DMBOK Data Governance Framework](https://dama.org/)
- [GDPR Data Classification Guidelines](https://gdpr.eu/)
- [Data Quality Dimensions](https://www.dataversity.net/)

## Expected Time
- Part A: 45 minutes
- Part B: 60 minutes
- Part C: 75 minutes
- **Total: 3 hours**