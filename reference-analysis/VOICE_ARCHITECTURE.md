# VOICE_ARCHITECTURE — Değiştirilebilir seslendirme katmanı

Hedef: ses sağlayıcısı henüz seçilmeden görsel üretim ilerleyebilsin; sağlayıcı sonradan tek bir config satırıyla değiştirilebilsin.

## Sözleşme (`voice/base.py`)
- `Line(id, text, lang, style, pause_after)`: senaryonun tek cümlesi. `id`, sahne planındaki cümle anahtarıdır.
- `LineResult(id, audio_path, duration, words[], timing_source, provider)`: süre zorunlu. Kelime zamanları varsa doldurulur, yoksa hizalama adımı sonradan ekler.
- `VoiceProvider.synthesize(line, out_dir, voice_cfg) -> LineResult`

Görsel hat (Remotion sahne zamanlayıcısı) **yalnızca `timing.json`'u okur**; hangi sağlayıcının ürettiğini bilmez.

## Sağlayıcılar (`voice/providers/`)
| Ad | Durum | Ne zaman |
|---|---|---|
| `estimate` | **Çalışıyor, test edildi.** Ses üretmez (isteğe bağlı sessiz wav); hece sayısından süre ve kelime zamanı tahmin eder | Şimdi: storyboard ve animatik |
| `external` | Çalışıyor (wav süresi okunur; mp3 için ffprobe) | İnsan kaydı veya başka bir araçla üretilmiş dosyalar |
| `chatterbox` | İskelet, test edilmedi | TR/DE/EN aday (MIT) |
| `piper` | İskelet | Yalnızca ticari lisanslı sesler (tr dfki = NC, kullanma) |
| `kokoro` | İskelet | Yalnızca EN (TR ve DE yok) |

Yedek mekanizma: istenen sağlayıcı kurulu değilse veya dili desteklemiyorsa `get_provider()` uyarı verir ve `estimate`e düşer. **Üretim durmaz.** (Test edildi: chatterbox→estimate, kokoro+tr→estimate, bilinmeyen→estimate.)

## Kullanım
```
python3 -m voice ornek_senaryo_tr.json voice_config.json cikti/
# -> cikti/timing.json  (+ cikti/audio/L001.wav sessiz)
```
Örnek çıktı (TR, 3 cümle): 10,6 sn; DE aynı içerik: 11,0 sn.

## Tahmin varsayımları (ölçülmedi, kalibre edilecek)
TR 5,6 hece/sn · DE 5,0 · EN 4,6. Türkçede hece = ünlü sayısı. DE/EN'de ünlü grupları sayılıyor. Rakamlar uzun okunduğu için ek pay var. Stil katsayısı: vurgu ×0,92, sıcak ×0,90, şaka ×1,05. Gerçek ses gelince: `timing.json` süreleri ile ses süreleri karşılaştırılıp `rate_sps` güncellenecek.

## Sonraki adım (ses testi aşaması)
1. Bir sağlayıcının `synthesize()` gövdesini doldurmak.
2. Kelime zamanlarını Whisper + lisansı uygun bir hizalayıcıyla `words[]`'e eklemek (MMS_FA CC-BY-NC, ticari kullanma).
3. `voice_config.json` içinde dil başına `provider` alanını değiştirmek. Dil başına ayrı sağlayıcı mümkün (ör. EN=kokoro, TR=chatterbox).
