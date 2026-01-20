import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

'''
Q1. Load and inspect the dataset
Task
Load the CSV file and:

Display the first 5 rows
Show column names and data types
💡 Hint
Use:

pd.read_csv
.head()
.info()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html
🧠 Explanation
You are learning how to inspect unfamiliar data quickly and verify 
that Pandas interpreted types correctly (dates, numbers, strings).
'''
def read_data() -> pd.DataFrame:
    """
    Reads data from an Excel file and returns a pandas DataFrame.
    """
    # Read the Excel file "https://s3.hothienlac.com/yomitoon/sales_data.csv"
    df_can = pd.read_csv('https://s3.hothienlac.com/yomitoon/sales_data.csv')

    return df_can

def task_1(df: pd.DataFrame) -> None:
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\nColumn names and data types:")
    print(df.info())

'''
Q2. Create a new column for total order value
Task
Create a new column called total_amount Formula:

quantity × unit_price
💡 Hint
Use:
.assign()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html
🧠 Explanation
This teaches feature engineering and the functional Pandas mindset 
(inplace=False, return a new DataFrame).
'''
def create_total(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.assign(total_amount = df['quantity']* df['unit_price'])

    return df

def task_2(df: pd.DataFrame) -> pd.DataFrame:
    df = create_total(df)
    print("\nDataFrame with new 'total_amount' column:")
    print(df)
    # print(df.head())
    return df

'''
Q3. Filter high-value orders
Task
Select only orders where:

total_amount > 500
💡 Hint
Use one of:
.query()
Boolean indexing (df[condition])
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html
🧠 Explanation
Filtering is the foundation of real data analysis. 
You learn how Pandas handles boolean logic
'''
def filter_high_value_orders(df: pd.DataFrame) -> pd.DataFrame:
    df_high_value = df.query('total_amount > 500')
    return df_high_value

def task_3(df: pd.DataFrame) -> pd.DataFrame:
    df_high_value = filter_high_value_orders(df)
    print("\nHigh-value orders (total_amount > 500):")
    print(df_high_value)
    return df_high_value
'''
Q4. Count how many orders each customer made
Task
Create a table showing:

customer_id
number of orders per customer
💡 Hint
Use:
.groupby()
.count() or .size()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
🧠 Explanation
You learn how Pandas splits data into groups and applies calculations per group.
'''
def count_orders_per_customer(df: pd.DataFrame) -> pd.DataFrame:
    df_orders_count = df.groupby('customer_id').size().reset_index(name='order_count')
    return df_orders_count


def task_4(df: pd.DataFrame) -> pd.DataFrame:
    df_orders_count = count_orders_per_customer(df)
    print("\nNumber of orders per customer:")
    print(df_orders_count)
    return df_orders_count

'''
Q5. Calculate total spending per customer
Task
For each customer_id, compute:

Total money spent
💡 Hint
Use:

.groupby()
.agg()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html
🧠 Explanation
This introduces aggregation pipelines and prepares you for more complex analytics.
'''
def calculate_total(df: pd.DataFrame) -> pd.DataFrame:
    df_total_spent = df.groupby('customer_id').agg(total_spent=('total_amount', 'sum')).reset_index()
    return df_total_spent

def task_5(df: pd.DataFrame) -> pd.DataFrame:
    df_total_spent = calculate_total(df)
    print("\nTotal spending per customer:")
    print(df_total_spent)
    return df_total_spent

'''
Q6. Daily revenue analysis
Task
Calculate:

Total revenue per day
Sort results by date
💡 Hint
Use:

parse_dates in read_csv
.groupby()
.sort_values()
📚 Reference
https://pandas.pydata.org/docs/user_guide/timeseries.html
🧠 Explanation
Time-based grouping is essential for business dashboards and reports.
'''
def daily_revenue_analysis(df: pd.DataFrame) -> pd.DataFrame:
    df['order_date'] = pd.to_datetime(df['order_date'])
    df_daily_revenue = df.groupby('order_date').agg(daily_revenue=('total_amount', 'sum')).reset_index()
    df_daily_revenue = df_daily_revenue.sort_values(by='order_date')
    return df_daily_revenue

def task_6(df: pd.DataFrame) -> pd.DataFrame:
    df_daily_revenue = daily_revenue_analysis(df)
    print("\nDaily revenue analysis:")
    print(df_daily_revenue)
    return df_daily_revenue

'''
Q7. Rank customers by spending
Task
Rank customers from highest to lowest total spending.

💡 Hint
Use:

.rank()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.rank.html
🧠 Explanation
Ranking teaches you how Pandas handles ordering, ties, and numeric comparisons.
'''
def rank_customer(df: pd.DataFrame) -> pd.DataFrame:
    df_ranked = df.sort_values(by='total_spent', ascending=False)
    df_ranked['rank'] = df_ranked['total_spent'].rank(method='min', ascending=False)
    return df_ranked

def task_7(df: pd.DataFrame) -> pd.DataFrame:
    df_ranked = rank_customer(df)
    print("\nCustomers ranked by total spending:")
    print(df_ranked)
    return df_ranked

def main():
    #Read data
    df_can = read_data()
    # Perform Task 1 - Inspect the dataset
    task_1(df_can)
    print("="*100)
    # Perform Task 2 - Create total_amount column
    df_total = task_2(df_can)
    print("="*100)
    # Perform Task 3 - Filter high-value orders
    df_can = task_3(df_total)
    print("="*100)
    # Perform Task 4 - Count orders per customer
    df_can = task_4(df_total)
    print("="*100)
    # Perform Task 5 - Calculate total spending per customer
    df_total_spend = task_5(df_total)
    print("="*100)
    # Perform Task 6 - Daily revenue analysis
    df_can = task_6(df_total)
    print("="*100)
    # Perform Task 7 - Rank customers by spending
    df_can = task_7(df_total_spend)

if __name__ == "__main__":  
    main()