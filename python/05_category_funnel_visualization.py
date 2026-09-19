import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CATEGORY-WISE FUNNEL DATA
# ============================================================

data = {
    "Category": [
        "Beauty",
        "Grocery",
        "Sports",
        "Home & Kitchen",
        "Fashion",
        "Electronics"
    ],

    "Sessions": [
        83526,
        83466,
        83375,
        83372,
        83255,
        83006
    ],

    "PDP Views": [
        69237,
        69168,
        68856,
        68813,
        68731,
        68598
    ],

    "Add to Cart": [
        23528,
        23514,
        23458,
        23448,
        23708,
        23495
    ],

    "Checkout": [
        12197,
        11954,
        12110,
        12106,
        12374,
        12204
    ],

    "Payment": [
        9092,
        8895,
        9039,
        8947,
        9125,
        9150
    ],

    "Orders": [
        7313,
        7121,
        7279,
        7145,
        7349,
        7430
    ]
}


df = pd.DataFrame(data)


# ============================================================
# CALCULATE FUNNEL CONVERSION RATES
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
# DISPLAY ANALYSIS
# ============================================================

print("\nCategory-wise Funnel Analysis:\n")

print(df.to_string(index=False))


# ============================================================
# CATEGORY CONVERSION CHART
# ============================================================

plt.figure(figsize=(12, 7))

plt.bar(
    df["Category"],
    df["Overall CVR %"]
)

plt.ylabel("Overall Conversion Rate (%)")
plt.xlabel("Product Category")

plt.title(
    "Category-wise E-commerce Conversion Rate"
)

plt.xticks(
    rotation=20,
    ha="right"
)


# Add values above bars

for i, value in enumerate(df["Overall CVR %"]):

    plt.text(
        i,
        value + 0.05,
        f"{value:.2f}%",
        ha="center"
    )


plt.tight_layout()


# ============================================================
# SAVE CHART
# ============================================================

plt.savefig(
    "outputs/category_conversion_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nChart saved successfully:")
print("outputs/category_conversion_rate.png")


# ============================================================
# HIGHEST / LOWEST CATEGORY
# ============================================================

highest_category = df.loc[
    df["Overall CVR %"].idxmax()
]

lowest_category = df.loc[
    df["Overall CVR %"].idxmin()
]


print("\nCategory Conversion Summary:")

print(
    f"Highest CVR Category: "
    f"{highest_category['Category']} "
    f"({highest_category['Overall CVR %']:.2f}%)"
)

print(
    f"Lowest CVR Category: "
    f"{lowest_category['Category']} "
    f"({lowest_category['Overall CVR %']:.2f}%)"
)