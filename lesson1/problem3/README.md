# Problem 3: Data Merging and Deduplication 数据合并和重复数据删除

## Objective
Merge two CSV files containing customer data from different quarters, handle duplicates intelligently, and create a unified dataset.

## Current Situation
You have two CSV files:
- `customers_q1.csv` - Customer data from Q1 (8 customers)
- `customers_q2.csv` - Customer data from Q2 (12 customers)

These files contain **overlapping customers** (some customers appear in both files) and need to be merged into a single, deduplicated dataset.

## Task
Create a Python script called `merge_customers.py` that:

1. **Loads** both CSV files using pandas
2. **Identifies** overlapping customers (same customer_id)
3. **Handles conflicts** in data when the same customer has different information
4. **Merges** the datasets while avoiding duplicates
5. **Creates** a final unified dataset
6. **Saves** the result to `merged_customers.csv`

## Data Challenges

### Overlapping Customers
Some customers appear in both files with:
- **Identical data** - These should be deduplicated (keep one copy)
- **Conflicting data** - Same customer_id but different values (address, purchase amounts, etc.)

### Conflict Resolution Strategy
When the same customer has different data in both files:
- **Keep the most recent data** (Q2 data is more recent than Q1)
- **Combine purchase amounts** (sum total_purchases from both quarters)
- **Use the earliest registration_date**
- **For other conflicts**, prioritize Q2 data

## Requirements
- Use pandas for data manipulation
- Handle exact duplicates by removing them
- Implement intelligent conflict resolution for partial duplicates
- Print summary of merge operations
- Document your merge strategy with comments

## Expected Merge Logic

### Case 1: Exact Duplicates
```
Q1: [ID=1, Name="John", Purchases=1500]
Q2: [ID=1, Name="John", Purchases=1500]
Result: [ID=1, Name="John", Purchases=1500] (keep one copy)
```

### Case 2: Purchase Amount Conflicts
```
Q1: [ID=1, Name="John", Purchases=1500, Date="2023-01-15"]
Q2: [ID=1, Name="John", Purchases=2000, Date="2023-01-15"]
Result: [ID=1, Name="John", Purchases=3500, Date="2023-01-15"] (sum purchases)
```

### Case 3: Other Data Conflicts
```
Q1: [ID=1, Name="John", City="NYC", Date="2023-01-15"]
Q2: [ID=1, Name="John", City="LA", Date="2023-01-15"]
Result: [ID=1, Name="John", City="LA", Date="2023-01-15"] (Q2 takes priority)
```

## Testing Your Solution
After creating your merge script, test it using:
```bash
python validate_problem3.py merged_customers.csv
```

The validation script will verify:
- No duplicate customer_ids in final result
- All unique customers from both files are included
- Merge conflicts were handled appropriately

## Expected Output
Your merged CSV should contain:
- All unique customers from both files
- No duplicate customer_ids
- Properly resolved data conflicts
- Combined purchase amounts where appropriate

## Analysis Questions
After completing the merge, analyze your results:
1. How many total unique customers are there?
2. How many customers appeared in both files?
3. What was the total purchase amount before and after merging?
4. Which customers had conflicting data?

## Bonus Challenges
1. Create a detailed merge report showing what conflicts were resolved
2. Implement different conflict resolution strategies (user choice)
3. Handle cases where customer names don't match but IDs do
4. Add data validation to ensure merge quality