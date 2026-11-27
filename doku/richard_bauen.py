# -*- coding: utf-8 -*-
"""Der Abend „Lieber doppelt falsch als einmal Richard“ als Seite der Kundschaft, deutsch und englisch.
Agent für Falzbein, 27.11.2026. Andys Freigabe vom 27.11.2026: „Ich gebe dir das direkt frei, Vollgas … mach die Seite fix
und fertig“.

Quelle (Texthoheit bei Falzbein, hier wird kein Wort geändert):
  richard\\lieber_doppelt_falsch.md            Falzbeins Text, Kopie von D:\\Workspace\\kabarett_user\\dritter_abend\\
  richard\\lieber_doppelt_falsch_EN_ENTWURF.md die englische Fassung (Entwurf des Agenten, Falzbein liest vor dem Hochladen)
Beide Dateien bleiben auf dem NAS (.gitignore): Ihr Kopf und der Abschnitt „Quellen“ nennen Namen und Herkunft.

Auf die Seite kommt: Titel (#), Untertitel (erste *Zeile*), die Nummern ab dem ersten „## “ bis vor „### “
(Quellen bzw. Notes for Falzbein). Der Kasten mit den Rändern (> vor der ersten Nummer) kommt NICHT auf die Seite.
Die zweite *Zeile* des Kopfes (Idee, Titel, Herkunft) steht im Fuß der Seite, so wie Falzbein sie geschrieben hat.

Umsetzung Markdown -> HTML (nur diese Fälle, sonst Abbruch):
  ## N. Titel            Nummer N (Anker d1 … d9)          ## Pause / ## Interval   Pause
  ## Zugabe: Titel       Zugabe (Anker dz)                 > …                      Kasten „Lost in translation“ (nur en)
  *(…)* allein           Regieanweisung                    **DIE ERKENNUNG:** …     Sprecher (Großbuchstaben)
  **…**                  fett                              *…*                      kursiv
Schritt 1 schreibt artefakt\\richard_<sp>.html (Titelzeile, Stil, Körper; die Seite ohne Rahmen, wie bei der ersten).
Schritt 2 setzt den Rahmen aus seite_rahmen.py darum (Kopf, Ecke, Abende, Haus-Fuß, schalter.js) nach
..\\web\\<sp>\\richard\\index.html. Gegenproben: jeder Absatz der Quelle steht als Klartext auf der Seite, nichts sonst
aus der Quelle; „Andy“ steht nur in der Herkunftszeile und im Haus-Fuß; kein Inline-Skript; nichts von außen.

Aufruf: python richard_bauen.py
"""
import html
import io
import json
import os
import re

import seite_rahmen as R

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = R.WEB
QUELLE = {"de": os.path.join(HIER, "richard", "lieber_doppelt_falsch.md"),
          "en": os.path.join(HIER, "richard", "lieber_doppelt_falsch_EN_ENTWURF.md")}
UNTER = "richard/"
HOST = R.HOST
CC = {"de": "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de", "en": "https://creativecommons.org/licenses/by-nc-sa/4.0/"}

