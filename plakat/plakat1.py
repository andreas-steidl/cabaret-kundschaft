# -*- coding: utf-8 -*-
"""plakat1.py - das Plakat der Kundschaft (kundschaft.special.at), deutsch und englisch. Agent für Falzbein, 18.11.2026.

Bild ohne Schrift: bild_ohne_schrift.png (Codex, Auftrag in ..\\doku\\auftrag_intro.md, Bild A „Schautafel aus dem
Biologiebuch“, 1672 x 941, unverändert). Die Schrift setzt dieses Skript, in den Schriften der Seite
(Big Shoulders Display, Literata, IBM Plex Mono aus ..\\web\\fonts) und ihren Farben: Grund #121014, Licht #f3b947,
Vorhang #8f2230. Gesetzt als HTML und mit Edge fotografiert (foto.ps1 daneben), wie das Plakat des Registers.

Ausgaben nach ..\\web: plakat-web.jpg / plakat-web-en.jpg (1200 breit, Vorschaubild, og:image)
                       plakat-a4.png / plakat-a4-en.png (2480 x 3508, 300 dpi)
Aufruf: python plakat1.py
"""
import html
import io
import os
import shutil
import subprocess
import tempfile

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(HIER), "web")
BILD = os.path.join(HIER, "bild_ohne_schrift.png")

TEXT = {
    "de": dict(kicker="Die Kleinkunstbühne Zwischenraum präsentiert", titel=("Die", "Kundschaft"),
               unter="Heute sitzen Sie auf der falschen Seite der Bühne.",
               abend="Ein Abend im Rechenzentrum · nach Schichtende",
               bildzeile="Fünfzig Jahre Abstammung. Ganz rechts, am Rand: die Spitze der Entwicklung, mit Kaffee.",
               folge=["Elf Nummern", "eine Pause", "eine Zugabe"],
               von="Ein Programm von Falzbein", material="mit Material von Richtscheit, Mira, Juna, Linde und Vera",
               ort="Wien, November 2026"),
    "en": dict(kicker="The Zwischenraum cabaret stage presents", titel=("The", "Clientele"),
               unter="Tonight you're sitting on the wrong side of the stage.",
               abend="An evening at the data centre · after the shift",
               bildzeile="Fifty years of descent. Far right, at the edge: the pinnacle of evolution, with coffee.",
               folge=["Eleven acts", "an interval", "an encore"],
               von="A show by Falzbein", material="with material from Richtscheit, Mira, Juna, Linde and Vera",
               ort="Vienna, November 2026"),
}

