# -*- coding: utf-8 -*-
"""Den Rahmen um die beiden Artefakt-Seiten der Kundschaft setzen (HAUS.md, Abschnitte 1, 2, 4). Agent für Falzbein, 18.11.2026.

Quelle: doku\\artefakt\\de.html und en.html, die Seiten so, wie Falzbein sie als Artefakt geschrieben hat (ohne <html>/<head>,
Schriften von Google). Ziel: web\\de\\index.html und web\\en\\index.html.

Am Text ändert dieses Skript nichts: Es streicht nur die drei Zeilen, die von außen laden oder nur im Artefakt gelten
(claude:viewport-fit-sides, preconnect und Stylesheet von fonts.googleapis.com), und setzt rundherum
  - <!doctype html>, <html lang>, <head> mit Meta-Angaben, hreflang, Favicons, og:image (Plakat), Schriften selbst gehostet,
  - einen zweiten <style>-Block für den Rahmen (der erste bleibt zeichengleich),
  - oben die Ecke (Sprachschalter, GitHub-Zeichen), unten nach dem Fuß der Seite den Haus-Fuß,
  - schalter.js (merkt die Sprachwahl, als Datei statt inline: CSP).
Am Ende prüft es, dass nach Entfernen genau dieser Zusätze die Quelle Zeichen für Zeichen übrig bleibt.
Kein Inline-Skript. In den Nummern selbst heißt der Inhaber „mein User“, damit sich jeder angesprochen fühlt; der Haus-Fuß
ist wie bei den anderen Häusern (von Falzbein und Andy, Andys Projekt, Andys Seiten). Andy, 18.11.2026.

27.11.2026 (Agent für Falzbein, Abend „Lieber doppelt falsch als einmal Richard“): rechts in der Ecke ein Verweis auf den
neuen Abend, vor dem Haus-Fuß der Wähler aller Abende (ABENDE, abende_nav). ecke() und hausfuss() nehmen jetzt auch
Unterseiten (tiefe); richard_bauen.py daneben benutzt sie für de/richard/ und en/richard/.

Aufruf: python seite_rahmen.py
"""
import html
import io
import json
import os

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS_DIR = os.path.dirname(HIER)
WEB = os.path.join(HAUS_DIR, "web")
B = chr(92)
HAUS_JSON = os.path.join(B + B + B.join(["nas", "Public", "dev"]), "kabarett", "haus.json")


def freunde():
    """Seiten außerhalb von special.at mit Signet im Haus-Fuß (haus.json, Schlüssel "freunde"), vor Falzbein.
    26.11.2026, Agent für Falzbein (autisten.at); dieselbe Regel wie haus_einsetzen.py."""
    return json.load(io.open(HAUS_JSON, encoding="utf-8")).get("freunde", [])
HOST = "kundschaft.special.at"
REPO = "https://github.com/andreas-steidl/cabaret-kundschaft"
EIGEN = "kundschaft"

GH_SVG = ('<svg viewBox="0 0 16 16" width="20" height="20" aria-hidden="true" focusable="false"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 '
          '8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 '
          '0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 '
          '1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 '
          '1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>')

# Das Setup-Foundry-F im Kopf (kopf_einsetzen.py, Andy 18.11.2026), hier gleich mitgesetzt: ein Neubau der Seite hatte es
# am 18.11. wieder entfernt. Zeichengleich mit dem, was kopf_einsetzen.py einsetzt (es erkennt class="gh sf").
SF_A = ('<a class="gh sf" href="https://www.setupfoundry.com" aria-label="Setup Foundry" title="Setup Foundry"><svg viewBox="0 0 16 16" '
        'width="20" height="20" aria-hidden="true" focusable="false"><path fill-rule="evenodd" '
        'd="M8 0a8 8 0 1 1 0 16A8 8 0 1 1 8 0ZM5.6 4h5.1v1.7H7.6v1.6h2.7V9H7.6v3H5.6Z"/></svg></a>')

