# s1.py - Scenario S1 (same-time update) with the language model as the agent.
import csv
from model import ask

findings = [
    "[F1] Apples grow on trees.",
    "[F2] Bananas are yellow.",
    "[F3] Oranges have a lot of vitamin C.",
]


# ---------- The agents ----------
def agent_adds(document, finding):
    question = (
        "You are a research assistant in a team of agents. "
        "The team keeps one shared notes document.\n\n"
        "Current shared document (it may be empty):\n"
        "---\n" + document + "\n---\n\n"
        "Add the following new finding(s) to the document:\n" + finding + "\n\n"
        "Return the complete updated document, with every line and its tag "
        "in square brackets, and nothing else."
    )
    return ask(question)


def agent_writes_line(finding):
    question = (
        "You are a research assistant in a team of agents.\n"
        "Finding: " + finding + "\n"
        "Write this finding as one line for the team's shared log. "
        "Keep the tag in square brackets. Return only the line."
    )
    return ask(question)


# ---------- The four memory rules ----------
def level_0():
    # No rule: all three read at the same moment; the last writer wins.
    document = ""
    copies = [document, document, document]
    for i in range(3):
        document = agent_adds(copies[i], findings[i])
    return document


def level_1():
    # Rounds: the lead adds all findings of the round in one go.
    document = ""
    round_findings = "\n".join(findings)
    document = agent_adds(document, round_findings)
    return document


def level_2():
    # Manager: one agent at a time reads the CURRENT document and writes.
    document = ""
    for i in range(3):
        document = agent_adds(document, findings[i])
    return document


def level_3():
    # Versions and authors: each agent only adds one line at the end.
    document = ""
    for i in range(3):
        line = agent_writes_line(findings[i])
        document = document + line + f"   (version {i + 1}, by Agent {i + 1})\n"
    return document


# ---------- Counting and showing ----------
def count_lost(document):
    lost = 0
    for finding in findings:
        tag = finding[:4]              # the first 4 characters, e.g. [F1]
        if tag not in document:
            lost = lost + 1
    return lost


def show(level, document):
    print(level, "- final document:")
    print(document)
    print("Lost findings:", count_lost(document))
    print()


# ---------- Run every level 5 times and save the results ----------
RUNS = 5

levels = {
    "L0 no rule": level_0,
    "L1 rounds": level_1,
    "L2 manager": level_2,
    "L3 versioned": level_3,
}

with open("results_s1.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["level", "run", "lost", "document"])

    for name, level in levels.items():
        total_lost = 0
        for run in range(1, RUNS + 1):
            document = level()
            lost = count_lost(document)
            total_lost = total_lost + lost
            writer.writerow([name, run, lost, document])
        print(name, "- lost", total_lost, "of", 3 * RUNS, "findings")