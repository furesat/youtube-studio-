# PRODUCTION_PIPELINE — Yeniden kullanılabilir üretim sistemi tasarımı

Bu belge tasarımdır; **hiçbir parçası henüz yerelde çalıştırılıp doğrulanmadı.** Referanstan öğrenilen teknikler: statik katmanlı kompozisyon, ~2 sn kesme ritmi, hızlı kuru anlatım, kart/grafik/illüstrasyon dönüşümü, bookend ve söz–ödeme yapısı. Karakter, marka, senaryo ve çizimler **özgün** olacak.

## 1. İlke
"Hareket"i animasyon değil **ritim + katman yeniden kullanımı** yaratır. Bu yüzden sistem şu üç şeyi ucuza ve tutarlı üretmeli: (1) karakter/poz/nesne varlık kütüphanesi, (2) senaryo → sahne planı, (3) otomatik zamanlama.

## 2. Akış

```
Senaryo (TR, kısa cümleler)
   → sahne_plani.json (cümle → 1-3 sahne, her sahne: tip, arka plan, karakterler, nesneler, kart metni)
   → TTS (Chatterbox TR, cümle bazlı wav)
   → zamanlama.json (cümle süreleri + kelime vurgu işaretleri)
   → Remotion kompozisyonu (sahne tipleri → şablonlar)
   → ffmpeg (ses miksajı, −14 LUFS) → 1080p / 4K render
```

## 3. Katmanlı sahne şablonları (SCENE_CATALOG scene_types'tan)
`CampDay`, `NightFire`, `InteriorHut`, `ModernRoom`, `TextCard`, `CompareSplit`, `RoadCheckpoints`, `MapPin`, `ChartLine/NumberLine/Iceberg`, `CloseUp`, `ExpertAtWork`, `AnimalVignette`, `IconCard`, `RedX`, `Crowd`, `SponsorBlock` (tek çok kareli şablon).
Her şablon = sabit katman sırası: `bg → mid (nesne) → characters → fx (X, daire, ok) → label`. Remotion props: `{bg, chars:[{id,pose,expr,x,y,scale}], objects, label}`.

## 4. Özgün karakter ve marka kimliği (karar bekliyor)
- Kendi karakter ailemiz (referanstaki çubuk adam + kürk ikilemini birebir kullanma). Öneri: **ortak tek bir "anlatıcı" tasarımı + zaman/tema başına 3–4 yardımcı karakter**, her biri ayrı model sayfası: ön, üç-çeyrek, yan, 8 poz, 8 ifade (göz/kaş/ağız varyantları ayrı katman).
- Kendi renk paletimiz: referans HEX'lerini aynen almak yerine 8–10 renklik özgün palet + 1 vurgu rengi + beyaz kâğıt tonu. Kanal adı/logo/jingle sonra.
- Çizgi: tek kalınlık seti (ince 3 px / orta 5 px / kalın 10 px @1080p), kenar hafif titrek.

## 5. Varlık üretim hattı
1. Karakter master çizimi (elle veya vektör). Tutarlılık için **model üretimi yerine elle çizim/vektör**; ifade ve poz varyantı katman olarak.
2. Arka planlar: FLUX.1 schnell (yerel mflux) ile üretip elle düzelt; her dünya için 1 ana kompozisyon + 3 varyant.
3. Nesne/ikon kütüphanesi: SVG (kendi çizimimiz).
4. Harita: Natural Earth (kamu malı) SVG.
5. Tüm varlıklar `assets/<kategori>/<id>@v1.png` ve `assets.json` içinde etiketli.

## 6. Ses ve zamanlama
- Chatterbox Multilingual (tr) ile cümle cümle üret; duygu parametresi sahne tipine göre (nötr, vurgu, gerilim).
- Kelime/cümle zamanlaması: Whisper `word_timestamps` ile hizalama (Apple Silicon: mlx-whisper); sonuç `zamanlama.json`.
- Otomatik sahne zamanlaması: sahne süresi = bağlı cümlelerin sesi / sahne sayısı; hedef 1,4–2,8 sn aralığına sıkıştırma; çok uzunsa bölme önerisi.
- Ses efektleri: CC0 kütüphane, kısa, düşük ses; müzik yatağı opsiyonel, −28 LUFS civarı. Hedef nihai −14 LUFS (`ffmpeg loudnorm` iki geçiş).

## 7. Render
- Remotion `renderMedia` 1920×1080 @30; 4K için `scale: 2` (aynı kompozisyon). Gerçek 4K kalite için varlıklar ≥2× ham üretilmeli (3840×2160 arka plan).
- Kodlama: H.264/H.265 (VideoToolbox) — donanım hızlandırma ile süre kısalır. M5 üzerinde gerçek süre **ölçülmedi**.

## 8. Kalite kontrol (otomatik)
- Sahne süresi aralığı, boş sahne yok, kelime/sahne ≤ 12, LUFS, pik < −1 dBTP, metin taşma, varlık ID doğrulama.
- İlk 60 sn için manuel izleme.

## 9. Yol haritası (sonraki oturum)
1. **Kalite kapısı (yarım gün):** Chatterbox TR'yi M5'te kur, 10 Türkçe cümle üret, dinle. Karar: yeterli mi?
2. Karakter ailesi + palet onayı.
3. Remotion iskeleti (5 sahne tipi) + sahne_plani.json şeması.
4. 60 sn'lik özgün test videosu (sorumluluk: kullanıcı onayı sonrası).

## 10. Açık kararlar
- Kanal konusu/dili: Türkçe mi, çift dil mi?
- Karakter yönü: çubuk-adam benzeri tek "anlatıcı" mı, farklı bir dünya mı?
- Sesi kim verecek: sentetik mi, kendi sesin mi?
