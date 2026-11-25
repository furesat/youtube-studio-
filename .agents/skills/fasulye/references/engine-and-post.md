# Motor, ses, altyazı ve montaj

## Sahne planı ve araçlar

Çalışılan bölüm yolunu `videos/NNN` yerine koy, komutları kaynak repo kökünden çalıştır. Mevcut bölümde deneme yaparken ayrı kopya kullan. Aşağıdaki araçlar bölüm dosyalarına yazabilir.

- `videos/001/SCENES.json` çalışan veri örneği. Üst düzeyde `video`, `title` (dil anahtarları), `lang_primary`, `resolution`, `fps`, `target_shot_sec`, `cast`, `fasulye_costumes`, `scenes` ve isteğe bağlı `thumbnail`. 001 örneğinde 1920×1080, 30 fps, hedef çekim 2,2 sn. Güncel montaj kodunda tuval 1920×1080 sabit ve FPS bölümden okunur.
- `S001` gibi sahne kimliği, `lines: ["L001"]`, sahne türü, dil anahtarlı `overlay`, `effects` ve `focus: [x, y]` (0–1) kullan. `imagegen` ana görsel bekler. `derived` tipi `source: "Sxxx"` ile eldeki ana görseli çağırır. `engine_card` motorda çizilir. Uygulanan efekt örnekleri `punch_in`, `red_x`, `stamp`, `check_cross` ve `map_pins`. Damga metni `overlay.stamp.tr` gibi dil anahtarı taşır.
- `python3 engine/tools/prompts.py videos/NNN --lang tr` istem ve storyboard'u yeniden yazar, sahne süre alanlarını ve kaynağı günceller. 001'e özel `build_scenes_001.py` yalnız o bölümün planını yeniden kurar. 001 planını düzenlerken doğrudan düzenleme veya üretici dosyayı güncelleme yolundan hangisinin kullanıldığını kaydet.
- `python3 engine/tools/status.py videos/NNN` yerel görüntüleri tarar ve durum dosyasını günceller. Tarama `_final` > en yüksek `vK` > sürümsüz sırasını izler. Durum aracı yazdığı zamanlama veya ses dosyası sayısını gerçek oynatma kontrolüyle tamamla.
- Repo stratejisinde uzun bölüm için yaklaşık 40–55 ana sahne, geri kalan ritim için türev çekimler ve kartlar başlangıç planıdır. Sert kesme ve durum değişimi temel kurgu dilidir. Güncel montajda ana sahne başına en fazla iki yakınlaşma (geniş, 1,14×, 1,28×) var. Uzun planın neden sürdüğünü içerikle değerlendir.
- Kodla çizim gereken görevlerde `engine/fasulye.py` içindeki `Fasulye.g(...)` poz, ifade, kostüm ve `front | tq | side | back` görünümünü parametreyle seçer. `engine/library.py` nesne ve mekân, `engine/palettes.py` palet A, `engine/examples/pilot_gobeklitepe/` kodla üretilen pilot örneğidir. Bu akışta Playwright + Chrome kullanılan adımlar vardır. Ana bölümün `assemble.py` yolu Pillow + FFmpeg kullanır.

## Ses ve gerçek zamanlama

