/* =====================================================================
   app.js — Home page controller
   ---------------------------------------------------------------------
   Wires up:
     • Start Game  -> duration modal -> launch exam (all questions)
     • Review Mistakes -> (if any) duration modal -> launch review exam
                          (if none) friendly empty-state message
   Persists the chosen duration as a default for next time.
   ===================================================================== */
(function (global) {
  "use strict";

  const DURATIONS = [
    { min: 20, label: "20 Minutes", sub: "Quick drill" },
    { min: 30, label: "30 Minutes", sub: "Standard" },
    { min: 40, label: "40 Minutes", sub: "Deep focus" },
    { min: 60, label: "60 Minutes", sub: "Full mock" },
  ];

  document.addEventListener("DOMContentLoaded", function () {
    const UI = global.UI;
    const $ = UI.$;

    const startBtn = $("#startBtn");
    const reviewBtn = $("#reviewBtn");
    const statsEl = $("#homeStats");
    const overlay = $("#durationOverlay");
    const grid = $("#durationGrid");
    const desc = $("#durationDesc");
    const cancelBtn = $("#durationCancel");
    const startModalBtn = $("#durationStart");
    const modal = UI.createModal(overlay);

    let pendingMode = null; // "exam" | "review"
    let selectedMin = global.Storage.settings.get().lastDuration || 30;

    /* ---- Home stats ---- */
    function refreshStats() {
      const total = global.Quiz.getAllQuestions().length;
      const wrong = global.Storage.mistakes.count();
      statsEl.innerHTML =
        '<span class="stat-chip"><strong>' +
        total +
        "</strong> questions</span>" +
        '<span class="stat-chip"><strong>' +
        wrong +
        "</strong> mistakes saved</span>";
    }

    /* ---- Duration modal ---- */
    function buildDurationGrid() {
      grid.innerHTML = DURATIONS.map(function (d) {
        const selected = d.min === selectedMin ? " selected" : "";
        return (
          '<button class="duration-btn' +
          selected +
          '" role="radio" aria-checked="' +
          (d.min === selectedMin) +
          '" data-min="' +
          d.min +
          '">' +
          d.label +
          "<small>" +
          d.sub +
          "</small></button>"
        );
      }).join("");

      UI.$all(".duration-btn", grid).forEach(function (btn) {
        btn.addEventListener("click", function () {
          selectedMin = parseInt(btn.dataset.min, 10);
          UI.$all(".duration-btn", grid).forEach(function (b) {
            const on = b === btn;
            b.classList.toggle("selected", on);
            b.setAttribute("aria-checked", on ? "true" : "false");
          });
          startModalBtn.focus();
        });
      });
    }

    function openDuration(mode) {
      pendingMode = mode;
      desc.textContent =
        mode === "review"
          ? "Practice only your incorrect questions."
          : "How long should the timer run?";
      buildDurationGrid();
      modal.open();
    }

    function launch() {
      const sec = selectedMin * 60;
      global.Storage.settings.set({ lastDuration: selectedMin });
      // Hand off to the quiz page via the URL.
      const params = new URLSearchParams({
        mode: pendingMode,
        duration: sec,
      });
      modal.close();
      window.location.href = "quiz.html?" + params.toString();
    }

    /* ---- Wire buttons ---- */
    startBtn.addEventListener("click", function () {
      openDuration("exam");
    });

    reviewBtn.addEventListener("click", function () {
      const wrong = global.Storage.mistakes.count();
      if (wrong === 0) {
        UI.toast("No mistakes available yet. Complete at least one exam first.");
        return;
      }
      openDuration("review");
    });

    cancelBtn.addEventListener("click", function () {
      modal.close();
    });
    startModalBtn.addEventListener("click", function () {
      if (pendingMode === "review" && global.Storage.mistakes.count() === 0) {
        UI.toast("No mistakes available yet.");
        modal.close();
        return;
      }
      launch();
    });

    refreshStats();
  });
})(window);
