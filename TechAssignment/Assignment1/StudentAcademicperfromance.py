import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# STUDENT ACADEMIC PERFORMANCE ANALYSIS
# Fictional data for assignment demonstration.
# All marks are out of 100.
# Subjects represent recurring learning categories, not an actual syllabus.

output = Path("academic_output")
output.mkdir(exist_ok=True)

plt.style.use("ggplot")


def answer(number, question, result):
    print(f"\nQ{number}. {question}")
    print(result)


def save_graph(fig, filename):
    fig.tight_layout()
    fig.savefig(output / filename, dpi=180, bbox_inches="tight")


# Q1. Create your dataset containing marks from Semester 1 to 6.
data = {
    "Semester": [1, 2, 3, 4, 5, 6],
    "Programming": [65, 70, 75, 80, 85, 90],
    "Mathematics": [60, 64, 68, 72, 76, 80],
    "Database": [62, 68, 74, 78, 84, 88],
    "Communication": [70, 72, 74, 76, 78, 82],
    "Practical": [75, 78, 82, 85, 88, 92],
}

df = pd.DataFrame(data)

subjects = [
    "Programming",
    "Mathematics",
    "Database",
    "Communication",
    "Practical",
]

# Long format: one row per semester-subject result.
records = df.melt(
    id_vars="Semester",
    value_vars=subjects,
    var_name="Subject",
    value_name="Marks",
).sort_values(["Semester", "Subject"]).reset_index(drop=True)

records["Maximum_Marks"] = 100

df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

# Illustrative class averages; not actual class records.
df["Class_Average"] = [68, 70, 73, 76, 79, 82]

subject_average = df[subjects].mean()
target = 75

answer(1, "Create the dataset using Pandas.",
       df[["Semester"] + subjects].to_string(index=False))


# Q2. How many semesters are present?
answer(2, "How many semesters are present?",
       df["Semester"].nunique())


# Q3. How many subjects have you studied in total?
answer(
    3,
    "How many subjects have you studied in total?",
    f"Unique subject categories: {len(subjects)}\n"
    f"Total semester-subject records: {len(records)}",
)


# Q4. Find your highest marks.
highest = records["Marks"].max()
answer(
    4,
    "Find your highest marks.",
    records.loc[
        records["Marks"] == highest,
        ["Semester", "Subject", "Marks"]
    ].to_string(index=False),
)


# Q5. Find your lowest marks.
lowest = records["Marks"].min()
answer(
    5,
    "Find your lowest marks.",
    records.loc[
        records["Marks"] == lowest,
        ["Semester", "Subject", "Marks"]
    ].to_string(index=False),
)


# Q6. Which semester has the highest total marks?
answer(
    6,
    "Which semester has the highest total marks?",
    df.loc[
        df["Total"] == df["Total"].max(),
        ["Semester", "Total"]
    ].to_string(index=False),
)


# Q7. Which semester has the lowest total marks?
answer(
    7,
    "Which semester has the lowest total marks?",
    df.loc[
        df["Total"] == df["Total"].min(),
        ["Semester", "Total"]
    ].to_string(index=False),
)


# Q8. Display the first five records.
answer(8, "Display the first five records.",
       records.head().to_string(index=False))


# Q9. Find average marks for each semester.
answer(
    9,
    "Find average marks for each semester.",
    df[["Semester", "Average"]].to_string(index=False),
)


# Q10. Create a line graph of semester-wise average marks.
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    df["Semester"], df["Average"],
    marker="o", linewidth=2, label="Student average"
)
ax.set(
    title="Figure 1: Semester-wise Average — Sample Data",
    xlabel="Semester",
    ylabel="Average marks (%)",
    ylim=(0, 100),
)
ax.set_xticks(df["Semester"])
ax.legend()
save_graph(fig, "figure_1_semester_average.png")
answer(10, "Create a line graph of semester-wise average marks.",
       "Saved: figure_1_semester_average.png")


# Q11. Create a bar graph of subject-wise average marks.
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(
    subject_average.index,
    subject_average.values,
    color="steelblue"
)
ax.bar_label(bars, fmt="%.1f", padding=3)
ax.set(
    title="Figure 2: Subject-wise Average — Sample Data",
    xlabel="Subject category",
    ylabel="Average marks (%)",
    ylim=(0, 100),
)
ax.tick_params(axis="x", rotation=15)
save_graph(fig, "figure_2_subject_average.png")
answer(11, "Create a bar graph of subject-wise average marks.",
       "Saved: figure_2_subject_average.png")


