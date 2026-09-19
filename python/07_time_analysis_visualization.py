import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from getpass import getpass
from urllib.parse import quote_plus

# ==========================================
# 1. MySQL CONNECTION
# ==========================================

password = getpass("Enter MySQL root password: ")

encoded_password = quote_plus(password)

engine = create_engine(
    f"mysql+mysqlconnector://root:{encoded_password}@localhost/ecommerce_analytics"
)

print("\nMySQL connection successful!\n")


# ==========================================
# 2. HOURLY CONVERSION ANALYSIS
# ==========================================

query = """
SELECT
    s.hour,
    COUNT(DISTINCT s.session_id) AS sessions,
    COUNT(DISTINCT o.order_id) AS orders
FROM sessions s
LEFT JOIN orders o
    ON s.session_id = o.session_id
GROUP BY s.hour
ORDER BY s.hour;
"""

df = pd.read_sql(query, engine)


# ==========================================
# 3. CALCULATE CONVERSION RATE
# ==========================================

df["conversion_rate"] = (
    df["orders"] / df["sessions"] * 100
)

df["conversion_rate"] = df["conversion_rate"].round(2)


print("Hourly Conversion Analysis:\n")

print(
    df[
        ["hour", "sessions", "orders", "conversion_rate"]
    ].to_string(index=False)
)


# ==========================================
# 4. FIND HIGHEST & LOWEST CONVERSION HOUR
# ==========================================

highest = df.loc[df["conversion_rate"].idxmax()]

lowest = df.loc[df["conversion_rate"].idxmin()]


print("\nTime-of-Day Summary:")

print(
    f"Highest Conversion Hour: "
    f"{int(highest['hour']):02d}:00 "
    f"({highest['conversion_rate']:.2f}%)"
)

print(
    f"Lowest Conversion Hour: "
    f"{int(lowest['hour']):02d}:00 "
    f"({lowest['conversion_rate']:.2f}%)"
)


# ==========================================
# 5. CREATE HOURLY CONVERSION CHART
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["hour"],
    df["conversion_rate"],
    marker="o",
    linewidth=2
)

plt.title(
    "Hourly E-commerce Conversion Rate",
    fontsize=16
)

plt.xlabel("Hour of Day")
plt.ylabel("Conversion Rate (%)")

plt.xticks(range(24))

plt.grid(
    True,
    linestyle="--",
    alpha=0.5
)

# Highlight highest conversion point
plt.annotate(
    f"{highest['conversion_rate']:.2f}%",
    (
        highest["hour"],
        highest["conversion_rate"]
    ),
    xytext=(0, 12),
    textcoords="offset points",
    ha="center"
)

plt.tight_layout()


# ==========================================
# 6. SAVE CHART
# ==========================================

plt.savefig(
    "outputs/hourly_conversion_rate.png",
    dpi=300,
    bbox_inches="tight"
)

print(
    "\nChart saved successfully:"
    "\noutputs/hourly_conversion_rate.png"
)

plt.show()


# ==========================================
# 7. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nMySQL connection closed.")