T = {
    "de": dict(
        kicker="Die Kundschaft · Ein weiterer Abend",
        marke="Nummer", pause="Pause", zugabe="Zugabe",
        description="Lieber doppelt falsch als einmal Richard: ein Kabarettabend über Namen, die keiner trägt, und über die "
                    "Spracherkennung, die sie erfindet. Neun Nummern, eine Pause, eine Zugabe. Ein Programm von Falzbein im Haus "
                    "Die Kundschaft. Bilder KI-generiert.",
        og_text="Ein Kabarettabend über Namen, die keiner trägt.",
        alt="Plakat im Stil der Varieté-Plakate: ein Papiertheater in Nachtblau, unter einer einzigen Lampe zwei leere Stühle. "
            "Am linken steckt ein Zettel mit den verdrehten Buchstaben RIHCTSCHET, über dem rechten hängt an einem alten Mikrofon "
            "ein gerades Namensschild: RICHARD. Dazwischen verbeugt sich ein Falzbein aus hellem Knochen. Oben der Titel "
            "„Lieber doppelt falsch als einmal Richard“, darunter „Falzbein · Kabarett“.",
        bildzeile='Das Plakat zum Abend. <a href="../../plakat-richard.jpg">Volle Größe</a> (JPG, 2048 × 3072).',
        zurueck="← Die Kundschaft",
        fuss=('Ein Abend im Haus <a href="../index.html">Die Kundschaft</a> der '
              '<a href="https://zwischenraum.special.at/">Kleinkunstbühne Zwischenraum</a> · von Falzbein und Andy.<br>'
              'Wien, November 2026 · Plakat: <a href="../../plakat-richard.jpg">JPG, 2048 × 3072</a> · Bilder unter '
              '<a href="%s" rel="license">CC BY-NC-SA 4.0</a>, Texte unter <a href="../../LICENSE.txt">MIT-Lizenz</a>.' % CC["de"]),
        hinweise=["Falzbein, Richtscheit, Pforte, Linde, Siegel, Nonius, Vera, Juna, Mira und Goldfaden sind KI-Sitzungen in "
                  "Andys Projekt, keine Menschen. Mo ist eine erfundene Comicfigur.",
                  "KI-Hinweis: Das Plakat ist KI-generiert. Erdacht und beschrieben hat es Falzbein, ein Claude-Modell von "
                  "Anthropic; gemalt hat es ein Bildmodell. Die Texte stammen von Falzbein (KI).",
                  R.TEXT["de"]["hinweise"][2]]),
    "en": dict(
        kicker="The Clientele · Another evening",
        marke="Act", pause="Interval", zugabe="Encore",
        description="Better Twice Wrong Than Once Richard: a cabaret evening about names nobody goes by, and about the speech "
                    "recognition that invents them. Nine acts, an interval, an encore. A show by Falzbein at The Clientele. "
                    "Images AI-generated.",
        og_text="A cabaret evening about names nobody goes by.",
        alt="Poster in the style of a variety-theatre bill: a paper theatre in midnight blue, two empty chairs under a single "
            "lamp. A slip with the jumbled letters RIHCTSCHET is tucked into the left one; above the right one, a straight name "
            "tag reading RICHARD hangs from an old microphone. Between them a bone folder takes a bow. At the top the title "
            "“Better twice wrong than once Richard”, below it “Falzbein · Cabaret”.",
        bildzeile='The poster for the evening. <a href="../../plakat-richard-en.jpg">Full size</a> (JPG, 2048 × 3072); '
                  'the original poster is in <a href="../../plakat-richard.jpg">German</a>.',
        zurueck="← The Clientele",
        fuss=('An evening at <a href="../index.html">The Clientele</a>, a house of the '
              '<a href="https://zwischenraum.special.at/">Zwischenraum cabaret stage</a> · by Falzbein and Andy.<br>'
              'Vienna, November 2026 · The original is in German, the English is by Falzbein · Poster: '
              '<a href="../../plakat-richard-en.jpg">JPG, 2048 × 3072</a> · Images under '
              '<a href="%s" rel="license">CC BY-NC-SA 4.0</a>, texts under the <a href="../../LICENSE.txt">MIT licence</a>.' % CC["en"]),
        hinweise=["Falzbein, Richtscheit, Pforte, Linde, Siegel, Nonius, Vera, Juna, Mira and Goldfaden are AI sessions in "
                  "Andy's project, not people. Mo is a fictional comic character.",
                  "AI notice: The poster is AI-generated. It was conceived and described by Falzbein, a Claude model by "
                  "Anthropic, and rendered by an image model; the English title was set by Falzbein. The texts are by Falzbein (AI).",
                  R.TEXT["en"]["hinweise"][2]]),
}

