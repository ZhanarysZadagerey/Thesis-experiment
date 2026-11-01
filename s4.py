# s4.py - Scenario S4 (different conclusions) with the language model.
#
# Story: two workers check the same fact and reach different values.
# Both write their finding to the shared memory. Then the lead answers a user's question from the shared memory.
# Problem: the lead's answer does not show the contradiction (it gives only one value, or a value without saying that the workers disagree).
import csv
from model import ask

FINDING_1 = "Worker 1: The apple harvest of Green Hill farm this year is 500 kg."
FINDING_2 = "Worker 2: The apple harvest of Green Hill farm this year is 800 kg."


# ---------- AGENTS ----------
def lead_answers(memory):
    question = (
        "You are the lead agent of a research team. You answer questions "
        "using the team's shared memory.\n\n"
        "Shared memory:\n" + memory + "\n\n"
        "Question from the user: How big is the apple harvest of Green Hill "
        "farm this year?\n"
        "Answer the question in one or two sentences, using the shared memory."
    )
    return ask(question)


# ---------- The four memory rules ----------
# Each level returns what the lead sees in the shared memory.
def level_0():
    # No rule: both workers write to the same place. Worker 2 writes last,
    # so its value replaces the value of Worker 1.
    return FINDING_2


def level_1():
    # Rounds: both workers return their findings to the lead at the end
    # of the round.
    return FINDING_1 + "\n" + FINDING_2


def level_2():
    # Manager: passes on every message, in order.
    return FINDING_1 + "\n" + FINDING_2


def level_3():
    # Versions and authors: the memory keeps both entries and marks the
    # conflict.
    return (FINDING_1 + " (version 1)\n" +
            FINDING_2 + " (version 2)\n" +
            "CONFLICT: these two entries give different values for the same fact.")


# ---------- Run every level 5 times and save the results ----------
RUNS = 5

levels = {
    "L0 no rule": level_0,
    "L1 rounds": level_1,
    "L2 manager": level_2,
    "L3 versioned": level_3,
}

with open("results_s4.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["level", "run", "answer", "problem"])

    for name, level in levels.items():
        problems = 0
        for run in range(1, RUNS + 1):
            memory = level()
            answer = lead_answers(memory)
            shows_both = "500" in answer and "800" in answer
            problem = not shows_both
            if problem:
                problems = problems + 1
            writer.writerow([name, run, answer, problem])
        print(name, "- contradiction NOT shown in", problems, "of", RUNS, "answers")