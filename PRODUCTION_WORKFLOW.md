# PRODUCTION_WORKFLOW — bir video konudan yayına

Her adımın çıktısı `videos/NNN/` içindedir. Durum `STATUS.json`'da tutulur. Her önemli adımdan sonra commit atılır (kısa, Türkçe mesaj).
Örnek video: `videos/001/` (Kahve). Yeni video bu yapıyı kopyalar.

## A. Hazırlık ve senaryo
| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 1 | Klasörü aç: `videos/NNN/` (001'in yapısını kopyala) | Claude | `STATUS.json` |
| 2 | Konu + kaynak araştırması; efsane/gerçek ayrımı (en az 3 güvenilir kaynak) | Claude | `RESEARCH.md` |
| 3 | Senaryo (cümle kimlikli: L001…), 6–9 dk, kanca → 3–5 bölüm → ters köşe → kapanış geri çağırması | Claude → kullanıcı onayı | `SCRIPT.md` |
| 4 | Temiz anlatım metni (sayılar okunuşuyla, telaffuz notları) | Claude | `NARRATION.txt`, `NARRATION_de.txt` |

## B. Görsel plan
| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 5 | Sahne planı: her sahne = 1 ana görsel (~6–7 sn anlatım) | Claude | `SCENES.json` (`build_scenes_NNN.py`) |
| 6 | Ana sahne promptları + storyboard | `engine/tools/prompts.py` | `IMAGE_PROMPTS.md`, `STORYBOARD.md` |
| 7 | **Ara çekim planı**: görüntü **2–3 sn'de bir** değişsin (referans kanal ~2 sn). Her ana sahne anlatım parçalarına bölünür; her parça için ara çekim içeriği **elle** yazılır | Claude | `shots_v2_NNN.py` → `SHOTS_v2.json`, `IMAGE_PROMPTS_v2.md` |
| 8 | Ana sahne görselleri → kullanıcı kaydeder | ChatGPT + kullanıcı | `images/NNN_Sxxx_v1.png` |
| 9 | Ana sahnelerin küçük referans kopyaları repoya (ChatGPT repodan okuyabilsin) | Claude | `images_ref/NNN_Sxxx_ref.jpg` (1024 px) |
| 10 | Ara çekim görselleri: ChatGPT'ye **30'arlı partiler** halinde, her partide yeni sohbet | ChatGPT + kullanıcı | `images/NNN_SxxxB_v1.png` |
| 11 | Görsel kontrolü (stil, yazı yok, karakter) | Claude (kontakt sayfası) | — |

ChatGPT'ye verilecek parti metni: `IMAGE_GENERATION_GUIDE.md` → "Ara çekimler (v2)".

## C. Ses
| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 12 | Seslendirme (ElevenLabs, ham; kurgu müdahalesi yok) | `voice_render.py` | `audio/<lang>/part_*.mp3` |
| 13 | Parçaları birleştir + cümle zamanlaması | `build_audio.py` | `audio/full_<lang>.mp3`, `timing_<lang>_final.json` |
| 14 | Miks. **Karar (001): müziksiz** — anlatım + seyrek efekt. Müzikli sürüm isteğe bağlı | `mix_audio.py --no-music` | `audio/mix_<lang>_muziksiz.wav` |
| 15 | **Dublaj izi** (aynı görüntüye başka dil): DE anlatımı TR sahne zamanlamasına oturtulur (sessizlik kısaltma, en çok %15 hızlandırma, ±0,6–1,4 sn kayma) | `fit_dub.py --lang de` + `mix_audio.py --voice … --out …` | `audio/dub_de_on_tr.wav` → YouTube için mp3 |

## D. Kurgu ve render
| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 16 | Ana sahne kareleri (yazı katmanı, harita iğneleri, damgalar) | `assemble.py --lang tr` | `renders/tr/shots/` |
| 17 | v2 render: ana sahne kareleri + ara çekimler, her çekimde yavaş yakınlaşma (ani zoom yok) | `render_v2.py` | `renders/tr/Kahve_001_TR_v2_muziksiz.mp4` (1080p) |
| 18 | Altyazı: TR = `renders/tr/001_tr.srt`; DE = dublaj zamanlamasından üretilir | `assemble.py` / `fit_dub.py` raporu | `youtube/*_altyazi.srt` |
| 19 | (İsteğe bağlı) düzenlenebilir Kdenlive projesi | Kdenlive MCP | bkz. `EDITING_KDENLIVE.md` |

## E. Yayın paketi
| # | Adım | Kim | Çıktı |
|---|---|---|---|
| 20 | Kapak: ChatGPT yazısız görsel üretir → başlık yazısı motorla eklenir | ChatGPT + `thumbnail.py` | `youtube/*_kapak.jpg` (1280×720) |
| 21 | Başlık, açıklama (bölüm zamanları + kaynaklar), etiketler; DE çevirisi | Claude | `youtube/youtube_aciklama*.txt` |
| 22 | FuresTube'da önizleme / karşılaştırma | Claude | bkz. `TEST_SITE.md` |
| 23 | Kullanıcı Mac'te tek klasörde toplar: `~/Downloads/youtube video/YouTube_yukleme_NNN/` | Claude | — |
| 24 | YouTube Studio'ya yükleme | kullanıcı | bkz. `YOUTUBE_PUBLISHING.md` |
| 25 | Shorts: aynı görsellerden 2–3 dikey kesit (45–60 sn) | Claude | (planlandı) |

## Komutlar (001 örneği, repo kökünden)
```
python3 engine/tools/build_scenes_001.py               # SCENES.json
python3 engine/tools/prompts.py videos/001              # IMAGE_PROMPTS.md + STORYBOARD.md
python3 engine/tools/shots_v2_001.py                    # SHOTS_v2.json + IMAGE_PROMPTS_v2.md
python3 engine/tools/build_audio.py videos/001 --lang tr
python3 engine/tools/mix_audio.py videos/001 --lang tr --no-music
python3 engine/tools/assemble.py videos/001 --lang tr   # ana sahne kareleri + TR SRT
python3 engine/tools/render_v2.py videos/001 --audio audio/mix_tr_muziksiz.wav --out renders/tr/Kahve_001_TR_v2_muziksiz.mp4
python3 engine/tools/fit_dub.py videos/001 --lang de
python3 engine/tools/mix_audio.py videos/001 --lang tr --no-music --voice videos/001/audio/dub_de_on_tr.wav --out videos/001/audio/dublaj_de_muziksiz.wav
python3 engine/tools/thumbnail.py videos/001 "YASAK!"
```
Not: DE dublaj miksini TR seviyesine eşitlemek için `ffmpeg -af "volume=+XdB,alimiter=limit=0.95"` (001'de +4,6 dB) ve süreyi videoya kırp (`-t`).

## Zamanlama
- Sesten önce: `voice/providers/estimate.py` hece sayısından süre tahmin eder (TR 5,6 hece/sn).
- Ses geldikten sonra: cümle süreleri `timing_<lang>_final.json`'dan; sahne süresi = bağlı cümlelerin toplamı.
- Ara çekimlerin başlangıcı anlatımdaki karakter oranına göre yaklaşık hesaplanır (`SHOTS_v2.json`); kayma görülürse elle düzeltilir.
- Kare sınırları kümülatif süreden hesaplanır (30 fps); toplam süre sesle birebir eşleşir.

## Dosya isimleri
- Ana sahne: `NNN_Sxxx_vK.png` (ör. `001_S014_v2.png`). En yüksek `vK` kullanılır; kilitlemek için `_final`.
- Ara çekim: `NNN_Sxxx{b,c,d…}_vK.png` (ör. `001_S014c_v1.png`).
- Kapak: `NNN_T01_vK.png`. Kanal görselleri: `kanal_banner_vK.png`, `kanal_avatar_vK.png`.
- Ses: `audio/<lang>/part_A.mp3` … + `audio/full_<lang>.mp3` + `audio/timing_<lang>_final.json`.

## Dil uyarlaması (DE / EN)
`SCRIPT.md` TR asıldır. Uyarlama: `NARRATION_de.txt`; `SCENES.json` içinde `overlay.de`. Görseller ortaktır (metinsiz).
İki yol: (1) aynı videoya **dublaj izi** (YouTube "Ses" özelliği — kanalda açık olmalı), (2) ayrı DE video (DE zamanlamasıyla ayrı render).

## Bölüm klasör standardı (2026-11-27)
- Her video kendi `videos/NNN/` dizininde yaşar. Numara sabit kalır; başlık değişse de klasör adı değişmez.
- `README.md` bölüm dizini, `STATUS.json` makinece okunabilir durum, `RESEARCH.md` tek araştırma kaynağıdır. Kaynakça, iddia kontrolü, tarihî tanıklık/kurmaca ayrımı, mizah fikirleri ve Shorts adayları aynı RESEARCH.md içinde başlıklarla tutulur. Ayrı geçici araştırma dosyaları repo köküne açılmaz.
- Senaryo, anlatım, sahne planı, promptlar ve storyboard mevcut araçlarla uyumlu olarak aynı bölüm dizininde kalır; ilgili alt klasörler `images_ref/`, `youtube/`, `shorts/` vb. sadece gerektiğinde oluşturulur. Ağır dosyalar yerelde kalır.
- Kaynağa erişilemediyse araştırmada belirt; görüş, espri ve varsayımları doğrulanmış olaylarla karıştırma. Kaynak kodlarını senaryoda izlenebilir tut.
- Mevcut 001 dosyaları yerinden taşınmaz; eski araç yolları korunur. Yeni bölümler bu standardı izler.
