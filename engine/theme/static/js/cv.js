// Vanilla JS on
(function() {
  window.onload = function(event) {
    var dom = {
      body: document.querySelector('body'),
      en_cv: document.querySelector('#cv-en'),
      ru_cv: document.querySelector('#cv-ru'),
      en_toggler: document.querySelector('#cv-en-toggler'),
      ru_toggler: document.querySelector('#cv-ru-toggler'),
      highlighter: {
        outer: document.querySelector('#cv-highlighter'),
        inner: document.querySelector('#cv-highlighter u')
      },
      essences: document.querySelectorAll('.essence'),
      as_pdf: document.querySelector('#cv-download-pdf-link'),
      age: document.querySelectorAll('.my-info.-age'),
      current_year: document.querySelectorAll('.meta.-current-year')
    };

    (function init() {
      var url = document.createElement('a');
      url.href = window.location.href;
      if (url.hash === '#ru') {
        show_ru_cv();
      } else {
        show_en_cv();
      }
      [].forEach.call(dom.age, function(age) {
        age.textContent = calculateAge(6, 30, 1993);
      });
      [].forEach.call(dom.current_year, function(year) {
        var date = new Date();
        year.textContent = date.getFullYear();
      });
    })();

    dom.en_toggler.onclick = function(event) {
      show_en_cv();
    };

    dom.ru_toggler.onclick = function(event) {
      show_ru_cv();
    };

    dom.highlighter.outer.onclick = function(event) {
      event.preventDefault();
      highlight_essences(!dom.highlighter.outer.classList.contains('-active'));
      return false;
    };

    function show_en_cv() {
      document.title = 'Dmitry Kharitonov';

      dom.en_cv.style.display = '';
      dom.ru_cv.style.display = 'none';

      dom.en_toggler.classList.add('-active');
      dom.ru_toggler.classList.remove('-active');

      dom.highlighter.inner.textContent = dom.highlighter.outer.dataset.entext;

      dom.as_pdf.textContent = dom.as_pdf.dataset.entext;
      dom.as_pdf.href = dom.as_pdf.dataset.enlink;

      highlight_essences(false);
    }

    function show_ru_cv() {
      document.title = 'Дмитрий Харитонов';

      dom.ru_cv.style.display = '';
      dom.en_cv.style.display = 'none';

      dom.ru_toggler.classList.add('-active');
      dom.en_toggler.classList.remove('-active');

      dom.highlighter.inner.textContent = dom.highlighter.outer.dataset.rutext;

      dom.as_pdf.textContent = dom.as_pdf.dataset.rutext;
      dom.as_pdf.href = dom.as_pdf.dataset.rulink;

      highlight_essences(false);
    }

    function highlight_essences(enable) {
      if (enable) {
        dom.highlighter.outer.classList.add('-active');
        for (var i = 0; i < dom.essences.length; i++) {
          dom.essences[i].classList.add('-active');
        }
        dom.body.classList.add('-highlight');
      } else {
        dom.highlighter.outer.classList.remove('-active');
        for (var i = 0; i < dom.essences.length; i++) {
          dom.essences[i].classList.remove('-active');
        }
        dom.body.classList.remove('-highlight');
      }
    }

    function calculateAge(birthMonth, birthDay, birthYear) {
      var todayDate = new Date();
      var todayYear = todayDate.getFullYear();
      var todayMonth = todayDate.getMonth();
      var todayDay = todayDate.getDate();
      var age = todayYear - birthYear;

      if (todayMonth < birthMonth - 1) {
        age--;
      }

      if (birthMonth - 1 == todayMonth && todayDay < birthDay) {
        age--;
      }
      return age;
    }
  };
})();
// Vanilla JS off