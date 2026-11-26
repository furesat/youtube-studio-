# AGENTS.md — Her AI oturumu buradan başlar (Claude, ChatGPT, diğerleri)

Bu repo, yüz göstermeyen, çizimli, Türkçe bir bilim/tarih anlatım kanalının (**Fasulye**) **ortak proje hafızasıdır**. Bir oturuma başladığında önce bu dosyayı, sonra aşağıdaki okuma sırasını izle. Kararlar dosyalarda yazılıdır; sohbet geçmişine güvenme.

## 1. Okuma sırası
1. `AGENTS.md` (bu dosya): kurallar, roller, mevcut durum
2. `CHANNEL_STRATEGY.md` + `ROADMAP.md`: kanalın amacı, içerik sütunları, sıradaki videolar
3. `PRODUCTION_WORKFLOW.md`: bir videonun adım adım üretimi (v2: ara çekimler, müziksiz miks, dublaj, kapak)
   `YOUTUBE_PUBLISHING.md` (yükleme), `EDITING_KDENLIVE.md` (düzenlenebilir proje), `TEST_SITE.md` (FuresTube)
4. `STYLE_GUIDE.md` + `CHARACTER_BIBLE.md`: görsel kimlik (Yön A "Mürekkep & Kiremit") ve Fasulye
5. `NARRATION_GUIDE.md`: senaryo ve anlatım dili
6. `IMAGE_GENERATION_GUIDE.md`: ChatGPT ImageGen protokolü (görsel üreten oturum için zorunlu)
7. Çalışılan videonun klasörü: `videos/NNN/STATUS.json` → orada `next_actions` alanı

## 2. Değişmez kararlar
- **Ana dil Türkçe.** Almanca (de) ve İngilizce (en) uyarlamaları için metin katmanları ayrı tutulur.
- **Görsel kimlik:** Yön A "Mürekkep & Kiremit". Ana karakter **Fasulye**. Kırmızı vurgu rengi `#B83A2B`.
- **Ana sahne çizimleri:** ChatGPT ImageGen ile **manuel** üretilir. Kullanıcı görselleri `videos/NNN/images/` klasörüne kaydeder.
- **Kullanılmayacaklar:** Higgsfield, ANDROMEDA. Kullanıcı onayı olmadan yeni ücretli abonelik veya API yok.
- **Görsellerde metin yok.** Bütün yazılar `engine/` tarafından ayrı katmanda eklenir.
- **Ses sağlayıcısı değiştirilebilir** (`voice/`, `voice_config.json`). Varsayılan: `estimate` (geçici zamanlama). Hedef: ElevenLabs veya benzeri profesyonel ses.
- **Referans kanal** (Ink Explainer) yalnızca teknik/anlatı analizi içindir. Karakterleri, çizimleri, senaryoları ve markası kopyalanmaz. Orijinal MP4 ve kareleri repoya **yüklenmez**.
- **Yeni büyük yazılım sistemi kurulmaz.** Öncelik yayınlanabilir videolar. Araçlar küçük kalır (`engine/tools/`).
- **Kanal adı: Fasulye.** Slogan: "Sıradan şeyler. Sıra dışı hikâyeler."
- **Kurgu kuralları (001'den):** görüntü 2–3 sn'de bir değişir (ana sahne + elle yazılmış ara çekimler); yalnızca yavaş, sürekli yakınlaşma; anlatıma kurgu müdahalesi yok (ham ses); varsayılan miks **müziksiz** (anlatım + seyrek efekt).
- **Promptlar** ilk 56 promptla aynı biçimde (stil + karakter blokları + elle yazılmış sahne içeriği). ChatGPT'ye 30'arlı partiler.
- **Yasak:** referans kanalın MP4'ü, API anahtarları, gereksiz büyük dosyalar repoya yüklenmez. ElevenLabs anahtarı yalnızca ortam değişkeninde. Mevcut dosyalar silinmez.

## 3. Roller
| Kim | Ne yapar |
|---|---|
| Claude | Konu araştırması (kaynaklı), senaryo, `SCENES.json`, promptların üretimi, görsel eşleştirme, zamanlama, render, `STATUS.json`, commit |
| ChatGPT | `IMAGE_GENERATION_GUIDE.md` + `videos/NNN/IMAGE_PROMPTS.md` okuyarak sahne görsellerini üretir; isimlendirme kuralına uyar |
| Kullanıcı | Konu/senaryo onayı, görselleri indirip doğru isimle kaydeder, seslendirmeyi onaylar, yayınlar |

## 4. Komutlar (repo kökünden)
Tam liste ve sıra: `PRODUCTION_WORKFLOW.md` → "Komutlar". Kısaca:
```
python3 engine/tools/prompts.py videos/001        # SCENES.json → IMAGE_PROMPTS.md + STORYBOARD.md
python3 engine/tools/shots_v2_001.py              # ara çekim planı → SHOTS_v2.json + IMAGE_PROMPTS_v2.md
python3 engine/tools/status.py  videos/001        # images/ ve audio/ tarar → STATUS.json
python3 engine/tools/build_audio.py videos/001 --lang tr
python3 engine/tools/mix_audio.py videos/001 --lang tr --no-music
python3 engine/tools/assemble.py videos/001 --lang tr      # ana sahne kareleri + SRT
python3 engine/tools/render_v2.py videos/001 --audio audio/mix_tr_muziksiz.wav --out renders/tr/X.mp4
python3 engine/tools/fit_dub.py videos/001 --lang de       # DE dublaj izini TR zamanlamasına oturt
python3 engine/tools/thumbnail.py videos/001 "YASAK!"      # kapak yazısı
python3 channel/make_channel_art.py                        # (channel/ içinden) banner + avatar
```
Gerekenler: Python 3, Pillow, NumPy, Playwright + Chrome (metin katmanı), FFmpeg.

## 5. Commit kuralı
Her önemli değişiklikten sonra commit at: araştırma, senaryo, sahne planı, yeni görsel seti, ses, render durumu. Mesaj Türkçe ve kısa olur. `STATUS.json` her commit'te güncel tutulur. Büyük dosyalar `.gitignore`'da: mp4, wav, render çıktıları.

## 6. Mevcut durum (son güncelleme: 2026-11-26)
- Kanal kimliği tamam: ad **Fasulye**, açıklama, banner, avatar → `channel/`, `YOUTUBE_PUBLISHING.md`
- **Video 001 "Kahve Neden Defalarca Yasaklandı?"**: v2 kurgu (142 çekim, ort. 2,8 sn, müziksiz) 1080p render edildi; YouTube'a yüklendi (TR altyazı, DE altyazı + DE başlık/açıklama). DE dublaj izi hazır, kanalda "Ses" özelliği açılınca yüklenecek → `videos/001/STATUS.json`
- FuresTube test sitesinde v1 ve v2 yan yana (v2'de DE dublaj seçeneği) → `TEST_SITE.md`
- Düzenlenebilir Kdenlive projesi (v1) → `EDITING_KDENLIVE.md`
- Sıradaki: **002 Lale çılgınlığı** araştırması → `ROADMAP.md`
- Göbeklitepe pilotu (60 sn, ses yok) → `engine/examples/pilot_gobeklitepe/`
