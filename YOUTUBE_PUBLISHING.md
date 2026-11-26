# YOUTUBE_PUBLISHING — yükleme kontrol listesi

Kanal: **Fasulye**. Yükleme paketi her video için tek klasörde: `~/Downloads/youtube video/YouTube_yukleme_NNN/` (repoda: `videos/NNN/youtube/`).

## Paket içeriği
| Dosya | Ne için |
|---|---|
| `Kahve_001_TR_v2_muziksiz.mp4` | Video (1080p) — repoda yok, Mac'te |
| `Kahve_001_TR_kapak.jpg` | Küçük resim (1280×720) |
| `Kahve_001_TR_altyazi.srt` | Türkçe altyazı |
| `youtube_aciklama.txt` | Başlık, açıklama, bölümler, kaynaklar, etiketler |
| `Kahve_001_DE_dublaj.mp3` | Almanca ses izi (çok dilli ses) — Mac'te |
| `Kahve_001_DE_altyazi.srt` | Almanca altyazı (dublaj zamanlamasına göre) |
| `youtube_aciklama_DE.txt` | Almanca başlık + açıklama |

## 1. Ayrıntılar
- **Başlık:** soru biçimi, aranabilir (001: "Kahve Neden Defalarca Yasaklandı?"). A/B testi için ikinci başlık.
- **Açıklama:** 2–3 cümle kanca · bölüm zamanları (00:00'dan başlar, her bölüm ≥10 sn) · kaynak listesi · efsane notu · 2–3 hashtag.
- **Küçük resim:** "Dosya yükle". Özel kapak için hesabın telefonla doğrulanmış olması gerekir.
- **Oynatma listesi:** konu sütununa göre (001 → "Yasaklanan Şeyler").
- **Kitle:** Çocuklara özel değil.
- **Değiştirilmiş/yapay içerik:** gerçekçi görünen yapay içerik (gerçek kişi/yer/olay sanılabilecek) ve **başka birinin sesinin klonu** işaretlenir. Çizgi film görseller işaretlenmez. Anlatıcı sesi bir klonsa (bkz. `voice_config.json` → `voice_name`) **Evet** seçmek güvenli taraftır; işaretlemek erişimi ve para kazanmayı kısıtlamaz.
- **Etiketler:** yazım farkları (ör. "IV. Murad", "4. Murad"), konu, kanal adı. Etkisi küçük.
- **Dil:** Türkçe · **Altyazı sertifikası:** Yok · **Kategori:** Eğitim.
- **Shorts remiksi:** Video ve ses remiksine izin ver. **Yorumlar:** Açık, Temel denetim.

## 2. Video öğeleri
- **Altyazılar:** önce video dili seçilmeli (yoksa "Ekle" gri). Dosya yükle → Zamanlama ile → SRT.
- **Bitiş ekranı / kartlar:** kanalda 2+ video olunca (önceki videoya ve abone ol).

## 3. Kontroller → 4. Görünürlük
Önce **Liste dışı**; telefonda baştan sona izle (altyazı, kapak, bölümler). Sorun yoksa **Herkese açık**.

## Çok dilli ses (dublaj)
- **Altyazı ve ses → Dil ekle → Almanca**: satırda Başlık ve açıklama, Altyazılar, **Ses** sütunları olmalı.
- "Ses" sütunu yoksa özellik kanalda açık değildir: **Ayarlar → Kanal → Özellik uygunluğu → Gelişmiş özellikler** (telefon/kimlik doğrulama) → birkaç gün sonra tekrar bak.
- 001 durumu (2026-11-26): DE altyazı + DE başlık/açıklama yayında; **Ses sütunu yok**, bekleniyor. Açılmazsa ayrı DE video seçeneği.

## Kanal ayarları
- **Ad:** Fasulye · **Avatar:** `channel/kanal_avatar_800.jpg` · **Banner:** `channel/kanal_banner_2560x1440.jpg` (güvenli alan ortadaki 1546×423).
- **Açıklama:**
```
FASULYE
Sıradan şeyler. Sıra dışı hikâyeler.
Dikkat: Gaz yapabilir.

Kahve neden defalarca yasaklandı? Takvimden 11 gün nasıl silindi? Orta Çağ'da insanlar gerçekten yıkanmıyor muydu?

Fasulye, her gün gördüğün şeylerin arkasındaki şaşırtıcı tarihi anlatır: çizimli, kısa ve kaynaklı. Efsaneyle gerçeği ayırırız; kaynaklar her videonun açıklamasında.
```
- **İkamet ülkesi:** kullanıcının gerçekten yaşadığı ülke (Avusturya). YPP uygunluğu ve AdSense/vergi buna bağlı; keşfedilmeyi etkilemez.
- **Haklar:** ElevenLabs ses/efekt/müziğin ticari kullanımı abonelik planına bağlı; para kazanmadan önce kontrol et.
