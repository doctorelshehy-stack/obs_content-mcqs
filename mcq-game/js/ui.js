/* =====================================================================
   ui.js — DOM helpers, modal, toast, escape util
   ---------------------------------------------------------------------
   Small reusable UI utilities shared by the home page and quiz page.
   Keeps the other modules free of boilerplate.
   ===================================================================== */
(function (global) {
  "use strict";

  /** Escape text for safe insertion as HTML text content. */
  function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  /** querySelector shorthand scoped to an optional root. */
  function $(sel, root) {
    return (root || document).querySelector(sel);
  }
  function $all(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /** Build an element from an HTML string (returns first child). */
  function elFromHTML(html) {
    const tpl = document.createElement("template");
    tpl.innerHTML = html.trim();
    return tpl.content.firstElementChild;
  }

  /* ---------- Toast ---------- */
  let toastTimer = null;
  function toast(message, ms) {
    ms = ms || 2200;
    let t = $("#toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.className = "toast";
      t.setAttribute("role", "status");
      t.setAttribute("aria-live", "polite");
      document.body.appendChild(t);
    }
    t.textContent = message;
    // force reflow so the transition replays even for repeated messages
    void t.offsetWidth;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      t.classList.remove("show");
    }, ms);
  }

  /* ---------- Modal factory ----------
     Creates a modal bound to an overlay element. Returns controls:
       open(), close(), setContent(node|html)
     The overlay markup is expected to look like:
       <div class="modal-overlay" id="...">
         <div class="modal" role="dialog" aria-modal="true"></div>
       </div>
  */
  function createModal(overlayEl) {
    const overlay = overlayEl;
    const box = overlay.querySelector(".modal");
    let lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      overlay.classList.add("open");
      overlay.setAttribute("aria-hidden", "false");
      // focus first focusable element
      const focusable = box.querySelector(
        "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
      );
      if (focusable) focusable.focus();
      document.addEventListener("keydown", onKey);
    }
    function close() {
      overlay.classList.remove("open");
      overlay.setAttribute("aria-hidden", "true");
      document.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function onKey(e) {
      if (e.key === "Escape") {
        // allow listeners to decide; default closes
        if (overlay._onEsc !== false) close();
      }
    }
    // click outside the modal box closes it
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay && overlay._backdropClose !== false) close();
    });

    return {
      overlay: overlay,
      box: box,
      open: open,
      close: close,
      setHTML: function (html) {
        box.innerHTML = html;
      },
      setContent: function (node) {
        box.innerHTML = "";
        box.appendChild(node);
      },
      isOpen: function () {
        return overlay.classList.contains("open");
      },
    };
  }

  /* ---------- Confirm dialog (uses a modal overlay) ----------
     opts: { title, message, confirmText, cancelText, danger }
     returns a Promise<boolean>
  */
  function confirmDialog(opts) {
    return new Promise(function (resolve) {
      let overlay = $("#confirmOverlay");
      if (!overlay) {
        overlay = elFromHTML(
          '<div class="modal-overlay" id="confirmOverlay" aria-hidden="true">' +
            '<div class="modal" role="dialog" aria-modal="true"></div></div>'
        );
        document.body.appendChild(overlay);
      }
      const modal = createModal(overlay);
      modal.setHTML(
        '<h3 class="modal-title">' +
          escapeHtml(opts.title || "Are you sure?") +
          "</h3>" +
          '<p class="confirm-text">' +
          escapeHtml(opts.message || "") +
          "</p>" +
          '<div class="modal-actions">' +
          '<button class="btn btn-ghost" data-act="cancel">' +
          escapeHtml(opts.cancelText || "Cancel") +
          "</button>" +
          '<button class="btn ' +
          (opts.danger ? "btn-danger" : "btn-primary") +
          '" data-act="ok">' +
          escapeHtml(opts.confirmText || "Confirm") +
          "</button>" +
          "</div>"
      );
      modal.box.querySelector('[data-act="cancel"]').addEventListener(
        "click",
        function () {
          modal.close();
          resolve(false);
        }
      );
      modal.box.querySelector('[data-act="ok"]').addEventListener(
        "click",
        function () {
          modal.close();
          resolve(true);
        }
      );
      modal.open();
    });
  }

  global.UI = {
    escapeHtml: escapeHtml,
    $: $,
    $all: $all,
    elFromHTML: elFromHTML,
    toast: toast,
    createModal: createModal,
    confirmDialog: confirmDialog,
  };
})(window);
