import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from getpass import getpass
from urllib.parse import quote_plus

# =============================
# MYSQL CONNECTION
# =============================

password = getpass("Enter MySQL root password: ")
encoded_password = quote_plus(password)

engine = create_engine(
    f"mysql+mysqlconnector://root:{encoded_password}@localhost/ecommerce_analytics"
)

print("\nMySQL connection successful!\n")


# =============================
# SESSION DURATION ANALYSIS
# =============================

query = """
SELECT
    s.session_id,
    TIMESTAMPDIFF(
        SECOND,
        MIN(e.event_time),
        MAX(e.event_time)
    ) AS session_duration_seconds,
    CASE
        WHEN o.order_id IS NOT NULL THEN 'Converted'
        ELSE 'Not Converted'
    END AS conversion_status
FROM sessions s
JOIN events e
    ON s.session_id = e.session_id
LEFT JOIN orders o
    ON s.session_id = o.session_id
GROUP BY
    s.session_id,
    o.order_id
"""

df = pd.read_sql(query, engine)


# =============================
# SUMMARY
# =============================

print("Session Duration Analysis:\n")

summary = (
    df.groupby("conversion_status")["session_duration_seconds"]
    .agg(["count", "mean", "median", "min", "max"])
    .reset_index()
)

summary.columns = [
    "Conversion Status",
    "Sessions",
    "Average Duration (sec)",
    "Median Duration (sec)",
    "Minimum Duration (sec)",
    "Maximum Duration (sec)"
]

summary["Average Duration (min)"] = (
    summary["Average Duration (sec)"] / 60
).round(2)

summary["Median Duration (min)"] = (
    summary["Median Duration (sec)"] / 60
).round(2)

print(summary.to_string(index=False))


# =============================
# CHART
# =============================

plt.figure(figsize=(8, 5))

plt.bar(
    summary["Conversion Status"],
    summary["Average Duration (min)"]
)

plt.title("Average Session Duration: Converted vs Not Converted")
plt.xlabel("Conversion Status")
plt.ylabel("Average Session Duration (Minutes)")

for i, value in enumerate(summary["Average Duration (min)"]):
    plt.text(
        i,
        value,
        f"{value:.1f} min",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "outputs/session_duration_conversion.png",
    dpi=300
)

plt.show()

print("\nChart saved successfully:")
print("outputs/session_duration_conversion.png")

print("\nMySQL connection closed.")