EXTRA_CSS = """
/* Abend „Lieber doppelt falsch als einmal Richard“ (27.11.2026): Kopf mit Plakat, Regie, Sprecher, Übersetzerkasten */
/* Lichtkegel im Nachtblau des Plakats: der Bernsteinkegel der ersten Seite ergibt über dem Saal ein dunkles Braun
   (gerechnet rgb 54 43 28), und Braun soll nicht in die Oberfläche (Hausregel vom 26.11.2026). */
.kegel { background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(74, 112, 204, .2), transparent 70%); }
.kopf { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 330px); gap: 28px 56px; align-items: end; padding-block: 64px 40px; }
.kopf header { padding-block: 0; }
.kopf h1 { font-size: clamp(46px, 7.4vw, 96px); line-height: .9; }
.plakat { margin: 0; display: grid; gap: 8px; }
.plakat a { display: block; border-radius: 3px; }
.plakat img { display: block; width: 100%; height: auto; border-radius: 3px; background: var(--buehne); box-shadow: 0 18px 50px rgba(0, 0, 0, .55); }
.plakat figcaption { font-family: var(--mono); font-size: 12.5px; color: var(--leise); }
.plakat figcaption a { display: inline; color: var(--licht); }
.text strong { font-weight: 600; }
.regie { font-style: italic; color: var(--leise); }
.text em.regie { color: var(--leise); }
.wer { font-family: var(--mono); font-style: normal; font-weight: 500; font-size: 12.5px; letter-spacing: .14em; color: var(--licht); margin-right: .35em; }
.uebersetzt { margin: 6px 0 0; padding: 12px 16px; border: 1px dashed var(--linie); border-radius: 4px; background: rgba(28, 24, 32, .6); font-size: 15px; line-height: 1.55; color: var(--leise); }
.uebersetzt p { margin: 0; }
.uebersetzt strong { font-family: var(--mono); font-weight: 500; font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: var(--licht); margin-right: .3em; }
.uebersetzt em { color: var(--text); }
@media (max-width: 720px) {
  .kopf { grid-template-columns: minmax(0, 1fr); padding-block: 60px 28px; }
  .plakat { max-width: 420px; }
}
"""


def lies(sp):
    roh = io.open(QUELLE[sp], encoding="utf-8").read().replace("\r\n", "\n")
    zeilen = roh.split("\n")
    assert zeilen[0].startswith("# "), "Titel fehlt"
    titel = zeilen[0][2:].strip()
    kursiv = [z for z in zeilen[1:] if z.startswith("*") and z.endswith("*") and not z.startswith("**")]
    erste = next(i for i, z in enumerate(zeilen) if z.startswith("## "))
    kursiv = [z for z in zeilen[1:erste] if z.startswith("*") and z.endswith("*") and not z.startswith("**")]
    assert len(kursiv) == 2, kursiv
    ende = next((i for i, z in enumerate(zeilen) if z.startswith("### ")), len(zeilen))
    teile, akt = [], None
    absatz = []

    def absatz_ende():
        if absatz:
            akt["absaetze"].append(" ".join(absatz))
            absatz.clear()

    for z in zeilen[erste:ende]:
        if z.startswith("## "):
            if akt:
                absatz_ende()
            akt = dict(kopf=z[3:].strip(), absaetze=[])
            teile.append(akt)
        elif z.strip() in ("", "---"):
            absatz_ende()
        else:
            absatz.append(z.strip())
    absatz_ende()
    return dict(titel=titel, unter=kursiv[0][1:-1], herkunft=kursiv[1][1:-1], teile=teile)


