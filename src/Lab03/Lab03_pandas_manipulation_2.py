import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Setup environment and load data
#Dataset: https://s3.hothienlac.com/yomitoon/sales_data.csv

def read_data() -> pd.DataFrame:
    """
    Reads data from an Excel file and returns a pandas DataFrame.
    """
    # Read the Excel file with link
    df_can = pd.read_csv('https://s3.hothienlac.com/yomitoon/sales_data.csv')
    df_can = df_can.assign(total_amount=df_can['quantity'] * df_can['unit_price'])

    return df_can

'''
Q8. Average order value (AOV) per customer
Task
For each customer, compute:

total spending
number of orders
average order value
💡 Hint
Use:

.groupby()
.agg()
basic arithmetic between aggregated columns
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
https://pandas.pydata.org/docs/user_guide/groupby.html
🧠 Explanation
This teaches:

multi-metric aggregation
ratio metrics (very common in dashboards)
separating raw data from business KPIs
'''
def aov(df: pd.DataFrame) -> pd.DataFrame:
    df_aov = df.groupby('customer_id').agg(
        total_spending=pd.NamedAgg(column='total_amount', aggfunc='sum'),
        number_of_orders=pd.NamedAgg(column='order_id', aggfunc='nunique')
    ).reset_index()
    df_aov = df_aov.assign(
        average_order_value = df_aov['total_spending'] / df_aov['number_of_orders']
    )
    return df_aov


def task_8(df: pd.DataFrame) -> None:
    df_aov = aov(df)
    print("Average Order Value (AOV) per customer:")
    print(df_aov.head())

'''
Q9. Revenue contribution by category (%)
Task
Calculate:

total revenue per product category
percentage contribution of each category to total revenue
💡 Hint
Use:

.groupby()
.sum()
.assign()
division by a global scalar
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.div.html
🧠 Explanation
You learn:

normalization
how to compare groups on the same scale
how to prepare data for pie charts / stacked bars
'''
def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    df_rev = df.groupby('category').agg(
        category_revenue=pd.NamedAgg(column='total_amount', aggfunc='sum')
    ).reset_index()

    total_revenue = df_rev['category_revenue'].sum()

    df_rev = df_rev.assign(
        percentage=df_rev['category_revenue'] / total_revenue * 100
    )
    return df_rev


def task_9(df: pd.DataFrame) -> None:
    df_rev = revenue_by_category(df)
    print("Revenue contribution by category (%):")
    print(df_rev.head())



'''
Q10. Identify top 20% customers by revenue (Pareto analysis)
Task
Determine:

which customers belong to the top 20% by total spending
💡 Hint
Use:

.sort_values()
.cumsum()
.quantile()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.quantile.html
🧠 Explanation
This is a classic 80/20 rule problem:

who really drives revenue?
foundational for customer segmentation
'''
def top_20_percent_customers(df: pd.DataFrame) -> pd.DataFrame:
    df_cus = df.groupby('customer_id').agg(
        total_spending=pd.NamedAgg(column='total_amount', aggfunc='sum')
    ).reset_index()

    df_cus = df_cus.sort_values('total_spending', ascending=False)

    df_cus = df_cus.assign(
        cumulative_pct=df_cus['total_spending'].cumsum() /
                       df_cus['total_spending'].sum()
    )

    top_customers = df_cus[df_cus['cumulative_pct'] <= 0.8]
    return top_customers


def task_10(df: pd.DataFrame) -> None:
    top_customers = top_20_percent_customers(df)
    print("Top 20% customers by revenue:")
    print(top_customers.head())



'''
Q11. Price distribution analysis per category
Task
For each product category, compute:

mean unit price
median unit price
standard deviation
💡 Hint
Use:

.groupby()
.agg(mean=..., median=..., std=...)
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
🧠 Explanation
This builds intuition for:

distribution shape
why median ≠ mean
choosing the right chart (boxplot vs bar)
'''
def price_stats_by_category(df: pd.DataFrame) -> pd.DataFrame:
    df_price = df.groupby('category').agg(
        mean_price=pd.NamedAgg(column='unit_price', aggfunc='mean'),
        median_price=pd.NamedAgg(column='unit_price', aggfunc='median'),
        std_price=pd.NamedAgg(column='unit_price', aggfunc='std')
    ).reset_index()

    return df_price


def task_11(df: pd.DataFrame) -> None:
    df_price = price_stats_by_category(df)
    print("Price distribution per category:")
    print(df_price.head())


'''
Q12. Day-over-day revenue growth (%)
Task
Compute:

daily revenue
percentage change compared to previous day
💡 Hint
Use:

.groupby()
.pct_change()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.pct_change.html
🧠 Explanation
This teaches:

growth vs absolute value
preparing data for line charts
understanding volatility
'''
def daily_revenue_growth(df: pd.DataFrame) -> pd.DataFrame:
    df_daily = df.groupby('order_date').agg(
        daily_revenue=pd.NamedAgg(column='total_amount', aggfunc='sum')
    ).reset_index().sort_values('order_date')

    df_daily = df_daily.assign(
        growth_pct=df_daily['daily_revenue'].pct_change() * 100
    )
    return df_daily


def task_12(df: pd.DataFrame) -> None:
    df_daily = daily_revenue_growth(df)
    print("Day-over-day revenue growth (%):")
    print(df_daily.head())



'''
Q13. Rolling average of daily revenue
Task
Calculate:

3-day rolling average of daily revenue
💡 Hint
Use:

.rolling(window=3)
.mean()
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.rolling.html
🧠 Explanation
Rolling metrics are used to:

smooth noisy data
reveal trends
support time-series visualization
'''
def rolling_3day_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df_daily = df.groupby('order_date').agg(
        daily_revenue=pd.NamedAgg(column='total_amount', aggfunc='sum')
    ).reset_index().sort_values('order_date')

    df_daily = df_daily.assign(
        rolling_3day_avg=df_daily['daily_revenue'].rolling(window=3).mean()
    )
    return df_daily


def task_13(df: pd.DataFrame) -> None:
    df_daily = rolling_3day_revenue(df)
    print("3-day rolling average of daily revenue:")
    print(df_daily.head())

'''
Q14. Detect unusually large orders (outliers)
Task
Flag orders where:

total_amount is significantly higher than normal (use a statistical threshold)
💡 Hint
Use:

.mean()
.std()
boolean conditions
📚 Reference
https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
🧠 Explanation
You are learning:

basic anomaly detection
how math supports intuition
how analysts decide what deserves investigation
'''
def detect_large_orders(df: pd.DataFrame) -> pd.DataFrame:
    mean_val = df['total_amount'].mean()
    std_val = df['total_amount'].std()

    df_outlier = df.assign(
        is_outlier=df['total_amount'] > (mean_val + 3 * std_val)
    )

    return df_outlier[df_outlier['is_outlier']]


def task_14(df: pd.DataFrame) -> None:
    df_outlier = detect_large_orders(df)
    print("Unusually large orders (outliers):")
    print(df_outlier.head())


def main():
    df = read_data()
    task_8(df)
    print('='*100)
    task_9(df)
    print('='*100)
    task_10(df)
    print('='*100)
    task_11(df)
    print('='*100)
    task_12(df)
    print('='*100)
    task_13(df)
    print('='*100)
    task_14(df)


if __name__ == "__main__":
	main()