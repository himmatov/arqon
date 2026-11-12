# Menga Consulting — "Sardorning Koreya sarguzashti" (60 soniya)

Video: `menga-consulting-koreya.mp4` (1080x1920, 9:16, 30 fps, ovozsiz).
Ovoz yozishda quyidagi vaqtlarga moslang. Qavs ichidagilar — ekranda nima bo'layotgani.

| Vaqt | Kim | Matn (ekranda ham yozilgan) |
|---|---|---|
| 0:00–0:04 | Diktor | Menga Consulting taqdim etadi: Sardorning Koreya sarguzashti! *(logo, Toshkent → Seul samolyoti)* |
| 0:04–0:06 | Diktor | Hammasi bitta K-dramadan boshlandi... *(Sardor telefonda serial ko'rib, ko'zlari yurakcha)* |
| 0:06–0:08 | Sardor | QAROR QILDIM! Men Koreyaga ketaman! *(karavotda sakraydi)* |
| 0:08–0:11 | Ona | Koreya qochmaydi! Avval idishlarni yuv! *(qo'lida shippak)* |
| 0:11–0:15 | Diktor | Birinchi muammo: hujjatlar. *(osmondan qog'ozlar yog'iladi, "Asab" 100% → 2%)* |
| 0:15–0:19 | Sardor | Spravkaning spravkasi ham kerakmi?! *(qog'oz tagida qoladi)* |
| 0:19–0:22 | Diktor / Sardor | Ikkinchi muammo: koreys tili. — Annyong... xase... OSH?! |
| 0:22–0:24 | Sardor | Kamsahamnida, mushukjon! |
| 0:24–0:26 | Mushuk / Diktor | Miyov?! — TOPIK: 0 ball. Ishtiyoq: 100 ball! |
| 0:26–0:28 | Diktor / 1-xola | Uchinchi muammo: qo'shnilar. — Koreyada sovuq! Paxtali chopon ol! |
| 0:28–0:29.5 | 2-xola | U yoqda osh yo'q! Qozon ol! |
| 0:29.5–0:32 | 1-xola | Qaytishda kelin bilan kel! *(Sardor terlaydi, "???" )* |
| 0:32–0:35 | Diktor / Konsultant | TA-DAAAM! — Muammo bormi? MENGA CONSULTING bor! |
| 0:35–0:38.5 | Konsultant | Universitet, hujjatlar, viza, grant — hammasini hal qilamiz! *(ro'yxatda belgilar paydo bo'ladi)* |
| 0:38.5–0:41 | Sardor | Voy! Shunaqasi ham bormidi?! |
| 0:41–0:44 | Diktor / Ona | Aeroport. — Yana non sol, bolam! U yoqda non yo'q! *(tarozida 47 kg, ruxsat 23 kg)* |
| 0:44–0:47 | Sardor | Oyi, Koreyaga ketyapman, Marsga emas! |
| 0:47–0:50 | Diktor | Menga Consulting bilan — vaqtida va muammosiz! *(Toshkent → Seul parvozi)* |
| 0:50–0:51.5 | Koreys do'st | Annyeonghaseyo! |
| 0:51.5–0:53 | Sardor | Annyeonghaseyo! Men Sardor, O'zbekistondan! |
| 0:53–0:55.5 | Diktor / Sardor | Bir yildan so'ng: TOPIK, grant, kimchi — hammasi bor! — ...lekin oyimning oshi qani? |
| 0:55.5–1:00 | Diktor | Menga Consulting: Koreyaga yo'lingiz biz bilan oson! Bepul konsultatsiya! |

## O'zgartirish
- Telefon/Instagram qo'shish: `animation.html` faylining boshidagi `CONTACT` qatoriga yozing, so'ng qayta render qiling:
  `node render.js menga-consulting-koreya.mp4 30` (Playwright + ffmpeg kerak).
- Brauzerda ko'rish: `animation.html` ni oching (bosilsa boshidan boshlanadi).

## Ovozli versiya
- `menga-consulting-koreya-ovozli.mp4` — video + fon musiqasi + multfilm ovoz effektlari (gapirish ovozi yo'q).
- `audio-sfx-music.wav` — faqat musiqa va effektlar, montaj dasturida alohida trek sifatida ishlatish uchun.
- Qayta yaratish: `python3 make_audio.py`, so'ng
  `ffmpeg -i menga-consulting-koreya.mp4 -i audio-sfx-music.wav -c:v copy -c:a aac -shortest menga-consulting-koreya-ovozli.mp4`

## To'liq versiya (diktor ovozi bilan)
- `menga-consulting-koreya-TOLIQ.mp4` — video + o'zbekcha ovozlar + musiqa + effektlar.
- Ovozlar: Microsoft neural TTS (edge-tts). Diktor/Sardor/konsultant — `uz-UZ-SardorNeural`, ona/xolalar — `uz-UZ-MadinaNeural`
  (har biriga boshqa balandlik/tezlik), koreys do'st — `ko-KR-SunHiNeural`.
- Har bir gap alohida: `voice_lines/*.mp3`. Matn va vaqtlar `make_voice.py` ichidagi `LINES` ro'yxatida.
- Qayta yaratish: `python3 make_voice.py && python3 make_audio.py`, so'ng `audio-full.wav` ni videoga qo'shing.
