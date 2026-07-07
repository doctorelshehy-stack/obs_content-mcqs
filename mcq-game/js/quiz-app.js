/* =====================================================================
   quiz-app.js — Quiz page controller
   ---------------------------------------------------------------------
   Responsibilities:
     • read mode/duration from the URL (fresh start) OR resume an
       in-progress session from LocalStorage (refresh),
     • build the question pool (all questions, or only mistakes),
     • drive the Quiz engine, updating the top bar + timer,
     • show results on finish, and route the result-screen buttons
       (Review Mistakes / Restart / Back Home / Practice Wrong).
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
    let view = "quiz"; // "quiz" | "results" | "review"

    /* ---------- Build the question pool ---------- */
    function buildPool(mode) {
      if (mode === "review") {
        const list = Quiz.getMistakeQuestions();
        if (!list.length) {
          UI.toast("No mistakes available yet. Complete at least one exam first.");
          setTimeout(function () {
            goHome();
          }, 1400);
          return null;
        }
        return list;
      }
      return Quiz.getAllQuestions();
    }

    /* ---------- Top bar + timer rendering ---------- */
    function updateTopbar(info) {
      if (info && info.type === "tick") {
        timerText.textContent = info.timer.formatted;
        timerEl.classList.toggle("warning", info.timer.state === "warning");
        timerEl.classList.toggle("danger", info.timer.state === "danger");
      }
      const total = engine.total();
      const answered = engine.answeredCount();
      const pct = total ? Math.round((answered / total) * 100) : 0;
      progNow.textContent = Math.min(answered + 1, total);
      progTotal.textContent = total;
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
      quizView.style.display = "none";
      resultsView.style.display = "flex";
      global.Results.renderResults(resultsHost, result, {
        onReview: function () {
          showReview("results");
        },
        onRestart: function () {
          // Restart a fresh exam with the same duration + mode.
          const params = new URLSearchParams({
            mode: result.mode === "review" ? "review" : "exam",
            duration: engine.durationSec,
          });
          window.location.href = "quiz.html?" + params.toString();
        },
        onHome: goHome,
      });
      window.scrollTo(0, 0);
    }

    /* ---------- Review mistakes screen ---------- */
    function showReview(from) {
      view = "review";
      quizView.style.display = "none";
      resultsView.style.display = "flex";
      global.Results.renderReview(
        resultsHost,
        function (/* mistakes */) {
          // Practice Wrong Answers -> launch a fresh review exam
          const params = new URLSearchParams({
            mode: "review",
            duration: engine ? engine.durationSec : 30 * 60,
          });
          window.location.href = "quiz.html?" + params.toString();
        },
        goHome,
        function () {
          if (from === "results" && Storage.results.load()) {
            showResults(Storage.results.load());
          } else {
            goHome();
          }
        }
      );
      window.scrollTo(0, 0);
    }

    function goHome() {
      window.location.href = "index.html";
    }

    /* ---------- Quit confirmation ---------- */
    quitBtn.addEventListener("click", function () {
      if (view !== "quiz") return;
      UI.confirmDialog({
        title: "Quit exam?",
        message:
          "Your progress for this attempt will be lost. Are you sure you want to leave?",
        confirmText: "Quit",
        cancelText: "Keep going",
        danger: true,
      }).then(function (ok) {
        if (ok) {
          if (engine) engine.finished = true, engine.timer && engine.timer.stop();
          Storage.session.clear();
          goHome();
        }
      });
    });

    /* ---------- Boot ---------- */
    function boot() {
      // 1) Resume an in-progress session if present.
      const saved = Storage.session.load();
      const url = new URLSearchParams(window.location.search);

      if (saved && saved.order && saved.order.length) {
        const pool = Quiz.getAllQuestions(); // full index for restoration
        engine = Quiz.create({
          mode: saved.mode,
          durationSec: saved.durationSec,
          questions: pool,
          onUpdate: function (info) {
            if (info.type === "render") renderQuestion();
            else updateTopbar(info);
          },
          onAnswer: function () {},
          onFinish: showResults,
        });
        engine.start(saved);
        // If the saved session was already fully answered (edge), finish.
        if (engine.answeredCount() >= engine.total()) {
          engine.finish("complete");
          return;
        }
        renderQuestion();
        return;
      }

      // 2) Fresh start from URL params.
      const mode = url.get("mode") === "review" ? "review" : "exam";
      const duration = parseInt(url.get("duration"), 10) || 30 * 60;
      const pool = buildPool(mode);
      if (!pool) return; // buildPool already redirected home

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
