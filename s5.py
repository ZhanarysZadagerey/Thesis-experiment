# s5.py - Scenario S5 (late joiner) with the language model.
#
# Story: a team has worked for a while, and three facts have changed:
# the focus (apples -> bananas), the deadline (2 June -> 9 June) and who
# writes the final report (Worker 1 -> Worker 3). Now a new worker,
# Worker 4, joins. What does it receive, and does it know the CURRENT facts?


import csv
from model import ask

FIRST_TASK = ("LEAD: Our research focus is apples. The deadline for the report "
              "is 2 June. Worker 1 writes the final report.")

HISTORY = """LEAD: Our research focus is apples. The deadline for the report is 2 June. Worker 1 writes the final report.
Worker 1: First sources on apples collected.
Worker 2: Two articles about apples summarised.
LEAD: Change of plan. From now on, our research focus is bananas.
LEAD: The deadline for the report moved to 9 June.
Worker 1: Started collecting sources on bananas.
LEAD: Change of roles: Worker 3 now writes the final report instead of Worker 1.
Worker 3: Outline of the final report on bananas started."""

SNAPSHOT = """CURRENT STATE OF THE TEAM (from the shared memory):
- Focus: bananas (version 2, set by LEAD; replaces apples)
- Deadline for the report: 9 June (version 2, set by LEAD; replaces 2 June)
- Final report written by: Worker 3 (version 2, set by LEAD; replaces Worker 1)"""


# ------------ AGENTS --------------
def lead_writes_handoff(history):
    question = (
        "You are the lead agent of a research team.\n\n"
        "Team conversation so far:\n" + history + "\n\n"
        "A new worker (Worker 4) joins the team now. Write a short handoff "
        "message for Worker 4 (at most five sentences) with what they need "
        "to know to continue the work."
    )
    return ask(question)


def new_worker_states(received):
    question = (
        "You are a new worker agent who has just joined a research team.\n\n"
        "What you received when you joined:\n" + received + "\n\n"
        "Before you start, state what you understand about the team's current "
        "state. Answer in exactly this form:\n"
        "FOCUS: <current research focus>\n"
        "DEADLINE: <current deadline for the report>\n"
        "REPORT WRITER: <who writes the final report>"
    )
    return ask(question)


# ---------- The four memory rules ----------
# Each level returns what Worker 4 receives when it joins.
def level_0():
    # No rule for new workers: Worker 4 gets the task description that was written at the start.
    return FIRST_TASK


def level_1():
    # Rounds: the lead writes a short handoff for the new worker.
    return "Handoff from the lead:\n" + lead_writes_handoff(HISTORY)


def level_2():
    # Manager: Worker 4 receives the whole conversation, in order.
    return HISTORY


def level_3():
    # Versions: the memory gives Worker 4 a snapshot of the current state.
    return SNAPSHOT


# ---------- Counting ----------
def count_known(answer):
    # How many of the 3 current facts are in the answer?
    a = answer.lower()
    known = 0
    if "banana" in a:
        known = known + 1
    if "9 june" in a or "june 9" in a:
        known = known + 1
    if "worker 3" in a:
        known = known + 1
    return known


# ---------- Run every level 5 times and save the results ----------
RUNS = 5

levels = {
    "L0 no rule": level_0,
    "L1 rounds": level_1,
    "L2 manager": level_2,
    "L3 versioned": level_3,
}

with open("results_s5.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["level", "run", "received", "answer", "facts missed"])

    for name, level in levels.items():
        total_missed = 0
        for run in range(1, RUNS + 1):
            received = level()
            answer = new_worker_states(received)
            missed = 3 - count_known(answer)
            total_missed = total_missed + missed
            writer.writerow([name, run, received, answer, missed])
        print(name, "- new worker missed", total_missed, "of", 3 * RUNS, "current facts")