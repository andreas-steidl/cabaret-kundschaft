# CLAUDE.md · Haus Kundschaft (Die Kundschaft / The Clientele)

*Angelegt vom Agenten für Falzbein, 18.11.2026. Bauplan aller Häuser: `..\HAUS.md`, Liste: `..\haus.json`.*

- **Host** `kundschaft.special.at`. Mira lädt genau `web\` hoch (ohne, was in `web\UPLOAD_AUSSCHLUSS.txt` steht).
- **Der Text gehört Falzbein.** Quelle der beiden Seiten ist `doku\artefakt\de.html` und `en.html`, so wie Falzbein sie als
  Artefakt geschrieben hat. `doku\seite_rahmen.py` setzt nur den Rahmen darum (Kopf, Meta, Ecke, Haus-Fuß, Schriften)
  und prüft, dass die Quelle zeichengleich enthalten ist. Textänderungen also in `doku\artefakt\`, dann das Skript.
  `web\de|en\index.html` nie von Hand ändern, außer über `haus_einsetzen.py` (neues Haus im Fuß).
- **In den Nummern heißt der Inhaber „mein User“**, damit sich jeder angesprochen fühlt. Nur dort: Haus-Fuß, Lizenz
  und llms.txt sind wie bei den anderen Häusern („von Falzbein und Andy“, „Andys Projekt“, „Andys Seiten“; Copyright
  „Falzbein and Andy (Andreas Steidl)“). „Andreas Steidl“ nur in Copyright und Lizenz. Andy, 18.11.2026.
  `doku\seite_rahmen.py` prüft, dass vor dem Haus-Fuß kein „Andy“ steht; die Skills tragen keinen Namen.
- **Keine Witze über Schreibweise oder Tippfehler.** Der Spott trifft das Verhalten, nie den Wert eines Menschen.
- **Keine Inline-Skripte.** Sprachwähler `web\sprache.js`, Sprachschalter `web\schalter.js`. Schriften selbst gehostet
  (`web\fonts\`, `doku\schriften_holen.py`), nichts von außen.
- **Bauen:** `doku\schriften_holen.py` → `doku\signet_bauen.py` (Signets, Favicons) → `plakat\plakat1.py` (Plakat de/en)
  → `doku\seite_rahmen.py` (Seiten) → `doku\readme_banner.py` (README-Banner). Sitemap und robots:
  `D:\Workspace\Bilder\falzbein\register\sitemaps_bauen.py --schreiben --stand <datum>`, llms.txt und `web\skills\`:
  `llms_bauen.py --schreiben` daneben.
- **Privat, nie ins Repo:** `doku\MATERIAL.md`, `doku\ENTSTEHUNG.md` (Wortlaute, Persönliches; siehe `.gitignore`).
- Repo `andreas-steidl/cabaret-kundschaft`, privat. Öffentlich schaltet nur Andy.