- Ses öncesi tahmin 5,6 hece/sn (TR). `common.py`, `audio/timing_<lang>_final.json` varsa önce onu, sonra `audio/timing_<lang>.json` dosyasını, ikisi de yoksa hece tahminini kullanır. Kod, zamanlama JSON'u gördüğünde kaynağa `audio` yazabilir. Ses kaydı, tam satır kapsaması, pozitif süreler ve senkronu ayrıca doğrula.
- Sağlayıcıyı güncel `voice_config.json` ve `voice/` üzerinden kontrol et. İncelenen ayarda TR için ElevenLabs, DE/EN için `estimate` seçili. Kullanılamayan sağlayıcı tahmine düşebilir. `voice_render.py` satır bazlı sesi ve zamanlamayı işler. `estimate` nihai ses sağlamaz ve bu girişte gerçek zamanlama dosyası yazılmaz. ElevenLabs API anahtarı ortamdan okunur. Mevcut ayardan kredi, sağlayıcı erişimi veya başarılı üretim sonucu çıkarma.
- 001'in ses örneği **Yasli Adam 3** ve A/B/C parçaları. Ses yönetimindeki oyunculuk yönü bilge, sıcak ve kuru esprili bir hikâyeci. Espriyi sakin, ciddi bölümleri ölçülü oku. `VOICE_QA_tr.md` saniyeli etiketlerin güvenilmezliğini, fazla duraklamanın ritmi bozduğunu ve fısıltının gövdeden yaklaşık 10 dB düşük ölçüldüğünü gösteriyor. Duygu değişince etiketle, `[pause]` ve `[long pause]` seyrek kullan. Kesin boşluğu kurguda ölç. Kritik telaffuzları dinle. IPA bir deneme aracıdır, doğru okunduğu kulakla doğrulanır. 001 testinin ölçülerini başka model veya bölüm için garanti olarak kullanma.
- 001 tipi eldeki parça kaydında `audio/<lang>/part_A.mp3` vb., `align_audio.py` ve ilgili `--parts` satır aralıkları kullanılır. Yerel `WHISPER_DIR` (sonunda `/`), sherpa-onnx, NumPy ve FFmpeg'i kontrol et. `build_audio.py`, hizalama ve `PAUSES_<lang>.json` dosyasındaki `default` / `after` ile `audio/full_<lang>.mp3` ve final zamanlamayı üretir. Bu araç `inside` duraklarını işlemez. Aralıklar, yeniden alınan kayıtlar ve seçilen zamanlama aynı çekime ait olmalı. Ham kayıtların üzerine yazmadan önce girdileri ve amaçlanan çıktıyı kontrol et.

## MP4, SRT ve editör teslimi

```bash
python3 engine/tools/assemble.py videos/NNN --lang tr --placeholders
python3 engine/tools/assemble.py videos/NNN --lang tr
```

İlk komut inceleme için eksik kareleri geçici kart yapar. İkinci komut eksik ana görselde durur, ses eksikse sessiz MP4 üretebilir. Kaynak ses olarak `audio/full_<lang>.{wav,mp3,m4a}` veya `audio/<lang>/L*.*` arar. A/B/C kayıtları kullanılıyorsa önce tam ses hazırlanır. `--only S001-S016` kısa inceleme içindir. Bu seçenek görsel aralığı filtreler ama ses girişini o aralığa kırpmaz. Tam oynatım testi ayrı yapılır.

Çıktı yolu `videos/NNN/renders/<lang>/`: `NNN_<lang>.mp4`, `NNN_<lang>.srt`, `render_report.json`. SRT'nin metni ilgili `SCRIPT*.md` içindeki **L** satırlarından, zamanları sahne sırasındaki satır sürelerinden gelir. Yazım, okunabilir satır bölümü, artan ve geçerli aralıklar, eksik/çift/boş satır ve A/V senkronu kontrol edilir. TTS etiketleri, IPA ve sahne notlarını SRT'ye alma. Motor satır metnini olduğu gibi alır, bu yüzden satır içindeki sahne notlarını ayrıca ayıkla. Nihai SRT ve YouTube bölüm zamanları onaylı montajı izler. Raporun `audio`, `placeholders` ve `timing_source` alanlarını oynatma ile doğrula.

Editör dosyası istenirse `timeline_map.py`, `export_fcpxml.py` ve `export_otio.py` mevcut. Zaman haritası ham parça zamanlarıyla `PAUSES` kullanır. Birleşik sesle aynı sonucu varsaymadan süreleri karşılaştır. Dışa aktarıcılara gerçek ses/görsel yollarını ver. Editörde açıp medya bağlantıları ve senkron kontrol edilebildiyse bunu teslimde belirt.
