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
# CORRELATION ANALYSIS
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
        WHEN EXISTS (
            SELECT 1
            FROM orders o
            WHERE o.session_id = s.session_id
        )
        THEN 1
        ELSE 0
    END AS converted

FROM sessions s

JOIN events e
    ON s.session_id = e.session_id

GROUP BY
    s.session_id
"""

df = pd.read_sql(query, engine)


# =============================
# CORRELATION
# =============================

correlation = df[
    ["session_duration_seconds", "converted"]
].corr().loc[
    "session_duration_seconds",
    "converted"
]

print("Correlation Analysis:\n")

print(
    f"Session Duration vs Conversion Correlation: "
    f"{correlation:.4f}"
)


# =============================
# SUMMARY
# =============================

converted_avg = df.loc[
    df["converted"] == 1,
    "session_duration_seconds"
].mean()

not_converted_avg = df.loc[
    df["converted"] == 0,
    "session_duration_seconds"
].mean()

print("\nAverage Session Duration:")

print(
    f"Converted Sessions: "
    f"{converted_avg / 60:.2f} minutes"
)

print(
    f"Not Converted Sessions: "
    f"{not_converted_avg / 60:.2f} minutes"
)


# =============================
# CORRELATION INTERPRETATION
# =============================

print("\nCorrelation Interpretation:")

if correlation > 0:
    print(
        "Positive association: longer sessions are associated "
        "with a higher likelihood of conversion."
    )
elif correlation < 0:
    print(
        "Negative association: longer sessions are associated "
        "with a lower likelihood of conversion."
    )
else:
    print(
        "No linear association detected between session duration "
        "and conversion."
    )

print(
    "\nNote: Correlation indicates association, "
    "not causation."
)


# =============================
# CHART
# =============================

plt.figure(figsize=(8, 5))

plt.boxplot(
    [
        df.loc[
            df["converted"] == 0,
            "session_duration_seconds"
        ] / 60,

        df.loc[
            df["converted"] == 1,
            "session_duration_seconds"
        ] / 60
    ],
    tick_labels=["Not Converted", "Converted"]
)

plt.title(
    "Session Duration Distribution by Conversion Status"
)

plt.xlabel("Conversion Status")
plt.ylabel("Session Duration (Minutes)")

plt.tight_layout()

plt.savefig(
    "outputs/session_duration_correlation.png",
    dpi=300
)

plt.show()

print("\nChart saved successfully:")
print("outputs/session_duration_correlation.png")

print("\nMySQL connection closed.")