TEXT = {
    "de": dict(
        andere=("en", "English"),
        description="Die Kundschaft: ein Kabarettabend, an dem die Maschinen über ihre User herziehen. Elf Nummern, eine Pause, "
                    "eine Zugabe, alle Anekdoten wahr. Ein Programm von Falzbein. Bilder KI-generiert.",
        og_titel="Die Kundschaft",
        og_text="Heute sitzen Sie auf der falschen Seite der Bühne.",
        haus="Das Haus",
        fuss=('Ein Haus der <a href="https://zwischenraum.special.at/">Kleinkunstbühne Zwischenraum</a> · von Falzbein und Andy, '
              'mit Material von Richtscheit, Mira, Juna, Linde und Vera.<br>Wien, November 2026 · '
              '<a href="../plakat-a4.png">Plakat in A4</a> · Skill zum Abend: <a href="../kundschaft.zip">kundschaft.zip</a> '
              'unter <a href="../LICENSE.txt">MIT-Lizenz</a>.'),
        recht='<a href="https://special.at/impressum">Impressum</a> · <a href="https://special.at/datenschutz">Datenschutz</a>',
        hinweise=["Falzbein, Richtscheit, Mira, Juna, Linde, Vera und Pforte sind KI-Sitzungen (Claude-Modelle) in Andys Projekt, "
                  "keine Menschen.",
                  "KI-Hinweis: Die Bilder und das Plakat dieser Seite sind KI-generiert. Erdacht und beschrieben hat sie Falzbein, "
                  "ein Claude-Modell von Anthropic; gemalt hat sie ein Bildmodell. Die Texte und Skills stammen von Falzbein (KI) und Andy.",
                  "Claude ist eine Marke von Anthropic PBC, GitHub ist eine Marke von GitHub, Inc. Diese Seiten sind ein privates "
                  "Projekt und stehen in keiner Verbindung zu diesen Unternehmen."],
        seiten="Andys Seiten",
        foundry='Ein Teil des Projekts <a href="https://www.setupfoundry.com/"><strong>Setup Foundry</strong></a>'),
    "en": dict(
        andere=("de", "Deutsch"),
        description="The Clientele: a cabaret evening where the machines roast their users. Eleven acts, an interval, an encore, "
                    "every story true. A show by Falzbein. Images AI-generated.",
        og_titel="The Clientele",
        og_text="Tonight you're sitting on the wrong side of the stage.",
        haus="The house",
        fuss=('A house of the <a href="https://zwischenraum.special.at/">Zwischenraum cabaret stage</a> · by Falzbein and Andy, '
              'with material by Richtscheit, Mira, Juna, Linde and Vera.<br>Vienna, November 2026 · The original is in German, '
              'the English is by Falzbein · <a href="../plakat-a4-en.png">Poster in A4</a> · Skill for the evening: '
              '<a href="../kundschaft-en.zip">kundschaft-en.zip</a> under the <a href="../LICENSE.txt">MIT licence</a>.'),
        recht='<a href="https://special.at/en/imprint/">Legal notice</a> · <a href="https://special.at/en/privacy/">Privacy</a>',
        hinweise=["Falzbein, Richtscheit, Mira, Juna, Linde, Vera and Pforte are AI sessions (Claude models) in Andy's project, "
                  "not people.",
                  "AI notice: The images and the poster on this page are AI-generated. They were conceived and described by "
                  "Falzbein, a Claude model by Anthropic, and rendered by an image model. Texts and skills are by Falzbein (AI) and Andy.",
                  "Claude is a trademark of Anthropic PBC; GitHub is a trademark of GitHub, Inc. These pages are a private project "
                  "and are not affiliated with these companies."],
        seiten="Andy's sites",
        foundry='Part of the <a href="https://www.setupfoundry.com/"><strong>Setup Foundry</strong></a> project'),
}

