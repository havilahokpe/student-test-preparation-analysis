import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# Load the dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

# Research question:
# Is more weekly study time associated with higher final math grades?

# Display basic information
print("Student Test Preparation Statistical Analysis")
print("=" * 50)

print(f"Number of students: {len(df)}")
print(f"Average final grade: {df['G3'].mean():.2f}")
print(f"Median final grade: {df['G3'].median():.2f}")
print(f"Standard deviation: {df['G3'].std():.2f}")

# Convert study-time codes into readable labels
studytime_labels = {
    1: "<2 hours",
    2: "2–5 hours",
    3: "5–10 hours",
    4: ">10 hours"
}

df["studytime_label"] = df["studytime"].map(studytime_labels)

# Calculate final grade statistics by study time
studytime_summary = (
    df.groupby("studytime")["G3"]
    .agg(["count", "mean", "median", "std"])
    .reset_index()
)

studytime_summary["studytime_label"] = (
    studytime_summary["studytime"].map(studytime_labels)
)

print("\nFinal Grade by Weekly Study Time")
print("=" * 50)
print(studytime_summary)

# Calculate Spearman correlation
rho, p_value = spearmanr(df["studytime"], df["G3"])

print("\nStatistical Test")
print("=" * 50)
print(f"Spearman correlation: {rho:.3f}")
print(f"p-value: {p_value:.4f}")

# Interpret the result
if p_value < 0.05:
    print("Result: There is a statistically significant association.")
else:
    print("Result: There is not a statistically significant association.")

# -----------------------------
# Visualization 1: Grade by Study Time
# -----------------------------

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="studytime_label",
    y="G3",
    order=["<2 hours", "2–5 hours", "5–10 hours", ">10 hours"]
)

plt.title("Final Math Grade by Weekly Study Time")
plt.xlabel("Weekly Study Time")
plt.ylabel("Final Grade (G3)")

plt.tight_layout()
plt.savefig("grade_by_studytime.png", dpi=300)
plt.show()

# -----------------------------
# Visualization 2: Study Time vs Final Grade
# -----------------------------

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="studytime",
    y="G3",
    alpha=0.6
)

sns.regplot(
    data=df,
    x="studytime",
    y="G3",
    scatter=False
)

plt.title("Study Time vs Final Math Grade")
plt.xlabel("Study Time Group (1–4)")
plt.ylabel("Final Grade (G3)")

plt.tight_layout()
plt.savefig("studytime_vs_grade.png", dpi=300)
plt.show()

print("\nAnalysis complete!")