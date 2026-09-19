import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass
from urllib.parse import quote_plus


# ============================================================
# MYSQL CONNECTION
# ============================================================

password = getpass("Enter MySQL root password: ")

encoded_password = quote_plus(password)

engine = create_engine(
    f"mysql+mysqlconnector://root:{encoded_password}@localhost/ecommerce_analytics"
)

print("\nMySQL connection successful!")


# ============================================================
# CHANNEL-WISE REVENUE ANALYSIS
# ============================================================

query = """
SELECT
    s.channel,

    COUNT(DISTINCT o.order_id) AS orders,

    SUM(o.order_value) AS total_gmv,

    AVG(o.order_value) AS average_order_value

FROM orders o

JOIN sessions s
    ON o.session_id = s.session_id

GROUP BY s.channel

ORDER BY total_gmv DESC;
"""


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_sql(query, engine)


# ============================================================
# GMV IN CRORES
# ============================================================

df["gmv_crore"] = df["total_gmv"] / 10000000


# ============================================================
# GMV SHARE
# ============================================================

total_gmv = df["total_gmv"].sum()

df["gmv_share"] = (
    df["total_gmv"] / total_gmv * 100
)


# ============================================================
# ROUND VALUES
# ============================================================

df["total_gmv"] = df["total_gmv"].round(2)

df["average_order_value"] = (
    df["average_order_value"].round(2)
)

df["gmv_crore"] = (
    df["gmv_crore"].round(2)
)

df["gmv_share"] = (
    df["gmv_share"].round(2)
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nChannel-wise GMV & AOV Analysis:\n")

print(
    df.to_string(index=False)
)


# ============================================================
# CHANNEL REVENUE SUMMARY
# ============================================================

highest_gmv = df.loc[
    df["total_gmv"].idxmax()
]

highest_aov = df.loc[
    df["average_order_value"].idxmax()
]


print("\nChannel Revenue Summary:")

print(
    f"Highest GMV Channel: {highest_gmv['channel']} "
    f"(₹{highest_gmv['gmv_crore']:.2f} Cr)"
)

print(
    f"Highest AOV Channel: {highest_aov['channel']} "
    f"(₹{highest_aov['average_order_value']:.2f})"
)


# ============================================================
# CLOSE CONNECTION
# ============================================================

engine.dispose()

print("\nMySQL connection closed.")