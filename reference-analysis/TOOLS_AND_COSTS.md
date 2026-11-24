# TOOLS_AND_COSTS — Üretim teknolojisi araştırması

Kurallar: Higgsfield yok, yeni ücretli abonelik yok, ücretli API yok. Doğrulama tarihi: 24 Kasım 2026 (web araştırması bu oturumda). **Doğrulanmayanları açıkça işaretledim.** Yasal tavsiye değildir.

## 0. Donanım notu
MacBook M5 bellek/depolama miktarını bu oturumda okuyamadım (cihaz kabuğu hâlâ indirme aşamasındaydı; yalnızca dosya aktarım araçları çalıştı). Aşağıdaki "donanım" sütunları kaynak belgelerdeki genel Apple Silicon gereksinimleridir. **M5'te gerçek performans ve bellek, kurulumdan sonra test edilmelidir.**

## 1. Türkçe seslendirme (en kritik karar)

| Araç | Türkçe | Lisans (doğrulandı) | Ticari kullanım | Not |
|---|---|---|---|---|
| **Chatterbox Multilingual (V3)** | **Var (tr)** — 23 dil | **MIT** (Resemble AI, kaynak: model kartı, resemble.ai) | Evet | 0,5B parametre; sıfır-atış ses klonlama; duygu "exaggeration" ayarı; çıktılar PerTh filigranlı. Türkçe kalite **henüz test edilmedi**. Apple Silicon (MPS) performansı doğrulanmadı. |
| **Kokoro-82M** | **Yok.** VOICES.md'ye göre 9 dil: İngilizce (US/UK), Japonca, Mandarin, İspanyolca, Fransızca, Hintçe, İtalyanca, Brezilya Portekizcesi | Apache-2.0 | Evet | Türkçede kullanılamaz. İngilizce/İspanyolca yan projelerde hızlı, hafif (82M). |
| **Piper tr_TR** | Var (dfki, fettah, fahrettin) | Ses deposu MIT etiketli; güncel Piper motoru (piper1-gpl) GPL-3.0; **dfki sesi model kartında CC BY-NC-SA 4.0 veri** | **dfki: hayır (NC)**; fettah/fahrettin veri lisansı **doğrulanamadı** | Tek tek ses kartı kontrol edilmeden ticari kullanma. Robotik, düşük duygu; yedek/taslak. |
| **Coqui XTTS-v2** | Var (tr dahil 17 dil) | **CPML — yalnızca ticari olmayan** | **Hayır** | Kanala gelir girecekse kullanma. |
| **Meta MMS-TTS (tur)** | Var | CC-BY-NC | **Hayır** | Kalite düşük, NC. |
| **F5-TTS Turkish topluluk modelleri** | Var | Orkhon-TTS: Apache-2.0 (alfa); marduk-ra: CC-BY-NC; Karayakar: MIT | Değişken | Topluluk alfa kalitesi, kaynak veri lisansı belirsiz (kaynak: bağımsız bir araştırma sayfası, resmi değil). |
| **Microsoft Edge TTS (tr-TR-EmelNeural/AhmetNeural)** | Var, doğal ses | Resmi API değil: Edge "Read Aloud" uç noktasını kullanan gayriresmî istemci | **Belirsiz / riskli** | Ücretsiz ve kaliteli ama resmi lisans/SLA yok, servis kapanabilir; ticari kanalın omurgası yapma. |
| **Cloudflare Workers AI TTS** | tr listesinde yok (MeloTTS vb. İngilizce ağırlıklı; doğrulanmadı) | — | — | Günlük ücretsiz 10.000 neuron (aşağıya bak). |

**Öneri:** Birincil: Chatterbox Multilingual (MIT) ile Türkçe, kendi yazdığımız/izinli referans ses (10 sn) veya klonlamasız; **gerçek test zorunlu** (duygu, vurgu, tekrar, telaffuz). Yedek: Piper fettah/fahrettin (veri lisansı doğrulanırsa). Edge TTS yalnızca taslak/zamanlama için. **Başka birinin sesini klonlamayacağız** — kendi sesimiz veya izinli sesle.

Kelime zamanlaması: Whisper (MIT) + wav2vec2 tabanlı zorlamalı hizalama (WhisperX stili; Apple Silicon: `mlx-whisper`, `whispermlx`). **Uyarı:** torchaudio MMS_FA hizalayıcı CC-BY-NC; ticari kullanım için lisansı uygun CTC hizalayıcı (ör. Apache-2.0 wav2vec2 tabanlı) kullanılmalı. Türkçe hizalama modeli lisansı **doğrulanmadı**; alternatif: Chatterbox çıktısını cümle bazlı üretip cümle sınırlarını doğrudan kullanmak (hizalamaya gerek kalmaz), kelime vurgusu için Whisper `word_timestamps`.

## 2. Görsel üretim

