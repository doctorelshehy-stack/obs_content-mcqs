/* =====================================================================
   storage.js — LocalStorage persistence layer
   ---------------------------------------------------------------------
   Persistent stores:
     • session  — the in-progress exam (so a refresh resumes exactly).
     • mistakes — the mistake DB (dedup by id, with mastery tracking).
     • history  — per-question learning history (seen / counts).
     • results  — last finished exam summary (for quick re-view).
     • settings — small UI preferences (last duration, etc).
   All reads are defensive: a corrupt value never throws.
   ===================================================================== */
(function (global) {
  "use strict";

  const KEYS = {
    session: "mcq.session",
    mistakes: "mcq.mistakes",
    history: "mcq.history",
    results: "mcq.lastResults",
    settings: "mcq.settings",
  };

  function safeGet(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      console.warn("[storage] failed to read", key, e);
      return null;
    }
  }
  function safeSet(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      console.warn("[storage] failed to write", key, e);
      return false;
    }
  }
  function safeRemove(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {}
  }

  /* ---------- Session (active exam) ---------- */
  const session = {
    save(data) {
      return safeSet(KEYS.session, data);
    },
    load() {
      return safeGet(KEYS.session);
    },
    clear() {
      safeRemove(KEYS.session);
    },
    exists() {
      return !!localStorage.getItem(KEYS.session);
    },
  };

  /* ---------- Mistake database (with mastery tracking) ----------
     Each record:
       { id, userAnswer, correctAnswer, question, topic, ts,
         consecutiveCorrect }
     `consecutiveCorrect` counts successive correct answers in practice
     mode; the record is dropped once it reaches the mastery threshold. */
  const mistakes = {
    getAll() {
      const arr = safeGet(KEYS.mistakes);
      return Array.isArray(arr) ? arr : [];
    },
    count() {
      return this.getAll().length;
    },
    _save(arr) {
      return safeSet(KEYS.mistakes, arr);
    },
    /** Merge new wrong-answer records (dedup by id, reset mastery). */
    add(records) {
      const map = new Map();
      this.getAll().forEach((r) => map.set(r.id, r));
      (records || []).forEach((r) => {
        if (!r || !r.id) return;
        map.set(r.id, {
          id: r.id,
          userAnswer: r.userAnswer,
          correctAnswer: r.correctAnswer,
          question: r.question,
          topic: r.topic,
          ts: Date.now(),
          consecutiveCorrect: 0,
        });
      });
      const merged = [...map.values()];
      this._save(merged);
      return merged;
    },
    /** Called on a correct answer. Returns true if the record was removed. */
    markCorrect(id, threshold) {
      threshold = threshold || 2;
      const all = this.getAll();
      const i = all.findIndex((r) => r.id === id);
      if (i === -1) return false;
      const r = all[i];
      r.consecutiveCorrect = (r.consecutiveCorrect || 0) + 1;
      r.ts = Date.now();
      if (r.consecutiveCorrect >= threshold) {
        all.splice(i, 1);
        this._save(all);
        return true;
      }
      this._save(all);
      return false;
    },
    remove(id) {
      const filtered = this.getAll().filter((r) => r.id !== id);
      this._save(filtered);
      return filtered;
    },
    clear() {
      safeRemove(KEYS.mistakes);
    },
  };

  /* ---------- Per-question learning history ---------- */
  const history = {
    getAll() {
      const o = safeGet(KEYS.history);
      return o && typeof o === "object" ? o : {};
    },
    get(id) {
      return this.getAll()[id] || null;
    },
    _save(map) {
      return safeSet(KEYS.history, map);
    },
    _blank(id) {
      return {
        id: id,
        hasBeenSeen: false,
        lastSeenDate: null,
        correctCount: 0,
        wrongCount: 0,
        totalAttempts: 0,
      };
    },
    /** Mark a question as having been presented to the user. */
    markSeen(id) {
      const m = this.getAll();
      const r = m[id] || this._blank(id);
      r.hasBeenSeen = true;
      if (!r.lastSeenDate) r.lastSeenDate = new Date().toISOString();
      m[id] = r;
      this._save(m);
    },
    /** Record the outcome of an answer (correct / wrong). */
    record(id, isCorrect) {
      const m = this.getAll();
      const r = m[id] || this._blank(id);
      r.hasBeenSeen = true;
      if (!r.lastSeenDate) r.lastSeenDate = new Date().toISOString();
      r.totalAttempts = (r.totalAttempts || 0) + 1;
      if (isCorrect) r.correctCount = (r.correctCount || 0) + 1;
      else r.wrongCount = (r.wrongCount || 0) + 1;
      m[id] = r;
      this._save(m);
    },
    /** Number of questions marked seen at least once. */
    seenCount() {
      const m = this.getAll();
      return Object.keys(m).filter((k) => m[k].hasBeenSeen).length;
    },
    clear() {
      safeRemove(KEYS.history);
    },
  };

  /* ---------- Last results (for quick "view again") ---------- */
  const results = {
    save(data) {
      return safeSet(KEYS.results, data);
    },
    load() {
      return safeGet(KEYS.results);
    },
    clear() {
      safeRemove(KEYS.results);
    },
  };

  /* ---------- Settings ---------- */
  const settings = {
    get() {
      return safeGet(KEYS.settings) || {};
    },
    set(patch) {
      const next = Object.assign(this.get(), patch);
      safeSet(KEYS.settings, next);
      return next;
    },
  };

  global.Storage = { session, mistakes, history, results, settings };
})(window);
