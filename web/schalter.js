// Sprachschalter der Kundschaft: merkt die Wahl fuer den Waehler (WIE_MACH_ICH_SPRACHEN.md, Abschnitt 5).
// Als Datei statt inline, damit die Seite ohne Inline-Skript auskommt (CSP script-src 'self').
(function () {
  var a = document.querySelectorAll("a.sprache[hreflang]");
  for (var i = 0; i < a.length; i++) {
    a[i].addEventListener("click", function () {
      try { localStorage.setItem("sprache", this.getAttribute("hreflang")); } catch (e) {}
      this.href = this.getAttribute("href").split("#")[0] + location.hash;
    });
  }
})();
