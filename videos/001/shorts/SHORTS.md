# Video 001 – YouTube Shorts

Ana video: https://youtu.be/s7LHi37TYEk · Araç: `engine/tools/make_short.py` (1080x1920, üstte başlık, ortada 900 px görsel bandı, altta gömülü altyazı, 1,6 sn kapanış kartı "Tam hikâye kanalda").

## 1) Prusya – "Kahveyi koklayarak yakalayan polis" (46 sn) — HAZIR, yüklendi/yüklenecek
- Kaynak: S043 → S048 (Friedrich'in kahve yasağı, kahve koklayıcılar)
- Komut: `python3 engine/tools/make_short.py videos/001 --start-shot S043 --end-scene S048 --title "Kahveyi koklayarak|yakalayan polis" --out renders/shorts/001_short_prusya.mp4`
- Seçilen sürüm: yukarıdaki (yakınlaşma %6, kayma yok). Denenen alternatif: `--zoom 0.08 --pan 0.04 --snap-cuts` + başlık "1777: Kral kahveye|koku polisi saldı" → kullanıcı ilk sürümü tercih etti.
- Dosyalar: `001_short_prusya_kapak.jpg` (kapak), `001_short_prusya.srt` (TR), `001_short_prusya_DE.srt` (DE; zamanlama TR ses ile aynı). mp4 (46 MB) git'te yok (.gitignore).
- YouTube başlığı: `Kahveyi koklayarak yakalayan polis ☕👃 #kahve #osmanlı #tarih`
- Almanca başlık: `Friedrichs Kaffeeschnüffler ☕👃 #Kaffee #Geschichte #Preußen`
- Almanca açıklama:
  Friedrich der Große hatte ein Problem: Sein Volk liebte Kaffee, und das Geld floss ins Ausland. Seine Lösung? Eine Spezialtruppe aus rund 400 Kriegsveteranen, die durch die Straßen zog und heimlich gerösteten Kaffee erschnüffelte. ☕👃
  Das ganze Video: https://youtu.be/s7LHi37TYEk
  FASULYE – Gewöhnliche Dinge. Außergewöhnliche Geschichten. Achtung: Kann Blähungen verursachen.
- Altyazı yükleme: Short → Altyazılar → dil ekle (Türkçe / Deutsch) → Dosya yükle → Zamanlama ile. Not: videoda gömülü altyazı var, YouTube altyazısı varsayılan kapalı tutulabilir.
- "Değiştirilmiş içerik": anlatıcı klon ses → Evet.

## Sırada (henüz üretilmedi)
İsveç · IV. Murad · Londra · Mekke (aynı araçla `--start-shot/--end-scene`).

## Fikirler (uygulanmadı)
- Sesli giriş (ElevenLabs, klon ses): "1777'de sokaklarda kahve kokusu avlayan özel bir polis birliği kuruldu. Sebebi ne mi? Para." (+~4 sn)
- 1,5 sn sesli kapanış çağrısı; Studio'da Short'u ana videoya "İlgili video" ile bağlama.
- `make_short.py` bayrakları: `--zoom`, `--pan`, `--snap-cuts`.
