# REFERENCE_ANALYSIS — "Your Entire Life as an Ancient Human" (Ink Explainer)

Bu analiz gerçek MP4 üzerinden, kare kare yapıldı (FFmpeg/FFprobe, OpenCV, scikit-learn, sherpa-onnx Whisper small.en, Pillow). Referans kareler `reference_frames/` altında, hepsini görüntüleyerek inceledim: 389 sahnenin tamamı 13 contact sheet'te (`reference_frames/contact_sheets/`), 39 tam çözünürlüklü anahtar kare `key_frames/` içinde, ana özet `contact_sheet.jpg`.

## 1. Tek cümlelik çözüm

Bu video "animasyon" değil: **statik, katmanlı çizimlerin ~2 saniyede bir sert kesmeyle art arda gösterilmesi + çok yoğun, hızlı (~226 kelime/dk) bir anlatım**. Hareket hissini kamera, karakter animasyonu ya da geçiş efekti değil, **görüntü değişim sıklığı** (ortalama 1,99 sn) ve anlatımla birebir eşleşen illüstrasyon seçimi yaratıyor. Çok kareli animasyon sadece sponsor bloğunda var.

## 2. Teknik kimlik (FFprobe)

| Alan | Değer |
|---|---|
| Süre | 774,93 sn (12:55) |
| Çözünürlük / FPS | 1920×1080, 30 fps sabit (r_frame_rate = avg = 30/1) |
| Video | H.264 High L4.0, yuv420p, BT.709, ~347 kb/s (YouTube yeniden kodlaması: ince çizgi ve gradyan detayı sıkıştırma altında) |
| Ses | AAC-LC, 44,1 kHz stereo, ~128 kb/s |
| Ses seviyesi | −14,0 LUFS entegre, LRA 2,5 LU, true peak −0,9 dBFS |

Not: Dosya YouTube'dan inen bir yeniden kodlama; kaynak üretim çözünürlüğü, frame hızı ve renk ayarı hakkında kesin bilgi buradan çıkarılamaz. 30 fps ve 1080p görünen değerlerdir.

## 3. Ölçülen kurgu istatistikleri

- **389 sahne** (sert kesme); ortalama **1,99 sn**, medyan **1,8 sn**, p10 1,32 sn, p90 2,78 sn, en kısa 0,5 sn, en uzun 12,8 sn.
- Dağılım: <1 sn 7 · 1–2 sn 227 · 2–3 sn 128 · 3–5 sn 24 · ≥5 sn 3.
- Kesme yoğunluğu ≈ 0,50 kesme/sn. Sahne başına ortalama ~7,5 kelime anlatım.
- Ek **96 sahne-içi durum değişimi** (öğe ekleme 17, çıkarma 5, ufak değişim 74). Bunların ≈65'i sponsor bloğundaki UI/rozet değişimleri.
- Kare düzeyinde ölçüm: karelerin %91'inde (sahne içi) ardışık kareler arası fark ≈ 0. Sahne içinde karakter, ateş ve arka plan **hareketsiz** (ör. 14,6 sn ile 15,4 sn karesi arasında eşik üstü değişen piksel = 0).
- Kamera hareketi: 389 sahnenin yalnızca 3'ünde ölçülebilir ölçek değişimi var (255,4 sn; 263,2 sn; 538 sn). Ken Burns zoom/pan **ana hikâyede yok**.
- Animasyonlu geçiş (itme/kaydırma, 8–36 kare): 24 adet, hepsi sponsor girişinde (48,4 sn), sponsor bloğunda (207,9–281,3 sn) ve çıkışta (770,6 sn). Ana hikâyede **yalnızca tek karelik sert kesme**.

## 4. Anlatı yapısı (transkript, zaman damgalı)

