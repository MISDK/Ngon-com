#!/usr/bin/env python3
"""Rendert einen fertigen Short (MP4, 1080x1920) aus einem Projektordner.

Projektordner:
    script.json   Szenen mit Sprechertext und Bild
    *.svg / *.png Ein Bild pro Szene (am besten 1080x1920 oder groesser)

script.json:
{
  "title": "Was passiert, wenn du einen Kaugummi verschluckst?",
  "voice": "de_DE-thorsten-medium",      (optional)
  "speed": 1.0,                           (optional, >1 = langsamer)
  "scenes": [
    {"text": "Sprechertext der Szene", "image": "s01.svg", "motion": "zoom_in"},
    ...
  ]
}
motion: zoom_in | zoom_out | pan_up | pan_down | pan_left | pan_right | still

Aufruf:
    python3 tools/shorts/make_short.py videos/<projekt>
Ergebnis:
    videos/<projekt>/<projekt>.mp4
"""

import io
import json
import math
import subprocess
import sys
import tempfile
import urllib.request
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
OVERSCAN = 1.18  # Bild wird groesser gerendert, damit Zoom/Schwenk Platz hat
PAD = 0.35  # Pause nach jeder Szene in Sekunden
VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"
CACHE = Path.home() / ".cache" / "piper"
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def voice_model(name: str) -> Path:
    """Laedt eine Piper-Stimme beim ersten Mal herunter."""
    CACHE.mkdir(parents=True, exist_ok=True)
    lang = name.split("-")[0]  # de_DE
    family = lang.split("_")[0]  # de
    _, speaker, quality = name.split("-")
    onnx = CACHE / f"{name}.onnx"
    for suffix in (".onnx", ".onnx.json"):
        target = CACHE / f"{name}{suffix}"
        if not target.exists():
            url = f"{VOICE_BASE}/{family}/{lang}/{speaker}/{quality}/{name}{suffix}"
            print(f"Lade Stimme: {url}")
            urllib.request.urlretrieve(url, target)
    return onnx


def synthesize(voice, text: str, out: Path, speed: float) -> float:
    from piper import SynthesisConfig

    with wave.open(str(out), "wb") as wf:
        voice.synthesize_wav(text, wf, syn_config=SynthesisConfig(length_scale=speed))
    with wave.open(str(out), "rb") as wf:
        return wf.getnframes() / wf.getframerate()


def load_image(path: Path) -> Image.Image:
    bw, bh = int(W * OVERSCAN), int(H * OVERSCAN)
    if path.suffix.lower() == ".svg":
        import cairosvg

        png = cairosvg.svg2png(url=str(path), output_width=bw, output_height=bh)
        img = Image.open(io.BytesIO(png))
    else:
        img = Image.open(path)
    img = img.convert("RGB")
    # auf Hochformat zuschneiden (cover)
    scale = max(bw / img.width, bh / img.height)
    img = img.resize((math.ceil(img.width * scale), math.ceil(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - bw) // 2, (img.height - bh) // 2
    return img.crop((left, top, left + bw, top + bh))


def ease(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)


def frame_at(img: Image.Image, motion: str, t: float) -> Image.Image:
    """Ken-Burns-Ausschnitt bei Fortschritt t (0..1)."""
    e = ease(t)
    bw, bh = img.size
    zoom = 1.0
    cx, cy = 0.5, 0.5
    if motion == "zoom_in":
        zoom = 1.0 + 0.15 * e
    elif motion == "zoom_out":
        zoom = 1.15 - 0.15 * e
    elif motion == "pan_left":
        cx = 0.58 - 0.16 * e
    elif motion == "pan_right":
        cx = 0.42 + 0.16 * e
    elif motion == "pan_up":
        cy = 0.58 - 0.16 * e
    elif motion == "pan_down":
        cy = 0.42 + 0.16 * e
    cw, ch = W / zoom, H / zoom
    x = min(max(cx * bw - cw / 2, 0), bw - cw)
    y = min(max(cy * bh - ch / 2, 0), bh - ch)
    return img.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def chunks(text: str, n: int = 4) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + n]) for i in range(0, len(words), n)] or [""]


def caption_timeline(text: str, duration: float) -> list[tuple[float, str]]:
    """Untertitel-Bloecke, zeitlich nach Textlaenge verteilt."""
    parts = chunks(text)
    total = sum(len(p) + 3 for p in parts)
    t, out = 0.0, []
    for p in parts:
        out.append((t, p))
        t += duration * (len(p) + 3) / total
    return out


def draw_caption(frame: Image.Image, text: str, f: ImageFont.FreeTypeFont) -> None:
    if not text:
        return
    d = ImageDraw.Draw(frame)
    words, lines, line = text.split(), [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if d.textlength(test, font=f) > W * 0.86 and line:
            lines.append(line)
            line = w
        else:
            line = test
    lines.append(line)
    lh = f.size * 1.2
    y = H * 0.70 - lh * len(lines) / 2
    for ln in lines:
        d.text((W / 2, y), ln.upper(), font=f, fill="white", anchor="ma",
               stroke_width=10, stroke_fill="black")
        y += lh


def main(project: Path) -> Path:
    spec = json.loads((project / "script.json").read_text(encoding="utf-8"))
    scenes = spec["scenes"]
    speed = float(spec.get("speed", 1.0))

    from piper import PiperVoice

    voice = PiperVoice.load(str(voice_model(spec.get("voice", "de_DE-thorsten-medium"))))
    cap_font = font(78)
    out = project / f"{project.name}.mp4"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        durations = []
        for i, sc in enumerate(scenes):
            d = synthesize(voice, sc["text"], tmp / f"a{i:02d}.wav", speed)
            durations.append(d + PAD)
            print(f"Szene {i + 1}: {d:.1f} s Ton")

        # Ton zusammensetzen (mit Pause nach jeder Szene)
        audio = tmp / "voice.wav"
        filt = ";".join(f"[{i}:a]apad=pad_dur={PAD}[p{i}]" for i in range(len(scenes)))
        filt += ";" + "".join(f"[p{i}]" for i in range(len(scenes)))
        filt += f"concat=n={len(scenes)}:v=0:a=1[out]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for i in range(len(scenes)):
            cmd += ["-i", str(tmp / f"a{i:02d}.wav")]
        cmd += ["-filter_complex", filt, "-map", "[out]", str(audio)]
        subprocess.run(cmd, check=True)

        # Bilder rendern und an ffmpeg schicken
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
             "-i", str(audio),
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)],
            stdin=subprocess.PIPE,
        )
        for i, sc in enumerate(scenes):
            img = load_image(project / sc["image"])
            motion = sc.get("motion", "zoom_in")
            n = round(durations[i] * FPS)
            timeline = caption_timeline(sc["text"], durations[i] - PAD)
            for k in range(n):
                t = k / FPS
                frame = frame_at(img, motion, k / max(n - 1, 1))
                cap = ""
                if t < durations[i] - PAD:
                    for start, txt in timeline:
                        if t >= start:
                            cap = txt
                draw_caption(frame, cap, cap_font)
                ff.stdin.write(frame.tobytes())
            print(f"Szene {i + 1}/{len(scenes)} gerendert")
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit("ffmpeg ist fehlgeschlagen")

    print(f"Fertig: {out}  ({sum(durations):.1f} s)")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Aufruf: python3 tools/shorts/make_short.py <projektordner>")
    main(Path(sys.argv[1]).resolve())
