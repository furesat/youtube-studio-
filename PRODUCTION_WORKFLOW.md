# PRODUCTION_WORKFLOW — bir video konudan yayına

Her adımın çıktısı `videos/NNN/` içindedir. Durum `STATUS.json`'da tutulur. Her adımdan sonra commit atılır.

| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 1 | Klasörü aç: `videos/NNN/` (001'in yapısını kopyala) | Claude | boş dosyalar + `STATUS.json` |
| 2 | Konu + kaynak araştırması; efsane/gerçek ayrımı | Claude | `RESEARCH.md` |
| 3 | Senaryo (cümle kimlikli: L001…) | Claude → kullanıcı onayı | `SCRIPT.md` |
| 4 | Temiz anlatım metni (ses sağlayıcısına gidecek) | Claude | `NARRATION.txt` |
| 5 | Sahne planı: her sahne = 1 görsel birimi + türev çekimler | Claude | `SCENES.json` |
| 6 | Prompt + storyboard üretimi | `engine/tools/prompts.py` | `IMAGE_PROMPTS.md`, `STORYBOARD.md` |
| 7 | Görselleri üret ve kaydet | ChatGPT + kullanıcı | `images/001_S007_v1.png` … |
| 8 | Görsel eşleştirme ve durum | `engine/tools/status.py` | `STATUS.json` (eksikler listesi) |
| 9 | Seslendirme | ses sağlayıcısı (`voice/`) | `audio/` + `timing_tr.json` |
| 10 | Zamanlamayı gerçek sese göre güncelle + render | `engine/tools/assemble.py` | `renders/` (git dışı) |
| 11 | Başlık, açıklama, thumbnail | Claude + ChatGPT (thumbnail görseli) | `TITLE_THUMBNAIL.md` |
| 12 | Kalite kontrol → yayın | kullanıcı | `STATUS.json: published` |

## Zamanlama
- Sesten önce: `voice/providers/estimate.py` hece sayısından süre tahmin eder (TR 5,6 hece/sn). `SCENES.json` içinde `est_dur` alanı.
- Ses geldikten sonra: cümle süreleri gerçek ses dosyalarından okunur. Sahne süresi = bağlı cümlelerin süresi × ağırlık. `timing.source` alanı `"audio"` olur.
- Kelime düzeyi senkron (isteğe bağlı): ElevenLabs "with-timestamps" yanıtı veya Whisper ile hizalama.

## Dosya isimleri
- Görsel: `NNN_Sxxx_vK.png` (ör. `001_S014_v2.png`). Aynı sahnenin en yüksek `vK` sürümü kullanılır. Bir sahneyi zorla seçmek için `_final` ekle: `001_S014_final.png`.
- Ses: `audio/L001.mp3` (cümle başına) **veya** `audio/full_tr.mp3` + `audio/timing_tr.json`.

## Dil uyarlaması (DE / EN)
`SCRIPT.md` TR asıldır. Uyarlama: `SCRIPT_de.md`, `NARRATION_de.txt`; `SCENES.json` içinde `overlay.de`. Görseller ortak kalır (metinsiz oldukları için).
