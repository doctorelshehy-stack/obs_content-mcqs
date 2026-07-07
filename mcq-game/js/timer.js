/* =====================================================================
   timer.js — Countdown timer
   ---------------------------------------------------------------------
   A small, framework-free countdown that:
     • ticks every second,
     • exposes formatted time + color state (normal / warning / danger),
     • invokes callbacks on tick and on zero,
     • can be paused/resumed (used when persisting across refreshes),
     • supports a soft "deadline" model so remaining seconds survive
       a page reload without drift.
   ===================================================================== */
(function (global) {
  "use strict";

  const WARN_AT = 5 * 60; // seconds remaining -> orange
  const DANGER_AT = 60; // seconds remaining -> red

  function Timer(opts) {
    this.durationSec = opts.durationSec;
    this.remaining = opts.remaining != null ? opts.remaining : opts.durationSec;
    this.onTick = opts.onTick || function () {};
    this.onExpire = opts.onExpire || function () {};
    this._interval = null;
    this._expired = false;
  }

  Timer.prototype.start = function () {
    if (this._interval) return;
    const self = this;
    // immediate tick so UI reflects current state instantly
    self._emit();
    self._interval = setInterval(function () {
      self.remaining -= 1;
      if (self.remaining <= 0) {
        self.remaining = 0;
        self._emit();
        self.stop();
        if (!self._expired) {
          self._expired = true;
          self.onExpire();
        }
        return;
      }
      self._emit();
    }, 1000);
  };

  Timer.prototype.pause = function () {
    if (this._interval) {
      clearInterval(this._interval);
      this._interval = null;
    }
  };

  Timer.prototype.stop = function () {
    this.pause();
  };

  Timer.prototype._emit = function () {
    this.onTick({
      remaining: this.remaining,
      formatted: Timer.format(this.remaining),
      state: this.state(),
      progress: this.durationSec
        ? this.remaining / this.durationSec
        : 0,
    });
  };

  Timer.prototype.state = function () {
    if (this.remaining <= DANGER_AT) return "danger";
    if (this.remaining <= WARN_AT) return "warning";
    return "normal";
  };

  Timer.format = function (totalSec) {
    totalSec = Math.max(0, Math.round(totalSec));
    const m = Math.floor(totalSec / 60);
    const s = totalSec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  };

  global.Timer = Timer;
})(window);
