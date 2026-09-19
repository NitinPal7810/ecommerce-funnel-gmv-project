import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from getpass import getpass
from urllib.parse import quote_plus

# ==========================================
# 1. MYSQL CONNECTION
# ==========================================

password = getpass("Enter MySQL root password: ")

encoded_password = quote_plus(password)

engine = create_engine(
    f"mysql+mysqlconnector://root:{encoded_password}@localhost/ecommerce_analytics"
)

print("\nMySQL connection successful!\n")


# ==========================================
# 2. CHANNEL-WISE CONVERSION ANALYSIS
# ==========================================

query = """
SELECT
    s.channel,
    COUNT(DISTINCT s.session_id) AS sessions,
    COUNT(DISTINCT o.order_id) AS orders
FROM sessions s
LEFT JOIN orders o
    ON s.session_id = o.session_id
GROUP BY s.channel
ORDER BY sessions DESC;
"""

df = pd.read_sql(query, engine)


# ==========================================
# 3. CALCULATE CONVERSION RATE
# ==========================================

df["conversion_rate"] = (
    df["orders"] / df["sessions"] * 100
)

df["conversion_rate"] = df["conversion_rate"].round(2)


print("Channel-wise Conversion Analysis:\n")

print(
    df[
        ["channel", "sessions", "orders", "conversion_rate"]
    ].to_string(index=False)
)


# ==========================================
# 4. HIGHEST & LOWEST CONVERSION CHANNEL
# ==========================================

highest = df.loc[df["conversion_rate"].idxmax()]

lowest = df.loc[df["conversion_rate"].idxmin()]


print("\nChannel Conversion Summary:")

print(
    f"Highest Conversion Channel: "
    f"{highest['channel']} "
    f"({highest['conversion_rate']:.2f}%)"
)

print(
    f"Lowest Conversion Channel: "
    f"{lowest['channel']} "
    f"({lowest['conversion_rate']:.2f}%)"
)


# ==========================================
# 5. CREATE BAR CHART
# ==========================================

plot_df = df.sort_values(
    "conversion_rate",
    ascending=True
)

plt.figure(figsize=(11, 6))

bars = plt.bar(
    plot_df["channel"],
    plot_df["conversion_rate"]
)

plt.title(
    "Channel-wise E-commerce Conversion Rate",
    fontsize=16
)

plt.xlabel("Marketing Channel")
plt.ylabel("Conversion Rate (%)")

plt.xticks(
    rotation=30,
    ha="right"
)


# Add values on bars
for bar, value in zip(
    bars,
    plot_df["conversion_rate"]
):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{value:.2f}%",
        ha="center",
        va="bottom"
    )


plt.tight_layout()


# ==========================================
# 6. SAVE CHART
# ==========================================

plt.savefig(
    "outputs/channel_conversion_rate.png",
    dpi=300,
    bbox_inches="tight"
)

print(
    "\nChart saved successfully:"
    "\noutputs/channel_conversion_rate.png"
)

plt.show()


# ==========================================
# 7. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nMySQL connection closed.")