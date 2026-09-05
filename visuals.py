import pandas as pd
import matplotlib.pyplot as plt


# LOAD DATA
df = pd.read_csv("data/opportunity_signals.csv")


# ==============================
# 1. OPPORTUNITY DISTRIBUTION
# ==============================

opportunity_counts = df["label"].value_counts()

plt.figure(figsize=(7, 5))

plt.bar(
    ["Low Priority / Noise", "Potential Opportunity"],
    [
        opportunity_counts.get(0, 0),
        opportunity_counts.get(1, 0)
    ]
)

plt.title("Opportunity Signal Distribution")
plt.xlabel("Signal Classification")
plt.ylabel("Number of Signals")

plt.tight_layout()
plt.savefig("opportunity_distribution.png", dpi=300)
plt.close()


# ==============================
# 2. STATE-WISE OPPORTUNITIES
# ==============================

state_opportunities = (
    df[df["label"] == 1]
    .groupby("state")
    .size()
    .sort_values(ascending=False)
)

plt.figure(figsize=(7, 5))

plt.bar(
    state_opportunities.index,
    state_opportunities.values
)

plt.title("Potential Opportunities by State")
plt.xlabel("State")
plt.ylabel("Number of Potential Opportunities")

plt.tight_layout()
plt.savefig("state_opportunities.png", dpi=300)
plt.close()


# ==============================
# 3. SIGNAL TYPE ANALYSIS
# ==============================

signal_analysis = (
    df.groupby("signal_type")["label"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

plt.bar(
    signal_analysis.index,
    signal_analysis.values * 100
)

plt.title("Opportunity Rate by Signal Type")
plt.xlabel("Signal Type")
plt.ylabel("Opportunity Rate (%)")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig("signal_type_analysis.png", dpi=300)
plt.close()


print("Visualizations created successfully!")

print("\nGenerated files:")
print("opportunity_distribution.png")
print("state_opportunities.png")
print("signal_type_analysis.png")