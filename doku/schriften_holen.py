# -*- coding: utf-8 -*-
"""Schriften des Hauses Kundschaft selbst hosten (HAUS.md, Abschnitt 4: nichts von außen). Agent für Falzbein, 18.11.2026.

Big Shoulders Display 700/900 und Literata 400/600/400 kursiv aus Google Fonts (nur latin und latin-ext),
IBM Plex Mono 400/500 aus falzbein-seite\\fonts (dieselben Dateien wie dort). Schreibt web\\fonts\\schriften.css und OFL.txt.
Überschreibt keine vorhandene Schriftdatei. Aufruf: python schriften_holen.py
"""
import os
import re
import shutil
import urllib.request

B = chr(92)
DEV = B + B + B.join(["nas", "Public", "dev"])
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(HIER), "web")
FONTS = os.path.join(WEB, "fonts")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
CSS_URL = ("https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900"
           "&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap")

OFL_KOPF = """Schriften auf dieser Seite / Fonts on this site

Selbst gehostet, unveraendert aus Google Fonts (Teilmengen latin und latin-ext).
Self-hosted, unmodified from Google Fonts (latin and latin-ext subsets).

Big Shoulders Display:
  Copyright 2019 The Big Shoulders Project Authors (https://github.com/xotypeco/big_shoulders)

Literata:
  Copyright 2017 The Literata Project Authors (https://github.com/googlefonts/literata)

IBM Plex Mono:
  Copyright © 2017 IBM Corp. with Reserved Font Name "Plex"

"""


def holen(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def main():
    os.makedirs(FONTS, exist_ok=True)
    css = holen(CSS_URL).decode("utf-8")
    bloecke = re.findall(r"/\* (latin-ext|latin) \*/\s*@font-face \{(.*?)\}", css, re.S)
    eintraege = []
    for teil, rumpf in bloecke:
        fam = re.search(r"font-family: '([^']+)'", rumpf).group(1)
        stil = re.search(r"font-style: (\w+)", rumpf).group(1)
        gewicht = re.search(r"font-weight: ([\d ]+);", rumpf).group(1).strip()
        url = re.search(r"url\((https[^)]+)\)", rumpf).group(1)
        rng = re.search(r"unicode-range: ([^;]+);", rumpf).group(1)
        eintraege.append((fam, stil, gewicht, teil, url, rng))
    # Variable Schriften liefern für mehrere Gewichte dieselbe Datei: dann heißt sie "var".
    zahl = {}
    for e in eintraege:
        zahl[e[4]] = zahl.get(e[4], 0) + 1
    namen = {}
    regeln = []
    for fam, stil, gewicht, teil, url, rng in eintraege:
        kurz = fam.lower().replace(" ", "")
        name = namen.get(url) or "%s-%s-%s-%s.woff2" % (kurz, stil, "var" if zahl[url] > 1 else gewicht, teil)
        namen[url] = name
        ziel = os.path.join(FONTS, name)
        if not os.path.exists(ziel):
            with open(ziel, "wb") as f:
                f.write(holen(url))
        regeln.append("/* %s */\n@font-face {\n  font-family: '%s';\n  font-style: %s;\n  font-weight: %s;\n  font-display: swap;\n"
                      "  src: url(%s) format('woff2');\n  unicode-range: %s;\n}" % (teil, fam, stil, gewicht, name, rng))
    fq = os.path.join(DEV, "falzbein-seite", "fonts")
    for f in os.listdir(fq):
        if f.startswith("ibmplexmono"):
            ziel = os.path.join(FONTS, f)
            if not os.path.exists(ziel):
                shutil.copyfile(os.path.join(fq, f), ziel)
    alt = open(os.path.join(fq, "schriften.css"), encoding="utf-8").read()
    plex = [m.group(0) for m in re.finditer(r"/\* [a-z-]+ \*/\s*@font-face \{[^}]*IBM Plex Mono[^}]*\}", alt)]
    assert len(plex) == 4, len(plex)
    kopf = ("/* Schriften des Hauses Kundschaft, selbst gehostet seit 18.11.2026.\n"
            "   Aus Google Fonts geladen, nur die Teilmengen latin und latin-ext.\n"
            "   Familien: Big Shoulders Display, Literata, IBM Plex Mono. Lizenz: SIL Open Font License 1.1, siehe OFL.txt. */\n\n")
    with open(os.path.join(FONTS, "schriften.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(kopf + "\n".join(regeln + plex) + "\n")
    # OFL-Text: Lizenzteil unverändert aus falzbein-seite, Kopf mit den Familien dieses Hauses
    ofl = open(os.path.join(fq, "OFL.txt"), encoding="utf-8").read()
    i = ofl.index("-" * 70)
    with open(os.path.join(FONTS, "OFL.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(OFL_KOPF + ofl[i:])
    print("fonts:", sorted(os.listdir(FONTS)))


if __name__ == "__main__":
    main()