# Q12. Identify your highest-performing subject.
best_subject = subject_average.idxmax()
answer(
    12,
    "Identify your highest-performing subject.",
    f"{best_subject}: {subject_average[best_subject]:.2f}%",
)


# Q13. Identify your lowest-performing subject.
worst_subject = subject_average.idxmin()
answer(
    13,
    "Identify your lowest-performing subject.",
    f"{worst_subject}: {subject_average[worst_subject]:.2f}%",
)


# Q14. Identify your best and worst semester.
best_row = df.loc[df["Average"].idxmax()]
worst_row = df.loc[df["Average"].idxmin()]

answer(
    14,
    "Identify your best and worst semester.",
    f"Best: Semester {int(best_row['Semester'])} "
    f"({best_row['Average']:.2f}%)\n"
    f"Worst: Semester {int(worst_row['Semester'])} "
    f"({worst_row['Average']:.2f}%)",
)


# Q15. Calculate improvement between Semester 1 and Semester 6.
sem1 = df.loc[df["Semester"] == 1, "Average"].iloc[0]
sem6 = df.loc[df["Semester"] == 6, "Average"].iloc[0]

improvement = sem6 - sem1
relative_improvement = (improvement / sem1) * 100

answer(
    15,
    "Calculate improvement between Semester 1 and Semester 6.",
    f"Semester 1: {sem1:.2f}%\n"
    f"Semester 6: {sem6:.2f}%\n"
    f"Improvement: {improvement:.2f} percentage points\n"
    f"Relative improvement: {relative_improvement:.2f}%",
)


# Q16. Calculate statistics using NumPy.
marks_array = df[subjects].to_numpy().flatten()

statistics = {
    "Mean": np.mean(marks_array),
    "Median": np.median(marks_array),
    "Maximum": np.max(marks_array),
    "Minimum": np.min(marks_array),
    # Population SD: these 30 records are the complete sample dataset.
    "Standard deviation (population)": np.std(marks_array, ddof=0),
}

answer(
    16,
    "Calculate mean, median, maximum, minimum and standard deviation.",
    "\n".join(f"{key}: {value:.2f}"
              for key, value in statistics.items()),
)


# Q17. Show each subject's performance across six semesters.
fig, ax = plt.subplots(figsize=(10, 6))

for subject in subjects:
    ax.plot(
        df["Semester"], df[subject],
        marker="o", linewidth=2, label=subject
    )

ax.set(
    title="Subject Performance Across Six Semesters — Sample Data",
    xlabel="Semester",
    ylabel="Marks (%)",
    ylim=(0, 100),
)
ax.set_xticks(df["Semester"])


# Q18. Show the academic target using axhline().
ax.axhline(
    y=target,
    color="black",
    linestyle="--",
    linewidth=2,
    label="Target: 75%",
)
ax.legend(loc="lower right")
save_graph(fig, "subject_progress_with_target.png")

answer(17, "Graph each subject's performance across six semesters.",
       "Saved: subject_progress_with_target.png")

answer(18, "Show a 75% academic target using axhline().",
       "The dashed horizontal line marks the 75% target.")


# Q19. Compare performance with the class average.
# Actual class data is unavailable, so this is illustrative.
df["Difference_From_Class"] = df["Average"] - df["Class_Average"]

answer(
    19,
    "Compare your performance with the class average.",
    "Using fictional class averages for demonstration:\n"
    + df[
        ["Semester", "Average", "Class_Average", "Difference_From_Class"]
    ].to_string(index=False),
)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    df["Semester"], df["Average"],
    marker="o", label="Sample student"
)
ax.plot(
    df["Semester"], df["Class_Average"],
    marker="s", linestyle="--", label="Sample class average"
)
ax.set(
    title="Figure 4: Student vs Class Average — Sample Data",
    xlabel="Semester",
    ylabel="Average marks (%)",
    ylim=(0, 100),
)
ax.set_xticks(df["Semester"])
ax.legend()
save_graph(fig, "figure_4_student_vs_class.png")


# Required Figure 3: Semester-wise total marks.
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df["Semester"], df["Total"], color="teal")
ax.bar_label(bars, padding=3)
ax.set(
    title="Figure 3: Semester-wise Total — Sample Data",
    xlabel="Semester",
    ylabel="Total marks (out of 500)",
    ylim=(0, 500),
)
ax.set_xticks(df["Semester"])
save_graph(fig, "figure_3_semester_total.png")


