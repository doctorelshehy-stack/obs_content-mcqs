/* =====================================================================
   results.js — Results screen + Review (mistakes) viewer
   ---------------------------------------------------------------------
   • renderResults: full scorecard with the 12 requested statistics and
     working Review / Restart / Back-Home buttons.
   • renderReview: a one-mistake-at-a-time viewer with Previous / Next /
     Practice navigation. Shows the question, the user's (red) answer,
     the correct (green) answer, and the explanation when available.
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

  /** Render the results card. `actions` = { onReview, onRestart, onHome }. */
  function renderResults(container, result, actions) {
    const color = ringColor(result.scorePct);
    const card = UI.elFromHTML(
      '<div class="results-card fade-in">' +
        '<h1 class="results-title">Exam Finished 🎉</h1>' +
        '<p class="results-sub">' +
        (result.finishedReason === "time"
          ? "Time ran out — exam auto-submitted."
          : "You completed every presented question.") +
        "</p>" +
        '<div class="score-ring" style="--ring-color:' +
        color +
        ";--p:" +
        result.scorePct +
        '">' +
        '<div class="score-ring-inner">' +
        '<div class="score-pct">' +
        result.scorePct +
        '%</div><div class="score-label">Final Score</div></div></div>' +
        '<div class="stat-grid">' +
        statBox("plain", result.bankSize, "Question Bank") +
        statBox("plain", result.presented, "Presented") +
        statBox("plain", result.answered, "Answered") +
        statBox("correct", result.correct, "Correct") +
        statBox("wrong", result.wrong, "Wrong") +
        statBox("skipped", result.skipped, "Presented & Skipped") +
        statBox("accuracy", result.accuracy + "%", "Accuracy") +
        statBox("plain", result.scorePct + "%", "Final Score") +
        statBox("plain", result.completion + "%", "Completion") +
        statBox("plain", fmtTime(result.timeUsedSec), "Time Used") +
        statBox("plain", fmtTime(result.timeRemainingSec), "Time Remaining") +
        statBox("plain", result.neverPresented, "Never Presented") +
        "</div>" +
        '<div class="results-actions">' +
        '<button class="btn btn-ghost btn-block" data-act="review">❌ Review Mistakes</button>' +
        '<button class="btn btn-primary btn-block" data-act="restart">🔄 Restart Exam</button>' +
        '<button class="btn btn-ghost btn-block" data-act="home">🏠 Back Home</button>' +
        "</div>" +
        "</div>"
    );

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

    container.innerHTML = "";
    container.appendChild(card);
  }

  /** Render the mistake-review viewer (one mistake at a time). */
  function renderReview(container, mistakes, opts) {
    opts = opts || {};
    const byId = global.Quiz.getAllQuestions().reduce(function (acc, q) {
      acc[q.id] = q;
      return acc;
    }, {});

    if (!mistakes.length) {
      container.innerHTML =
        '<div class="results-card" style="text-align:center">' +
        '<h1 class="results-title">Review Mistakes</h1>' +
        '<div class="review-empty"><span class="emoji">🎯</span>' +
        "<h3>No mistakes available.</h3>" +
        "<p>You have no incorrect answers to review yet.</p></div>" +
        '<div class="results-actions">' +
        '<button class="btn btn-primary btn-block" data-act="home">🏠 Back Home</button>' +
        "</div></div>";
      const h = container.querySelector('[data-act="home"]');
      if (h && opts.onHome) h.addEventListener("click", opts.onHome);
      return;
    }

    let idx = 0;
    const total = mistakes.length;

    function optionText(q, label) {
      const o = q && q.options.find(function (x) {
        return x.label === label;
      });
      return o ? o.text : label;
    }

    function show() {
      const rec = mistakes[idx];
      const q = byId[rec.id];
      const correctText = optionText(q, rec.correctAnswer);
      const userText = rec.userAnswer ? optionText(q, rec.userAnswer) : "—";
      const explanation = q && q.justification ? q.justification : "";

      const card = UI.elFromHTML(
        '<div class="results-card fade-in" style="text-align:left">' +
          '<h1 class="results-title" style="text-align:center">Review Mistakes</h1>' +
          '<p class="results-sub" style="text-align:center">Mistake ' +
          (idx + 1) +
          " of " +
          total +
          "</p>" +
          '<div class="review-item">' +
          "<h4>" +
          UI.escapeHtml(rec.question || (q ? q.question : "")) +
          "</h4>" +
          '<div class="review-row user"><span class="tag">Your answer</span><span>' +
          UI.escapeHtml((rec.userAnswer ? rec.userAnswer.toUpperCase() + ") " : "") + userText) +
          "</span></div>" +
          '<div class="review-row answer"><span class="tag">Correct</span><span>' +
          UI.escapeHtml(rec.correctAnswer.toUpperCase() + ") " + correctText) +
          "</span></div>" +
          (explanation
            ? '<div class="review-explain"><b>Explanation:</b> ' +
              UI.escapeHtml(explanation) +
              "</div>"
            : "") +
          "</div>" +
          '<div style="display:flex;gap:10px;margin-top:8px">' +
          '<button class="btn btn-ghost" data-act="prev">← Previous</button>' +
          '<button class="btn btn-ghost" data-act="next">Next →</button>' +
          "</div>" +
          '<div class="results-actions" style="margin-top:12px">' +
          '<button class="btn btn-primary btn-block" data-act="practice">🎯 Practice Mistakes</button>' +
          '<button class="btn btn-ghost btn-block" data-act="home">🏠 Back Home</button>' +
          "</div>" +
          "</div>"
      );

      const prev = card.querySelector('[data-act="prev"]');
      const next = card.querySelector('[data-act="next"]');
      prev.disabled = idx === 0;
      next.disabled = idx === total - 1;
      prev.addEventListener("click", function () {
        if (idx > 0) {
          idx -= 1;
          show();
        }
      });
      next.addEventListener("click", function () {
        if (idx < total - 1) {
          idx += 1;
          show();
        }
      });
      const pr = card.querySelector('[data-act="practice"]');
      if (pr && opts.onPractice) pr.addEventListener("click", opts.onPractice);
      const ho = card.querySelector('[data-act="home"]');
      if (ho && opts.onHome) ho.addEventListener("click", opts.onHome);

      container.innerHTML = "";
      container.appendChild(card);
    }

    show();
  }

  global.Results = {
    renderResults: renderResults,
    renderReview: renderReview,
  };
})(window);
