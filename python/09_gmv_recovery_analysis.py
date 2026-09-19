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
# 2. GET CART & REVENUE DATA
# ==========================================

cart_query = """
SELECT
    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN e.session_id
    END) AS abandoned_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN e.session_id
    END) AS checkout_sessions

FROM events e;
"""

revenue_query = """
SELECT
    COUNT(*) AS total_orders,
    SUM(order_value) AS total_gmv,
    AVG(order_value) AS average_order_value
FROM orders;
"""

cart_df = pd.read_sql(cart_query, engine)
revenue_df = pd.read_sql(revenue_query, engine)


# ==========================================
# 3. CALCULATE ABANDONED CARTS
# ==========================================

add_to_cart_sessions = int(
    cart_df["abandoned_cart_sessions"].iloc[0]
)

checkout_sessions = int(
    cart_df["checkout_sessions"].iloc[0]
)

abandoned_carts = (
    add_to_cart_sessions - checkout_sessions
)

total_orders = int(
    revenue_df["total_orders"].iloc[0]
)

total_gmv = float(
    revenue_df["total_gmv"].iloc[0]
)

aov = float(
    revenue_df["average_order_value"].iloc[0]
)


# ==========================================
# 4. RECOVERY SCENARIOS
# ==========================================

recovery_rates = [0, 5, 10, 15, 20]

results = []

for rate in recovery_rates:

    recovered_carts = round(
        abandoned_carts * rate / 100
    )

    potential_gmv = (
        recovered_carts * aov
    )

    results.append({
        "Recovery Rate (%)": rate,
        "Recovered Carts": recovered_carts,
        "Potential GMV": potential_gmv,
        "Potential GMV (Cr)": potential_gmv / 10000000
    })


df = pd.DataFrame(results)


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("GMV Recovery Scenario Analysis:\n")

print(
    df.to_string(index=False)
)


# ==========================================
# 6. BUSINESS SUMMARY
# ==========================================

recovery_10 = df.loc[
    df["Recovery Rate (%)"] == 10,
    "Potential GMV (Cr)"
].iloc[0]

recovery_20 = df.loc[
    df["Recovery Rate (%)"] == 20,
    "Potential GMV (Cr)"
].iloc[0]


print("\nGMV Recovery Summary:")

print(
    f"Total GMV: ₹{total_gmv:,.2f}"
)

print(
    f"Average Order Value: ₹{aov:,.2f}"
)

print(
    f"Abandoned Cart Sessions: {abandoned_carts:,}"
)

print(
    f"10% Recovery Potential: ₹{recovery_10:.2f} Cr"
)

print(
    f"20% Recovery Potential: ₹{recovery_20:.2f} Cr"
)


# ==========================================
# 7. CREATE RECOVERY CHART
# ==========================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    df["Recovery Rate (%)"].astype(str) + "%",
    df["Potential GMV (Cr)"]
)

plt.title(
    "Potential GMV Recovery from Abandoned Carts",
    fontsize=16
)

plt.xlabel("Cart Recovery Rate")

plt.ylabel("Potential GMV (₹ Crore)")


# Add values on bars

for bar, value in zip(
    bars,
    df["Potential GMV (Cr)"]
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.03,
        f"₹{value:.2f} Cr",
        ha="center",
        va="bottom"
    )


plt.tight_layout()


# ==========================================
# 8. SAVE CHART
# ==========================================

plt.savefig(
    "outputs/gmv_recovery_scenarios.png",
    dpi=300,
    bbox_inches="tight"
)

print(
    "\nChart saved successfully:"
    "\noutputs/gmv_recovery_scenarios.png"
)

plt.show()


# ==========================================
# 9. CLOSE CONNECTION
# ==========================================

engine.dispose()

print("\nMySQL connection closed.")