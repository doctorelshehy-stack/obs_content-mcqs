/* =====================================================================
   quiz.js — Quiz engine
   ---------------------------------------------------------------------
   Owns the run-time state of a single exam attempt:
     • builds a question pool (all / mistakes-only),
     • Fisher–Yates shuffle so every question appears once per attempt,
     • renders ONE question at a time (perf-friendly),
     • records the answer, plays the selection animation, locks the
       question, and auto-advances after ~450ms (no Next button),
     • tracks mistakes and persists the session to LocalStorage so a
       refresh resumes exactly where the user left off,
     • finishes when time expires OR all questions are answered.
   ===================================================================== */
(function (global) {
  "use strict";

  const AUTO_ADVANCE_MS = 450; // sweet spot between "fast" and "readable"
  const ADVANCE_KEYS = ["1", "2", "3", "4", "5", "a", "A", "b", "B", "c", "C", "d", "D", "e", "E"];

  /* ---------- Data access ----------
     The source of truth is the global QUESTIONS_DATA produced by
     questions-data.js (the same data the reference dashboard uses).
     Questions are parsed dynamically — their text is never rewritten. */
  function getAllQuestions() {
    let all = [];
    try {
      all = (global.QUESTIONS_DATA && global.QUESTIONS_DATA.questions) || [];
    } catch (e) {
      all = [];
    }
    // Keep only answerable MCQs (must have options + a known correct answer)
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

  /** Map a question id -> the full question object (for review lookups). */
  function indexById() {
    const map = {};
    getAllQuestions().forEach(function (q) {
      map[q.id] = q;
    });
    return map;
  }

  /** Build a pool of mistakes (question objects) from the mistake DB. */
  function getMistakeQuestions() {
    const byId = indexById();
    return global.Storage.mistakes.getAll().map(function (m) {
      return byId[m.id];
    }).filter(Boolean);
  }

  /* ---------- Fisher–Yates shuffle (pure, returns a new array) ---------- */
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

  /* ---------- Engine ---------- */
  function Quiz(opts) {
    opts = opts || {};
    this.mode = opts.mode || "exam"; // "exam" | "review"
    this.durationSec = opts.durationSec || 30 * 60;
    this.questions = opts.questions || []; // ordered list of question objects
    this.answers = opts.answers || {}; // id -> { selected, correct }
    this.index = opts.index || 0;
    this.timer = null;
    this.finished = false;
    this._advanceTimer = null;
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

  /** Persist current progress so a refresh can resume. */
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
    });
  };

  Quiz.prototype._restoreQuestions = function (orderIds) {
    const byId = indexById();
    const restored = [];
    orderIds.forEach(function (id) {
      if (byId[id]) restored.push(byId[id]);
    });
    // The saved order is the source of truth; only include questions that
    // still exist in the bank. (Questions removed from the bank are dropped.)
    return restored;
  };

  /**
   * Start (or resume) the exam.
   * If `resumeState` is provided, the engine restores order/answers/index.
   */
  Quiz.prototype.start = function (resumeState) {
    const self = this;
    if (resumeState && resumeState.order) {
      this.questions = this._restoreQuestions(resumeState.order);
      this.answers = resumeState.answers || {};
      this.index = Math.min(resumeState.index || 0, this.questions.length - 1);
      this._startedAt = resumeState.startedAt || Date.now();
    } else {
      this.questions = shuffle(this.questions);
      this._startedAt = Date.now();
    }

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

  /** Render the current question into `container`. */
  Quiz.prototype.render = function (container) {
    const q = this.current();
    if (!q) return;
    const answered = this.answers[q.id];
    const UI = global.UI;

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
          (answered ? 'aria-disabled="true"' : 'aria-label="Option ' + UI.escapeHtml(o.label.toUpperCase()) + '"') +
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
        (this.mode === "review" ? "Review" : "Exam") +
        "</span>" +
        '<span class="q-tag topic">' +
        UI.escapeHtml(topicLabel) +
        "</span>" +
        '<span class="q-number">Q ' +
        (this.index + 1) +
        " / " +
        this.total() +
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

    // wire option clicks
    if (!answered) {
      const self = this;
      UI.$all(".opt", card).forEach(function (btn) {
        btn.addEventListener("click", function () {
          self_answer(self, q, btn.dataset.label, card);
        });
      });
    }

    container.innerHTML = "";
    container.appendChild(card);

    // keyboard support (only when not yet answered)
    if (!answered) this._bindKeys(card);
  };

  Quiz.prototype._bindKeys = function (card) {
    const self = this;
    const q = this.current();
    this._keyHandler = function (e) {
      if (self.answeredCount() && self.isAnswered(q.id)) return;
      const k = e.key;
      const idx = ADVANCE_KEYS.indexOf(k);
      if (idx === -1) return;
      const label = k.toLowerCase();
      const btn = card.querySelector('.opt[data-label="' + label + '"]');
      if (btn) {
        e.preventDefault();
        self_answer(self, q, label, card);
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
  function self_answer(self, q, label, card) {
    if (self.isAnswered(q.id) || self.finished) return;
    const isCorrect = label === q.answer;

    self.answers[q.id] = { selected: label, correct: q.answer };
    self._onAnswer({ id: q.id, selected: label, correct: q.answer, isCorrect: isCorrect });

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

    self.persist();
    self._onUpdate({ type: "progress" });

    // auto-advance (no Next button)
    clearTimeout(self._advanceTimer);
    self._advanceTimer = setTimeout(function () {
      self.next();
    }, AUTO_ADVANCE_MS);
  }

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

  /** Compute the per-question result set. */
  Quiz.prototype.computeResults = function () {
    let correct = 0;
    let wrong = 0;
    let skipped = 0;
    const mistakeRecords = [];
    const byId = indexById();

    this.questions.forEach(function (q) {
      const a = this.answers[q.id];
      if (!a) {
        skipped += 1;
        return;
      }
      if (a.selected === a.correct) {
        correct += 1;
      } else {
        wrong += 1;
        mistakeRecords.push({
          id: q.id,
          userAnswer: a.selected,
          correctAnswer: a.correct,
          question: q.question,
          topic: q.topic,
          ts: Date.now(),
        });
      }
    }, this);

    const total = this.questions.length;
    const attempted = correct + wrong;
    const scorePct = total ? Math.round((correct / total) * 100) : 0;
    const accuracy = attempted ? Math.round((correct / attempted) * 100) : 0;
    const timeUsed = this.durationSec - (this.timer ? this.timer.remaining : this.durationSec);

    return {
      mode: this.mode,
      total: total,
      correct: correct,
      wrong: wrong,
      skipped: skipped,
      scorePct: scorePct,
      accuracy: accuracy,
      timeUsedSec: timeUsed,
      finishedReason: this._finishReason || "complete",
      mistakeRecords: mistakeRecords,
    };
  };

  /** End the exam and hand results to the finish callback. */
  Quiz.prototype.finish = function (reason) {
    if (this.finished) return;
    this.finished = true;
    this._finishReason = reason;
    this._unbindKeys();
    clearTimeout(this._advanceTimer);
    if (this.timer) this.timer.stop();

    const result = this.computeResults();
    // Persist the mistake database (dedup handled inside storage)
    if (result.mistakeRecords.length) {
      global.Storage.mistakes.add(result.mistakeRecords);
    }
    // clear the in-progress session; the attempt is over
    global.Storage.session.clear();
    global.Storage.results.save(result);

    this._onFinish(result);
  };

  /* ---------- small helpers ---------- */
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
    shuffle: shuffle,
    topicName: topicName,
  };
})(window);
