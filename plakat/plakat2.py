# -*- coding: utf-8 -*-
"""plakat2.py - das Plakat zum Abend „Lieber doppelt falsch als einmal Richard“, deutsch und englisch.
Agent für Falzbein, 27.11.2026.

Quelle: richard\\plakat_richard_schrift.png und richard\\plakat_richard_ohne.png (Codex, ein Lauf, Auftrag in
richard\\AUFTRAG_plakat_richard.md; Rohfassungen und Rollout in D:\\Workspace\\kabarett_user\\plakate\\richard_2026-11-27\\herkunft).
Beide 2048 x 3072, Hochformat 2:3.

  de  = plakat_richard_schrift.png, unverändert (Titel, „RIHCTSCHET“ und „RICHARD“ hat das Bildmodell gemalt).
  en  = dieselbe Szene: die oberen 400 Zeilen (nur Nachtblau und der deutsche Titel) aus der Fassung OHNE Schrift,
        darunter ab Zeile 440 die Fassung MIT Schrift (Zettel „RIHCTSCHET“ und Schild „RICHARD“ tragen auch englisch),
        dazwischen 40 Zeilen weich überblendet. Die beiden Fassungen sind dort fast deckungsgleich (mittlere
        Abweichung unter 2 von 255, gemessen am 27.11.). Den englischen Titel setzt dieses Skript in den Schriften
        des Hauses (Big Shoulders Display, IBM Plex Mono aus ..\\web\\fonts), fotografiert mit Playwright (Chromium).
        Das ist eine Bearbeitung nach CLAUDE.md Abschnitt 7 (Regel aufgehoben 12.10.2026): angesehen, hier festgehalten.

Ausgaben nach ..\\web (alle ohne Metadaten, aus dem Pixelpuffer neu geschrieben):
  bilder/richard-de.webp, bilder/richard-en.webp            1200 x 1800, Kopfbild der Seite
  bilder/richard-de-600.webp, bilder/richard-en-600.webp     600 x 900, srcset
  plakat-richard-web.jpg, plakat-richard-web-en.jpg          1200 x 1800, og:image
  plakat-richard.jpg, plakat-richard-en.jpg                  2048 x 3072, Plakat zum Herunterladen
  bilder/abend-kundschaft-de.webp, -en.webp                  240 breit, Vorschau im Abend-Wähler (aus plakat-web*.jpg)
  bilder/abend-richard-de.webp, -en.webp                     240 breit, Vorschau im Abend-Wähler
Bilder unter CC BY-NC-SA 4.0 (Andy, 27.11.2026), nicht unter der MIT-Lizenz des Repos.
Aufruf: python plakat2.py
"""
import io
import os
import shutil
import tempfile

import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(HIER), "web")
QUELLE = os.path.join(HIER, "richard")
OBEN, UEBERGANG = 400, 40

TITEL_EN = """<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="schriften.css"><style>
html,body{margin:0;width:2048px;height:3072px;overflow:hidden;background:#000}
body{background:url(grund.png) 0 0/2048px 3072px no-repeat;position:relative}
h1{position:absolute;top:58px;left:0;right:0;margin:0;text-align:center;font-family:"Big Shoulders Display",sans-serif;
font-weight:900;font-size:168px;line-height:.98;letter-spacing:.045em;text-transform:uppercase;color:#f1e6cf;
text-shadow:5px 6px 0 rgba(222,160,58,.85),0 0 30px rgba(0,0,0,.35)}
p{position:absolute;top:418px;left:0;right:0;margin:0;text-align:center;font-family:"IBM Plex Mono",monospace;font-weight:500;
font-size:50px;letter-spacing:.24em;text-transform:uppercase;color:#f0b443}
</style></head><body><h1>Better twice wrong<br>than once Richard</h1><p>Falzbein · Cabaret</p></body></html>"""


def lade(name):
    return Image.open(os.path.join(QUELLE, name)).convert("RGB")


