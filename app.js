(() => {
  "use strict";
  const ALL = window.QUESTIONS || [];
  const TOPICS = [...new Set(ALL.map(q => q.topic))];
  const KEYS = ["A", "B", "C", "D"];
  const PRAISE = ["Correct! 🎉", "Well done! ⭐", "Super! 🌟", "Great job! 👏", "You got it! ✅"];
  const $ = id => document.getElementById(id);

  let selected = new Set(TOPICS);
  let deck = [], idx = 0, score = 0, answered = false, results = [];

  const shuffle = a => {
    a = a.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  const show = id => ["start", "quiz", "result"].forEach(s => ($(s).hidden = s !== id));
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };
  const pool = () => ALL.filter(q => selected.has(q.topic));

  // ---------- start screen
  function renderTopics() {
    const box = $("topics");
    box.replaceChildren();
    const allBtn = el("button", "chip", `All topics (${ALL.length})`);
    allBtn.setAttribute("aria-pressed", selected.size === TOPICS.length);
    allBtn.onclick = () => {
      selected = selected.size === TOPICS.length ? new Set() : new Set(TOPICS);
      renderTopics();
    };
    box.append(allBtn);
    for (const t of TOPICS) {
      const n = ALL.filter(q => q.topic === t).length;
      const b = el("button", "chip", `${t} (${n})`);
      b.dataset.topic = t;
      b.setAttribute("aria-pressed", selected.has(t));
      b.onclick = () => {
        selected.has(t) ? selected.delete(t) : selected.add(t);
        renderTopics();
      };
      box.append(b);
    }
    const count = pool().length;
    $("countSel").textContent = count;
    $("startAll").disabled = $("startQuick").disabled = count === 0;
    const best = localStorage.getItem("g4-best");
    $("best").textContent = best ? `🏆 Best score so far: ${best}` : "";
  }

  function start(questions) {
    deck = questions; idx = 0; score = 0; results = [];
    show("quiz");
    renderQuestion();
  }

  // ---------- question screen
  function renderQuestion() {
    const q = deck[idx];
    answered = false;
    $("qnum").textContent = `Question ${idx + 1} of ${deck.length}`;
    $("topicTag").textContent = q.topic;
    $("score").textContent = `Score: ${score}`;
    $("barFill").style.width = `${(idx / deck.length) * 100}%`;
    $("question").textContent = q.q;
    $("feedback").hidden = true;
    $("next").hidden = true;
    const box = $("options");
    box.replaceChildren();
    q.options.forEach((text, i) => {
      const b = el("button", "opt");
      b.append(el("span", "key", KEYS[i]), el("span", "txt", text));
      b.onclick = () => choose(i);
      box.append(b);
    });
    box.firstChild.focus({ preventScroll: true });
  }

  function choose(i) {
    if (answered) return;
    answered = true;
    const q = deck[idx];
    const ok = i === q.answer;
    if (ok) score++;
    results.push({ q, chosen: i, ok });

    [...$("options").children].forEach((b, j) => {
      b.disabled = true;
      if (j === q.answer) b.classList.add("correct");
      else if (j === i) b.classList.add("wrong");
      else b.classList.add("dim");
    });

    const fb = $("feedback");
    fb.className = "feedback " + (ok ? "ok" : "bad");
    fb.replaceChildren();
    fb.append(el("p", "head", ok
      ? PRAISE[Math.floor(Math.random() * PRAISE.length)]
      : `Not quite. The right answer is ${KEYS[q.answer]}: ${q.options[q.answer]}`));
    const why = !ok && q.why && q.why[q.options[i]];
    if (why) fb.append(el("p", "why", `Why "${q.options[i]}" is wrong: ${why}`));
    fb.append(el("p", "explain", `💡 ${q.explain}`));
    fb.hidden = false;

    $("score").textContent = `Score: ${score}`;
    $("next").textContent = idx + 1 < deck.length ? "Next ➜" : "See results 🏁";
    $("next").hidden = false;
    $("next").focus({ preventScroll: true });
  }

  function next() {
    if (!answered) return;
    if (++idx < deck.length) renderQuestion();
    else finish();
  }

  // ---------- result screen
  function finish() {
    show("result");
    const total = results.length;
    const pct = total ? Math.round((score / total) * 100) : 0;
    $("resultTitle").textContent =
      pct === 100 ? "Perfect score! 🏆" : pct >= 80 ? "Excellent work! 🌟" :
      pct >= 50 ? "Good effort! 👍" : "Keep practising! 💪";
    $("resultScore").textContent = `${score} / ${total} (${pct}%)`;

    if (total >= 10) {
      const prev = localStorage.getItem("g4-best");
      const prevPct = prev ? parseInt(prev.match(/\((\d+)%\)/)?.[1] || "0", 10) : -1;
      if (pct > prevPct) localStorage.setItem("g4-best", `${score} / ${total} (${pct}%)`);
    }

    const table = $("breakdown");
    table.replaceChildren();
    const head = el("tr");
    head.append(el("th", "", "Topic"), el("th", "", "Correct"));
    table.append(head);
    const by = {};
    for (const r of results) {
      by[r.q.topic] = by[r.q.topic] || [0, 0];
      by[r.q.topic][1]++;
      if (r.ok) by[r.q.topic][0]++;
    }
    for (const [t, [c, n]] of Object.entries(by)) {
      const tr = el("tr");
      tr.append(el("td", "", t), el("td", "num", `${c} / ${n} ${c === n ? "✅" : ""}`));
      table.append(tr);
    }

    const wrong = results.filter(r => !r.ok);
    $("retryWrong").hidden = wrong.length === 0;
    $("reviewTitle").hidden = wrong.length === 0;
    const list = $("review");
    list.replaceChildren();
    for (const r of wrong) {
      const li = el("li");
      li.append(el("div", "", r.q.q));
      const line = el("div");
      line.append("You chose ", el("span", "ans-bad", r.chosen >= 0 ? r.q.options[r.chosen] : "—"),
                  " → correct: ", el("span", "ans-ok", r.q.options[r.q.answer]));
      li.append(line, el("div", "muted small", r.q.explain));
      list.append(li);
    }
  }

  // ---------- wiring
  $("startAll").onclick = () => start(shuffle(pool()));
  $("startQuick").onclick = () => start(shuffle(pool()).slice(0, 10));
  $("next").onclick = next;
  $("quit").onclick = () => (results.length ? finish() : (show("start"), renderTopics()));
  $("home").onclick = () => { show("start"); renderTopics(); };
  $("retryWrong").onclick = () => start(shuffle(results.filter(r => !r.ok).map(r => r.q)));

  document.addEventListener("keydown", e => {
    if ($("quiz").hidden) return;
    if (!answered && ["1", "2", "3", "4"].includes(e.key)) choose(Number(e.key) - 1);
    else if (answered && e.key === "Enter") { e.preventDefault(); next(); }
  });

  renderTopics();
  show("start");
})();
