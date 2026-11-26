# CHANNEL_STRATEGY

## Kanal
- **Ne:** Tarih ve bilimde az bilinen, şaşırtıcı ama kaynaklı hikâyeler. Kuru mizahla, hızlı tempoyla anlatılır.
- **Kim için:** Türkçe konuşan meraklı yetişkinler (18–45). İkinci aşamada DE ve EN kanallar/dublajlar.
- **Vaat:** "Bildiğini sandığın şeyin arkasındaki gerçek hikâye; 7 dakikada, gülümseterek, kaynağıyla."
- **Ayırt edici:** Fasulye karakteri ("iki dünya" şakası: aynı kişi, farklı çağ), sıcak kâğıt dokulu çizimler, her videoda efsane ile gerçeği ayıran dürüstlük.

## Kanal adı ve kimlik (karar: 2026-11-26)
- **Kanal adı: Fasulye** (maskotla aynı; TR/DE/EN kanallarda aynı isim). Slogan önerisi: *"Bildiğin hikâyenin bilmediğin tarafı."*
- Kanal görselleri: `channel/kanal_gorsel_promptlari.txt` (banner 2560×1440, güvenli alan 1546×423 ortada; avatar 800×800). Yazılar motorla eklenir.

## Konumlandırma ve içerik sütunları (karar: 2026-11-26, güncellendi)
**Merkez tarih değil merak.** Kimlik = anlatım (Fasulye, kuru mizah, çizim stili, şaşırtıcı gerçekler); konu serbest. Kalıp: *herkesin bildiği bir şey + bilmediği bir hikâye.*
Kategori tablosu, ilk 10 video dağılımı (%60 gündelik tarih), Shorts ile test kuralı ve Kasketli Tarih rakip notu: **ROADMAP.md**.

Tarih içi alt sütunlar:
1. **Yasaklar ve tuhaf kurallar** (kahve, çatal, tütün…)
2. **Gündelik şeylerin gizli tarihi** (takvim, saat, uyku, tuvalet, şeker)
3. **Efsane mi gerçek mi?** (Orta Çağ'da yıkanma, Napolyon'un boyu…)
4. **Türkiye bağlantılı dünya hikâyeleri** (Lale Devri, Osmanlı'da saat)
Ritim: haftada 1 uzun video (6–9 dk) + aynı görsellerden 2–3 Shorts.

### Sıradaki konular
002 Çatal · 003 11 gün · 004 Kolomb'dan önce olmayan yiyecekler · 005 İki uyku · 006 Orta Çağ/hamam · 007 Lale (farklı açı). Göbeklitepe en sona.

## Format
- **Süre:** 6–9 dk (ilk videolar ~7 dk). Kısa versiyonlar: 45–60 sn dikey kesitler (aynı görseller, yeniden kadrajlanmış).
- **Yapı:** kanca (0–30 sn) → 3–5 bölüm (kontrol noktaları) → ters köşe/ders → kapanış geri çağırması.
- **Ritim:** görsel değişim ortalama 2–3 sn (referans ~2 sn; 001 v2 = 2,8 sn). Anlatım gerektirdiğinde yavaşlar.
- **Ses:** ham anlatım + seyrek efekt, varsayılan **müziksiz** (001 kararı).

## Üretim ekonomisi (manuel ImageGen ile sürdürülebilirlik)
7 dakikalık bir video ~200 görsel değişimi demek. Hepsini ImageGen'le üretmek sürdürülemez. Bu yüzden **hibrit model**:
| Tür | Payı | Kaynak |
|---|---|---|
| **Ana sahne görselleri** | ~40–55 / video | ChatGPT ImageGen (manuel) |
| **Türev çekimler** (aynı görselden yakın plan, kaydırma, durum değişimi) | ~80–100 | `engine` (kırpma, katman, kırmızı X/daire, ok) |
| **Kartlar ve grafikler** (beyaz kart, zaman çizgisi, harita iğnesi, sayı doğrusu) | ~30–50 | `engine` (kendi çizim motorumuz) |

Hedef iş yükü: video başına ~3–4 saat görsel üretimi + 1 saat kurgu.

## Yayın ritmi
Başlangıç: haftada 1 video. Her 4 videoda bir: format, izlenme ve tutma oranı değerlendirmesi.

## Konu seçme ölçütleri (her video için puanla, 1–5)
1. Merak boşluğu: başlıkta bir soru doğuyor mu?
2. Kaynak kalitesi: en az 3 güvenilir kaynak var mı?
3. Görselleştirilebilirlik: sahneleri çizilebilir mi?
4. Mizah potansiyeli
5. Çok dilli potansiyel (DE/EN'de de ilgi çeker mi?)
6. Kanalın Türk izleyicisiyle bağ (zorunlu değil, artı puan)

## Konu havuzu
- 001 Kahve neden defalarca yasaklandı? (**üretimde**)
- Göbeklitepe: tarladan önce tapınak mı? (pilot var, uzun versiyon)
- Lale çılgınlığı gerçekten ekonomiyi çökertti mi?
- Orta Çağ'da insanlar gerçekten yıkanmıyor muydu?
- Takvimden 11 gün nasıl silindi? (Rumi / Gregoryen takvim)
- Çatal neden "günah" sayıldı? (**002**)
- Kolomb'dan önce olmayan yiyecekler (domates/biber/patates; Fatih menemen yiyemezdi)
- İnsanlar neden iki kez uyuyordu? (bölünmüş uyku)
- Duşta neden güzel fikirler gelir? (Short testi; bilimsel kısım kesin değil, dikkatli anlat)
- Kendi sesimiz bize neden garip gelir? (Short testi)
- Marketler sütü neden en arkaya koyar? (Short testi; satış + soğutma lojistiği)
- İnsanlar neden tokalaşır? (Short testi)
- Avustralya'nın emu savaşı (Türkçe'de var mı kontrol et)
