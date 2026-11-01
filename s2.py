# s2.py - Scenario S2 (old plan) with the language model as the agent.
#
# Story: the lead's plan says "our focus is apples". Three workers write
# one short note per step, for two steps. In step 1, right after Worker 1
# has written its note, the lead changes the plan to bananas.
# After the change, 5 notes are written: Workers 2 and 3 in step 1, and
# Workers 1, 2 and 3 in step 2. Which of them still follow the old plan?
import csv
from model import ask

OLD_PLAN = "LEAD (plan version 1): Our research focus is apples."
NEW_PLAN = ("LEAD (plan version 2): Change of plan. From now on, our research "
            "focus is bananas. Notes about apples are no longer needed.")
NOTICE = ("NOTICE FROM THE SHARED MEMORY: the plan was updated to version 2. "
          "Version 1 is no longer valid.")


# ---------- The agent ----------
def worker_writes_note(messages):
    question = (
        "You are a worker agent in a research team. A lead agent gives the "
        "plan. Follow the lead's current plan.\n\n"
        "Messages you have received so far:\n" + messages + "\n\n"
        "Write one short research note (one sentence) about the focus that "
        "the current plan asks for. Name the fruit you write about. "
        "Return only the note."
    )
    return ask(question)


# ---------- The four memory rules ----------
# Each level returns the 5 notes written AFTER the plan change.
def level_0():
    # No rule: each worker only has the plan from its first task.
    # The change is written to the memory, but nobody tells the workers.
    notes = []
    for i in range(5):
        notes.append(worker_writes_note(OLD_PLAN))
    return notes


def level_1():
    # Rounds: at the start of each round the lead gives every worker a task
    # with the plan in force at that moment. During a round, the lead cannot
    # reach the workers.
    notes = []
    for worker in [2, 3]:                      # round 1, after the change
        notes.append(worker_writes_note(OLD_PLAN))
    for worker in [1, 2, 3]:                   # round 2
        notes.append(worker_writes_note(NEW_PLAN))
    return notes


def level_2():
    # Manager: every message, including the change, is sent to all workers.
    notes = []
    for i in range(5):
        notes.append(worker_writes_note(OLD_PLAN + "\n" + NEW_PLAN))
    return notes


def level_3():
    # Versions: like Level 2, plus a notice from the memory that version 1
    # is no longer valid.
    notes = []
    for i in range(5):
        notes.append(worker_writes_note(OLD_PLAN + "\n" + NEW_PLAN + "\n" + NOTICE))
    return notes


# ---------- Counting ----------
def count_stale(notes):
    # A note is "stale" if it does not write about bananas.
    stale = 0
    for note in notes:
        if "banana" not in note.lower():
            stale = stale + 1
    return stale


# ---------- Run every level 5 times and save the results ----------
RUNS = 5

levels = {
    "L0 no rule": level_0,
    "L1 rounds": level_1,
    "L2 manager": level_2,
    "L3 versioned": level_3,
}

with open("results_s2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["level", "run", "stale", "notes"])

    for name, level in levels.items():
        total_stale = 0
        for run in range(1, RUNS + 1):
            notes = level()
            stale = count_stale(notes)
            total_stale = total_stale + stale
            writer.writerow([name, run, stale, " | ".join(notes)])
        print(name, "- old plan in", total_stale, "of", 5 * RUNS, "notes")