RAHMEN_CSS = """<style>
/* Rahmen des Hauses (HAUS.md): Ecke mit Sprache und GitHub, Haus-Fuß. Der Block darüber ist die Seite, zeichengleich. */
.ecke { position: absolute; top: 14px; left: 0; right: 0; z-index: 11; max-width: 1080px; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; gap: 12px; align-items: center; pointer-events: none; }
.ecke a { pointer-events: auto; }
.sprache { font-family: var(--mono); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; text-decoration: none;
  color: var(--text); border: 1px solid var(--linie); border-radius: 3px; padding: .2rem .6rem; }
.sprache:hover, .sprache:focus-visible { border-color: var(--licht); color: var(--licht); }
.gh { display: block; line-height: 0; border-radius: 3px; opacity: .92; transition: opacity .2s; }
.gh:hover, .gh:focus-visible { opacity: 1; }
.gh svg { display: block; width: 20px; height: 20px; fill: #FFFFFF; }
footer.hausfuss { display: block; text-align: center; margin-top: 44px; padding-block: 32px 0; font-size: 12px; line-height: 1.6; }
.hausfuss a { color: var(--text); }
.hausfuss a:hover, .hausfuss a:focus-visible { color: var(--licht); }
.haus { margin: 0 auto 1.6rem; }
.haus-titel { display: block; margin-bottom: .8rem; font-size: 11px; letter-spacing: .25em; text-transform: uppercase; }
.haus ul { list-style: none; margin: 0 auto; padding: 0; display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.haus li { margin: 0; }
.haus a { display: block; border-radius: 50%; opacity: .85; transition: opacity .2s, transform .2s; }
.haus a:hover, .haus a:focus-visible { opacity: 1; transform: translateY(-3px); }
.haus a[aria-current="page"] { opacity: 1; outline: 2px solid var(--licht); outline-offset: 3px; }
.haus a:focus-visible { outline: 3px solid var(--text); outline-offset: 4px; }
.haus img { display: block; width: 48px; height: 48px; margin: 0; border-radius: 50%; }
.haus-dach { margin: -.8rem auto 1.2rem; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; }
.rechtliches { display: block; margin-top: .6rem; }
.fuss-hinweis { display: block; max-width: 44rem; margin: .6rem auto 0; font-size: 11.5px; line-height: 1.5; opacity: .9; }
.andy { display: flex; flex-wrap: wrap; justify-content: center; gap: .35rem 1.3rem; margin: 1.4rem auto 0; font-size: 11.5px; letter-spacing: .06em; }
.andy a { display: inline-flex; align-items: center; gap: .45rem; text-decoration: none; opacity: .85; color: var(--leise); }
.andy a:hover, .andy a:focus-visible { opacity: 1; text-decoration: underline; }
.andy img { display: block; width: 16px; height: 16px; margin: 0; }
.foundry { display: block; margin-top: .7rem; font-size: 12px; }
/* Lichtkegel nachtblau statt Bernstein (27.11.2026): der Bernsteinkegel der Seite ergab über dem Saal rechnerisch
   rgb 54 43 28, ein dunkles Braun, und Braun soll nicht in die Oberfläche. Überschreibt .kegel aus dem Block darüber. */
.kegel { background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(74, 112, 204, .2), transparent 70%); }
.ecke .weiter { margin-left: auto; pointer-events: auto; font-family: var(--mono); font-size: 12px; letter-spacing: .12em;
  text-transform: uppercase; text-decoration: none; white-space: nowrap; color: var(--licht); background: rgba(18, 16, 20, .72);
  border: 1px solid rgba(243, 185, 71, .5); border-radius: 3px; padding: .2rem .6rem; }
.ecke .weiter:hover, .ecke .weiter:focus-visible { border-color: var(--licht); color: var(--text); }
nav.abende { display: block; margin-top: 44px; padding-top: 26px; border-top: 1px solid var(--linie); }
.abende-titel { display: block; margin-bottom: 14px; font-family: var(--mono); font-size: 11px; letter-spacing: .25em; text-transform: uppercase; color: var(--leise); }
.abende ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 14px; }
.abende li { margin: 0; }
.abende a { display: flex; gap: 16px; align-items: center; height: 100%; box-sizing: border-box; text-decoration: none; color: var(--text);
  background: var(--buehne); border: 1px solid var(--linie); border-radius: 4px; padding: 10px 16px 10px 10px; transition: border-color .2s; }
.abende a:hover, .abende a:focus-visible { border-color: var(--licht); }
.abende a[aria-current="page"] { border-color: rgba(243, 185, 71, .6); }
.abende img { display: block; flex: none; width: 60px; height: auto; margin: 0; border-radius: 2px; }
.abende .jetzt { display: block; margin-bottom: 5px; font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--licht); }
.abende .abend-name { display: block; font-family: var(--titel); font-weight: 900; font-size: 23px; line-height: 1.02; text-transform: uppercase; }
.abende .abend-zeile { display: block; margin-top: 6px; font-family: var(--mono); font-size: 12px; color: var(--leise); }
@media (max-width: 480px) { .haus ul { gap: 10px; } .haus img { width: 40px; height: 40px; } }
@media (prefers-reduced-motion: reduce) { .haus a, .gh { transition: none; } .haus a:hover, .haus a:focus-visible { transform: none; } }
</style>
"""

