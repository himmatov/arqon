"""Generates the Uzbek voice-over (Microsoft neural voices via edge-tts) synced to animation.html.
Output: voice.wav (60 s, 44.1 kHz mono) + voice_lines/*.mp3
Run: python3 make_voice.py   (needs `pip install edge-tts`, ffmpeg, internet)
"""
import asyncio, os, subprocess, wave
import numpy as np
import edge_tts

SR = 44100
PROXY = os.environ.get("HTTPS_PROXY")

VOICES = {
    "diktor":     ("uz-UZ-SardorNeural", "+5%",  "-6Hz"),
    "sardor":     ("uz-UZ-SardorNeural", "+12%", "+18Hz"),
    "ona":        ("uz-UZ-MadinaNeural", "+8%",  "-8Hz"),
    "xola1":      ("uz-UZ-MadinaNeural", "+12%", "+6Hz"),
    "xola2":      ("uz-UZ-MadinaNeural", "+5%",  "-18Hz"),
    "konsultant": ("uz-UZ-SardorNeural", "+8%",  "-14Hz"),
    "dost":       ("ko-KR-SunHiNeural",  "+0%",  "+10Hz"),
}

# (start_sec, end_limit_sec, character, text)
LINES = [
    (0.4, 3.7, "diktor", "Menga Konsalting taqdim etadi: Sardorning Koreya sarguzashti!"),
    (4.2, 5.95, "diktor", "Hammasi bitta K-dramadan boshlandi..."),
    (6.0, 8.2, "sardor", "Qaror qildim! Men Koreyaga ketaman!"),
    (8.4, 11.0, "ona", "Koreya qochmaydi! Avval idishlarni yuv!"),
    (11.3, 14.8, "diktor", "Birinchi muammo: hujjatlar! Apostil, notarius..."),
    (15.0, 18.6, "sardor", "Spravkaning spravkasi ham kerakmi?!"),
    (19.2, 20.7, "diktor", "Ikkinchi muammo: koreys tili."),
    (20.8, 22.8, "sardor", "Annyon... xase... osh?!"),
    (22.9, 24.15, "sardor", "Kamsahamnida, mushukjon!"),
    (24.6, 25.8, "diktor", "TOPIK nol, ishtiyoq yuz!"),
    (26.2, 28.25, "xola1", "Koreyada sovuq! Paxtali chopon ol!"),
    (28.3, 30.15, "xola2", "U yoqda osh yoʻq! Qozon ol!"),
    (30.2, 31.75, "xola1", "Qaytishda kelin bilan kel!"),
    (32.15, 33.2, "diktor", "Ta-daaam!"),
    (33.2, 35.5, "konsultant", "Muammo bormi? Menga Konsalting bor!"),
    (35.55, 38.95, "konsultant", "Universitet, hujjatlar, viza, grant — hammasini hal qilamiz!"),
    (39.0, 41.0, "sardor", "Voy! Shunaqasi ham bormidi?!"),
    (41.15, 41.85, "diktor", "Aeroport."),
    (41.7, 44.15, "ona", "Yana non sol, bolam! U yoqda non yoʻq!"),
    (44.2, 46.6, "sardor", "Oyi, Koreyaga ketyapman, Marsga emas!"),
    (47.2, 49.7, "diktor", "Menga Konsalting bilan — vaqtida va muammosiz!"),
    (50.4, 51.2, "dost", "안녕하세요!"),
    (51.2, 53.65, "sardor", "Annyonhaseyo! Men Sardor, Oʻzbekistondan!"),
    (53.7, 55.3, "sardor", "...lekin oyimning oshi qani?"),
    (55.6, 59.9, "diktor", "Menga Konsalting: Koreyaga yoʻlingiz biz bilan oson! Bepul konsultatsiya!"),
]


def load_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768


def to_wav(src, dst, tempo=1.0):
    af = ["silenceremove=start_periods=1:start_threshold=-45dB", "areverse",
          "silenceremove=start_periods=1:start_threshold=-45dB", "areverse"]
    if tempo > 1.0:
        af.append(f"atempo={tempo:.3f}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", ",".join(af),
                    "-ar", str(SR), "-ac", "1", dst], check=True)


async def synth(i, who, text):
    voice, rate, pitch = VOICES[who]
    path = f"voice_lines/{i:02d}_{who}.mp3"
    await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=PROXY).save(path)
    return path


async def main():
    os.makedirs("voice_lines", exist_ok=True)
    paths = await asyncio.gather(*(synth(i, w, t) for i, (_, _, w, t) in enumerate(LINES)))
    track = np.zeros(int(SR * 60))
    for (start, limit, who, text), mp3 in zip(LINES, paths):
        wav = mp3[:-4] + ".wav"
        to_wav(mp3, wav)
        x = load_wav(wav)
        slot = limit - start
        if len(x) / SR > slot:  # too long for its slot: speed it up a little
            tempo = min(1.3, len(x) / SR / slot)
            to_wav(mp3, wav, tempo)
            x = load_wav(wav)
        x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
        i0 = int(start * SR)
        x = x[: len(track) - i0]
        track[i0:i0 + len(x)] += x
        print(f"{start:5.2f}s  {len(x)/SR:4.2f}s / {slot:4.2f}s  {who:10s} {text}")
        os.remove(wav)
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    with wave.open("voice.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


asyncio.run(main())
