import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# OVERALL E-COMMERCE FUNNEL
# ============================================================

funnel_data = {
    "Stage": [
        "Sessions",
        "PDP Views",
        "Add to Cart",
        "Checkout",
        "Payment",
        "Orders"
    ],
    "Users": [
        500000,
        413403,
        141151,
        72945,
        54248,
        43637
    ]
}


# Convert to DataFrame
df = pd.DataFrame(funnel_data)


# ============================================================
# CONVERSION FROM TOTAL SESSIONS
# ============================================================

df["conversion_from_sessions"] = (
    df["Users"] / df.loc[0, "Users"] * 100
)


# ============================================================
# DISPLAY FUNNEL DATA
# ============================================================

print("\nOverall Funnel Data:\n")

print(df.to_string(index=False))


# ============================================================
# CREATE FUNNEL CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.barh(
    df["Stage"],
    df["Users"]
)

plt.xlabel("Number of Sessions / Users")
plt.ylabel("Funnel Stage")
plt.title("E-commerce Overall Conversion Funnel")

plt.gca().invert_yaxis()

plt.tight_layout()


# ============================================================
# SAVE CHART
# ============================================================

plt.savefig(
    "outputs/overall_funnel.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nChart saved successfully:")
print("outputs/overall_funnel.png")