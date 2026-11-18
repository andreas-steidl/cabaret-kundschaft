# -*- coding: utf-8 -*-
"""Banner für das README des Repos cabaret-kundschaft, nach dem Muster von ..\\..\\readme_bauen.py (BANNER_SPIELZEIT):
links Titel und Unterzeile, rechts das Plakat schräg und das runde Signet. Je Sprache hell und dunkel, 1280 x 400 bei
Faktor 2, mit Edge fotografiert (plakat\\foto.ps1). Agent für Falzbein, 18.11.2026.

Ausgabe: .github\\readme\\banner-<de|en>-<hell|dunkel>.png      Aufruf: python readme_banner.py
"""
import html
import os
import shutil
import subprocess
import tempfile

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(HIER)
WEB = os.path.join(HAUS, "web")
ZIEL = os.path.join(HAUS, ".github", "readme")

SEITE = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="schriften.css">
<style>
 html,body{margin:0;width:1280px;height:400px;overflow:hidden}
 body{background:%(bg)s;background-image:radial-gradient(ellipse 55%% 80%% at 30%% 0%%,%(glow)s,transparent 70%%);color:%(text)s;font-family:'Literata',Georgia,serif;position:relative}
 .vorhang{position:absolute;left:0;right:0;bottom:0;height:10px;background:repeating-linear-gradient(90deg,#8f2230 0 14px,transparent 14px 22px);opacity:.7}
 .links{position:absolute;left:84px;top:58px;width:720px}
 .kicker{font-family:'IBM Plex Mono',monospace;font-weight:500;letter-spacing:.2em;text-transform:uppercase;font-size:15px;color:%(akzent)s}
 h1{font-family:'Big Shoulders Display',sans-serif;font-weight:900;text-transform:uppercase;font-size:112px;line-height:.9;margin:16px 0 14px;letter-spacing:.01em}
 .unter{font-style:italic;font-size:25px;opacity:.85}
 .host{margin-top:24px;font-family:'IBM Plex Mono',monospace;font-size:16px;letter-spacing:.12em;color:%(akzent)s}
 .plakat{position:absolute;right:110px;top:30px;width:236px;transform:rotate(3deg);box-shadow:0 18px 40px rgba(0,0,0,.45);border:5px solid %(rand)s}
 .signet{position:absolute;right:300px;top:236px;width:130px;transform:rotate(-9deg);filter:drop-shadow(0 8px 14px rgba(0,0,0,.4))}
</style></head><body>
<div class="links"><div class="kicker">%(kicker)s</div><h1>%(titel)s</h1><div class="unter">%(unter)s</div><div class="host">kundschaft.special.at</div></div>
<img class="plakat" src="%(plakat)s"><img class="signet" src="signet.svg">
<div class="vorhang"></div></body></html>"""

TEXT = {"de": dict(kicker="Kleinkunstbühne Zwischenraum · Eigenes Haus", titel="Die Kundschaft",
                   unter="Heute sitzen Sie auf der falschen Seite der Bühne.", plakat="plakat-web.jpg"),
        "en": dict(kicker="Zwischenraum cabaret stage · A house of its own", titel="The Clientele",
                   unter="Tonight you're sitting on the wrong side of the stage.", plakat="plakat-web-en.jpg")}
FARBE = {"dunkel": dict(bg="#121014", text="#efe7da", akzent="#f3b947", glow="rgba(243,185,71,.18)", rand="#efe7da"),
         "hell": dict(bg="#f5efe4", text="#1c1820", akzent="#8f2230", glow="rgba(243,185,71,.35)", rand="#fffaf0")}


def main():
    tmp = tempfile.mkdtemp(prefix="kundschaft_banner_")
    for f in os.listdir(os.path.join(WEB, "fonts")):
        shutil.copyfile(os.path.join(WEB, "fonts", f), os.path.join(tmp, f))
    for f in ("plakat-web.jpg", "plakat-web-en.jpg"):
        shutil.copyfile(os.path.join(WEB, f), os.path.join(tmp, f))
    shutil.copyfile(os.path.join(WEB, "signets", "signet-kundschaft-rund.svg"), os.path.join(tmp, "signet.svg"))
    os.makedirs(ZIEL, exist_ok=True)
    for sp, t in TEXT.items():
        for art, farbe in FARBE.items():
            h = os.path.join(tmp, "b-%s-%s.html" % (sp, art))
            with open(h, "w", encoding="utf-8") as f:
                f.write(SEITE % dict(farbe, kicker=html.escape(t["kicker"]), titel=html.escape(t["titel"]),
                                     unter=html.escape(t["unter"]), plakat=t["plakat"]))
            png = os.path.join(tmp, "b-%s-%s.png" % (sp, art))
            subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HAUS, "plakat", "foto.ps1"),
                            "-Html", h, "-Png", png, "-Breite", "1280", "-Hoehe", "400", "-Hell", "-Faktor", "2"], check=True, capture_output=True)
            im = Image.open(png).convert("RGB")
            assert im.size == (2560, 800), im.size
            im.save(os.path.join(ZIEL, "banner-%s-%s.png" % (sp, art)), optimize=True)
            print("banner", sp, art)
    return tmp


if __name__ == "__main__":
    print(main())
