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
# CATEGORY-WISE GMV ANALYSIS
# ==============================

query = """
SELECT
    category,
    COUNT(order_id) AS orders,
    SUM(order_value) AS total_gmv,
    AVG(order_value) AS average_order_value
FROM orders
GROUP BY category
ORDER BY total_gmv DESC;
"""

df = pd.read_sql(query, engine)

# Convert GMV to Crores
df["gmv_crore"] = df["total_gmv"] / 10000000

# Calculate GMV share
total_gmv = df["total_gmv"].sum()
df["gmv_share_pct"] = (df["total_gmv"] / total_gmv) * 100

# ==============================
# DISPLAY RESULTS
# ==============================

print("Category-wise GMV Analysis:\n")

print(
    df[
        [
            "category",
            "orders",
            "total_gmv",
            "average_order_value",
            "gmv_crore",
            "gmv_share_pct"
        ]
    ].to_string(index=False)
)

# ==============================
# SUMMARY
# ==============================

highest_category = df.loc[df["total_gmv"].idxmax()]

print("\nCategory GMV Summary:")
print(
    f"Highest GMV Category: {highest_category['category']} "
    f"(₹{highest_category['gmv_crore']:.2f} Cr, "
    f"{highest_category['gmv_share_pct']:.2f}% of total GMV)"
)

# ==============================
# CHART
# ==============================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    df["category"],
    df["gmv_crore"]
)

plt.title("GMV by Product Category")
plt.xlabel("Product Category")
plt.ylabel("GMV (₹ Crore)")
plt.xticks(rotation=30, ha="right")

for bar, value in zip(bars, df["gmv_crore"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"₹{value:.2f} Cr",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "outputs/category_gmv.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved successfully:")
print("outputs/category_gmv.png")

# ==============================
# CLOSE CONNECTION
# ==============================

engine.dispose()

print("\nMySQL connection closed.")
