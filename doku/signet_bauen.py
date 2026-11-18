# -*- coding: utf-8 -*-
"""Signets (rund, eckig) und Favicons des Hauses Kundschaft. Agent für Falzbein, 18.11.2026.

Farben der Seite: Grund #121014, Bühne #1c1820, Licht #f3b947, Vorhang #8f2230.
Motiv: der Vorhang ist offen, ein Lichtkegel fällt auf die Kundschaft, und die Kundschaft ist eine Kaffeetasse
(der kleine Mensch am Rand des Titelbilds hat einen Kaffee). Name im Ring „KUNDSCHAFT“, als Pfade gesetzt
(Big Shoulders Display 900 aus web\\fonts), damit das Signet auch als <img> ohne Schrift richtig steht.
Favicon: ohne Ringtext, gerendert mit Edge (foto.ps1 im Ordner plakat), Größen 16/32/48 und 180.

Aufruf: python signet_bauen.py     schreibt web\\signets\\signet-kundschaft-rund.svg, -eckig.svg,
                                    web\\favicon.ico, web\\favicon-32.png, web\\apple-touch-icon.png
"""
import math
import os
import shutil
import subprocess
import tempfile

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(HIER)
WEB = os.path.join(HAUS, "web")
FOTO = os.path.join(HAUS, "plakat", "foto.ps1")

GRUND, BUEHNE, LICHT, VORHANG, TEXT = "#121014", "#1c1820", "#f3b947", "#8f2230", "#efe7da"


class Schrift:
    def __init__(self, pfad, wght):
        self.f = TTFont(pfad)
        self.gs = self.f.getGlyphSet(location={"wght": wght})
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm

    def glyph(self, ch):
        return self.gs[self.cmap[ord(ch)]]

    def breite(self, text, groesse, sperre=0.0):
        s = groesse / self.upm
        return sum(self.glyph(c).width * s for c in text) + sperre * groesse * (len(text) - 1)

    def pfad(self, ch, groesse, matrix):
        """Pfad eines Zeichens; matrix bildet Font-Einheiten (y nach oben) auf das Bild ab."""
        pen = SVGPathPen(self.gs)
        self.glyph(ch).draw(TransformPen(pen, matrix))
        return pen.getCommands()