| Zaman | Bölüm |
|---|---|
| 0:00–0:26 | Soğuk açılış: "hayatının en tehlikeli günü zaten yaşandı" + oyun kuralı (50.000 yıl önce doğuyorsun, aynı beden, aynı beyin) |
| 0:27–0:47 | Yanlış inanış ("30'da ölürlerdi") + açık döngü: "şu an tam senin yaşındayken inanılmaz bir şey yapıyor olurdun" |
| 0:48–0:51 | Sponsor duyurusu ("later") |
| 0:52–3:16 | Bölüm 1 — doğum ve bebeklik; 1. kontrol noktası |
| 3:22–4:13 | Bölüm 2 — çocukluk geçişi |
| 3:22–4:43 | Sponsor entegrasyonu (tehdit anlatısına bağlanıyor: "saklanmak güvenlikti, bugün bulunmak birkaç tıklama") |
| 4:44–6:33 | Bölüm 3 — 5-8 yaş oyun, "30" sayısının ortalama olduğunun açılması |
| 6:34–9:15 | Bölüm 4 — ergenlik/ilk av, 19–20 yaş "söz #1" |
| 9:15–10:13 | Bölüm 5 — 30'lar, tepe 33, "söz #2" |
| 10:13–11:49 | Bölüm 6 — büyükanne hipotezi, 50–60 yaş "söz #3" |
| 11:50–12:25 | Final: 78.000 yıllık gömü, açılışla aynı cümle yapısıyla bookend |
| 12:26–12:55 | Kapanış: açılış cümlesinin geri dönüşü + sponsor teşekkürü |

Kullanılan kalıplar: 3 aşamalı "kontrol noktası" ilerlemesi, 3 kez tekrarlanan "söz" (yaşına göre izleyiciye hitap), "Remember that" geri çağırma (8 kez), açılıştaki cümlenin kapanışta döndürülmesi, tek sahne üzerinde bilimsel kanıt (White Sands ayak izleri) ile duygusal bağ.

## 5. Bulgular → kendi sistemimize etkisi

1. **Üretim maliyeti düşük, etki yüksek**: ~390 statik kompozisyon + ses. Karakter animasyon sistemi şart değil; asıl yük illüstrasyon varlıkları ve senaryo-sahne eşleştirmesi.
2. **Katmanlı yeniden kullanım**: Aynı arka planlar (savana kampı, kulübe içi, modern oturma odası, hastane) tekrar tekrar kullanılıyor; yalnızca karakter/poz/nesne katmanı değişiyor.
3. **İki farklı üretim modu**: (a) ana hikâye: sert kesme, tam statik; (b) sponsor: çok kareli animasyon, itme geçişleri, UI ekran görüntüleri. Sistemimizde iki şablon gerekiyor.
4. **Anlatımın tempo olarak neredeyse kesintisiz** olması (konuşma karelerinin %88'i −40 dBFS üstü) görsel değişimin sıklığını zorunlu kılıyor.

## 6. Doğrulanamayan / sınırlar

- **Müzik ve ses efektlerini duyamadım.** Spektrogramda cümle aralarında sürekli bir müzik yatağı görünmüyor; çok kısık müzik/efekt olasılığını dışlayamam. Bu konuda kesin iddiada bulunmuyorum.
- Transkript ASR çıktısı (Whisper small.en, int8): özel adlarda hata var ("Incogme", "FA people" gibi okunan özel isim vb.). **Kelime düzeyinde zaman damgası yok**, sadece cümle/duraklama düzeyi; `narration_estimated` alanları bu yüzden tahmini.
- Çizimin elle mi, görüntü modeliyle mi üretildiğini kesin bilemem. Görünüm (gradyanlı boyalı arka planlar + tutarlı kalın kontur) katmanlı illüstrasyon varlıklarıyla uyumlu; üretim yöntemi hakkında kanıtım yok.
- `bg_family_heuristic` otomatik sezgiseldir; `scene_types[].examples_s` görsel incelemeden gelen yaklaşık zamanlardır.
- ANDROMEDA Image Engine ve "mevcut görsel üretim bağdaştırıcıları" yerel projenize ait; bu oturumda cihaz kabuğu hazır olmadığı için inceleyemedim (bkz. TOOLS_AND_COSTS.md).
