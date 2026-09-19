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
# CATEGORY × DEVICE GMV ANALYSIS
# ==============================

query = """
SELECT
    s.category,
    s.device,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY
    s.category,
    s.device
ORDER BY
    s.category,
    total_gmv DESC;
"""

df = pd.read_sql(query, engine)

# Convert GMV to Crores
df["gmv_crore"] = df["total_gmv"] / 10000000

print("Category × Device GMV Analysis:\n")
print(df.to_string(index=False))

# ==============================
# PIVOT TABLE
# ==============================

pivot = df.pivot(
    index="category",
    columns="device",
    values="gmv_crore"
)

print("\nGMV by Category and Device (₹ Crore):\n")
print(pivot.round(2))

# ==============================
# VISUALIZATION
# ==============================

ax = pivot.plot(
    kind="bar",
    figsize=(12, 7)
)

plt.title("GMV by Product Category and Device")
plt.xlabel("Product Category")
plt.ylabel("GMV (₹ Crore)")
plt.xticks(rotation=30)
plt.legend(title="Device")
plt.tight_layout()

plt.savefig(
    "outputs/category_device_gmv.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved successfully:")
print("outputs/category_device_gmv.png")

engine.dispose()

print("\nMySQL connection closed.")
