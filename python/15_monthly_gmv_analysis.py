import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from getpass import getpass
from urllib.parse import quote_plus

# ==============================
# MYSQL CONNECTION
# ==============================

password = getpass("Enter MySQL root password: ")
encoded_password = quote_plus(password)

engine = create_engine(
    f"mysql+mysqlconnector://root:{encoded_password}@localhost/ecommerce_analytics"
)

print("\nMySQL connection successful!\n")

# ==============================
# MONTHLY GMV ANALYSIS
# ==============================

query = """
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(order_id) AS orders,
    SUM(order_value) AS total_gmv,
    AVG(order_value) AS average_order_value
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
"""

df = pd.read_sql(query, engine)

# Convert GMV to Crores
df["gmv_crore"] = df["total_gmv"] / 10000000

# ==============================
# DISPLAY RESULTS
# ==============================

print("Monthly GMV Analysis:\n")

print(
    df[
        [
            "month",
            "orders",
            "total_gmv",
            "average_order_value",
            "gmv_crore"
        ]
    ].to_string(index=False)
)

# ==============================
# SUMMARY
# ==============================

highest_month = df.loc[df["total_gmv"].idxmax()]
lowest_month = df.loc[df["total_gmv"].idxmin()]

print("\nMonthly GMV Summary:")

print(
    f"Highest GMV Month: {highest_month['month']} "
    f"(₹{highest_month['gmv_crore']:.2f} Cr)"
)

print(
    f"Lowest GMV Month: {lowest_month['month']} "
    f"(₹{lowest_month['gmv_crore']:.2f} Cr)"
)

# ==============================
# CHART
# ==============================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    df["month"],
    df["gmv_crore"]
)

plt.title("Monthly GMV Trend")
plt.xlabel("Month")
plt.ylabel("GMV (₹ Crore)")
plt.xticks(rotation=30)

for bar, value in zip(bars, df["gmv_crore"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"₹{value:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "outputs/monthly_gmv.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved successfully:")
print("outputs/monthly_gmv.png")

# ==============================
# CLOSE CONNECTION
# ==============================

engine.dispose()

print("\nMySQL connection closed.")
