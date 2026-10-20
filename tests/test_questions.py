"""Validate the generated question bank (questions.js)."""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    text = (ROOT / "questions.js").read_text(encoding="utf-8")
    return json.loads(re.search(r"window\.QUESTIONS = (.*);\s*$", text, re.S).group(1))


def test_questions_js_is_up_to_date(tmp_path):
    before = (ROOT / "questions.js").read_bytes()
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_questions.py")], check=True, capture_output=True)
    assert (ROOT / "questions.js").read_bytes() == before, "run tools/build_questions.py and commit questions.js"


def test_exactly_100_well_formed_questions():
    qs = load()
    assert len(qs) == 100
    assert [q["id"] for q in qs] == list(range(1, 101))
    for q in qs:
        assert q["q"].strip() and q["explain"].strip() and q["topic"].strip()
        assert len(q["options"]) == 4 and len(set(q["options"])) == 4
        assert 0 <= q["answer"] < 4
        for wrong_opt in q["why"]:
            assert wrong_opt in q["options"] and wrong_opt != q["options"][q["answer"]]


def test_topic_counts():
    counts = Counter(q["topic"] for q in load())
    assert counts == {
        "Numbers & Place Value": 14, "Addition": 8, "Subtraction": 8, "Multiplication": 10,
        "Division": 9, "Factors & Multiples": 6, "Fractions": 11, "Decimals & Money": 8,
        "Time": 8, "Measurement": 7, "Geometry": 7, "Patterns & Data": 4,
    }


def test_answers_spread_across_positions():
    pos = Counter(q["answer"] for q in load())
    assert all(15 <= pos[i] <= 35 for i in range(4)), pos


def test_simple_arithmetic_answers_recomputed():
    """For every plain 'a op b = ?' question, independently recompute the answer."""
    ops = {"+": lambda a, b: a + b, "−": lambda a, b: a - b, "×": lambda a, b: a * b, "÷": lambda a, b: a // b}
    checked = 0
    for q in load():
        m = re.fullmatch(r"([\d,]+) ([+−×÷]) ([\d,]+) = \?", q["q"])
        if not m:
            continue
        a, op, b = int(m[1].replace(",", "")), m[2], int(m[3].replace(",", ""))
        if op == "÷":
            assert a % b == 0
        assert int(q["options"][q["answer"]].replace(",", "")) == ops[op](a, b), q["q"]
        checked += 1
    assert checked >= 20


def test_explanation_mentions_correct_answer_for_numeric_questions():
    for q in load():
        ans = q["options"][q["answer"]]
        if re.fullmatch(r"[\d,]+", ans):
            assert ans in q["explain"] or ans.replace(",", "") in q["explain"], (q["q"], ans)
