# Depo kaynakları ve paketteki görseller

Kaynak depo `furesat/youtube-studio-`. İlk paket için incelenen temel commit `d3da61579a2bfedba7d511b89c98895af24f1630`. Bir bölümü sürdürürken açık çalışma kopyasının güncel dosyaları o bölümün teknik başvurusudur. **BOONIE** adı kullanıcı tarafından bu paket hazırlanırken verildi. Kaynak görsellerin üzerindeki FASULYE etiketleri arşivdeki özgün halleriyle durur.

| İş | Depodaki başvuru |
|---|---|
| Seri kararları ve adımlar | `AGENTS.md`, `CHANNEL_STRATEGY.md`, `PRODUCTION_WORKFLOW.md` |
| Karakter ve stil | `STYLE_GUIDE.md`, `CHARACTER_BIBLE.md`, `IMAGE_GENERATION_GUIDE.md`, `character-references/`, `engine/fasulye.py`, `engine/palettes.py` |
| Senaryo, ses ve dil | `NARRATION_GUIDE.md`, `reference-analysis/LOCALIZATION.md`, `reference-analysis/AUDIO_DNA.md`, `voice_config.json`, `voice/` |
| 001 Kahve örneği | `videos/001/{RESEARCH.md,SCRIPT.md,NARRATION.txt,SCENES.json,IMAGE_PROMPTS.md,STORYBOARD.md,TITLE_THUMBNAIL.md,STATUS.json}` |
| 001 test ve montaj | `videos/001/VOICE_QA_tr.md`, `VOICE_SCRIPT_tr.md`, `VOICE_PROMPT_tr_*.txt`, `PAUSES_tr.json`, `audio/timing_tr*.json`, `timeline_tr.json`, `engine/tools/` |
| Kodla çizilen pilot | `engine/examples/pilot_gobeklitepe/` ve ilgili `reference-analysis/PILOT_README.md`. Belgede bazı eski yollar geçer, çalıştırmak için mevcut dosya yollarını doğrula. |

001'de `stages.images` notu 56 görselin önceki bir çalışma ortamında bulunduğunu belirtiyor. Aynı durum dosyasının tarama alanı 0 diyor. İncelenen Git kopyasında `images/` altında yalnızca `.gitkeep` kayıtlıydı. Parça MP3'leri ve zaman dosyaları kayıtlı, birleşik ses ve render yerel çıktı. Bu örnekte olduğu gibi, eksik varlıkta önce mevcut yerel klasörü ve eldeki onaylı dosyaları kontrol et. Yalnız geçmiş nottan yeni üretim, tamamlanmış kapak veya yayın sonucu çıkarma.

## Paketteki özgün PNG'ler

- `assets/fasulye/` içindeki 40 PNG, deponun `character-references/fasulye/` klasöründeki dosyaların birebir kopyasıdır. Beş pano, beş kostümün dört açıdan tekil çizimleri ve 15 tekil ifade içerir. `front` ön, `tq` üç çeyrek, `side` yan, `back` arka. Bazı adlar Türkçe karakter içerir.
- `assets/boards/` içindeki beş PNG, deponun `character-references/boards/` klasöründeki dosyalardır. [Genel bakış](../assets/boards/01_genel_bakis.png), [nesneler](../assets/boards/01_nesneler.png), [mekânlar](../assets/boards/02_mekanlar.png), [paletler](../assets/boards/03_paletler.png) ve [tipografi](../assets/boards/04_tipografi.png). Çoklu tasarım panolarında yalnızca A yönünü kullan.
- Tekil mekân ve nesne arşivleri için depodaki `character-references/locations/` ve `character-references/objects/` yollarını kullan. Bölüme özel sahne ve kapak girdileri ilgili bölümün yerel `images/` klasöründedir. Ink Explainer analizi yalnızca kurgu ve anlatım teknikleri için başvurudur.
