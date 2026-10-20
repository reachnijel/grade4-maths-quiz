"""End-to-end browser test. Uses the installed Microsoft Edge via Playwright (no browser download).

Loads index.html directly from disk (file://), which is also how it works offline.
Skipped automatically if Playwright or Edge is unavailable.
"""

import pytest

pw = pytest.importorskip("playwright.sync_api")
from pathlib import Path  # noqa: E402

from test_questions import load  # noqa: E402

URL = (Path(__file__).resolve().parents[1] / "index.html").as_uri()
QS = {q["q"]: q for q in load()}


@pytest.fixture(scope="module")
def browser():
    with pw.sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="msedge", headless=True)
        except Exception as e:  # pragma: no cover
            pytest.skip(f"Edge not available: {e}")
        yield b
        b.close()


@pytest.fixture
def page(browser):
    pg = browser.new_page(viewport={"width": 900, "height": 1000})
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL)
    yield pg
    assert not errors, errors
    pg.close()


def current(page):
    return QS[page.inner_text("#question")]


def test_start_screen_lists_topics(page):
    assert page.inner_text("#countSel") == "100"
    assert page.locator("#topics .chip").count() == 13  # "All" + 12 topics


def test_correct_answer_feedback(page):
    page.click("#startAll")
    q = current(page)
    page.locator(".opt").nth(q["answer"]).click()
    fb = page.locator("#feedback")
    assert fb.is_visible() and "ok" in fb.get_attribute("class")
    assert q["explain"] in fb.inner_text()
    assert "correct" in page.locator(".opt").nth(q["answer"]).get_attribute("class")
    assert page.locator(".opt:disabled").count() == 4
    assert page.inner_text("#score") == "Score: 1"


def test_wrong_answer_shows_right_answer_and_reason(page):
    page.click("#startAll")
    # advance until we land on a question that has a specific "why" note
    for _ in range(100):
        q = current(page)
        if q["why"]:
            break
        page.keyboard.press(str(q["answer"] + 1))
        page.keyboard.press("Enter")
    wrong_text = next(iter(q["why"]))
    wrong = q["options"].index(wrong_text)
    page.keyboard.press(str(wrong + 1))
    fb = page.locator("#feedback")
    assert "bad" in fb.get_attribute("class")
    text = fb.inner_text()
    assert q["options"][q["answer"]] in text and q["why"][wrong_text] in text and q["explain"] in text
    assert "wrong" in page.locator(".opt").nth(wrong).get_attribute("class")
    assert "correct" in page.locator(".opt").nth(q["answer"]).get_attribute("class")


def test_quick10_results_review_and_retry(page):
    page.click("#startQuick")
    for i in range(10):
        q = current(page)
        choice = q["answer"] if i % 2 == 0 else (q["answer"] + 1) % 4  # 5 right, 5 wrong
        page.locator(".opt").nth(choice).click()
        page.click("#next")
    assert page.locator("#result").is_visible()
    assert page.inner_text("#resultScore") == "5 / 10 (50%)"
    assert page.locator("#review li").count() == 5
    page.click("#retryWrong")
    assert page.inner_text("#qnum") == "Question 1 of 5"
    page.click("#quit")  # nothing answered yet -> straight back to start
    assert page.locator("#start").is_visible()
    assert "Best score so far: 5 / 10 (50%)" in page.inner_text("#best")


def test_topic_filter(page):
    page.click("#topics .chip >> nth=0")  # deselect all
    assert page.inner_text("#countSel") == "0" and page.is_disabled("#startAll")
    page.click("#topics .chip[data-topic='Fractions']")
    assert page.inner_text("#countSel") == "11"
    page.click("#startAll")
    assert page.inner_text("#topicTag") == "Fractions"
    assert page.inner_text("#qnum") == "Question 1 of 11"


def test_mobile_layout_screenshot(browser, tmp_path):
    pg = browser.new_page(viewport={"width": 390, "height": 844})
    pg.goto(URL)
    pg.click("#startQuick")
    q = current(pg)
    pg.locator(".opt").nth((q["answer"] + 1) % 4).click()
    out = Path(__file__).resolve().parents[1] / "docs" / "screenshot-mobile.png"
    out.parent.mkdir(exist_ok=True)
    pg.screenshot(path=str(out), full_page=True)
    assert pg.evaluate("document.documentElement.scrollWidth <= 390")
    pg.close()