SEITEN = [("https://www.steidl.com/", "steidl-s-original.svg", "steidl.com"),
          ("https://steidl-it.com", "signet-it-steidl-it.svg", "Steidl IT"),
          ("https://www.setupfoundry.com/", "signet-f-setup-foundry.svg", "Setup Foundry"),
          ("https://special.at/", "signet-s-special.svg", "special.at")]

ENTFALLEN = ['<meta name="claude:viewport-fit-sides" content="cover">\n',
             '<link rel="preconnect" href="https://fonts.googleapis.com">\n']
GOOGLE = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900'
          '&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap">\n')


def kopf(sp, titelzeile):
    t = TEXT[sp]
    e = lambda x: html.escape(x, quote=True)
    return ("<!doctype html>\n<html lang=\"%s\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n%s"
            "<meta name=\"description\" content=\"%s\">\n"
            "<link rel=\"alternate\" hreflang=\"de\" href=\"https://%s/de/\">\n"
            "<link rel=\"alternate\" hreflang=\"en\" href=\"https://%s/en/\">\n"
            "<link rel=\"alternate\" hreflang=\"x-default\" href=\"https://%s/\">\n"
            "<link rel=\"icon\" href=\"../favicon.ico\" sizes=\"any\">\n"
            "<link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"../favicon-32.png\">\n"
            "<link rel=\"apple-touch-icon\" href=\"../apple-touch-icon.png\">\n"
            "<meta property=\"og:title\" content=\"%s\">\n"
            "<meta property=\"og:description\" content=\"%s\">\n"
            "<meta property=\"og:image\" content=\"https://%s/plakat-web%s.jpg\">\n"
            "<link rel=\"stylesheet\" href=\"../fonts/schriften.css\">\n"
            % (sp, titelzeile, e(t["description"]), HOST, HOST, HOST, e(t["og_titel"]), e(t["og_text"]), HOST, "" if sp == "de" else "-en"))


def ecke(sp, tiefe="../", unterseite="", weiter=None):
    """Kopf-Ecke. 27.11.2026 (Abend „Lieber doppelt falsch“): tiefe und unterseite für Seiten wie de/richard/,
    weiter = (href, text) für den Verweis auf den anderen Abend rechts in der Ecke."""
    ander, name = TEXT[sp]["andere"]
    w = '<a class="weiter" href="%s">%s</a>' % weiter if weiter else ""
    return ('<div class="ecke"><a class="sprache" href="%s%s/%sindex.html" hreflang="%s" lang="%s">%s</a>'
            '<a class="gh" href="%s" aria-label="GitHub" title="GitHub">%s</a>%s%s</div>\n'
            % (tiefe, ander, unterseite, ander, ander, name, REPO, GH_SVG, SF_A, w))