def zahl(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


def text_gerade(s, text, groesse, cx, grundlinie, sperre=0.0):
    """Waagerechter Text, zentriert auf cx; liefert ein d-Attribut."""
    k = groesse / s.upm
    x = cx - s.breite(text, groesse, sperre) / 2
    teile = []
    for c in text:
        teile.append(s.pfad(c, groesse, (k, 0, 0, -k, x, grundlinie)))
        x += s.glyph(c).width * k + sperre * groesse
    return " ".join(teile)


def text_bogen(s, text, groesse, r, mitte_grad=-90, sperre=0.0):
    """Text auf einem Kreis um (100,100), Grundlinie auf Radius r, oben lesbar, zentriert bei mitte_grad."""
    k = groesse / s.upm
    gesamt = s.breite(text, groesse, sperre)
    winkel = math.degrees(gesamt / r)
    a = mitte_grad - winkel / 2
    teile = []
    for c in text:
        w = s.glyph(c).width * k
        am = math.radians(a + math.degrees((w / 2) / r))
        # Mitte des Zeichens auf dem Kreis, Zeichen tangential gedreht
        px, py = 100 + r * math.cos(am), 100 + r * math.sin(am)
        rot = am + math.pi / 2
        ca, sa = math.cos(rot), math.sin(rot)
        # lokales System: x' entlang der Tangente, y' nach außen (Font-y nach oben = zum Kreisrand)
        m = (ca * k, sa * k, sa * k, -ca * k, px - ca * w / 2, py - sa * w / 2)
        teile.append(s.pfad(c, groesse, m))
        a += math.degrees((w + sperre * groesse) / r)
    return " ".join(teile)


def tasse(x, y, m=1.0, licht=LICHT, grund=GRUND):
    """Kaffeetasse mit Untertasse und Dampf, Mittelpunkt des Bodens bei (x, y), Maßstab m."""
    def p(px, py):
        return "%s %s" % (zahl(x + px * m), zahl(y + py * m))
    sw = zahl(2.2 * m)
    return (
        '<g fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">' % (licht, sw)
        + '<path d="M%s Q%s %s"/>' % (p(-11, -27), p(-14, -33), p(-11, -38))
        + '<path d="M%s Q%s %s"/>' % (p(-1, -29), p(-4, -36), p(-1, -42))
        + '<path d="M%s Q%s %s"/>' % (p(9, -27), p(6, -33), p(9, -38))
        + "</g>"
        + '<path d="M%s L%s Q%s %s L%s Q%s %s Z" fill="%s"/>' % (
            p(-17, -22), p(17, -22), p(16, -4), p(9, -1), p(-9, -1), p(-16, -4), p(-17, -22), licht)
        + '<path d="M%s Q%s %s Q%s %s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            p(16, -18), p(27, -18), p(25, -11), p(23, -6), p(14, -7), licht, zahl(2.6 * m))
        + '<path d="M%s L%s" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity=".55"/>' % (
            p(-12, -18), p(11, -18), grund, zahl(1.3 * m))
        + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (
            zahl(x), zahl(y + 1 * m), zahl(26 * m), zahl(3.4 * m), licht)
    )


def buehne(clip_id, clip_form, cx, oben, unten, breite):
    """Lichtkegel von oben und offener Vorhang, beschnitten auf clip_form."""
    kegel = ('<defs><clipPath id="%s">%s</clipPath><linearGradient id="%s-k" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity=".05"/><stop offset="1" stop-color="%s" stop-opacity=".34"/>'
             '</linearGradient></defs>' % (clip_id, clip_form, clip_id, LICHT, LICHT))
    g = '<g clip-path="url(#%s)">' % clip_id
    g += '<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="url(#%s-k)"/>' % (
        zahl(cx - 7), zahl(oben), zahl(cx + 7), zahl(oben), zahl(cx + 34), zahl(unten), zahl(cx - 34), zahl(unten), clip_id)
    l, r = cx - breite / 2, cx + breite / 2
    # Vorhang: links und rechts gerafft, oben ein Querbehang mit Bögen
    g += ('<path d="M%s %s L%s %s Q%s %s %s %s Q%s %s %s %s Z" fill="%s"/>' % (
        zahl(l), zahl(oben), zahl(l + 30), zahl(oben), zahl(l + 20), zahl(oben + 40), zahl(l + 24), zahl(unten - 8),
        zahl(l + 10), zahl(unten), zahl(l), zahl(unten), VORHANG))
    g += ('<path d="M%s %s L%s %s Q%s %s %s %s Q%s %s %s %s Z" fill="%s"/>' % (
        zahl(r), zahl(oben), zahl(r - 30), zahl(oben), zahl(r - 20), zahl(oben + 40), zahl(r - 24), zahl(unten - 8),
        zahl(r - 10), zahl(unten), zahl(r), zahl(unten), VORHANG))
    bogen = "M%s %s" % (zahl(l), zahl(oben))
    n = 4
    for i in range(n):
        x0 = l + breite * i / n
        x1 = l + breite * (i + 1) / n
        bogen += " Q%s %s %s %s" % (zahl((x0 + x1) / 2), zahl(oben + 20), zahl(x1), zahl(oben))
    g += '<path d="%s Z" fill="%s"/>' % (bogen, VORHANG)
    g += '<path d="%s" fill="none" stroke="%s" stroke-width="1.2" opacity=".7"/>' % (bogen, LICHT)
    g += "</g>"
    return kegel + g


def rund(s, mit_text=True):
    teile = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">',
             "<title>Die Kundschaft</title>",
             '<circle cx="100" cy="100" r="99" fill="%s"/>' % GRUND,
             '<circle cx="100" cy="100" r="95.5" fill="none" stroke="%s" stroke-width="1.1" opacity="0.8"/>' % LICHT]
    ri = 67 if mit_text else 86
    teile.append('<circle cx="100" cy="100" r="%d" fill="%s"/>' % (ri, BUEHNE))
    teile.append(buehne("kr" if mit_text else "kf", '<circle cx="100" cy="100" r="%d"/>' % ri, 100, 100 - ri, 100 + ri, 2 * ri))
    if mit_text:
        teile.append(tasse(100, 140, 1.25))
        teile.append('<path d="M60 141.5 H140" stroke="%s" stroke-width="1" opacity=".35"/>' % LICHT)
    else:
        teile.append(tasse(100, 154, 1.85))
    teile.append('<circle cx="100" cy="100" r="%d" fill="none" stroke="%s" stroke-width="%s"/>' % (ri, LICHT, "1.6" if mit_text else "3"))
    if mit_text:
        teile.append('<path d="%s" fill="%s"/>' % (text_bogen(s, "KUNDSCHAFT", 21, 75.5, -90, 0.14), TEXT))
        for grad in (150, 90, 30):  # drei Scheinwerfer unten
            a = math.radians(grad)
            teile.append('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (zahl(100 + 81 * math.cos(a)), zahl(100 + 81 * math.sin(a)), LICHT))
        for grad in (180, 0):
            a = math.radians(grad)
            x, y = 100 + 81 * math.cos(a), 100 + 81 * math.sin(a)
            teile.append('<path d="M%s %s l3 -3 l3 3 l-3 3 Z" fill="%s"/>' % (zahl(x - 3), zahl(y), LICHT))
    teile.append("</svg>")
    return "\n".join(teile) + "\n"


def eckig(s):
    teile = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">',
             "<title>Die Kundschaft</title>",
             '<rect x="2" y="2" width="196" height="196" rx="30" fill="%s"/>' % GRUND,
             '<rect x="11" y="11" width="178" height="178" rx="23" fill="%s" stroke="%s" stroke-width="1.4"/>' % (BUEHNE, LICHT),
             buehne("ke", '<rect x="12" y="12" width="176" height="128" rx="22"/>', 100, 12, 140, 176),
             tasse(100, 122, 1.3),
             '<path d="M30 140 H170" stroke="%s" stroke-width="1.2" opacity=".6"/>' % LICHT,
             '<path d="%s" fill="%s"/>' % (text_gerade(s, "KUNDSCHAFT", 31, 100, 173, 0.06), TEXT),
             "</svg>"]
    return "\n".join(teile) + "\n"


