# Almanca kanal (paralel yayın) — 27.11.2026

Karar: Türkçe kanalla paralel, ayrı Almanca kanal. Görseller metinsiz olduğu için her video = Almanca ses + Almanca ekran etiketleri + Almanca kapak/başlık/açıklama.

## İsim adayları (YouTube'da 27.11.2026'da boş görünen handle'lar)
| Kanal adı | Handle | Not |
|---|---|---|
| **Bohne erzählt** | @BohneErzaehlt | Öneri. Karakter = Bohne, kanal = anlatıcı. |
| Bohne erklärt | @BohneErklaert | "erklärt" eğitim kanalı tınısı |
| Bohnenwissen | @Bohnenwissen | kısa, ama kişiliksiz |
| Die kluge Bohne | @DieKluegeBohne | sevimli, biraz çocuk kanalı gibi |
| Bohne weiß mehr | @BohneWeissMehr | esprili |

Kaçınılacak: "Herr Bohne" (@HerrBohne, @DerHerrBohne dolu; arama Dr. Michael Bohne'ye gidiyor), "Die Bohne" (@DieBohne dolu).
404 dönmesi handle'ın kesin alınabilir olduğunu göstermez; kanal açarken YouTube kontrol eder.

## Marka çevirisi
- Slogan: *Gewöhnliche Dinge. Ungewöhnliche Geschichten.*
- Şaka: *Achtung: Kann Blähungen verursachen.*
- Renk, font, karakter aynı (CHARACTER_BIBLE.md).

## Video başına Almanca paket
1. Almanca metin (NARRATION_de.txt) → ElevenLabs ses → `fit_dub.py` ile TR zaman çizelgesine oturt.
2. `render_v2.py <video> --lang de --audio audio/dublaj_de_muziksiz.wav --out renders/de/...` (ekran etiketleri Almanca).
3. `thumbnail.py <video> "<METİN>" de` → Almanca kapak.
4. Almanca SRT + başlık/açıklama.

## Durum
| İçerik | Almanca durum |
|---|---|
| 001 Kahve (uzun) | **Hazır**: Mac `YouTube_DE_001/` (1080p video, kapak VERBOTEN!, SRT, açıklama) |
| Short: Prusya | Almanca ses yok (dublajdan kesilebilir) |
| FM01 Tokalaşma | Almanca ses yok (yeni üretim gerekir) |
