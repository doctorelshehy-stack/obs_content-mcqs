/* =====================================================================
   quiz.js — Quiz engine
   ---------------------------------------------------------------------
   Owns the run-time state of a single exam attempt:
     • builds the question pool (unseen-first rotation / mistake pool),
     • tracks which questions were actually PRESENTED (rendered) so the
       score is computed only over presented questions,
     • records per-question history (seen / correct / wrong) and updates
       the mistake DB with mastery tracking,
     • renders ONE question at a time (perf-friendly),
     • auto-advances after ~450ms (no Next button),
     • finishes when time expires OR all presented questions are answered,
     • persists the session so a refresh resumes exactly.
   ===================================================================== */
(function (global) {
  "use strict";

  const AUTO_ADVANCE_MS = 450; // fast yet readable
  const MASTERY_THRESHOLD = 2; // correct-in-a-row to clear a mistake
  const ADVANCE_KEYS = [
    "1", "2", "3", "4", "5",
    "a", "A", "b", "B", "c", "C", "d", "D", "e", "E",
  ];

  /* ---------- Data access ----------
     QUESTIONS_DATA is the global produced by questions-data.js (the same
     data the reference dashboard uses). Questions are parsed at runtime
     and never rewritten; only answerable MCQs are kept. */
  function getAllQuestions() {
    let all = [];
    try {
      all = (global.QUESTIONS_DATA && global.QUESTIONS_DATA.questions) || [];
    } catch (e) {
      all = [];
    }
    return all.filter(function (q) {
      return (
        q &&
        q.type === "mcq" &&
        Array.isArray(q.options) &&
        q.options.length > 0 &&
        q.answer != null &&
        q.options.some(function (o) {
          return o.label === q.answer;
        })
      );
    });
  }

  function indexById() {
    const map = {};
    getAllQuestions().forEach(function (q) {
      map[q.id] = q;
    });
    return map;
  }

  /** Question objects for the current mistake list (for review/practice). */
  function getMistakeQuestions() {
    const byId = indexById();
    return global.Storage.mistakes.getAll().map(function (m) {
      return byId[m.id];
    }).filter(Boolean);
  }

  /* ---------- Fisher–Yates shuffle (pure) ---------- */
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  /* ---------- Exam pool with unseen-first rotation ----------
     Unseen questions come first (so the student always works through new
     material), then previously-seen questions. Because an exam only
     presents as many questions as time allows, the unseen ones are hit
     first; never-presented questions simply stay unseen for next time.
     Once every question has been seen, there are no unseen left and the
     pool falls back to a fresh full-bank shuffle (a new randomized pass). */
  function buildExamPool(bank) {
    const unseen = [];
    const seen = [];
    bank.forEach(function (q) {
      const h = global.Storage.history.get(q.id);
      if (h && h.hasBeenSeen) seen.push(q);
      else unseen.push(q);
    });
    return shuffle(unseen).concat(shuffle(seen));
  }

  /* ---------- Engine ---------- */
  function Quiz(opts) {
    opts = opts || {};
    this.mode = opts.mode || "exam"; // "exam" | "review" | "practice"
    this.durationSec = opts.durationSec || 30 * 60;
    this.questions = opts.questions || []; // already ordered pool
    this.answers = opts.answers || {}; // id -> { selected, correct }
    this.index = opts.index || 0;
    this.presentedCount = opts.presentedCount || 0; // # rendered so far
    this.timer = null;
    this.finished = false;
    this._startedAt = null;
    this._advanceTimer = null;
    this._finishReason = null;
    this._onUpdate = opts.onUpdate || function () {};
    this._onFinish = opts.onFinish || function () {};
    this._onAnswer = opts.onAnswer || function () {};
  }

  Quiz.prototype.total = function () {
    return this.questions.length;
  };

  Quiz.prototype.current = function () {
    return this.questions[this.index] || null;
  };

  Quiz.prototype.answeredCount = function () {
    return Object.keys(this.answers).length;
  };

  Quiz.prototype.isAnswered = function (id) {
    return Object.prototype.hasOwnProperty.call(this.answers, id);
  };

  /** Persist current progress (enables refresh-resume). */
  Quiz.prototype.persist = function () {
    global.Storage.session.save({
      mode: this.mode,
      durationSec: this.durationSec,
      order: this.questions.map(function (q) {
        return q.id;
      }),
      answers: this.answers,
      index: this.index,
      startedAt: this._startedAt,
      remaining: this.timer ? this.timer.remaining : this.durationSec,
      presentedCount: this.presentedCount,
    });
  };

  Quiz.prototype._restoreQuestions = function (orderIds) {
    const byId = indexById();
    const restored = [];
    orderIds.forEach(function (id) {
      if (byId[id]) restored.push(byId[id]);
    });
    // The saved order is the source of truth; only include questions that
    // still exist in the bank (removed questions are dropped).
    return restored;
  };

  /** Start (or resume) the exam. */
  Quiz.prototype.start = function (resumeState) {
    if (resumeState && resumeState.order) {
      this.questions = this._restoreQuestions(resumeState.order);
      this.answers = resumeState.answers || {};
      this.index = Math.min(resumeState.index || 0, this.questions.length - 1);
      this.presentedCount = resumeState.presentedCount || this.index + 1;
      this._startedAt = resumeState.startedAt || Date.now();
    } else {
      // Pool is already ordered by the caller (unseen-first or mistake pool).
      this.presentedCount = 0;
      this._startedAt = Date.now();
    }

    const self = this;
    this.timer = new global.Timer({
      durationSec: this.durationSec,
      remaining:
        resumeState && resumeState.remaining != null
          ? resumeState.remaining
          : this.durationSec,
      onTick: function (info) {
        self._onUpdate({ type: "tick", timer: info });
      },
      onExpire: function () {
        self.finish("time");
      },
    });

    this.timer.start();
    this.persist();
    this._onUpdate({ type: "render" });
  };

  /** Render the current question; mark it as presented + seen. */
  Quiz.prototype.render = function (container) {
    const q = this.current();
    if (!q) return;

    // This question is now presented to the user.
    this.presentedCount = Math.max(this.presentedCount, this.index + 1);
    global.Storage.history.markSeen(q.id);

    const UI = global.UI;
    const answered = this.answers[q.id];

    const optsHtml = q.options
      .map(function (o) {
        let cls = "opt";
        let fb = "";
        if (answered) {
          cls += " locked";
          if (o.label === answered.correct) {
            cls += " correct";
            fb = '<span class="feedback-icon" aria-hidden="true">✓</span>';
          } else if (o.label === answered.selected) {
            cls += " wrong";
            fb = '<span class="feedback-icon" aria-hidden="true">✕</span>';
          } else {
            cls += " reveal";
          }
        }
        return (
          '<button class="' +
          cls +
          '" data-label="' +
          UI.escapeHtml(o.label) +
          '" ' +
          (answered
            ? 'aria-disabled="true"'
            : 'aria-label="Option ' + UI.escapeHtml(o.label.toUpperCase()) + '"') +
          ">" +
          '<span class="opt-label">' +
          UI.escapeHtml(o.label.toUpperCase()) +
          "</span>" +
          '<span class="opt-text">' +
          UI.escapeHtml(o.text) +
          "</span>" +
          fb +
          "</button>"
        );
      })
      .join("");

    const topicLabel = topicName(q.topic);

    const card = UI.elFromHTML(
      '<section class="q-card" aria-live="polite">' +
        '<div class="q-meta">' +
        '<span class="q-tag">' +
        (this.mode === "exam" ? "Exam" : "Practice") +
        "</span>" +
        '<span class="q-tag topic">' +
        UI.escapeHtml(topicLabel) +
        "</span>" +
        '<span class="q-number">Q ' +
        (this.index + 1) +
        "</span>" +
        "</div>" +
        '<h2 class="q-text">' +
        UI.escapeHtml(q.question) +
        "</h2>" +
        '<div class="q-options" role="group" aria-label="Answer choices">' +
        optsHtml +
        "</div>" +
        "</section>"
    );

    if (!answered) {
      const self = this;
      UI.$all(".opt", card).forEach(function (btn) {
        btn.addEventListener("click", function () {
          self._answer(q, btn.dataset.label, card);
        });
      });
    }

    container.innerHTML = "";
    container.appendChild(card);

    if (!answered) this._bindKeys(card);
  };

  Quiz.prototype._bindKeys = function (card) {
    const self = this;
    const q = this.current();
    this._keyHandler = function (e) {
      if (self.answeredCount() && self.isAnswered(q.id)) return;
      const k = e.key;
      const label = k.toLowerCase();
      if (ADVANCE_KEYS.indexOf(k) === -1) return;
      const btn = card.querySelector('.opt[data-label="' + label + '"]');
      if (btn) {
        e.preventDefault();
        self._answer(q, label, card);
      }
    };
    document.addEventListener("keydown", this._keyHandler);
  };

  Quiz.prototype._unbindKeys = function () {
    if (this._keyHandler) {
      document.removeEventListener("keydown", this._keyHandler);
      this._keyHandler = null;
    }
  };

  /* ---------- Answer handling ---------- */
  Quiz.prototype._answer = function (q, label, card) {
    if (this.isAnswered(q.id) || this.finished) return;
    const isCorrect = label === q.answer;

    this.answers[q.id] = { selected: label, correct: q.answer };

    // Learning history + mistake DB (persisted immediately so a refresh
    // mid-exam never loses progress).
    global.Storage.history.record(q.id, isCorrect);
    if (isCorrect) {
      global.Storage.mistakes.markCorrect(q.id, MASTERY_THRESHOLD);
    } else {
      global.Storage.mistakes.add([
        {
          id: q.id,
          userAnswer: label,
          correctAnswer: q.answer,
          question: q.question,
          topic: q.topic,
        },
      ]);
    }

    this._onAnswer({ id: q.id, selected: label, correct: q.answer, isCorrect: isCorrect });

    // visual feedback
    const UI = global.UI;
    const chosen = card.querySelector('.opt[data-label="' + label + '"]');
    if (chosen) {
      chosen.classList.add(isCorrect ? "correct" : "wrong", "just-selected");
      if (chosen.querySelector(".feedback-icon") === null) {
        const fb = document.createElement("span");
        fb.className = "feedback-icon";
        fb.setAttribute("aria-hidden", "true");
        fb.textContent = isCorrect ? "✓" : "✕";
        chosen.appendChild(fb);
      }
      chosen.classList.add("locked");
    }
    UI.$all(".opt", card).forEach(function (b) {
      b.classList.add("locked");
      if (b.dataset.label === q.answer && b !== chosen) {
        b.classList.add("reveal");
        if (b.querySelector(".feedback-icon") === null) {
          const fb = document.createElement("span");
          fb.className = "feedback-icon";
          fb.setAttribute("aria-hidden", "true");
          fb.textContent = "✓";
          b.appendChild(fb);
        }
      }
    });

    this.persist();
    this._onUpdate({ type: "progress" });

    // auto-advance (no Next button)
    const self = this;
    clearTimeout(this._advanceTimer);
    this._advanceTimer = setTimeout(function () {
      self.next();
    }, AUTO_ADVANCE_MS);
  };

  Quiz.prototype.next = function () {
    this._unbindKeys();
    clearTimeout(this._advanceTimer);
    if (this.index >= this.questions.length - 1) {
      this.finish("complete");
      return;
    }
    const self = this;
    const body = global.UI.$(".quiz-body");
    const card = body && body.querySelector(".q-card");
    if (card) {
      card.classList.add("leaving");
      setTimeout(function () {
        self.index += 1;
        self.persist();
        self._onUpdate({ type: "render" });
      }, 300);
    } else {
      this.index += 1;
      this.persist();
      this._onUpdate({ type: "render" });
    }
  };

  /** Compute results over PRESENTED questions only. */
  Quiz.prototype.computeResults = function () {
    const presented = this.questions.slice(0, this.presentedCount);
    let correct = 0;
    let wrong = 0;
    let skipped = 0;
    let answered = 0;

    presented.forEach(function (q) {
      const a = this.answers[q.id];
      if (!a) {
        skipped += 1; // presented but never answered
        return;
      }
      answered += 1;
      if (a.selected === a.correct) correct += 1;
      else wrong += 1;
    }, this);

    const total = presented.length; // presented count (NOT the whole bank)
    const attempted = correct + wrong;
    const scorePct = total ? Math.round((correct / total) * 100) : 0;
    const accuracy = attempted ? Math.round((correct / attempted) * 100) : 0;
    const completion = total ? Math.round((answered / total) * 100) : 0;
    const timeUsed = this.durationSec - (this.timer ? this.timer.remaining : this.durationSec);
    const timeRemaining = this.timer ? this.timer.remaining : 0;
    const bankSize = getAllQuestions().length;
    const neverPresented = Math.max(0, bankSize - total);

    return {
      mode: this.mode,
      bankSize: bankSize,
      presented: total,
      answered: answered,
      correct: correct,
      wrong: wrong,
      skipped: skipped,
      scorePct: scorePct,
      accuracy: accuracy,
      completion: completion,
      timeUsedSec: timeUsed,
      timeRemainingSec: timeRemaining,
      neverPresented: neverPresented,
      finishedReason: this._finishReason || "complete",
    };
  };

  /** End the exam; destroy the session; report results. */
  Quiz.prototype.finish = function (reason) {
    if (this.finished) return;
    this.finished = true;
    this._finishReason = reason;
    this._unbindKeys();
    clearTimeout(this._advanceTimer);
    if (this.timer) this.timer.stop();

    const result = this.computeResults();
    // History + mistakes were already updated per answer; nothing to do here
    // except clear the in-progress session and stash the summary.
    global.Storage.session.clear();
    global.Storage.results.save(result);

    this._onFinish(result);
  };

  /* ---------- helpers ---------- */
  function topicName(key) {
    try {
      const t = global.QUESTIONS_DATA.topics;
      if (t && t[key] && t[key].label) return t[key].label;
    } catch (e) {}
    return key || "General";
  }

  global.Quiz = {
    create: function (opts) {
      return new Quiz(opts);
    },
    getAllQuestions: getAllQuestions,
    getMistakeQuestions: getMistakeQuestions,
    buildExamPool: buildExamPool,
    shuffle: shuffle,
    topicName: topicName,
    MASTERY_THRESHOLD: MASTERY_THRESHOLD,
  };
})(window);
