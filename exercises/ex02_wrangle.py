# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.20.2",
#     "plotly[express]>=6.6.0",
#     "polars>=1.39.3",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 2: Data Wrangling

    **Practice Polars!**

    **What you'll do:**

    - Load and explore real datasets
    - Filter and transform data
    - Answer questions with data

    **Instructions:**

    - Complete each TODO section
    - Run cells to see your results

    ---
    """)
    return


@app.cell
def _():
    import polars as pl
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime
    import marimo as mo

    return mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: Load and Explore Data
    """)
    return


@app.cell
def _(pl):
    # TODO: Load the students.csv file using Polars
    # The file is at: ../data/raw/students.csv

    students = pl.read_csv("../data/raw/students.csv")
    df = pl.DataFrame(data=students)
    print(df.head())

    # TODO: Display the first 10 rows
    return df, students


@app.cell
def _(df):
    # TODO: Display basic information about the students dataset
    # - How many rows and columns?
    # - What are the column names?
    # - What are the data types?

    # Hint: Use students.shape, students.columns, students.dtypes, or students.describe()
    print(df.columns)
    print(df.shape)
    print(df.dtypes)
    print(df.describe())

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2: Filtering Practice
    """)
    return


@app.cell
def _(pl, students):
    # TODO: Filter to find students who scored above 85 on their test

    high_scorers = students.filter(pl.col("test_score") > 85)  

    print(f"Number of high scorers: {len(high_scorers) if high_scorers is not None else 0}")
    return


@app.cell
def _(pl, students):
    # TODO: Filter to find students in grade_level 10 with attendance_rate > 90%

    grade_10_good_attendance = students.filter((pl.col("grade_level") == 10) & (pl.col("attendance_rate") > 0.9))
    print(f"Number of grade 10 students with good attendance: {len(grade_10_good_attendance) if grade_10_good_attendance is not None else 0}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3: Selecting and Creating Columns
    """)
    return


@app.cell
def _(pl, students):
    # TODO: Select only the name, grade_level, and test_score columns

    subset = students.select(pl.col("name"), pl.col("grade_level"), pl.col("test_score"))
    print(subset.head())
    return


@app.cell
def _(pl, students):
    # TODO: Create a new column "performance_category" that categorizes students:
    # - "Excellent" if test_score >= 90
    # - "Good" if test_score >= 75
    # - "Needs Improvement" if test_score < 75
    # - Handle null values appropriately

    # Hint: Use pl.when().then().otherwise() chains

    students_categorized = students.with_columns(
        pl.when(pl.col("test_score") >= 90)
          .then(pl.lit("Excellent"))
          .when(pl.col("test_score") >= 75)
          .then(pl.lit("Good"))
          .when(pl.col("test_score") < 75)
          .then(pl.lit("Needs Improvement"))
          .otherwise(pl.lit("Unknown"))
          .alias("performance_category")
    )
    print(students_categorized)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4: Working with Sales Data
    """)
    return


@app.cell
def _(pl):
    # TODO: Load the sales.json file
    # The file is at: ../data/raw/sales.json

    sales = pl.read_json("../data/raw/sales.json") 
    print(sales.head())
    return (sales,)


@app.cell
def _(sales):
    # TODO: Display basic info about the sales dataset
    # How many transactions? What's the date range?

    num_transactions = sales.shape[0]
    date_range = (sales['date'].min(), sales['date'].max())
    print(F"Number of transactions: {num_transactions}") 
    print(f"Date range: {date_range[0]} to {date_range[1]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5: Aggregations and Grouping
    """)
    return


@app.cell
def _(pl, sales):
    # TODO: Calculate total sales by product_category
    # Sum up the total_amount for each category
    # Sort by total sales descending

    category_sales =  (
        sales.group_by("product_category")
          .agg(pl.col("total_amount").sum().alias("total_sales"))
          .sort("total_sales", descending=True)
    )

    print(category_sales)
    return


@app.cell
def _(pl, sales):
    # TODO: Find the average transaction amount by payment_method

    avg_by_payment = (
        sales.group_by("payment_method")
          .agg(pl.col("total_amount").mean().alias("avg_transaction_amount"))
          .sort("avg_transaction_amount", descending=True)
    )
    print(avg_by_payment)
    return


@app.cell
def _(pl, sales):
    # TODO: Count how many transactions each region had
    # Also calculate the total revenue per region

    region_summary = (  # Group by region, count and sum
        sales.group_by("region")
          .agg(
              pl.col("total_amount").sum().alias("total_revenue"),
              pl.len().alias("transaction_count")
          )
          .sort("total_revenue", descending=True)
    )
    print(region_summary)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 6: Date Operations
    """)
    return


app._unparsable_cell(
    r"""
    # TODO: Convert the date column to datetime type
    # Then extract the month and create a new column "month"

     sales_with_month = None  # Use with_columns() and pl.col().str.to_date()
        return
    """,
    name="_"
)


@app.cell
def _(pl, sales):
    sales_with_month = sales.with_columns(
        pl.col("date")
        .str.to_date()           # convert string → date
        .dt.month()              # extract month as number (1–12)
        .alias("month")          # new column name
    )
    print(sales_with_month)
    return (sales_with_month,)


@app.cell
def _(pl, sales_with_month):
    # TODO: Calculate total sales by month
    # Show which month had the highest revenue

    monthly_sales = (
        sales_with_month.group_by("month")
          .agg(pl.col("total_amount").sum().alias("total_sales"))
          .sort("total_sales", descending=True)
    )
    print(monthly_sales)
    print(highest_month := monthly_sales.sort("total_sales", descending=True).head(1))
    print(highest_month)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎉 Excellent Work!

    You've completed the data wrangling exercises!

    **What you practiced:**

    - ✅ Loading CSV and JSON data with Polars
    - ✅ Filtering and selecting data
    - ✅ Creating calculated columns
    - ✅ Grouping and aggregating
    - ✅ Date operations

    **What's next?**

    - Move on to Exercise 3: Plot

    **Pro Tips:**

    - Chain Polars operations for cleaner code
    - Always explore your data before plotting
    """)
    return


if __name__ == "__main__":
    app.run()
