---
name: zack-d-films
description: Plant einen kurzen 3D-Erklär-Short (30–60 Sek., Hochformat) im Stil "Was passiert, wenn …" / "So funktioniert …" – mit Hook, Sprechertext, Szenenliste, Prompts für Bild- und Video-KI, Titel, Beschreibung und Tags. Verwenden, wenn der Nutzer /zack-d-films aufruft oder einen solchen Short planen will.
argument-hint: "[Thema, z. B. 'Was passiert, wenn du einen Kaugummi verschluckst']"
---

# 3D-Erklär-Short planen

Du planst einen kurzen, animierten Erklär-Short für YouTube Shorts, TikTok und Reels.
Das Format: ein überraschendes Alltags- oder Körper-Thema, erklärt in 30–60 Sekunden mit
realistischer 3D-Animation, einer ruhigen Erzählstimme und einem starken Hook.

Thema: `$ARGUMENTS`

Ist kein Thema angegeben, schlage zuerst 10 Themen vor (Liste mit je einem Satz, warum es
neugierig macht) und frag, welches genommen werden soll. Danach weiter mit Schritt 1.

## Regeln

- **Eigene Inhalte.** Nur das Format ist das Vorbild. Keine Videos, Skripte, Titel, Figuren
  oder Thumbnails bestehender Kanäle kopieren oder nachbauen. Keinen fremden Kanalnamen
  nennen und kein fremdes Logo verwenden.
- **Fakten stimmen.** Nur belegbare Aussagen. Wenn Websuche verfügbar ist, prüfe die
  Kernfakten und nenne 2–3 Quellen am Ende. Unsichere Punkte klar markieren.
- **Keine Schockeffekte um ihrer selbst willen.** Medizinische Themen sachlich und ohne
  blutige Details beschreiben (YouTube-Richtlinien, Altersfreigabe).
- **Sprache:** Deutsch, du-Form, kurze Sätze, die man gut vorlesen kann.

## Ablauf

### 1. Hook (0–2 Sek.)
Drei Varianten, jeweils max. 10 Wörter. Der Hook stellt eine Frage oder Behauptung, die
man beantwortet sehen will ("Das passiert in deinem Magen, wenn …"). Empfiehl eine.

### 2. Sprechertext
Komplettes Skript zum Vorlesen, 80–140 Wörter (≈ 30–60 Sek.).
- Aufbau: Hook → Schritt für Schritt erklären → überraschende Wendung → kurzer Schluss,
  der zum erneuten Anschauen einlädt (Loop: der letzte Satz führt zurück zum Anfang).
- Gib die geschätzte Länge in Sekunden an.

### 3. Szenenliste
Tabelle mit 6–10 Szenen:

| Nr. | Zeit | Sprechertext | Was man sieht | Kamera |
| --- | --- | --- | --- | --- |

"Was man sieht" konkret beschreiben (Objekt, Material, Licht, Bewegung).
Kamera z. B.: Nahaufnahme, Fahrt in den Körper hinein, Querschnitt, Zeitlupe.

### 4. KI-Prompts pro Szene
Für jede Szene einen englischen Prompt, der in Bild- oder Video-KIs funktioniert.
Einheitlicher Stil-Zusatz an jedem Prompt, damit alle Szenen gleich aussehen:

`photorealistic 3D render, cinematic lighting, shallow depth of field, clean neutral background, vertical 9:16, 4k, smooth camera motion`

Bei Video-KI zusätzlich Bewegung und Dauer (z. B. "slow push-in, 4 seconds").

### 5. Ton
- Musik: Stimmung + Tempo (z. B. "ruhig, mysteriös, 90 BPM") – nur lizenzfreie Musik
  (YouTube Audio Library).
- 2–4 Soundeffekte mit Zeitpunkt.
- Stimme: Hinweis, wie gesprochen werden soll (ruhig, leicht flüsternd, Pausen wo).

### 6. Veröffentlichung
- 5 Titel (max. 60 Zeichen, auf Deutsch, neugierig machend, kein Clickbait, das das Video
  nicht einlöst).
- Beschreibung (2–3 Sätze + Quellen).
- 10–15 Tags / Hashtags, darunter `#shorts`.
- Hinweis: Beim Upload "veränderte oder synthetische Inhalte" angeben, wenn die Animation
  realistisch wirkt.

### 7. Umsetzung (kurz)
Zwei Wege in je 2–3 Sätzen nennen:
- **Kostenlos:** Blender (3D-Modelle, z. B. von Sketchfab mit passender Lizenz) + DaVinci
  Resolve oder CapCut für Schnitt und Untertitel.
- **Mit KI-Video:** Szenen-Prompts aus Schritt 4 in einen KI-Videogenerator, Stimme mit
  eigener Aufnahme oder Piper, Schnitt in CapCut.

## Ausgabe

Alles in einer Antwort, mit Überschriften für die Schritte 1–7. Am Ende eine Zeile:
"Soll ich etwas anpassen (Hook, Länge, Stil) oder das nächste Thema planen?"