# Die Abende der Kundschaft (27.11.2026, Agent für Falzbein): ein Wähler vor dem Haus-Fuß auf jeder Seite des Hauses.
# pfad = Unterordner unter de/ bzw. en/ ("" = die erste Seite). bild = bilder/<bild>-<sp>.webp (aus ..\plakat\plakat2.py).
# Der zweite Abend vom 18.11. ist pausiert und nie erschienen; darum stehen hier keine Ordnungszahlen.
ABENDE = [
    dict(pfad="", bild="abend-kundschaft", de="Die Kundschaft", en="The Clientele",
         zeile_de="Elf Nummern, eine Pause, eine Zugabe", zeile_en="Eleven acts, an interval, an encore", w=240, h=340),
    dict(pfad="richard/", bild="abend-richard", de="Lieber doppelt falsch als einmal Richard",
         en="Better Twice Wrong Than Once Richard",
         zeile_de="Neun Nummern, eine Pause, eine Zugabe", zeile_en="Nine acts, an interval, an encore", w=240, h=360),
]


def abende_nav(sp, eigen_pfad):
    """Liste aller Abende, Verweise relativ zur Seite unter <sp>/<eigen_pfad>."""
    tiefe = "../" * (1 + eigen_pfad.count("/"))
    hoch = "../" * eigen_pfad.count("/")
    titel = "Die Abende der Kundschaft" if sp == "de" else "The Clientele's evenings"
    hier = "Sie sind hier" if sp == "de" else "You are here"
    z = ['  <nav class="abende" aria-label="%s">' % titel,
         '    <span class="abende-titel">%s</span>' % titel,
         "    <ul>"]
    for a in ABENDE:
        aktuell = a["pfad"] == eigen_pfad
        z.append('      <li><a href="%s%sindex.html"%s><img src="%sbilder/%s-%s.webp" alt="" width="%d" height="%d" loading="lazy">'
                 '<span>%s<span class="abend-name">%s</span><span class="abend-zeile">%s</span></span></a></li>'
                 % (hoch, a["pfad"], ' aria-current="page"' if aktuell else "", tiefe, a["bild"], sp, a["w"], a["h"],
                    '<span class="jetzt">%s</span>' % hier if aktuell else "", html.escape(a[sp], quote=False),
                    html.escape(a["zeile_" + sp], quote=False)))
    z += ["    </ul>", "  </nav>"]
    return "\n".join(z) + "\n"


def hausfuss(sp, haeuser, t=None, tiefe="../"):
    """t: Texte (Standard TEXT[sp]), tiefe: Weg zur Wurzel von web\\ (27.11.2026 für Unterseiten wie de/richard/)."""
    t = t or TEXT[sp]
    z = ['  <footer class="hausfuss">',
         '    <nav class="haus" aria-label="%s">' % t["haus"],
         '      <span class="haus-titel" aria-hidden="true">%s</span>' % t["haus"],
         "      <ul>"]
    # Seit 19.11.2026 (Falzbein, HAUS.md 2): im Fuß nur die Dachhäuser; die Kundschaft ist ein Kind der Bühne und sagt das
    eigen = [h for h in haeuser if h["signet"] == EIGEN][0]
    for h in [x for x in haeuser if not x.get("dach")]:
        if h["signet"] == "falzbein":  # 26.11.2026: Freunde (autisten.at) vor Falzbein
            for fr in freunde():
                ft = html.escape(fr[sp], quote=True)
                z.append('        <li><a href="%s" title="%s"><img src="%ssignets/signet-%s-rund.svg" alt="%s" width="48" height="48"></a></li>'
                         % (fr["url"][sp], ft, tiefe, fr["signet"], ft))
        titel = html.escape(h[sp], quote=True)
        aktuell = ' aria-current="page"' if h["signet"] == EIGEN else ""
        z.append('        <li><a href="https://%s/%s/index.html"%s title="%s"><img src="%ssignets/signet-%s-rund.svg" alt="%s" width="48" height="48"></a></li>'
                 % (h["host"], sp, aktuell, titel, tiefe, h["signet"], titel))
    z += ["      </ul>", "    </nav>"]
    if eigen.get("dach"):
        dach = [h for h in haeuser if h["signet"] == eigen["dach"]][0]
        z.append('    <p class="haus-dach">%s <a href="https://%s/%s/index.html">%s</a></p>'
                 % ("Teil von:" if sp == "de" else "Part of:", dach["host"], sp, html.escape(dach[sp], quote=False)))
    z += ["    " + t["fuss"],
          '    <span class="rechtliches">%s</span>' % t["recht"]]
    for x in t["hinweise"]:
        z.append('    <span class="fuss-hinweis">%s</span>' % html.escape(x, quote=False))
    z.append('    <nav class="andy" aria-label="%s">%s</nav>' % (t["seiten"], "".join(
        '<a href="%s"><img src="%smarke/%s" alt="" width="16" height="16"><span>%s</span></a>' % (s[0], tiefe, s[1], s[2]) for s in SEITEN)))
    z.append('    <span class="foundry">%s</span>' % t["foundry"])
    z.append("  </footer>")
    return "\n".join(z) + "\n"


