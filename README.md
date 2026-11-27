# youtube-studio — Fasulye kanalının üretim deposu

**Fasulye** · *Sıradan şeyler. Sıra dışı hikâyeler.* · Yüz göstermeyen, çizimli, Türkçe tarih/bilim anlatım kanalı (DE/EN uyarlamalı).
**Yeni bir AI oturumu `AGENTS.md`'den başlar.**

- [Fasulye Opportunity Engine](engine/tools/opportunity_engine/README.md) — YouTube araştırma paneli, GitHub Actions, Supabase rapor deposu ve asistan bağlantısı
- `shorts/` — bağımsız Shorts serileri (Fasulye Mahkemesi), rakip taraması

## Durum (2026-11-26)
- **Video 001 "Kahve Neden Defalarca Yasaklandı?"**: yayına hazır, YouTube'a yüklendi (TR ses + TR/DE altyazı + DE başlık/açıklama). Almanca dublaj izi hazır; kanalda "Ses" özelliği açılınca eklenecek.
- Kanal kimliği tamam: ad, slogan, açıklama, banner, avatar → `channel/`
- Sıradaki: 002 "Lale çılgınlığı gerçekten ekonomiyi çökertti mi?" → `ROADMAP.md`

## Belgeler
| Dosya | İçerik |
|---|---|
| `AGENTS.md` | Kurallar, roller, komutlar, mevcut durum (**başlangıç noktası**) |
| `CHANNEL_STRATEGY.md` | Kanal adı, vaat, içerik sütunları, format, konu seçimi |
| `ROADMAP.md` | Sıradaki videolar, kanal hedefleri, açık işler |
| `PRODUCTION_WORKFLOW.md` | Bir videonun konudan yayına tüm adımları (v2 süreci dahil) |
| `YOUTUBE_PUBLISHING.md` | YouTube Studio yükleme kontrol listesi, ayarlar, dublaj |
| `EDITING_KDENLIVE.md` | Düzenlenebilir Kdenlive projesi nasıl kurulur |
| `TEST_SITE.md` | FuresTube test sitesi (karşılaştırma ve önizleme) |
| `STYLE_GUIDE.md` · `CHARACTER_BIBLE.md` | Görsel kimlik ("Mürekkep & Kiremit") ve Fasulye |
| `NARRATION_GUIDE.md` | Senaryo dili, tempo, mizah |
| `IMAGE_GENERATION_GUIDE.md` | ChatGPT ImageGen protokolü ve dosya isimlendirme |

## Klasörler
| Klasör | İçerik |
|---|---|
| `channel/` | Kanal görselleri (banner, avatar), promptları ve üretim betiği |
| `reference-analysis/` | Referans kanal analizi (yalnızca metin ve özet; orijinal video yok) |
| `character-references/` | Fasulye dönüş sayfası, ifadeler, pozlar, kostümler |
| `engine/` | Çizim motoru, fontlar, araçlar (`engine/tools/`) |
| `voice/` + `voice_config.json` | Değiştirilebilir seslendirme katmanı (anahtar yalnızca ortam değişkeninde) |
| `videos/NNN/` | Her video: araştırma, senaryo, sahneler, promptlar, ses, YouTube paketi, durum |

Büyük dosyalar (MP4, WAV, görseller, renderlar) GitHub'a yüklenmez; kullanıcının Mac'inde `~/Downloads/youtube video/` altında durur. Ana sahne görsellerinin küçük referans kopyaları: `videos/NNN/images_ref/`.
