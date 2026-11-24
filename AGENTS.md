# AGENTS.md — Her AI oturumu buradan başlar (Claude, ChatGPT, diğerleri)

Bu repo, yüz göstermeyen, çizimli, Türkçe bir bilim/tarih anlatım kanalının **ortak proje hafızasıdır**. Bir oturuma başladığında önce bu dosyayı, sonra aşağıdaki okuma sırasını izle. Kararlar dosyalarda yazılıdır; sohbet geçmişine güvenme.

## 1. Okuma sırası
1. `AGENTS.md` (bu dosya): kurallar, roller, mevcut durum
2. `CHANNEL_STRATEGY.md`: kanalın amacı, format, video uzunluğu, üretim ekonomisi
3. `PRODUCTION_WORKFLOW.md`: bir videonun adım adım üretimi
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

## 3. Roller
| Kim | Ne yapar |
|---|---|
| Claude | Konu araştırması (kaynaklı), senaryo, `SCENES.json`, promptların üretimi, görsel eşleştirme, zamanlama, render, `STATUS.json`, commit |
| ChatGPT | `IMAGE_GENERATION_GUIDE.md` + `videos/NNN/IMAGE_PROMPTS.md` okuyarak sahne görsellerini üretir; isimlendirme kuralına uyar |
| Kullanıcı | Konu/senaryo onayı, görselleri indirip doğru isimle kaydeder, seslendirmeyi onaylar, yayınlar |

## 4. Komutlar (repo kökünden)
```
python3 engine/tools/prompts.py videos/001       # SCENES.json → IMAGE_PROMPTS.md + STORYBOARD.md + tahmini süreler
python3 engine/tools/status.py  videos/001       # images/ ve audio/ tarar → STATUS.json günceller
python3 engine/tools/assemble.py videos/001 --lang tr --placeholders  # eksik görseller kart olur → animatik MP4
python3 engine/tools/assemble.py videos/001 --lang tr   # tüm görseller hazırsa final render (renders/, git dışı)
python3 engine/tools/voice_render.py videos/001 --lang tr  # voice_config.json'daki sağlayıcıyla ses + timing_tr.json
python3 engine/tools/build_scenes_001.py         # 001'in sahne planı kaynağı (SCENES.json'u yeniden üretir)
```
Sahne planını değiştirmek: ya `SCENES.json`'u doğrudan düzenle ya da `build_scenes_001.py`'yi düzenleyip çalıştır; sonra `prompts.py`.
Gerekenler: Python 3, Pillow, Playwright + Chrome (metin katmanı), FFmpeg.

## 5. Commit kuralı
Her önemli değişiklikten sonra commit at: araştırma, senaryo, sahne planı, yeni görsel seti, ses, render durumu. Mesaj Türkçe ve kısa olur. `STATUS.json` her commit'te güncel tutulur. Büyük dosyalar `.gitignore`'da: mp4, wav, render çıktıları.

## 6. Mevcut durum (son güncelleme: 2026-11-24)
- Referans analizi tamam → `reference-analysis/`
- Görsel kimlik ve Fasulye referansları tamam → `character-references/`
- 60 sn Göbeklitepe pilotu (ses yok, motorla çizildi) → `engine/examples/pilot_gobeklitepe/`
- **Video 001: "Kahve Neden Defalarca Yasaklandı?"**: araştırma, senaryo, sahne planı ve promptlar hazır; görseller bekleniyor → `videos/001/STATUS.json`
- Video 002: konu seçilmedi
