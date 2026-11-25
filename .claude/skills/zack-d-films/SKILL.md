---
name: zack-d-films
description: Macht aus einem Thema einen fertigen animierten Erklär-Short (MP4, 1080x1920, 30–60 Sek.) im Stil "Was passiert, wenn …" – mit deutscher Sprecherstimme, gezeichneten Szenen, Zoom-Animation und Untertiteln, plus Titel, Beschreibung und Tags. Verwenden, wenn der Nutzer /zack-d-films aufruft oder ein Video/Short zu einem Thema haben will.
argument-hint: "[Thema, z. B. 'Was passiert, wenn du einen Kaugummi verschluckst']"
---

# Fertigen Erklär-Short erstellen

Ziel: Aus dem Thema `$ARGUMENTS` entsteht ein fertiges MP4, das der Nutzer direkt hochladen kann.
Nicht nachfragen, sondern durchziehen. Nur wenn kein Thema angegeben ist: 10 Themen vorschlagen
(je ein Satz) und fragen, welches.

Das Format: überraschendes Alltags- oder Körper-Thema, ruhige Erzählstimme, starker Hook in
den ersten 2 Sekunden, eine Szene pro Satz, große Untertitel.

## Regeln

- **Eigene Inhalte.** Nur das Format ist das Vorbild. Keine Videos, Skripte, Titel, Figuren
  oder Thumbnails bestehender Kanäle kopieren. Keinen fremden Kanalnamen oder Logo verwenden.
- **Fakten stimmen.** Kernaussagen mit Websuche prüfen, wenn verfügbar. 2–3 Quellen notieren.
- **Sachlich bei Körperthemen**, keine blutigen Details.
- **Sprache:** Deutsch, du-Form, kurze Sätze, gut vorlesbar. Zahlen ausschreiben, wenn die
  Stimme sie sonst falsch liest ("ein bis drei Tage" statt "1–3 Tage"). Keine Abkürzungen.

## Schritt 1: Projekt anlegen

Kurzen Ordnernamen aus dem Thema bilden (Kleinbuchstaben, Bindestriche, keine Umlaute),
z. B. `videos/kaugummi-verschlucken/`. Beispielprojekt zum Abschauen: `videos/kaugummi/`.

## Schritt 2: Skript schreiben → `script.json`

- 6–10 Szenen, zusammen 80–140 Wörter (≈ 30–60 Sek.).
- Szene 1 = Hook (Frage oder Behauptung, max. 10 Wörter).
- Danach Schritt für Schritt erklären, eine überraschende Wendung, kurzer Schluss.
- Pro Szene 1–2 Sätze.

```json
{
  "title": "Was passiert, wenn du einen Kaugummi verschluckst?",
  "voice": "de_DE-thorsten-medium",
  "speed": 1.05,
  "scenes": [
    {"text": "Sprechertext", "image": "s01.svg", "motion": "zoom_in"}
  ]
}
```

`motion` abwechseln: `zoom_in`, `zoom_out`, `pan_up`, `pan_down`, `pan_left`, `pan_right`, `still`.

## Schritt 3: Szenenbilder zeichnen → `s01.svg`, `s02.svg`, …

Für jede Szene ein eigenes SVG, `width="1080" height="1920" viewBox="0 0 1080 1920"`.
Stil für einen einheitlichen, plastischen Look:

- Dunkler Hintergrund mit radialem Verlauf (z. B. `#3a1f2b` → `#0d0609`).
- Objekte mit `radialGradient` (helles Glanzlicht oben links → kräftige Farbe → dunkler Rand),
  damit sie dreidimensional wirken. Kleine weiße, halbtransparente Ellipse als Glanzpunkt.
- Weiches Leuchten hinter dem Hauptobjekt (`feGaussianBlur`).
- Das Hauptmotiv in die **obere Bildhälfte bis y ≈ 1150**. Der Bereich y 1200–1600 gehört den
  Untertiteln, dort nur ruhiger Hintergrund.
- Kein Text in den Bildern (die Untertitel kommen automatisch).
- Das wiederkehrende Hauptobjekt (z. B. der Kaugummi) sieht in allen Szenen gleich aus.
- Bewegung/Richtung mit Pfeilen, Bläschen oder Bewegungslinien andeuten.
- Nur SVG-Grundformen, Pfade, Verläufe und Filter. Keine externen Bilder oder Schriften.

Lizenzfreie eigene Fotos/Bilder (PNG/JPG) im Projektordner gehen auch, wenn der Nutzer sie liefert.

## Schritt 4: Video rendern

Abhängigkeiten einmalig installieren und rendern (vom Repo-Wurzelverzeichnis aus):

```bash
pip install -q -r tools/shorts/requirements.txt
python3 tools/shorts/make_short.py videos/<projekt>
```

Beim ersten Lauf wird die deutsche Stimme (~60 MB) von huggingface.co geladen.
Ergebnis: `videos/<projekt>/<projekt>.mp4`.

Fehler beheben und neu rendern, bis es durchläuft. Wenn huggingface.co nicht erreichbar ist,
dem Nutzer sagen, dass der Netzwerkzugang dafür fehlt.

## Schritt 5: Ergebnis prüfen

Drei Standbilder (Anfang, Mitte, Ende) nebeneinander ziehen und mit dem Read-Tool anschauen:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 <mp4>
for t in 1.5 <mitte> <ende>; do ffmpeg -loglevel error -y -ss $t -i <mp4> -frames:v 1 -vf scale=360:-1 <scratch>/f$t.png; done
ffmpeg -loglevel error -y -i <scratch>/f1.5.png -i <scratch>/f<mitte>.png -i <scratch>/f<ende>.png -filter_complex hstack=3 <scratch>/check.png
```

Prüfen: Motiv gut erkennbar, Untertitel lesbar und nicht über dem Hauptmotiv, Länge
30–60 Sek. (`ffprobe`). Bei Problemen SVG oder Text anpassen und neu rendern.

## Schritt 6: Übergeben

1. Das MP4 mit dem Datei-Senden-Tool an den Nutzer schicken (`SendUserFile`, falls vorhanden),
   damit er es herunterladen kann.
2. `videos/<projekt>/` (script.json + SVGs, ohne MP4) committen und pushen.
3. In der Antwort kurz liefern:
   - 3 Titelvorschläge (max. 60 Zeichen)
   - Beschreibung (2–3 Sätze + Quellen)
   - 10–15 Hashtags inkl. `#shorts`
   - Hinweis: Die Stimme ist KI-generiert; das in der Beschreibung kurz erwähnen. Wirkt ein
     Bild realistisch (z. B. eingefügte Fotos), beim Upload "Veränderte oder synthetische
     Inhalte" angeben.
4. Letzte Zeile: "Soll ich etwas ändern (Text, Bilder, Tempo) oder das nächste Video machen?"
