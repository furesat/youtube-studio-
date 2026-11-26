# ROADMAP — Fasulye kanalı

Son güncelleme: 2026-11-26

## Kanal
- **Ad:** Fasulye · **Slogan:** Sıradan şeyler. Sıra dışı hikâyeler. · **Şaka:** Dikkat: Gaz yapabilir.
- **Vaat:** Herkesin bildiği şeylerin bilinmeyen tarihi; 6–9 dk, çizimli, kaynaklı, kuru mizahla.
- **Ritim hedefi:** haftada 1 uzun video + aynı görsellerden 2–3 Shorts. Her 4 videoda bir: izlenme, tutma oranı, kapak tıklama oranı değerlendirmesi.
- **Diller:** TR ana kanal. DE: önce dublaj izi + altyazı (aynı video), talep görürse ayrı DE kanal/video. EN: sonra.

## İçerik sütunları
1. **Yasaklar ve tuhaf kurallar** — kahve, tütün, çatal, dans, kahkaha…
2. **Gündelik şeylerin gizli tarihi** — tuz, şeker, saat, takvim
3. **Efsane mi gerçek mi?** — Orta Çağ'da yıkanma, Napolyon'un boyu…
4. **Türkiye bağlantılı dünya hikâyeleri** — Lale Devri, Osmanlı'da saat, Göbeklitepe

## Video sırası
| No | Konu | Sütun | Durum |
|---|---|---|---|
| 001 | Kahve neden defalarca yasaklandı? | 1 | **Yüklendi** (TR); DE ses izi bekliyor |
| 002 | Lale çılgınlığı gerçekten ekonomiyi çökertti mi? | 3/4 | sıradaki — araştırma |
| 003 | Takvimden 11 gün nasıl silindi? | 2 | plan |
| 004 | Orta Çağ'da insanlar gerçekten yıkanmıyor muydu? | 3 | plan |
| 005 | Çatal neden "günah" sayıldı? | 1/2 | plan |
| 006 | Göbeklitepe: tarımdan önce tapınak mı? | 4 | plan (pilot var: `engine/examples/pilot_gobeklitepe/`) |

## 001'den öğrenilenler (sonraki videolara kural)
- Görüntü **2–3 sn'de bir** değişmeli: ana sahne (~55) + elle yazılmış ara çekimler (~80) → ~140 çekim / 7 dk.
- Ara çekim promptları ilk promptlarla **aynı biçimde** (stil + karakter blokları + elle yazılmış sahne içeriği). Kısa alternatif ayrıca tutulur.
- ChatGPT'ye **30'arlı partiler**, her partide yeni sohbet; ana sahne referansları repodaki `images_ref/` klasöründen.
- **Müziksiz** sürüm tercih edildi (referans kanal "kuru ses"); efektler seyrek kalır.
- Yakınlaşma yalnızca **yavaş ve sürekli**; ani zoom yok. Anlatıma kurgu müdahalesi yok (ham ElevenLabs sesi).
- Kapak: tek kelime, büyük, kırmızı (#B83A2B), sağ üst; sağ alt köşe boş (süre etiketi).

## Açık işler
- [ ] 001: YouTube'da "Ses" sütunu açılınca `Kahve_001_DE_dublaj.mp3` yükle
- [ ] 001: Shorts kesitleri (Kahve koklayıcılar · IV. Murad gece devriyesi · İsveç ikiz deneyi)
- [ ] 001: Kdenlive projesini 142 çekimle güncelle (isteğe bağlı)
- [ ] Telefon/kimlik doğrulaması (özel kapak, uzun video, çok dilli ses)
- [ ] ElevenLabs planının ticari kullanım hakkını kontrol et
- [ ] Anlatıcı sesinin kaynağını netleştir (klon mu, kütüphane sesi mi) → YouTube "yapay içerik" beyanı
- [ ] 002 araştırması