# Q20. Create a 2x2 Matplotlib dashboard.
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Student Academic Performance Dashboard — Fictional Dataset",
    fontsize=16,
)

# Dashboard panel 1: Semester-wise average.
axes[0, 0].plot(
    df["Semester"], df["Average"],
    marker="o", color="royalblue", label="Student average"
)
axes[0, 0].axhline(
    target, color="red", linestyle="--", label="Target: 75%"
)
axes[0, 0].set(
    title="Figure 1: Semester-wise Average",
    xlabel="Semester",
    ylabel="Average (%)",
    ylim=(0, 100),
)
axes[0, 0].set_xticks(df["Semester"])
axes[0, 0].legend()

# Dashboard panel 2: Subject-wise average.
bars = axes[0, 1].bar(
    subject_average.index, subject_average.values,
    color="steelblue"
)
axes[0, 1].bar_label(bars, fmt="%.1f", padding=3)
axes[0, 1].set(
    title="Figure 2: Subject-wise Average",
    ylabel="Average (%)",
    ylim=(0, 100),
)
axes[0, 1].tick_params(axis="x", rotation=20)

# Dashboard panel 3: Semester-wise total.
bars = axes[1, 0].bar(
    df["Semester"], df["Total"], color="teal"
)
axes[1, 0].bar_label(bars, padding=3)
axes[1, 0].set(
    title="Figure 3: Semester-wise Total",
    xlabel="Semester",
    ylabel="Total marks (out of 500)",
    ylim=(0, 500),
)
axes[1, 0].set_xticks(df["Semester"])

# Dashboard panel 4: Student versus sample class average.
axes[1, 1].plot(
    df["Semester"], df["Average"],
    marker="o", label="Sample student"
)
axes[1, 1].plot(
    df["Semester"], df["Class_Average"],
    marker="s", linestyle="--", label="Sample class average"
)
axes[1, 1].set(
    title="Figure 4: Student vs Class Average",
    xlabel="Semester",
    ylabel="Average (%)",
    ylim=(0, 100),
)
axes[1, 1].set_xticks(df["Semester"])
axes[1, 1].legend()

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(
    output / "academic_dashboard.png",
    dpi=180,
    bbox_inches="tight",
)

answer(20, "Create a 2x2 Matplotlib dashboard.",
       "Saved: academic_dashboard.png")


# Q21. Write five observations based on the visualizations.
first_target_sem = int(
    df.loc[df["Average"] >= target, "Semester"].iloc[0]
)
above_class = int((df["Difference_From_Class"] > 0).sum())

observations = [
    (
        f"Average performance increased from {sem1:.1f}% in Semester 1 "
        f"to {sem6:.1f}% in Semester 6, an improvement of "
        f"{improvement:.1f} percentage points."
    ),
    (
        f"{best_subject} had the highest subject average "
        f"({subject_average[best_subject]:.2f}%), while "
        f"{worst_subject} had the lowest "
        f"({subject_average[worst_subject]:.2f}%)."
    ),
    (
        f"Semester {int(best_row['Semester'])} had the highest total "
        f"({int(best_row['Total'])}/500), while Semester "
        f"{int(worst_row['Semester'])} had the lowest "
        f"({int(worst_row['Total'])}/500)."
    ),
    (
        f"The semester average first reached the 75% target in "
        f"Semester {first_target_sem} and remained above it afterward."
    ),
    (
        f"The sample student exceeded the fictional class average "
        f"in {above_class} of 6 semesters; the final advantage was "
        f"{df['Difference_From_Class'].iloc[-1]:.1f} percentage points."
    ),
]

answer(
    21,
    "Write five observations based on the visualizations.",
    "\n".join(
        f"{number}. {text}"
        for number, text in enumerate(observations, start=1)
    ),
)

# Export data and observations.
records.to_csv(output / "student_marks.csv", index=False)
df.to_csv(output / "semester_summary.csv", index=False)

subject_average.rename("Average").to_csv(
    output / "subject_averages.csv",
    index_label="Subject",
)

(output / "observations.txt").write_text(
    "Observations based on fictional assignment data.\n\n"
    + "\n".join(
        f"{number}. {text}"
        for number, text in enumerate(observations, start=1)
    ),
    encoding="utf-8",
)

print(f"\nAll output files will be saved in: {output.resolve()}")

plt.show()