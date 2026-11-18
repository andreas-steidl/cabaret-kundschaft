# -*- coding: utf-8 -*-
"""Freigabe nach HAUS.md, Abschnitt 4.1: Verweise in jeder HTML-Datei gegen die vorhandenen Dateien zählen.
Agent für Falzbein, 18.11.2026.

Prüft alle .html (ohne *.vor-*) im web-Ordner jedes Hauses aus haus.json, dazu fonts/schriften.css.
Gezählt werden href, src, srcset, content="https://<haus>/...", url(...) in CSS und die bild:-Einträge der Litfaßsäule.
Relative Verweise werden gegen die Datei aufgelöst; https://<host eines Hauses>/... gegen den web-Ordner dieses Hauses.
Fremde Hosts werden nur gezählt. Ende mit Exit 1, wenn etwas fehlt.
Aufruf: python verweise_pruefen.py [host ...]     ohne Host: alle Häuser
"""
import io
import json
import os
import re
import sys
from urllib.parse import urlparse, unquote

B = chr(92)
DEV = B + B + B.join(["nas", "Public", "dev"])
HAUS_JSON = os.path.join(DEV, "kabarett", "haus.json")
MUSTER = [r'(?:href|src)="([^"]+)"', r'srcset="([^"]+)"', r'content="(https://[^"]+)"', r'url\(([^)]+)\)', r'bild: "([^"]+)"']


def web_ordner(h):
    w = os.path.join(DEV, *h["werkstatt"].split(B))
    return w if h["werkstatt"] == "falzbein-seite" else os.path.join(w, "web")


def ziele(text):
    for m in MUSTER:
        for v in re.findall(m, text):
            for teil in (v.split(",") if "srcset" in m else [v]):
                teil = teil.strip().split(" ")[0].strip("'\"")
                if teil:
                    yield teil


def main(nur):
    hs = json.load(io.open(HAUS_JSON, encoding="utf-8"))["haeuser"]
    hosts = {h["host"]: web_ordner(h) for h in hs}
    fehler, gesamt = [], 0
    for h in hs:
        if nur and h["host"] not in nur:
            continue
        web = web_ordner(h)
        dateien = []
        for wurzel, dirs, files in os.walk(web):
            dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
            dateien += [os.path.join(wurzel, f) for f in files
                        if (f.endswith(".html") and ".vor-" not in f) or (f == "schriften.css")]
        zaehl, vorlagen = 0, 0
        for p in sorted(dateien):
            t = io.open(p, encoding="utf-8").read()
            for z in ziele(t):
                if "${" in z:  # Vorlage in einem Skript (`../${n}.zip`), kein Verweis
                    vorlagen += 1
                    continue
                if z.startswith(("#", "mailto:", "data:", "javascript:")) or z.startswith("http://www.w3.org"):
                    continue
                u = urlparse(z)
                if u.scheme in ("http", "https"):
                    if u.netloc not in hosts:
                        continue
                    basis = hosts[u.netloc]
                    pfad = os.path.join(basis, *[x for x in unquote(u.path).split("/") if x])
                else:
                    pfad = os.path.normpath(os.path.join(os.path.dirname(p), unquote(u.path)))
                if unquote(u.path).endswith("/") or os.path.isdir(pfad):
                    pfad = os.path.join(pfad, "index.html")
                zaehl += 1
                if not os.path.isfile(pfad):
                    fehler.append("%s -> %s" % (os.path.relpath(p, web), z))
        gesamt += zaehl
        print("%-30s %3d Dateien, %4d Verweise geprüft%s" % (h["host"], len(dateien), zaehl,
                                                              ", %d Skript-Vorlagen übergangen" % vorlagen if vorlagen else ""))
    for f in fehler:
        print("  FEHLT:", f)
    print("Verweise gesamt:", gesamt, "· fehlend:", len(fehler))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