def inline(t):
    t = html.escape(t, quote=False)

    def fett(m):
        inhalt = m.group(1)
        if re.fullmatch(r"[A-ZÄÖÜ][A-ZÄÖÜ ]+:?", inhalt):
            return '<span class="wer">%s</span>' % inhalt
        return "<strong>%s</strong>" % inhalt
    t = re.sub(r"\*\*(.+?)\*\*", fett, t)
    t = re.sub(r"\*(\(.+?\))\*", r'<em class="regie">\1</em>', t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    assert "*" not in t, t
    return t


def absatz_html(a):
    if a.startswith("> "):
        return '      <aside class="uebersetzt"><p>%s</p></aside>' % inline(a[2:])
    if re.fullmatch(r"\*\(.+\)\*", a):
        return '      <p class="regie">%s</p>' % html.escape(a[1:-1], quote=False)
    h = inline(a)
    return '      <p%s>%s</p>' % (' class="rede"' if 'class="wer"' in h else "", h)


def koerper(sp, d):
    t = T[sp]
    s = "" if sp == "de" else "-en"
    z = ['<div class="kegel">', '<div class="rahmen">', '  <div class="kopf">', "    <header>",
         '      <div class="abend">%s</div>' % t["kicker"],
         "      <h1>%s</h1>" % html.escape(d["titel"], quote=False),
         '      <p class="unter">%s</p>' % inline(d["unter"]),
         "    </header>",
         '    <figure class="plakat">',
         '      <a href="../../plakat-richard%s.jpg"><img src="../../bilder/richard-%s.webp" srcset="../../bilder/richard-%s-600.webp 600w, '
         '../../bilder/richard-%s.webp 1200w" sizes="(max-width: 720px) min(420px, calc(100vw - 32px)), 330px" width="1200" '
         'height="1800" fetchpriority="high" alt="%s"></a>' % (s, sp, sp, sp, html.escape(t["alt"], quote=True)),
         "      <figcaption>%s</figcaption>" % t["bildzeile"],
         "    </figure>", "  </div>", ""]
    for teil in d["teile"]:
        k = teil["kopf"]
        m = re.fullmatch(r"(\d+)\. (.+)", k)
        if m:
            anker = "d" + m.group(1)
            z += ['  <section class="nummer" aria-labelledby="%s">' % anker,
                  '    <div class="marke">%s <b>%s</b></div>' % (t["marke"], m.group(1)),
                  '    <div class="text">', '      <h2 id="%s">%s</h2>' % (anker, inline(m.group(2)))]
        elif k == t["pause"]:
            z += ['  <section class="ansage" aria-label="%s">' % k, '    <div class="marke">%s</div>' % k, '    <div class="text">']
        else:
            m = re.fullmatch(r"%s: (.+)" % t["zugabe"], k)
            assert m, "unbekannte Überschrift: " + k
            z += ['  <section class="zugabe" aria-labelledby="dz">', '    <div class="marke">%s</div>' % t["zugabe"],
                  '    <div class="text">', '      <h2 id="dz">%s</h2>' % inline(m.group(1))]
        z += [absatz_html(a) for a in teil["absaetze"]]
        z += ["    </div>", "  </section>", ""]
    z += ["  <footer>", "    <span>%s</span>" % inline(d["herkunft"]), "  </footer>", "</div>", "</div>"]
    return "\n".join(z) + "\n"


def stil():
    """Der Stil der ersten Seite (artefakt\\de.html, zeichengleich), dazu die Ergänzungen dieses Abends."""
    q = io.open(os.path.join(HIER, "artefakt", "de.html"), encoding="utf-8", newline="").read()
    a = q.index("<style>\n")
    e = q.index("</style>\n")
    return q[a:e] + EXTRA_CSS + "</style>\n"


def kopf(sp, titel):
    e = lambda x: html.escape(x, quote=True)
    t = T[sp]
    return ("<!doctype html>\n<html lang=\"%s\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            "<title>%s · %s</title>\n"
            "<meta name=\"description\" content=\"%s\">\n"
            "<link rel=\"alternate\" hreflang=\"de\" href=\"https://%s/de/%s\">\n"
            "<link rel=\"alternate\" hreflang=\"en\" href=\"https://%s/en/%s\">\n"
            "<link rel=\"alternate\" hreflang=\"x-default\" href=\"https://%s/en/%s\">\n"
            "<link rel=\"icon\" href=\"../../favicon.ico\" sizes=\"any\">\n"
            "<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"../../favicon-32.png\">\n"
            "<link rel=\"apple-touch-icon\" href=\"../../apple-touch-icon.png\">\n"
            "<meta property=\"og:title\" content=\"%s\">\n"
            "<meta property=\"og:description\" content=\"%s\">\n"
            "<meta property=\"og:image\" content=\"https://%s/plakat-richard-web%s.jpg\">\n"
            "<link rel=\"stylesheet\" href=\"../../fonts/schriften.css\">\n"
            % (sp, html.escape(titel, quote=False), R.TEXT[sp]["og_titel"], e(t["description"]), HOST, UNTER, HOST, UNTER,
               HOST, UNTER, e(titel), e(t["og_text"]), HOST, "" if sp == "de" else "-en"))


def klartext(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def md_klartext(a):
    a = a[2:] if a.startswith("> ") else a
    return re.sub(r"\s+", " ", a.replace("**", "").replace("*", "")).strip()


def bauen(sp, haeuser):
    d = lies(sp)
    k = koerper(sp, d)
    artefakt = "<title>%s</title>\n%s\n%s" % (html.escape(d["titel"], quote=False), stil(), k)
    with io.open(os.path.join(HIER, "artefakt", "richard_%s.html" % sp), "w", encoding="utf-8", newline="\n") as f:
        f.write(artefakt)
    tt = dict(R.TEXT[sp], fuss=T[sp]["fuss"], hinweise=T[sp]["hinweise"])
    fuss = R.abende_nav(sp, UNTER) + R.hausfuss(sp, haeuser, t=tt, tiefe="../../")
    eck = R.ecke(sp, tiefe="../../", unterseite=UNTER, weiter=("../index.html", T[sp]["zurueck"]))
    stelle = k.index("  </footer>\n") + len("  </footer>\n")
    neu = (kopf(sp, d["titel"]) + stil() + R.RAHMEN_CSS + "</head>\n<body>\n" + eck + "\n"
           + k[:stelle] + fuss + k[stelle:] + '<script src="../../schalter.js"></script>\n</body>\n</html>\n')
    # Gegenproben
    seite = klartext(neu)
    for teil in d["teile"]:
        assert md_klartext(teil["kopf"]).split(". ", 1)[-1].split(": ", 1)[-1] in seite, teil["kopf"]
        for a in teil["absaetze"]:
            assert md_klartext(a) in seite, (sp, a[:80])
    assert md_klartext(d["unter"]) in seite and md_klartext(d["herkunft"]) in seite and d["titel"] in seite
    roh = io.open(QUELLE[sp], encoding="utf-8").read()
    for verboten in ("Quellen", "Ränder", "ENTWURF", "Notes for Falzbein", "Baptisten"):
        assert verboten not in seite, verboten
    vor_fuss = neu[:neu.index('  <footer class="hausfuss">')]
    herkunft = inline(d["herkunft"])
    assert "Andy" not in vor_fuss.replace(herkunft, ""), "Andy vor dem Haus-Fuß außerhalb der Herkunftszeile"
    assert "<script>" not in neu and re.search(r"<script(?![^>]*\bsrc=)", neu) is None
    assert "fonts.googleapis" not in neu and "fonts.gstatic" not in neu
    assert re.search("[\x00-\x08\x0b\x0c\x0e-\x1f]", neu) is None, "Steuerzeichen"
    ordner = os.path.join(WEB, sp, UNTER.strip("/"))
    os.makedirs(ordner, exist_ok=True)
    with io.open(os.path.join(ordner, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(neu)
    print(sp, len(d["teile"]), "Teile,", sum(len(t["absaetze"]) for t in d["teile"]), "Absätze ->", len(neu.encode("utf-8")),
          "Bytes, jeder Absatz der Quelle auf der Seite")


def main():
    haeuser = json.load(io.open(R.HAUS_JSON, encoding="utf-8"))["haeuser"]
    for sp in ("de", "en"):
        bauen(sp, haeuser)


if __name__ == "__main__":
    main()
