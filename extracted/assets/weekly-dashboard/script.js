(function () {
  const cards = document.querySelectorAll('.week-card');
  cards.forEach(function (card) {
    const mainLink = card.querySelector('.card-main-link');
    if (!mainLink) return;
    mainLink.addEventListener('click', function (e) {
      const target = mainLink.getAttribute('href');
      if (!target) return;
      e.preventDefault();
      window.location.href = target;
    });
  });
})();
