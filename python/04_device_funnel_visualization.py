import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# DEVICE-WISE FUNNEL DATA
# ============================================================

data = {
    "Device": [
        "Mobile",
        "Desktop",
        "Tablet"
    ],

    "Sessions": [
        325083,
        149698,
        25219
    ],

    "PDP Views": [
        266322,
        125954,
        21127
    ],

    "Add to Cart": [
        91195,
        42719,
        7237
    ],

    "Checkout": [
        44438,
        24411,
        4096
    ],

    "Payment": [
        31969,
        19054,
        3225
    ],

    "Orders": [
        24894,
        16034,
        2709
    ]
}


df = pd.DataFrame(data)


# ============================================================
# CONVERSION RATES
# ============================================================

df["Session to PDP %"] = (
    df["PDP Views"] / df["Sessions"] * 100
)

df["PDP to Cart %"] = (
    df["Add to Cart"] / df["PDP Views"] * 100
)

df["Cart to Checkout %"] = (
    df["Checkout"] / df["Add to Cart"] * 100
)

df["Checkout to Payment %"] = (
    df["Payment"] / df["Checkout"] * 100
)

df["Payment to Order %"] = (
    df["Orders"] / df["Payment"] * 100
)

df["Overall CVR %"] = (
    df["Orders"] / df["Sessions"] * 100
)


# ============================================================
# ROUND VALUES
# ============================================================

rate_columns = [
    "Session to PDP %",
    "PDP to Cart %",
    "Cart to Checkout %",
    "Checkout to Payment %",
    "Payment to Order %",
    "Overall CVR %"
]

df[rate_columns] = df[rate_columns].round(2)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nDevice-wise Funnel Analysis:\n")

print(df.to_string(index=False))


# ============================================================
# DEVICE FUNNEL CONVERSION CHART
# ============================================================

stages = [
    "Session to PDP",
    "PDP to Cart",
    "Cart to Checkout",
    "Checkout to Payment",
    "Payment to Order"
]

mobile = [
    df.loc[0, "Session to PDP %"],
    df.loc[0, "PDP to Cart %"],
    df.loc[0, "Cart to Checkout %"],
    df.loc[0, "Checkout to Payment %"],
    df.loc[0, "Payment to Order %"]
]

desktop = [
    df.loc[1, "Session to PDP %"],
    df.loc[1, "PDP to Cart %"],
    df.loc[1, "Cart to Checkout %"],
    df.loc[1, "Checkout to Payment %"],
    df.loc[1, "Payment to Order %"]
]

tablet = [
    df.loc[2, "Session to PDP %"],
    df.loc[2, "PDP to Cart %"],
    df.loc[2, "Cart to Checkout %"],
    df.loc[2, "Checkout to Payment %"],
    df.loc[2, "Payment to Order %"]
]


# ============================================================
# CREATE GROUPED BAR CHART
# ============================================================

x = range(len(stages))
width = 0.25

plt.figure(figsize=(12, 6))

plt.bar(
    [i - width for i in x],
    mobile,
    width=width,
    label="Mobile"
)

plt.bar(
    x,
    desktop,
    width=width,
    label="Desktop"
)

plt.bar(
    [i + width for i in x],
    tablet,
    width=width,
    label="Tablet"
)


plt.xticks(
    list(x),
    stages,
    rotation=20
)

plt.ylabel("Conversion Rate (%)")
plt.xlabel("Funnel Stage")
plt.title("Device-wise E-commerce Funnel Conversion")

plt.legend()

plt.tight_layout()


# ============================================================
# SAVE CHART
# ============================================================

plt.savefig(
    "outputs/device_funnel_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nChart saved successfully:")
print("outputs/device_funnel_comparison.png")


# ============================================================
# MOBILE vs DESKTOP CHECKOUT GAP
# ============================================================

mobile_checkout = df.loc[
    df["Device"] == "Mobile",
    "Cart to Checkout %"
].iloc[0]

desktop_checkout = df.loc[
    df["Device"] == "Desktop",
    "Cart to Checkout %"
].iloc[0]

gap = desktop_checkout - mobile_checkout


print("\nMobile vs Desktop Checkout Analysis:")

print(f"Mobile Cart → Checkout: {mobile_checkout:.2f}%")

print(f"Desktop Cart → Checkout: {desktop_checkout:.2f}%")

print(f"Desktop-Mobile Gap: {gap:.2f} percentage points")