# ROADMAP — Fasulye kanalı

Son güncelleme: 2026-11-26

## Kanal
- **Ad:** Fasulye · **Slogan:** Sıradan şeyler. Sıra dışı hikâyeler. · **Şaka:** Dikkat: Gaz yapabilir.
- **Vaat:** Herkesin bildiği şeylerin bilinmeyen hikâyesi (merak kanalı); 6–9 dk, çizimli, kaynaklı, kuru mizahla.
- **Ritim hedefi:** haftada 1 uzun video + aynı görsellerden 2–3 Shorts. Her 4 videoda bir: izlenme, tutma oranı, kapak tıklama oranı değerlendirmesi.
- **Diller:** TR ana kanal. DE: önce dublaj izi + altyazı (aynı video), talep görürse ayrı DE kanal/video. EN: sonra.

## Konumlandırma (karar: 2026-11-26 — "tarih kanalı" değil, "merak kanalı")
Kanalın merkezi tarih değil **merak**. Değişmeyen şey konu değil **anlatım kimliği**: Fasulye karakteri, kuru mizah, çizim stili, şaşırtıcı gerçekler. Ortak kalıp: **herkesin bildiği bir şey + bilmediği bir hikâye**.
Başta dağılmamak için: **ilk 10 video ≈ %60 gündelik şeylerin tarihi**, kalan %40 diğer kategoriler. Yeni kategoriler (psikoloji, bilim, toplum, ekonomi, absürt olaylar) **önce Shorts ile test edilir** (2–3'er Short), tutan kategorinin uzun videosu yapılır. Sabit yüzdeler yerine izleyici verisine (tıklanma, tutma) bakılır.

| Kategori | Örnek | Uzun vadeli hedef pay |
|---|---|---|
| Tarih (gündelik şeylerin tarihi, yasaklar) | Kahve neden yasaklandı? | ~%30 (başlangıçta %60) |
| İnsan psikolojisi | Duşta neden güzel fikirler gelir? | ~%20 |
| Gündelik bilim | Kendi sesimiz bize neden garip gelir? (kafatası iletimi) | ~%15 |
| Toplum ve kültür | İnsanlar neden tokalaşır? | ~%15 |
| Ekonomi | Marketler sütü neden en arkaya koyar? (satış + soğutma lojistiği) | ~%10 |
| Absürt gerçek olaylar | Avustralya'nın emu savaşı (önce Türkçe'de var mı bak) | ~%10 |

Not: ATOMI derin bilim konularına odaklanırsa Fasulye gündelik merak + insan davranışı + tuhaf hikâyelerde kalır. Bilim/psikoloji videoları için Fasulye'yi **günümüzde** gösteren yeni sahne tipi ve görsel promptları gerekir.

## Rakip notu — Kasketli Tarih (@kasketlitarih, 2026-11-26'da bakıldı)
69 abone, 138 video, neredeyse günlük yükleme; son 30 videonun çoğu 100'ün altında izlenme (en yüksek 744). Konular Türkiye/Osmanlı gündelik tarihi: kahve/IV. Murad, Fatih'in sofrası, alaturka saat, lale çılgınlığı. **Kaçınılacak:** "Saat 12!", "Bir ev parası" gibi onların başlıklarına benzeyen başlık/kapaklar. Çakışan konularda farklı açı (dünya ↔ Osmanlı karşılaştırması, ters köşe). Konu kimsenin malı değil; izlenmeyi kapak/başlık/anlatım belirler. Son 30 videoda çatal, 11 gün, iki uyku, tuvalet kâğıdı yok (kalan 108 video kontrol edilmedi).

## Video sırası (güncel plan, 2026-11-26)
| No | Konu | Kapak yazısı | Durum |
|---|---|---|---|
| 001 | Kahve neden defalarca yasaklandı? | YASAK! | **Yüklendi** (TR); DE ses izi bekliyor |
| 002 | Çatal kullanmak gerçekten günah mıydı? (Avrupa ↔ Osmanlı sofrası) | GÜNAH! | araştırma v1 hazır — senaryo bekliyor |
| 003 | İnsanlar bir gecede 11 günü nasıl kaybetti? | 11 GÜN! | plan |
| 004 | Kolomb'dan önce dünyada olmayan yiyecekler (Fatih menemen yiyemezdi) | DOMATES YOK! | plan |
| 005 | İnsanlar neden eskiden iki kez uyuyordu? | İKİ UYKU! | plan |
| 006 | Orta Çağ insanları gerçekten pis miydi? (Avrupa ↔ hamam) | YIKANMAK! | plan |
| 007 | Lale çılgınlığı + Lale Devri (ters köşe: çılgınlık abartılmış olabilir) | LALE! | plan — Kasketli Tarih'ten farklı açı |
| ... | Tuvalet kâğıdı öncesi, Şeker "beyaz altın", Göbeklitepe (en sona; rakip çok) | | havuz |

Shorts ile test kuyruğu: psikoloji (duşta fikirler), bilim (kendi sesimiz), ekonomi (market/süt), toplum (tokalaşma). Tarihsel iddialar senaryo aşamasında doğrulanır.

## 001'den öğrenilenler (sonraki videolara kural)
- Görüntü **2–3 sn'de bir** değişmeli: ana sahne (~55) + elle yazılmış ara çekimler (~80) → ~140 çekim / 7 dk.
- Ara çekim promptları ilk promptlarla **aynı biçimde** (stil + karakter blokları + elle yazılmış sahne içeriği). Kısa alternatif ayrıca tutulur.
- ChatGPT'ye **30'arlı partiler**, her partide yeni sohbet; ana sahne referansları repodaki `images_ref/` klasöründen.
- **Müziksiz** sürüm tercih edildi (referans kanal "kuru ses"); efektler seyrek kalır.
- Yakınlaşma yalnızca **yavaş ve sürekli**; ani zoom yok. Anlatıma kurgu müdahalesi yok (ham ElevenLabs sesi).
- Kapak: tek kelime, büyük, kırmızı (#B83A2B), sağ üst; sağ alt köşe boş (süre etiketi).

## Açık işler
- [ ] 001: YouTube'da "Ses" sütunu açılınca `Kahve_001_DE_dublaj.mp3` yükle
- [x] 001: Prusya Short hazır (`videos/001/shorts/`)
- [ ] 001: Kdenlive projesini 142 çekimle güncelle (isteğe bağlı)
- [ ] Telefon/kimlik doğrulaması (özel kapak, uzun video, çok dilli ses)
- [ ] ElevenLabs planının ticari kullanım hakkını kontrol et
- [ ] Anlatıcı sesinin kaynağını netleştir (klon mu, kütüphane sesi mi) → YouTube "yapay içerik" beyanı
- [x] 002 (çatal) araştırma v1 (`videos/002/RESEARCH.md`; kaynak sınırları içeride)
- [ ] 002: kaynak pasajı son kontrolü ve senaryo onayı
- [ ] Shorts test kuyruğu: İsveç · IV. Murad · Londra · Mekke (001) + yeni kategorilerden 2–3'er Short
