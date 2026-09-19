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
# CHANNEL-WISE GMV ANALYSIS
# ==============================

query = """
SELECT
    s.channel,
    COUNT(o.order_id) AS orders,
    SUM(o.order_value) AS total_gmv,
    AVG(o.order_value) AS average_order_value
FROM orders o
JOIN sessions s
    ON o.session_id = s.session_id
GROUP BY s.channel
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

print("Channel-wise GMV Analysis:\n")

print(
    df[
        [
            "channel",
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

highest_channel = df.loc[df["total_gmv"].idxmax()]

print("\nChannel GMV Summary:")
print(
    f"Highest GMV Channel: {highest_channel['channel']} "
    f"(₹{highest_channel['gmv_crore']:.2f} Cr, "
    f"{highest_channel['gmv_share_pct']:.2f}% of total GMV)"
)

# ==============================
# CHART
# ==============================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    df["channel"],
    df["gmv_crore"]
)

plt.title("GMV by Acquisition Channel")
plt.xlabel("Channel")
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
    "outputs/channel_gmv.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved successfully:")
print("outputs/channel_gmv.png")

# ==============================
# CLOSE CONNECTION
# ==============================

engine.dispose()

print("\nMySQL connection closed.")

