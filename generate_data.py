import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

# ============================================================
# E-COMMERCE FUNNEL DATASET GENERATOR
# 500,000 SYNTHETIC SESSIONS
# ============================================================

np.random.seed(42)
fake = Faker()
Faker.seed(42)

# ------------------------------------------------------------
# PROJECT SETTINGS
# ------------------------------------------------------------

N_SESSIONS = 500_000
N_USERS = 150_000

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# BASIC CATEGORIES / CHANNELS / DEVICES
# ------------------------------------------------------------

categories = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Grocery"
]

channels = [
    "Organic Search",
    "Paid Search",
    "Social Media",
    "Email",
    "Direct",
    "Referral"
]

devices = [
    "Mobile",
    "Desktop",
    "Tablet"
]

# ------------------------------------------------------------
# 1. USERS TABLE
# ------------------------------------------------------------

print("Generating users...")

user_ids = np.arange(1, N_USERS + 1)

users = pd.DataFrame({
    "user_id": user_ids,
    "age": np.random.randint(18, 61, N_USERS),
    "gender": np.random.choice(
        ["Male", "Female", "Other"],
        N_USERS,
        p=[0.55, 0.43, 0.02]
    ),
    "city": np.random.choice(
        [
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Kolkata",
            "Ahmedabad",
            "Jaipur",
            "Lucknow"
        ],
        N_USERS
    )
})

# ------------------------------------------------------------
# 2. SESSIONS TABLE
# ------------------------------------------------------------

print("Generating sessions...")

session_ids = np.arange(1, N_SESSIONS + 1)

session_user_ids = np.random.randint(
    1,
    N_USERS + 1,
    N_SESSIONS
)

session_device = np.random.choice(
    devices,
    N_SESSIONS,
    p=[0.65, 0.30, 0.05]
)

session_channel = np.random.choice(
    channels,
    N_SESSIONS,
    p=[0.25, 0.20, 0.15, 0.10, 0.20, 0.10]
)

session_category = np.random.choice(
    categories,
    N_SESSIONS
)

# Dates over approximately 6 months
dates = pd.date_range(
    start="2025-01-01",
    end="2025-06-30",
    freq="min"
)

session_dates = np.random.choice(
    dates,
    N_SESSIONS
)

session_dates = pd.to_datetime(session_dates)

sessions = pd.DataFrame({
    "session_id": session_ids,
    "user_id": session_user_ids,
    "session_date": session_dates.date,
    "device": session_device,
    "channel": session_channel,
    "category": session_category
})

# Add hour separately
sessions["hour"] = np.random.randint(0, 24, N_SESSIONS)

# ------------------------------------------------------------
# 3. FUNNEL EVENTS
# ------------------------------------------------------------

print("Generating funnel events...")

# Base probabilities
# These are designed to create a realistic e-commerce funnel.

page_view = np.ones(N_SESSIONS, dtype=int)

# PDP visit
pdp_prob = np.where(
    sessions["device"].values == "Mobile",
    0.82,
    0.84
)

pdp_view = (
    np.random.random(N_SESSIONS) < pdp_prob
).astype(int)

# Add to Cart
atc_prob = np.where(
    sessions["device"].values == "Mobile",
    0.3425,
    0.3432
)

add_to_cart = (
    (pdp_view == 1) &
    (np.random.random(N_SESSIONS) < atc_prob)
).astype(int)

# Checkout
checkout_prob = np.where(
    sessions["device"].values == "Mobile",
    0.487,
    0.571
)

checkout_start = (
    (add_to_cart == 1) &
    (np.random.random(N_SESSIONS) < checkout_prob)
).astype(int)

# Payment initiated
payment_prob = np.where(
    sessions["device"].values == "Mobile",
    0.72,
    0.78
)

payment_initiated = (
    (checkout_start == 1) &
    (np.random.random(N_SESSIONS) < payment_prob)
).astype(int)

# Order placed
order_prob = np.where(
    sessions["device"].values == "Mobile",
    0.78,
    0.84
)

order_placed = (
    (payment_initiated == 1) &
    (np.random.random(N_SESSIONS) < order_prob)
).astype(int)

# ------------------------------------------------------------
# CREATE EVENTS TABLE
# ------------------------------------------------------------

event_rows = []

event_map = [
    ("page_view", page_view),
    ("pdp_view", pdp_view),
    ("add_to_cart", add_to_cart),
    ("checkout_start", checkout_start),
    ("payment_initiated", payment_initiated),
    ("order_placed", order_placed)
]

for event_name, flags in event_map:

    indexes = np.where(flags == 1)[0]

    temp = pd.DataFrame({
        "session_id": sessions.iloc[indexes]["session_id"].values,
        "event_name": event_name,
        "event_time": pd.to_datetime(
            sessions.iloc[indexes]["session_date"].astype(str)
        )
    })

    # Add random hour/minute/second
    temp["event_time"] = (
        temp["event_time"]
        + pd.to_timedelta(
            sessions.iloc[indexes]["hour"].values,
            unit="h"
        )
        + pd.to_timedelta(
            np.random.randint(0, 60, len(indexes)),
            unit="m"
        )
        + pd.to_timedelta(
            np.random.randint(0, 60, len(indexes)),
            unit="s"
        )
    )

    event_rows.append(temp)

events = pd.concat(
    event_rows,
    ignore_index=True
)

# ------------------------------------------------------------
# 4. ORDERS TABLE
# ------------------------------------------------------------

print("Generating orders...")

order_sessions = sessions.loc[
    order_placed == 1,
    ["session_id", "user_id", "category"]
].copy()

order_count = len(order_sessions)

orders = order_sessions.copy()

orders["order_id"] = np.arange(
    1,
    order_count + 1
)

# Generate realistic order value
orders["order_value"] = np.round(
    np.random.lognormal(
        mean=np.log(2379),
        sigma=0.45,
        size=order_count
    ),
    2
)

orders["order_date"] = sessions.loc[
    order_placed == 1,
    "session_date"
].values

orders = orders[
    [
        "order_id",
        "session_id",
        "user_id",
        "order_date",
        "category",
        "order_value"
    ]
]

# ------------------------------------------------------------
# SAVE CSV FILES
# ------------------------------------------------------------

print("Saving files...")

users.to_csv(
    OUTPUT_DIR / "users.csv",
    index=False
)

sessions.to_csv(
    OUTPUT_DIR / "sessions.csv",
    index=False
)

events.to_csv(
    OUTPUT_DIR / "events.csv",
    index=False
)

orders.to_csv(
    OUTPUT_DIR / "orders.csv",
    index=False
)

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n==========================================")
print("DATASET GENERATION COMPLETE")
print("==========================================")

print(f"Users       : {len(users):,}")
print(f"Sessions    : {len(sessions):,}")
print(f"Events      : {len(events):,}")
print(f"Orders      : {len(orders):,}")

print("\nFiles created inside data/:")
print("users.csv")
print("sessions.csv")
print("events.csv")
print("orders.csv")

print("\n==========================================")