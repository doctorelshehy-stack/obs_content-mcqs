/* =====================================================================
   quiz-app.js — Quiz page controller
   ---------------------------------------------------------------------
   • Boots from URL params (?mode=&duration=) OR resumes a saved session.
   • Builds the pool (unseen-first rotation, or the mistake pool for
     review/practice).
   • Drives the engine, updates the top bar + timer.
   • Routes the results buttons: Review (viewer) / Restart (fresh exam,
     mistakes kept) / Back Home (clears session).
   • Tears the engine down completely when the exam ends.
   ===================================================================== */
(function (global) {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    const UI = global.UI;
    const $ = UI.$;
    const Quiz = global.Quiz;
    const Storage = global.Storage;

    const quizView = $("#quizView");
    const resultsView = $("#resultsView");
    const resultsHost = $("#resultsHost");
    const body = $("#quizBody");

    const timerEl = $("#timer");
    const timerText = $("#timerText");
    const progNow = $("#progNow");
    const progTotal = $("#progTotal");
    const progPct = $("#progPct");
    const progFill = $("#progFill");
    const quitBtn = $("#quitBtn");

    let engine = null;
    let lastDuration = 30 * 60;
    let view = "quiz"; // "quiz" | "results" | "review"

    /* ---------- Build the question pool for a mode ---------- */
    function buildPoolForMode(mode) {
      if (mode === "review" || mode === "practice") {
        return Quiz.getMistakeQuestions();
      }
      return Quiz.buildExamPool(Quiz.getAllQuestions());
    }

    /* ---------- Top bar + timer ---------- */
    function updateTopbar(info) {
      if (info && info.type === "tick") {
        timerText.textContent = info.timer.formatted;
        timerEl.classList.toggle("warning", info.timer.state === "warning");
        timerEl.classList.toggle("danger", info.timer.state === "danger");
      }
      if (!engine) return;
      const bankSize = Quiz.getAllQuestions().length;
      const presented = engine.presentedCount;
      // Exam mode shows coverage of the whole bank; practice/review shows
      // progress through the (smaller) focused pool.
      const denom = engine.mode === "exam" ? bankSize : engine.total();
      progNow.textContent = presented;
      progTotal.textContent = denom;
      const pct = denom ? Math.round((presented / denom) * 100) : 0;
      progPct.textContent = pct + "%";
      progFill.style.width = pct + "%";
    }

    /* ---------- Render the question card ---------- */
    function renderQuestion() {
      engine.render(body);
      updateTopbar();
    }

    /* ---------- Finish -> results ---------- */
    function showResults(result) {
      view = "results";
      lastDuration = engine.durationSec;
      teardownEngine();
      quizView.style.display = "none";
      resultsView.style.display = "flex";
      global.Results.renderResults(resultsHost, result, {
        onReview: showReview,
        onRestart: function () {
          Storage.session.clear();
          window.location.href =
            "quiz.html?" +
            new URLSearchParams({ mode: "exam", duration: lastDuration }).toString();
        },
        onHome: goHome,
      });
      window.scrollTo(0, 0);
    }

    /* ---------- Review (mistakes) viewer ---------- */
    function showReview() {
      view = "review";
      quizView.style.display = "none";
      resultsView.style.display = "flex";
      global.Results.renderReview(resultsHost, Storage.mistakes.getAll(), {
        onPractice: function () {
          Storage.session.clear();
          window.location.href =
            "quiz.html?" +
            new URLSearchParams({ mode: "practice", duration: lastDuration }).toString();
        },
        onHome: goHome,
      });
      window.scrollTo(0, 0);
    }

    /* ---------- Empty / no-mistakes state (e.g. practice with 0 mistakes) ---------- */
    function showNoMistakes() {
      view = "review";
      quizView.style.display = "none";
      resultsView.style.display = "flex";
      global.Results.renderReview(resultsHost, [], { onHome: goHome });
      window.scrollTo(0, 0);
    }

    function goHome() {
      Storage.session.clear();
      window.location.href = "index.html";
    }

    /** Fully destroy the engine (no stale timers / listeners). */
    function teardownEngine() {
      if (engine) {
        if (engine.timer) engine.timer.stop();
        if (engine._unbindKeys) engine._unbindKeys();
        engine.finished = true;
      }
      engine = null;
    }

    /* ---------- Quit confirmation ---------- */
    quitBtn.addEventListener("click", function () {
      if (view !== "quiz" || !engine) return;
      UI.confirmDialog({
        title: "Quit exam?",
        message:
          "Your progress for this attempt will be lost. Are you sure you want to leave?",
        confirmText: "Quit",
        cancelText: "Keep going",
        danger: true,
      }).then(function (ok) {
        if (ok) {
          teardownEngine();
          goHome();
        }
      });
    });

    /* ---------- Boot ---------- */
    function boot() {
      const saved = Storage.session.load();
      const url = new URLSearchParams(window.location.search);

      // 1) Resume an in-progress session if present.
      if (saved && saved.order && saved.order.length) {
        engine = Quiz.create({
          mode: saved.mode,
          durationSec: saved.durationSec,
          questions: Quiz.getAllQuestions(), // full index for restoration
          onUpdate: function (info) {
            if (info.type === "render") renderQuestion();
            else updateTopbar(info);
          },
          onAnswer: function () {},
          onFinish: showResults,
        });
        engine.start(saved);
        if (engine.answeredCount() >= engine.presentedCount && engine.presentedCount > 0) {
          engine.finish("complete");
          return;
        }
        renderQuestion();
        return;
      }

      // 2) Fresh start from URL params.
      const mode =
        url.get("mode") === "practice" || url.get("mode") === "review"
          ? url.get("mode")
          : "exam";
      const duration = parseInt(url.get("duration"), 10) || 30 * 60;

      if (mode === "review" || mode === "practice") {
        const pool = buildPoolForMode(mode);
        if (!pool.length) {
          showNoMistakes();
          return;
        }
        engine = Quiz.create({
          mode: mode,
          durationSec: duration,
          questions: pool,
          onUpdate: function (info) {
            if (info.type === "render") renderQuestion();
            else updateTopbar(info);
          },
          onAnswer: function () {},
          onFinish: showResults,
        });
        engine.start(null);
        renderQuestion();
        return;
      }

      // 3) Standard exam (unseen-first rotation).
      engine = Quiz.create({
        mode: "exam",
        durationSec: duration,
        questions: buildExamPoolSafe(),
        onUpdate: function (info) {
          if (info.type === "render") renderQuestion();
          else updateTopbar(info);
        },
        onAnswer: function () {},
        onFinish: showResults,
      });
      engine.start(null);
      renderQuestion();
    }

    function buildExamPoolSafe() {
      try {
        return Quiz.buildExamPool(Quiz.getAllQuestions());
      } catch (e) {
        return Quiz.getAllQuestions();
      }
    }

    // Guard: if the data file failed to load, show a clear message.
    if (!global.QUESTIONS_DATA) {
      body.innerHTML =
        '<div class="review-empty"><span class="emoji">⚠️</span>' +
        "<h3>Question bank could not load.</h3>" +
        "<p>Check your connection and reload.</p></div>";
      return;
    }

    boot();
  });
})(window);