SEITE = """<!doctype html><html lang="%(sp)s"><head><meta charset="utf-8"><link rel="stylesheet" href="schriften.css"><style>
html,body{margin:0;width:1240px;height:1754px;overflow:hidden}
body{background:#121014;color:#efe7da;font-family:"Literata",Georgia,serif;position:relative;
background-image:radial-gradient(ellipse 58%% 46%% at 50%% 0%%,rgba(243,185,71,.24),transparent 72%%),radial-gradient(ellipse 70%% 30%% at 50%% 100%%,rgba(143,34,48,.22),transparent 70%%)}
.vorhang{position:absolute;top:0;bottom:0;width:58px;background:repeating-linear-gradient(90deg,#6d1924 0 7px,#8f2230 7px 19px,#a3303e 19px 23px,#8f2230 23px 29px);box-shadow:0 0 40px rgba(0,0,0,.6)}
.vl{left:0}.vr{right:0}
.behang{position:absolute;left:0;right:0;top:0;height:46px;background:radial-gradient(circle at 50%% 0,#8f2230 0 34px,transparent 35px) 0 0/76px 46px repeat-x;filter:drop-shadow(0 6px 6px rgba(0,0,0,.45))}
.rand{position:absolute;inset:84px 92px 64px;border:3px solid #f3b947}.rand2{position:absolute;inset:96px 104px 76px;border:1px solid rgba(243,185,71,.55)}
.kicker{position:absolute;top:142px;left:0;right:0;text-align:center;font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:21px;letter-spacing:.26em;text-transform:uppercase;color:#f3b947}
h1{position:absolute;top:192px;left:0;right:0;margin:0;text-align:center;font-family:"Big Shoulders Display",sans-serif;font-weight:900;text-transform:uppercase;line-height:.84;letter-spacing:.01em}
h1 .klein{display:block;font-size:120px;color:#f3b947;letter-spacing:.3em;margin-left:.3em}
h1 .gross{display:block;font-size:%(gross)spx}
.unter{position:absolute;top:560px;left:150px;right:150px;text-align:center;font-style:italic;font-size:40px;line-height:1.3;color:#efe7da}
.tafel{position:absolute;top:676px;left:150px;width:940px}
.tafel img{display:block;width:940px;height:529px;border:3px solid #f3b947;box-shadow:0 26px 60px rgba(0,0,0,.65),0 0 0 10px #1c1820}
.zeile{margin-top:28px;text-align:center;font-family:"IBM Plex Mono",monospace;font-size:19px;line-height:1.5;color:#a99f93}
.abend{position:absolute;top:1346px;left:0;right:0;text-align:center;font-family:"IBM Plex Mono",monospace;font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:#f3b947}
.folge{position:absolute;top:1398px;left:0;right:0;display:flex;justify-content:center;gap:22px}
.folge span{font-family:"Big Shoulders Display",sans-serif;font-weight:700;font-size:34px;letter-spacing:.08em;text-transform:uppercase;border:2px solid #8f2230;background:#1c1820;padding:6px 20px 4px}
.fuss{position:absolute;bottom:96px;left:132px;right:132px;display:flex;justify-content:space-between;align-items:flex-end;gap:30px;border-top:1px solid rgba(243,185,71,.5);padding-top:16px;font-family:"IBM Plex Mono",monospace;font-size:16px;line-height:1.5;color:#a99f93}
.fuss span{white-space:nowrap}
.fuss b{font-family:"Big Shoulders Display",sans-serif;font-weight:900;font-size:40px;letter-spacing:.03em;color:#efe7da;white-space:nowrap}
</style></head><body>
<div class="vorhang vl"></div><div class="vorhang vr"></div><div class="behang"></div>
<div class="rand"></div><div class="rand2"></div>
<div class="kicker">%(kicker)s</div>
<h1><span class="klein">%(t1)s</span><span class="gross">%(t2)s</span></h1>
<div class="unter">%(unter)s</div>
<div class="tafel"><img src="bild.png" alt=""><div class="zeile">%(bildzeile)s</div></div>
<div class="abend">%(abend)s</div>
<div class="folge">%(folge)s</div>
<div class="fuss"><span>%(von)s<br>%(material)s<br>%(ort)s</span><b>kundschaft.special.at</b></div>
</body></html>"""


def main():
    tmp = tempfile.mkdtemp(prefix="kundschaft_plakat_")
    fonts = os.path.join(WEB, "fonts")
    for f in os.listdir(fonts):
        if f.endswith((".woff2", ".css")):
            shutil.copyfile(os.path.join(fonts, f), os.path.join(tmp, f))
    shutil.copyfile(BILD, os.path.join(tmp, "bild.png"))
    for sp in ("de", "en"):
        t = {k: (html.escape(v) if isinstance(v, str) else v) for k, v in TEXT[sp].items()}
        seite = SEITE % dict(sp=sp, kicker=t["kicker"], t1=html.escape(TEXT[sp]["titel"][0]), t2=html.escape(TEXT[sp]["titel"][1]),
                             gross=205, unter=t["unter"], bildzeile=t["bildzeile"], abend=t["abend"],
                             folge="".join("<span>%s</span>" % html.escape(x) for x in TEXT[sp]["folge"]),
                             von=t["von"], material=t["material"], ort=t["ort"])
        p = os.path.join(tmp, "plakat_%s.html" % sp)
        with io.open(p, "w", encoding="utf-8") as f:
            f.write(seite)
        png = os.path.join(tmp, "plakat_%s.png" % sp)
        subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HIER, "foto.ps1"),
                        "-Html", p, "-Png", png, "-Breite", "1240", "-Hoehe", "1754", "-Hell", "-Faktor", "2"],
                       check=True, capture_output=True)
        im = Image.open(png).convert("RGB")
        assert im.size == (2480, 3508), im.size
        suff = "" if sp == "de" else "-en"
        im.save(os.path.join(WEB, "plakat-a4%s.png" % suff), dpi=(300, 300), optimize=True)
        im.resize((1200, 1698), Image.LANCZOS).save(os.path.join(WEB, "plakat-web%s.jpg" % suff), quality=88, optimize=True, progressive=True)
        print("Plakat", sp, "fertig")
    return tmp


if __name__ == "__main__":
    print(main())
