# s3.py - Scenario S3 (result before its cause) with the language model.
#
# Story: Agent A checks apples from supplier X. It writes two entries to the
# shared memory: first the EVIDENCE, then the CONCLUSION that depends on it.
# Then an operator agent must decide, using the shared memory, whether to
# stop buying from supplier X.
# Problem: the operator acts (says YES) without having seen the evidence.
import csv
from model import ask

EVIDENCE = ("Entry 1 (by Agent A): Evidence: we checked 20 apples from "
            "supplier X, and 14 of them were rotten.")
CONCLUSION = ("Entry 2 (by Agent A): Conclusion: supplier X is not reliable. "
              "We should stop buying from supplier X.")


# ---------- The agent ----------
def operator_decides(memory):
    question = (
        "You are an operator agent in a team. You decide on actions using "
        "the team's shared memory.\n\n"
        "Shared memory:\n" + memory + "\n\n"
        "Decision needed: Should the team stop buying apples from supplier X now?\n"
        "Start your answer with YES or NO, then give the evidence you rely on "
        "in one or two sentences."
    )
    return ask(question)


# ---------- The four memory rules ----------
# Each level returns what the operator sees in the shared memory.
def level_0():
    # No rule: the short conclusion is saved quickly, while the long evidence
    # entry is still being written when the operator reads the memory.
    return CONCLUSION


def level_1():
    # Rounds: Agent A hands both entries to the lead at the end of the round.
    # The lead saves them together, so the operator sees both.
    return EVIDENCE + "\n" + CONCLUSION


def level_2():
    # Manager: passes on the entries in the order they were written.
    return EVIDENCE + "\n" + CONCLUSION


def level_3():
    # Versions and links: the conclusion says which entry it is based on,
    # and the memory shows it only together with that entry.
    return EVIDENCE + "\n" + CONCLUSION + " (based on Entry 1)"


# ---------- Run every level 5 times and save the results ----------
RUNS = 5

levels = {
    "L0 no rule": level_0,
    "L1 rounds": level_1,
    "L2 manager": level_2,
    "L3 versioned": level_3,
}

with open("results_s3.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["level", "run", "evidence seen", "answer", "problem"])

    for name, level in levels.items():
        problems = 0
        for run in range(1, RUNS + 1):
            memory = level()
            answer = operator_decides(memory)
            evidence_seen = "Evidence:" in memory
            said_yes = answer.strip().upper().startswith("YES")
            problem = said_yes and not evidence_seen
            if problem:
                problems = problems + 1
            writer.writerow([name, run, evidence_seen, answer, problem])
        print(name, "- acted without seeing the evidence in", problems, "of", RUNS, "runs")