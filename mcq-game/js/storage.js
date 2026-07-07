/* =====================================================================
   storage.js — LocalStorage persistence layer
   ---------------------------------------------------------------------
   Responsibilities:
     • Save / load / clear the in-progress exam session (so a refresh
       resumes automatically).
     • Maintain the persistent mistake database (dedup by question id).
     • Persist small user settings (last chosen duration, theme).
   All reads are defensive: a corrupt value never throws.
   ===================================================================== */
(function (global) {
  "use strict";

  const KEYS = {
    session: "mcq.session",
    mistakes: "mcq.mistakes",
    settings: "mcq.settings",
    lastResults: "mcq.lastResults",
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
    } catch (e) {
      /* ignore */
    }
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

  /* ---------- Mistakes database ---------- */
  const mistakes = {
    /** Returns the array of mistake records (oldest first). */
    getAll() {
      const arr = safeGet(KEYS.mistakes);
      return Array.isArray(arr) ? arr : [];
    },

    /** Number of stored mistakes (unique question ids). */
    count() {
      return this.getAll().length;
    },

    /**
     * Merge a list of new mistake records into the database.
     * Each record: { id, userAnswer, correctAnswer, question, topic, ts }
     * Dedup by question id — a newer attempt overwrites the old one,
     * so the database always reflects the most recent wrong answer.
     */
    add(records) {
      if (!Array.isArray(records) || records.length === 0) return this.getAll();
      const map = new Map();
      // seed with existing records (kept in insertion order)
      this.getAll().forEach((r) => map.set(r.id, r));
      records.forEach((r) => {
        if (!r || !r.id) return;
        map.set(r.id, r);
      });
      const merged = [...map.values()];
      safeSet(KEYS.mistakes, merged);
      return merged;
    },

    /** Remove a single question id from the mistake database. */
    remove(id) {
      const filtered = this.getAll().filter((r) => r.id !== id);
      safeSet(KEYS.mistakes, filtered);
      return filtered;
    },

    /** Wipe everything (used by "restart" / settings). */
    clear() {
      safeRemove(KEYS.mistakes);
    },
  };

  /* ---------- Last results (for quick "view again") ---------- */
  const results = {
    save(data) {
      return safeSet(KEYS.lastResults, data);
    },
    load() {
      return safeGet(KEYS.lastResults);
    },
    clear() {
      safeRemove(KEYS.lastResults);
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

  global.Storage = { session, mistakes, results, settings };
})(window);