def grund_en():
    ohne = np.asarray(lade("plakat_richard_ohne.png")).astype(np.float32)
    mit = np.asarray(lade("plakat_richard_schrift.png")).astype(np.float32)
    assert ohne.shape == mit.shape == (3072, 2048, 3)
    abw = np.abs(ohne[OBEN:OBEN + UEBERGANG] - mit[OBEN:OBEN + UEBERGANG]).mean()
    assert abw < 4, "Fassungen im Übergang nicht deckungsgleich: %.1f" % abw
    gewicht = np.ones((3072, 1, 1), np.float32)          # 1 = Fassung ohne Schrift
    gewicht[OBEN:OBEN + UEBERGANG, 0, 0] = np.linspace(1, 0, UEBERGANG)
    gewicht[OBEN + UEBERGANG:] = 0
    return Image.fromarray(np.clip(ohne * gewicht + mit * (1 - gewicht), 0, 255).round().astype(np.uint8)), abw


def titel_setzen(grund):
    from playwright.sync_api import sync_playwright
    tmp = tempfile.mkdtemp(prefix="kundschaft_richard_")
    fonts = os.path.join(WEB, "fonts")
    for f in os.listdir(fonts):
        if f.endswith((".woff2", ".css")):
            shutil.copyfile(os.path.join(fonts, f), os.path.join(tmp, f))
    grund.save(os.path.join(tmp, "grund.png"))
    seite = os.path.join(tmp, "titel_en.html")
    with io.open(seite, "w", encoding="utf-8") as f:
        f.write(TITEL_EN)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page(viewport={"width": 2048, "height": 3072}, device_scale_factor=1)
        p.goto("file:///" + seite.replace(chr(92), "/"))
        p.evaluate("document.fonts.ready")
        p.wait_for_timeout(300)
        assert p.evaluate("document.fonts.check('900 168px \"Big Shoulders Display\"')"), "Titelschrift nicht geladen"
        png = os.path.join(tmp, "plakat_en.png")
        p.screenshot(path=png)
        b.close()
    im = Image.open(png).convert("RGB")
    assert im.size == (2048, 3072), im.size
    return im, tmp


def sauber(im):
    """Neu aus dem Pixelpuffer: kein EXIF, kein ICC, kein C2PA."""
    return Image.frombytes("RGB", im.size, im.convert("RGB").tobytes())


def schreiben(im, sp):
    s = "" if sp == "de" else "-en"
    im = sauber(im)
    gross = im.resize((1200, 1800), Image.LANCZOS)
    gross.save(os.path.join(WEB, "bilder", "richard-%s.webp" % sp), quality=82, method=6)
    im.resize((600, 900), Image.LANCZOS).save(os.path.join(WEB, "bilder", "richard-%s-600.webp" % sp), quality=80, method=6)
    gross.save(os.path.join(WEB, "plakat-richard-web%s.jpg" % s), quality=86, optimize=True, progressive=True)
    im.save(os.path.join(WEB, "plakat-richard%s.jpg" % s), quality=90, optimize=True, progressive=True, subsampling=0)
    im.resize((240, 360), Image.LANCZOS).save(os.path.join(WEB, "bilder", "abend-richard-%s.webp" % sp), quality=82, method=6)
    k = sauber(Image.open(os.path.join(WEB, "plakat-web%s.jpg" % s)))
    k.resize((240, round(240 * k.size[1] / k.size[0])), Image.LANCZOS).save(
        os.path.join(WEB, "bilder", "abend-kundschaft-%s.webp" % sp), quality=82, method=6)


def main():
    schreiben(lade("plakat_richard_schrift.png"), "de")
    grund, abw = grund_en()
    en, tmp = titel_setzen(grund)
    schreiben(en, "en")
    print("Plakat de und en fertig; Übergang deckungsgleich bis auf %.2f; Arbeitsordner %s" % (abw, tmp))


if __name__ == "__main__":
    main()
