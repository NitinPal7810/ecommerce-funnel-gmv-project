import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CATEGORY-WISE REVENUE DATA
# ============================================================

data = {
    "Category": [
        "Electronics",
        "Fashion",
        "Beauty",
        "Sports",
        "Grocery",
        "Home & Kitchen"
    ],

    "Orders": [
        7430,
        7349,
        7313,
        7279,
        7121,
        7145
    ],

    "Total GMV": [
        19664443.36,
        19403147.94,
        19354731.42,
        19112469.04,
        18847191.47,
        18831386.55
    ],

    "AOV": [
        2646.63,
        2640.24,
        2646.62,
        2625.70,
        2646.71,
        2635.60
    ]
}


df = pd.DataFrame(data)


# ============================================================
# GMV IN CRORES
# ============================================================

df["GMV Crore"] = df["Total GMV"] / 10000000

df["GMV Crore"] = df["GMV Crore"].round(2)


# ============================================================
# DISPLAY DATA
# ============================================================

print("\nCategory-wise Revenue Analysis:\n")

print(
    df[
        [
            "Category",
            "Orders",
            "Total GMV",
            "AOV",
            "GMV Crore"
        ]
    ].to_string(index=False)
)


# ============================================================
# CATEGORY-WISE GMV BAR CHART
# ============================================================

plt.figure(figsize=(12, 7))

plt.bar(
    df["Category"],
    df["GMV Crore"]
)

plt.xlabel("Product Category")

plt.ylabel("GMV (₹ Crore)")

plt.title(
    "Category-wise GMV Comparison"
)

plt.xticks(
    rotation=20,
    ha="right"
)


# ============================================================
# ADD GMV VALUES ABOVE BARS
# ============================================================

for i, value in enumerate(df["GMV Crore"]):

    plt.text(
        i,
        value + 0.01,
        f"₹{value:.2f} Cr",
        ha="center"
    )


plt.tight_layout()


# ============================================================
# SAVE CHART
# ============================================================

plt.savefig(
    "outputs/category_gmv_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nChart saved successfully:")

print(
    "outputs/category_gmv_comparison.png"
)


# ============================================================
# GMV SUMMARY
# ============================================================

highest_gmv = df.loc[
    df["Total GMV"].idxmax()
]

lowest_gmv = df.loc[
    df["Total GMV"].idxmin()
]


print("\nCategory Revenue Summary:")

print(
    f"Highest GMV Category: "
    f"{highest_gmv['Category']} "
    f"(₹{highest_gmv['GMV Crore']:.2f} Cr)"
)

print(
    f"Lowest GMV Category: "
    f"{lowest_gmv['Category']} "
    f"(₹{lowest_gmv['GMV Crore']:.2f} Cr)"
)