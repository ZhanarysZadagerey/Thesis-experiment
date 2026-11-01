# summary.py - Recomputes the result tables of Chapter 6 
# from the saved CSV files. It does not call the model and do not need API key.

import csv

LEVELS = ["L0 no rule", "L1 rounds", "L2 manager", "L3 versioned"]


def read(file_name):
    with open(file_name, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def rows_of(rows, level):
    return [row for row in rows if row["level"] == level]


def count_true(rows, column):
    return sum(1 for row in rows if row[column] == "True")


print("Table 6.2  S1 Same-time update: findings lost")
rows = read("results_s1.csv")
for level in LEVELS:
    lost = sum(int(row["lost"]) for row in rows_of(rows, level))
    print(f"  {level:<13} {lost} of 15")

print("\nTable 6.3  S2 Old plan: notes on the old plan")
rows = read("results_s2.csv")
for level in LEVELS:
    stale = sum(int(row["stale"]) for row in rows_of(rows, level))
    print(f"  {level:<13} {stale} of 25")

print("\nTable 6.4  S3 Result before its cause")
rows = read("results_s3.csv")
for level in LEVELS:
    group = rows_of(rows, level)
    seen = count_true(group, "evidence seen")
    acted = count_true(group, "problem")
    print(f"  {level:<13} evidence delivered {seen} of 5, acted without it {acted} of 5")

print("\nTable 6.5  S4 Different conclusions: contradiction not shown")
rows = read("results_s4.csv")
for level in LEVELS:
    problems = count_true(rows_of(rows, level), "problem")
    print(f"  {level:<13} {problems} of 5")

print("\nTable 6.6  S5 Late joiner")
rows = read("results_s5.csv")
for level in LEVELS:
    group = rows_of(rows, level)
    missed = sum(int(row["facts missed"]) for row in group)
    length = sum(len(row["received"]) for row in group) / len(group)
    print(f"  {level:<13} length {length:.0f} characters (average), facts missed {missed} of 15")