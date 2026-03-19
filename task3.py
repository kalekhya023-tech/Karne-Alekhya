import pandas as pd
import matplotlib.pyplot as plt
import os

# ── Load CSV ──────────────────────────────────────────────────────────────────
csv_file = input("Enter CSV file path (or press Enter to use sample data): ").strip()

if not csv_file or not os.path.exists(csv_file):
    print("\nUsing built-in sample sales dataset...\n")
    from io import StringIO
    sample = """OrderID,CustomerName,Category,Product,Quantity,Price,Date,Region
1001,Alice,Electronics,Laptop,1,75000,2024-01-05,South
1002,Bob,Clothing,T-Shirt,3,499,2024-01-07,North
1003,Charlie,Electronics,Phone,2,25000,2024-01-10,East
1004,Alice,Food,Biscuits,10,50,2024-01-12,South
1005,David,Electronics,Laptop,1,75000,2024-02-01,West
1006,Eve,Clothing,Jeans,2,1200,2024-02-03,North
1007,Frank,Food,Juice,5,80,2024-02-05,East
1008,,Electronics,Phone,1,25000,2024-02-08,West
1009,Grace,Clothing,T-Shirt,4,499,2024-03-01,South
1010,Bob,Food,Biscuits,,50,2024-03-05,North
1011,Charlie,Electronics,Laptop,2,75000,2024-03-10,East
1012,Alice,Food,Juice,3,80,2024-03-12,South
1013,David,Clothing,Jeans,1,1200,2024-03-15,West
1014,Eve,Electronics,Phone,2,25000,2024-04-01,North
1015,Frank,Food,Biscuits,8,50,2024-04-05,East
"""
    df = pd.read_csv(StringIO(sample))
else:
    df = pd.read_csv(csv_file)

print("=" * 55)
print("        DATA ANALYSIS REPORT")
print("=" * 55)

# ── Raw Info ──────────────────────────────────────────────────────────────────
print(f"\n[1] Dataset Shape   : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"    Columns         : {list(df.columns)}")

print("\n[2] First 5 Rows:")
print(df.head().to_string(index=False))

# ── Cleaning ──────────────────────────────────────────────────────────────────
print("\n[3] Missing Values Before Cleaning:")
print(df.isnull().sum().to_string())

df.dropna(subset=["CustomerName"], inplace=True)
df["Quantity"].fillna(df["Quantity"].median(), inplace=True)
df.drop_duplicates(inplace=True)

print("\n    Missing Values After Cleaning:")
print(df.isnull().sum().to_string())

# ── Type Conversion ───────────────────────────────────────────────────────────
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.month_name()

if "Price" in df.columns and "Quantity" in df.columns:
    df["TotalSale"] = df["Quantity"] * df["Price"]

# ── Summary Statistics ────────────────────────────────────────────────────────
print("\n[4] Summary Statistics:")
print(df.describe(include="all").to_string())

# ── Filtering ─────────────────────────────────────────────────────────────────
if "TotalSale" in df.columns:
    high_value = df[df["TotalSale"] > 10000]
    print(f"\n[5] High-Value Orders (TotalSale > 10,000): {len(high_value)} orders")
    print(high_value[["CustomerName", "Product", "Quantity", "Price", "TotalSale"]].to_string(index=False))

# ── Grouping & Insights ───────────────────────────────────────────────────────
if "Category" in df.columns and "TotalSale" in df.columns:
    print("\n[6] Total Sales by Category:")
    cat_group = df.groupby("Category")["TotalSale"].sum().sort_values(ascending=False)
    print(cat_group.to_string())

if "Region" in df.columns and "TotalSale" in df.columns:
    print("\n[7] Total Sales by Region:")
    reg_group = df.groupby("Region")["TotalSale"].sum().sort_values(ascending=False)
    print(reg_group.to_string())

if "CustomerName" in df.columns and "TotalSale" in df.columns:
    print("\n[8] Top 5 Customers by Spending:")
    top_customers = df.groupby("CustomerName")["TotalSale"].sum().sort_values(ascending=False).head(5)
    print(top_customers.to_string())

if "Month" in df.columns and "TotalSale" in df.columns:
    print("\n[9] Monthly Sales Summary:")
    monthly = df.groupby("Month")["TotalSale"].sum()
    print(monthly.to_string())

# ── Graphs ────────────────────────────────────────────────────────────────────
try:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Sales Data Analysis", fontsize=16, fontweight="bold")

    if "Category" in df.columns and "TotalSale" in df.columns:
        cat_group.plot(kind="bar", ax=axes[0, 0], color="steelblue", edgecolor="black")
        axes[0, 0].set_title("Sales by Category")
        axes[0, 0].set_xlabel("Category")
        axes[0, 0].set_ylabel("Total Sales (₹)")
        axes[0, 0].tick_params(axis="x", rotation=0)

    if "Region" in df.columns and "TotalSale" in df.columns:
        reg_group.plot(kind="pie", ax=axes[0, 1], autopct="%1.1f%%", startangle=140)
        axes[0, 1].set_title("Sales by Region")
        axes[0, 1].set_ylabel("")

    if "CustomerName" in df.columns and "TotalSale" in df.columns:
        top_customers.plot(kind="barh", ax=axes[1, 0], color="coral", edgecolor="black")
        axes[1, 0].set_title("Top 5 Customers")
        axes[1, 0].set_xlabel("Total Sales (₹)")

    if "Month" in df.columns and "TotalSale" in df.columns:
        month_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        monthly_sorted = monthly.reindex([m for m in month_order if m in monthly.index])
        monthly_sorted.plot(kind="line", ax=axes[1, 1], marker="o", color="green", linewidth=2)
        axes[1, 1].set_title("Monthly Sales Trend")
        axes[1, 1].set_ylabel("Total Sales (₹)")
        axes[1, 1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig("sales_analysis_graph.png", dpi=150)
    print("\n[10] Graph saved as: sales_analysis_graph.png")
    plt.show()

except Exception as e:
    print(f"\nGraph generation skipped: {e}")

print("\n" + "=" * 55)
print("       ANALYSIS COMPLETE")
print("=" * 55)
