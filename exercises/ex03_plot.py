# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.22.0",
#     "plotly[express]>=6.6.0",
#     "polars>=1.39.3",
#     "statsmodels>=0.14.6",
# ]
# ///

import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # Exercise 3: Plotting Visualizations 📊

    **Plot Visuals!**

    **What you'll do:**

    - Create visualizations

    **Instructions:**

    - Complete each TODO section
    - Run cells to see your results
    """)
    return


@app.cell
def _():
    import polars as pl
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime
    import marimo as mo
    import statsmodels.api as sm
    from plotly.subplots import make_subplots

    return go, make_subplots, mo, pl, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: Your First Plot - Bar Chart
    """)
    return


@app.cell
def _(pl, px):
    # TODO: Create a bar chart showing sales by category
    # Use plotly express (px.bar)
    # - x-axis: product_category
    # - y-axis: total sales
    # - Add a title
    # - Color the bars

    # Hint: Make sure category_sales is a valid dataframe first!

    sales=pl.read_json("../data/raw/sales.json")
    print(sales.head())
    category_sales = sales.group_by("product_category").agg(
        pl.col("total_amount").sum().alias("total_sales"))

    ex_fig1 = px.bar(
        category_sales,
        x="product_category",
        y="total_sales",
        title="Sales by Category",
        color="product_category",
    ) 
    ex_fig1.show()
    return category_sales, sales


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 2: Line Chart - Sales Over Time
    """)
    return


@app.cell
def _(pl, px, sales):
    # TODO: Create a line chart showing sales trends by month
    # Use px.line
    # - x-axis: month
    # - y-axis: total revenue
    # - Add markers to the line
    # - Add a title

    sales_with_month = sales.with_columns(
            pl.col("date")
            .str.to_date()           # convert string → date
            .dt.month()              # extract month as number (1–12)
            .alias("month") 
    )  
    monthly_sales = sales_with_month.group_by("month").agg(
        pl.col("total_amount").sum().alias("total_revenue")).sort("month")

    ex_fig2 = px.line(
        monthly_sales,
        x="month",
        y="total_revenue",
        title="Sales Over Time",
        markers=True
    )
    ex_fig2.show()
    # Uncomment when ready:
    # ex_fig2.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 3: Scatter Plot - Exploring Relationships
    """)
    return


@app.cell
def _(pl, px):
    # TODO: Create a scatter plot showing the relationship between
    # attendance_rate (x-axis) and test_score (y-axis)
    # - Color points by grade_level
    # - Add a trendline (trendline="ols")
    # - Add appropriate title and labels

    students = pl.read_csv("../data/raw/students.csv")

    ex_fig3 = px.scatter(
        students,
        x="attendance_rate",
        y="test_score",
        color="grade_level",
        trendline="ols",
        title="Exploring Relationships",
        labels={"attendance_rate": "Attendance Rate", "test_score": "Test Score"} 
    )
    ex_fig3.show()
    # Uncomment when ready:
    # ex_fig3.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 4: Histogram - Distribution Analysis
    """)
    return


@app.cell
def _(px, sales):
    # TODO: Create a histogram of transaction amounts (total_amount)
    # - Use 30 bins
    # - Add a title
    # - Label the axes
    # - Try adding nbins=30 parameter

    ex_fig4 = px.histogram(
        sales,
        x="total_amount",
        nbins=30,
        title="Distribution Analysis",
        labels={"total_amount": "Transaction Amount", "count": "Frequency"}
    )
    ex_fig4.show()
    # Uncomment when ready:
    # ex_fig4.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 5: Advanced - Multiple Subplots
    """)
    return


@app.cell
def _(category_sales, go, make_subplots, pl, sales):
    # TODO: Create a dashboard with 2 subplots:
    # 1. Top plot: Bar chart of sales by category (reuse category_sales)
    # 2. Bottom plot: Bar chart of sales by region (reuse region_summary)

    # Hint: Use go.Figure() with make_subplots or add multiple traces
    # This is challenging - check the solution if you get stuck!

    region_summary = (  # Group by region, count and sum
            sales.group_by("region")
              .agg(
                  pl.col("total_amount").sum().alias("total_revenue"),
                  pl.len().alias("transaction_count")
              )
              .sort("total_revenue", descending=True)
        )

    ex_fig5 = make_subplots(
        rows=2, cols=1,
        subplot_titles=["Category Sales", "Region Summary"]
    )

    ex_fig5.add_trace(
        go.Bar(x=category_sales["product_category"], y=category_sales["total_sales"], name="Category Sales"),
        row=1, col=1
    )
    ex_fig5.add_trace(
        go.Bar(x=region_summary["region"], y=region_summary["total_revenue"], name="Region Summary"),
        row=2, col=1
    )
    ex_fig5.update_layout(height=600, title_text="Sales Dashboard")
    ex_fig5.show()
    # Uncomment when ready:
    # ex_fig5.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎉 Excellent Work!

    You've completed the plotting exercises!

    **What you practiced:**

    - ✅ Bar charts
    - ✅ Line charts
    - ✅ Scatter plots
    - ✅ Histograms
    - ✅ Advanced: Subplots
    - ✅ Multiple chart types (bar, line, scatter, histogram)
    - ✅ Combining data analysis with visualization

    **What's next?**

    - Try creating your own visualizations with the data!

    **Pro Tips:**

    - Plotly charts are interactive - hover, zoom, pan!
    - Always explore your data before plotting
    """)
    return


if __name__ == "__main__":
    app.run()
