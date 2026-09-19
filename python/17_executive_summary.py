import pandas as pd
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
# FUNNEL ANALYSIS
# ==============================

funnel_query = """
SELECT
    COUNT(DISTINCT s.session_id) AS total_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'pdp_view'
        THEN e.session_id
    END) AS pdp_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN e.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN e.session_id
    END) AS checkout_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'payment_initiated'
        THEN e.session_id
    END) AS payment_sessions

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id;
"""

funnel = pd.read_sql(funnel_query, engine).iloc[0]

total_sessions = int(funnel["total_sessions"])
pdp_sessions = int(funnel["pdp_sessions"])
add_to_cart = int(funnel["add_to_cart_sessions"])
checkout_sessions = int(funnel["checkout_sessions"])
payment_sessions = int(funnel["payment_sessions"])

# ==============================
# ORDERS & GMV
# ==============================

revenue_query = """
SELECT
    COUNT(order_id) AS total_orders,
    SUM(order_value) AS total_gmv,
    AVG(order_value) AS average_order_value
FROM orders;
"""

revenue = pd.read_sql(revenue_query, engine).iloc[0]

total_orders = int(revenue["total_orders"])
total_gmv = float(revenue["total_gmv"])
average_order_value = float(revenue["average_order_value"])

# ==============================
# CART ABANDONMENT
# ==============================

abandonment_query = """
SELECT
    COUNT(DISTINCT CASE
        WHEN event_name = 'add_to_cart'
        THEN session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN event_name = 'checkout_start'
        THEN session_id
    END) AS checkout_sessions
FROM events;
"""

abandonment = pd.read_sql(abandonment_query, engine).iloc[0]

abandoned_cart_sessions = (
    int(abandonment["add_to_cart_sessions"])
    - int(abandonment["checkout_sessions"])
)

cart_abandonment_rate = (
    abandoned_cart_sessions
    / int(abandonment["add_to_cart_sessions"])
) * 100

# ==============================
# CONVERSION RATES
# ==============================

session_to_pdp = (pdp_sessions / total_sessions) * 100
pdp_to_cart = (add_to_cart / pdp_sessions) * 100
cart_to_checkout = (checkout_sessions / add_to_cart) * 100
checkout_to_payment = (payment_sessions / checkout_sessions) * 100
payment_to_order = (total_orders / payment_sessions) * 100
overall_conversion = (total_orders / total_sessions) * 100

# ==============================
# GMV RECOVERY
# ==============================

gmv_recovery_10 = abandoned_cart_sessions * 0.10 * average_order_value
gmv_recovery_20 = abandoned_cart_sessions * 0.20 * average_order_value

# ==============================
# DEVICE CHECKOUT GAP
# ==============================

device_query = """
SELECT
    device,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'add_to_cart'
        THEN e.session_id
    END) AS add_to_cart_sessions,

    COUNT(DISTINCT CASE
        WHEN e.event_name = 'checkout_start'
        THEN e.session_id
    END) AS checkout_sessions

FROM sessions s
LEFT JOIN events e
    ON s.session_id = e.session_id

GROUP BY device;
"""

device_df = pd.read_sql(device_query, engine)

device_df["cart_to_checkout_cvr"] = (
    device_df["checkout_sessions"]
    / device_df["add_to_cart_sessions"]
) * 100

desktop_cvr = float(
    device_df.loc[
        device_df["device"] == "Desktop",
        "cart_to_checkout_cvr"
    ].iloc[0]
)

mobile_cvr = float(
    device_df.loc[
        device_df["device"] == "Mobile",
        "cart_to_checkout_cvr"
    ].iloc[0]
)

desktop_mobile_gap = desktop_cvr - mobile_cvr

# ==============================
# EXECUTIVE SUMMARY
# ==============================

print("=" * 60)
print("E-COMMERCE FUNNEL & GMV EXECUTIVE SUMMARY")
print("=" * 60)

print(f"\nTotal Sessions        : {total_sessions:,}")
print(f"PDP Sessions          : {pdp_sessions:,}")
print(f"Add-to-Cart Sessions  : {add_to_cart:,}")
print(f"Checkout Sessions     : {checkout_sessions:,}")
print(f"Payment Sessions      : {payment_sessions:,}")
print(f"Total Orders          : {total_orders:,}")
print(f"Total GMV             : ₹{total_gmv:,.2f}")
print(f"Total GMV             : ₹{total_gmv / 10000000:.2f} Cr")
print(f"Average Order Value   : ₹{average_order_value:,.2f}")

print("\n--- Funnel Conversion Rates ---")

print(f"Session → PDP         : {session_to_pdp:.2f}%")
print(f"PDP → Add-to-Cart     : {pdp_to_cart:.2f}%")
print(f"Cart → Checkout       : {cart_to_checkout:.2f}%")
print(f"Checkout → Payment    : {checkout_to_payment:.2f}%")
print(f"Payment → Order       : {payment_to_order:.2f}%")
print(f"Overall Conversion    : {overall_conversion:.2f}%")

print("\n--- Cart Abandonment ---")

print(f"Abandoned Cart Sessions : {abandoned_cart_sessions:,}")
print(f"Cart Abandonment Rate   : {cart_abandonment_rate:.2f}%")

print("\n--- GMV Recovery Scenarios ---")

print(f"10% Recovery Potential : ₹{gmv_recovery_10 / 10000000:.2f} Cr")
print(f"20% Recovery Potential : ₹{gmv_recovery_20 / 10000000:.2f} Cr")

print("\n--- Mobile vs Desktop Checkout ---")

print(f"Desktop Cart → Checkout : {desktop_cvr:.2f}%")
print(f"Mobile Cart → Checkout  : {mobile_cvr:.2f}%")
print(f"Desktop-Mobile Gap      : {desktop_mobile_gap:.2f} pp")

print("\n" + "=" * 60)
print("Executive summary completed successfully.")
print("=" * 60)

# ==============================
# CLOSE CONNECTION
# ==============================

engine.dispose()

print("\nMySQL connection closed.")
