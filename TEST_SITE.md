# TEST_SITE — FuresTube

YouTube benzeri bağımsız önizleme/karşılaştırma sitesi. Kanal üretim dosyaları bu repoda; site yalnızca yayın katmanı.
- Repo: https://github.com/furesat/YouTubetest (main'e push → Netlify otomatik deploy)
- Canlı: https://youtubefur.netlify.app (Netlify projesi `youtubefur`; yeni site açılmaz)
- Kurallar: o reponun `AGENTS.md`'si — TEST ibaresi kalır, örnek istatistikler gerçek gibi sunulmaz, CC ilk açılışta kapalı, mevcut MP4/VTT silinmez/değiştirilmez, yeni video = ayrı MP4/VTT/poster yolları.

## Kartlar (2026-11-26)
| Kart | Dosyalar | Not |
|---|---|---|
| `kahve` | `kahve-001-tr.mp4`, `kahve-001-de.mp4` + VTT | v1 (müzikli, 61 sahne) |
| `kahve2` | `kahve-001-tr-v2.mp4`, `kahve-001-de-v2-dublaj.mp4` + VTT | v2 (142 çekim, müziksiz); DE = aynı görüntü + dublaj |
| `karadelik` | POSIES kara delik videosu | dokunulmaz |

## Yeni video ekleme
1. 720p kopya: `ffmpeg -vf scale=1280:720 -b:v 1150k -maxrate 1600k -movflags +faststart` (GitHub dosya sınırı 100 MB).
2. SRT → VTT (`,` → `.` ve `WEBVTT` başlığı).
3. `index.html`: `library` nesnesine giriş + ızgaraya `<article class="tile real" data-id="…">` kartı.
4. Yerelde Playwright ile: kart tıklama, video `readyState`, dil düğmesi, konsol hatası.
5. Push öncesi `git pull` (başka oturumlar da yazıyor); deploy'u Netlify MCP ile doğrula.
