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
# DEVICE-WISE GMV ANALYSIS
# ==============================

query = """
SELECT
    s.device,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(AVG(o.order_value), 2) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY
    s.device
ORDER BY
    total_gmv DESC;
"""

df = pd.read_sql(query, engine)

# ==============================
# GMV SHARE CALCULATION
# ==============================

total_gmv = df["total_gmv"].sum()

df["gmv_crore"] = df["total_gmv"] / 10000000
df["gmv_share_pct"] = (df["total_gmv"] / total_gmv) * 100

print("Device-wise GMV Analysis:\n")
print(df.to_string(index=False))

# ==============================
# SUMMARY
# ==============================

print("\nDevice GMV Summary:")

for _, row in df.iterrows():
    print(
        f"{row['device']}: "
        f"₹{row['gmv_crore']:.2f} Cr "
        f"({row['gmv_share_pct']:.2f}% of total GMV)"
    )

# ==============================
# VISUALIZATION
# ==============================

plt.figure(figsize=(9, 6))

bars = plt.bar(
    df["device"],
    df["gmv_share_pct"]
)

plt.title("Device-wise GMV Share")
plt.xlabel("Device")
plt.ylabel("GMV Share (%)")

for bar, value in zip(bars, df["gmv_share_pct"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "outputs/device_gmv_share.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved successfully:")
print("outputs/device_gmv_share.png")

engine.dispose()

print("\nMySQL connection closed.")