| Araç | Gerçek yetenek | Lisans | Donanım | Maliyet |
|---|---|---|---|---|
| **FLUX.1 schnell (MLX / mflux)** | Yerel metinden görüntüye, 4 adım, Apple Silicon yerel | Ağırlıklar **Apache-2.0**, mflux MIT | Kaynak sayfaya göre schnell 4-bit için ≥16 GB birleşik bellek; M2 Max'te 1024² schnell ~8–15 sn (M5'te ölçülmedi) | 0 $ |
| FLUX.1 **dev** | — | **Non-commercial** | — | Kullanma |
| **Cloudflare Workers AI — flux-1-schnell** | API, bulut | Cloudflare şartları geçerli | Gerek yok | Ücretsiz plan: günde 10.000 neuron. Sayfadaki oran: 4,80 neuron/512² karo + 9,60 neuron/adım. Hesabım: 1024² (4 karo) + 4 adım ≈ 57,6 neuron → günde ≈170 görsel (hesaplama; resmi değil, doğrula). Ücretli API'ye geçme (kuralımız). |
| **ANDROMEDA Image Engine (Cloudflare)** ve "mevcut görsel üretim bağdaştırıcıları" | **Doğrulanamadı**: yerel projenizde; inceleyemedim | ? | ? | ? |
| Blender (3B, Cycles/Eevee) | Statik/kompleks sahne render, kamera hareketi; 2D çizgi film için Grease Pencil | **GPL** (araç); ürettiğiniz çıktılar size ait *(bu oturumda yeniden doğrulamadım)* | Apple Silicon yerel (Metal) | 0 $ |
| SVG / Canvas / Python (Pillow, cairosvg) | Varlık montajı, metin kartları, haritalar, grafikler | Açık kaynak | Çok hafif | 0 $ |
| Manim Community | Matematik animasyonu, grafik/eksen/sayı doğrusu animasyonu | **MIT** | CPU, LaTeX isteğe bağlı | 0 $ |

**Yorum:** Referansın stilini üretmek için **katmanlı varlık** gerekir (arka plan, karakter pozları, nesneler ayrı PNG). Metinden görüntü modelleri tek parça kompozisyon verir; karakter tutarlılığı garanti değil. En sağlam yol: kendi karakterimizi vektör/ham çizim olarak bir kez tasarlayıp poz kütüphanesi çıkarmak; modeller yalnızca arka plan ve nesne varlığı için.

## 3. Animasyon / kompozisyon / render

| Araç | Gerçek yetenek | Lisans | Maliyet |
|---|---|---|---|
| **Remotion** | React ile video; 1080p/4K render (Chrome Headless + FFmpeg); `spring`, geçişler | Özel lisans: **bireyler ve ≤3 kişilik organizasyonlar ücretsiz**, ticari dahil; 4+ kişi için Company License. Tüm özellikler aynı. Remotion 5.0'da lisansın hafifçe değişeceği belirtilmiş — sürüm geçişinde kontrol et. | 0 $ (≤3 kişi) |
| **FFmpeg** | Kodlama, birleştirme, `xfade`, ses miksajı, `loudnorm` | LGPL/GPL (yapıya göre) *(oturumda yeniden doğrulanmadı)* | 0 $ |
| Python + OpenCV/Pillow | Toplu varlık işleme, sahne planlama | BSD/MIT/HPND | 0 $ |
| DaVinci Resolve (bağlı araç olarak listelenmiş) | Montaj/renk (ücretsiz sürüm) | Ticari, ücretsiz sürüm sınırlı | Kullanıcı zaten kurduysa 0 $; **bu oturumda test edilmedi** |

## 4. Ses tanıma ve yardımcılar
- **Whisper** (OpenAI, MIT): Türkçe dahil çok dilli. Apple Silicon: `mlx-whisper`. Bu oturumda small.en (İngilizce) ile referansı çözümledim.
- **Silero VAD**: MIT (bu oturumda kullanıldı).
- **sherpa-onnx**: Apache-2.0 (bu oturumda kullanıldı; whisper ONNX modelleri GitHub sürümlerinden indirildi).

## 5. Maliyet özeti (hedef: 0 $/video)
- Ses: Chatterbox yerel (0 $), hizalama: Whisper yerel (0 $).
- Görsel: mflux/FLUX schnell yerel (0 $) + elle çizilmiş karakter.
- Kompozisyon + render: Remotion (≤3 kişi) + FFmpeg (0 $).
- Elektrik/zaman maliyeti dışında lisans maliyeti **0 $**; tek risk: Türkçe TTS kalitesi ve Remotion'un ileride ekip büyümesinde lisans geçişi.

## 6. Bu oturumda yapılmayanlar / doğrulanamayanlar
- Kokoro/Chatterbox/mflux **yerelde çalıştırılmadı**; kalite ve hız iddiası yok.
- M5 donanım ayrıntıları okunamadı.
- ANDROMEDA ve yerel bağdaştırıcılar incelenmedi.
- Blender, FFmpeg lisansı bilgisi bilinen genel bilgidir; bu oturumda kaynaktan yeniden okunmadı.