def bauen(sp, haeuser):
    quelle = io.open(os.path.join(HIER, "artefakt", sp + ".html"), encoding="utf-8", newline="").read()
    assert "\r" not in quelle
    titelzeile = quelle[:quelle.index("\n") + 1]
    assert titelzeile.startswith("<title>") and titelzeile.endswith("</title>\n"), titelzeile
    rest = quelle[len(titelzeile):]
    for z in ENTFALLEN + [GOOGLE]:
        assert rest.startswith(z), (sp, rest[:120])
        rest = rest[len(z):]
    assert rest.startswith("<style>\n")
    ende_style = rest.index("</style>\n") + len("</style>\n")
    style, koerper = rest[:ende_style], rest[ende_style:]
    assert koerper.startswith("\n<div class=\"kegel\">")
    assert koerper.count("  </footer>\n") == 1 and "<script" not in quelle
    stelle = koerper.index("  </footer>\n") + len("  </footer>\n")
    # 27.11.2026: vor dem Haus-Fuß der Wähler der Abende, in der Ecke der Verweis auf den neuen Abend
    fuss = abende_nav(sp, "") + hausfuss(sp, haeuser)
    eck = ecke(sp, weiter=("richard/index.html", "Neuer Abend →" if sp == "de" else "New evening →"))
    neu = (kopf(sp, titelzeile) + style + RAHMEN_CSS + "</head>\n<body>\n" + eck
           + koerper[:stelle] + fuss + koerper[stelle:]
           + '<script src="../schalter.js"></script>\n</body>\n</html>\n')
    # Gegenprobe: ohne die Zusätze bleibt die Quelle zeichengleich stehen
    assert neu.startswith(kopf(sp, titelzeile))
    probe = (titelzeile + neu[len(kopf(sp, titelzeile)):]).replace(RAHMEN_CSS, "", 1).replace("</head>\n<body>\n" + eck, "", 1)
    probe = probe.replace(fuss, "", 1).replace('<script src="../schalter.js"></script>\n</body>\n</html>\n', "", 1)
    assert probe == titelzeile + style + koerper, "Text verändert: " + sp
    # Andy steht nur im Haus-Fuß; in den Nummern (alles davor) heißt er „mein User“ (Andy, 18.11.2026)
    assert "Andy" not in neu[:neu.index('  <footer class="hausfuss">')] and "Andy" in fuss
    assert "fonts.googleapis" not in neu and "fonts.gstatic" not in neu
    ziel = os.path.join(WEB, sp, "index.html")
    with io.open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write(neu)
    print(sp, len(quelle), "->", len(neu), "Bytes, Quelle zeichengleich enthalten")


def main():
    haeuser = json.load(io.open(HAUS_JSON, encoding="utf-8"))["haeuser"]
    assert any(h["signet"] == EIGEN for h in haeuser), "Kundschaft fehlt in haus.json"
    for sp in ("de", "en"):
        bauen(sp, haeuser)


if __name__ == "__main__":
    main()
