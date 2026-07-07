/* =====================================================================
   results.js — Results screen + Review Mistakes screen
   ---------------------------------------------------------------------
   Builds the DOM for:
     • the final scorecard (score %, correct/wrong/skipped, time, accuracy)
     • the full mistake review list (user answer in red, correct in green,
       explanation if available)
   Navigation decisions (restart / back home / practice wrong) are exposed
   via callbacks so the page controller stays in charge.
   ===================================================================== */
(function (global) {
  "use strict";

  const UI = global.UI;

  function fmtTime(sec) {
    sec = Math.max(0, Math.round(sec));
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return m + "m " + String(s).padStart(2, "0") + "s";
  }

  function ringColor(pct) {
    if (pct >= 80) return "var(--success)";
    if (pct >= 50) return "var(--primary)";
    return "var(--danger)";
  }

  /** Render the results card into `container`. Calls back on actions. */
  function renderResults(container, result, actions) {
    const color = ringColor(result.scorePct);
    const card = UI.elFromHTML(
      '<div class="results-card fade-in">' +
        '<h1 class="results-title">Exam Finished 🎉</h1>' +
        '<p class="results-sub">' +
        (result.finishedReason === "time"
          ? "Time ran out — exam auto-submitted."
          : "You answered every question.") +
        "</p>" +
        '<div class="score-ring" style="--ring-color:' +
        color +
        ';--p:' +
        result.scorePct +
        '">' +
        '<div class="score-ring-inner">' +
        '<div class="score-pct">' +
        result.scorePct +
        '%</div>' +
        '<div class="score-label">Score</div>' +
        "</div></div>" +
        '<div class="stat-grid">' +
        statBox("correct", result.correct, "Correct") +
        statBox("wrong", result.wrong, "Wrong") +
        statBox("skipped", result.skipped, "Skipped") +
        statBox("accuracy", result.accuracy + "%", "Accuracy") +
        "</div>" +
        '<div class="stat-grid" style="grid-template-columns:1fr 1fr">' +
        statBox("plain", result.total, "Total Questions") +
        statBox("plain", fmtTime(result.timeUsedSec), "Time Used") +
        "</div>" +
        '<div class="results-actions">' +
        '<button class="btn btn-ghost btn-block" data-act="review" ' +
        (result.wrong > 0 ? "" : "disabled") +
        ">❌ Review Mistakes</button>" +
        '<button class="btn btn-primary btn-block" data-act="restart">🔄 Restart Exam</button>' +
        '<button class="btn btn-ghost btn-block" data-act="home">🏠 Back Home</button>' +
        "</div>" +
        "</div>"
    );

    bind(card, actions);
    container.innerHTML = "";
    container.appendChild(card);
  }

  function statBox(kind, value, label) {
    return (
      '<div class="stat-box ' +
      kind +
      '"><div class="v">' +
      UI.escapeHtml(value) +
      '</div><div class="k">' +
      UI.escapeHtml(label) +
      "</div></div>"
    );
  }

  function bind(card, actions) {
    const map = {
      review: actions.onReview,
      restart: actions.onRestart,
      home: actions.onHome,
    };
    Object.keys(map).forEach(function (act) {
      const btn = card.querySelector('[data-act="' + act + '"]');
      if (btn && map[act]) {
        btn.addEventListener("click", function () {
          map[act](result);
        });
      }
    });
  }

  /** Render the mistake review screen into `container`. */
  function renderReview(container, onPractice, onHome, onBack) {
    const mistakes = global.Storage.mistakes.getAll();
    const byId = global.Quiz.getAllQuestions().reduce(function (acc, q) {
      acc[q.id] = q;
      return acc;
    }, {});

    let inner;
    if (!mistakes.length) {
      inner =
        '<div class="review-empty"><span class="emoji">🎯</span>' +
        "<h3>No mistakes available yet.</h3>" +
        "<p>Complete at least one exam first.</p></div>";
    } else {
      const items = mistakes
        .map(function (m) {
          const q = byId[m.id];
          const correctText = q
            ? optionText(q, m.correctAnswer)
            : m.correctAnswer;
          const userText = q ? optionText(q, m.userAnswer) : m.userAnswer || "—";
          const explanation = q && q.justification ? q.justification : "";
          return (
            '<div class="review-item">' +
            "<h4>" +
            UI.escapeHtml(m.question || (q ? q.question : "")) +
            "</h4>" +
            '<div class="review-row user"><span class="tag">Your answer</span>' +
            "<span>" +
            UI.escapeHtml(
              (m.userAnswer ? m.userAnswer.toUpperCase() + ") " : "") + userText
            ) +
            "</span></div>" +
            '<div class="review-row answer"><span class="tag">Correct</span>' +
            "<span>" +
            UI.escapeHtml(m.correctAnswer.toUpperCase() + ") " + correctText) +
            "</span></div>" +
            (explanation
              ? '<div class="review-explain"><b>Explanation:</b> ' +
                UI.escapeHtml(explanation) +
                "</div>"
              : "") +
            "</div>"
          );
        })
        .join("");

      inner =
        '<div class="review-list fade-in">' + items + "</div>" +
        '<div class="results-actions" style="margin-top:22px">' +
        '<button class="btn btn-primary btn-block" data-act="practice">🎯 Practice Wrong Answers</button>' +
        '<button class="btn btn-ghost btn-block" data-act="home">🏠 Back Home</button>' +
        '<button class="btn btn-ghost btn-block" data-act="back">↩ Back</button>' +
        "</div>";
    }

    const wrap = UI.elFromHTML(
      '<div class="results-card" style="text-align:left">' +
        '<h1 class="results-title" style="text-align:center">Review Mistakes</h1>' +
        '<p class="results-sub" style="text-align:center">' +
        mistakes.length +
        " question" +
        (mistakes.length !== 1 ? "s" : "") +
        " to learn from</p>" +
        inner +
        "</div>"
    );

    if (mistakes.length) {
      const p = wrap.querySelector('[data-act="practice"]');
      if (p && onPractice) p.addEventListener("click", function () {
        onPractice(mistakes);
      });
    }
    const h = wrap.querySelector('[data-act="home"]');
    if (h && onHome) h.addEventListener("click", onHome);
    const b = wrap.querySelector('[data-act="back"]');
    if (b && onBack) b.addEventListener("click", onBack);

    container.innerHTML = "";
    container.appendChild(wrap);
  }

  function optionText(q, label) {
    const opt = q.options.find(function (o) {
      return o.label === label;
    });
    return opt ? opt.text : label;
  }

  global.Results = {
    renderResults: renderResults,
    renderReview: renderReview,
  };
})(window);