def favicons(svg_text):
    tmp = tempfile.mkdtemp(prefix="kundschaft_favicon_")
    q = os.path.join(tmp, "favicon-quelle.svg")
    with open(q, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg_text)
    bilder = {}
    for n in (180, 48, 32, 16):
        h = os.path.join(tmp, "fav%d.html" % n)
        with open(h, "w", encoding="utf-8") as f:
            f.write('<html><body style="margin:0;background:transparent"><img src="favicon-quelle.svg" width=%d height=%d style="display:block"></body></html>' % (n, n))
        png = os.path.join(tmp, "fav%d.png" % n)
        subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", FOTO, "-Html", h, "-Png", png,
                        "-Breite", str(n), "-Hoehe", str(n), "-Hell"], check=True, capture_output=True)
        bilder[n] = Image.open(png).convert("RGBA")
        assert bilder[n].size == (n, n), (n, bilder[n].size)
    bilder[48].save(os.path.join(WEB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=[bilder[16], bilder[32]])
    bilder[32].save(os.path.join(WEB, "favicon-32.png"))
    grund = Image.new("RGBA", (180, 180), (18, 16, 20, 255))
    grund.alpha_composite(bilder[180])
    grund.convert("RGB").save(os.path.join(WEB, "apple-touch-icon.png"))
    shutil.copyfile(q, os.path.join(HIER, "favicon-quelle.svg"))
    return tmp


def main():
    s = Schrift(os.path.join(WEB, "fonts", "bigshouldersdisplay-normal-var-latin.woff2"), 900)
    os.makedirs(os.path.join(WEB, "signets"), exist_ok=True)
    for name, inhalt in (("signet-kundschaft-rund.svg", rund(s)), ("signet-kundschaft-eckig.svg", eckig(s))):
        with open(os.path.join(WEB, "signets", name), "w", encoding="utf-8", newline="\n") as f:
            f.write(inhalt)
    print("Favicon-Zwischenordner:", favicons(rund(s, mit_text=False)))
    print("fertig:", sorted(f for f in os.listdir(WEB) if f.startswith(("favicon", "apple"))))


if __name__ == "__main__":
    main()
