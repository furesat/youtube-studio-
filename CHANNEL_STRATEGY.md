# CHANNEL_STRATEGY

## Kanal
- **Ne:** Tarih ve bilimde az bilinen, şaşırtıcı ama kaynaklı hikâyeler. Kuru mizahla, hızlı tempoyla anlatılır.
- **Kim için:** Türkçe konuşan meraklı yetişkinler (18–45). İkinci aşamada DE ve EN kanallar/dublajlar.
- **Vaat:** "Bildiğini sandığın şeyin arkasındaki gerçek hikâye; 7 dakikada, gülümseterek, kaynağıyla."
- **Ayırt edici:** Fasulye karakteri ("iki dünya" şakası: aynı kişi, farklı çağ), sıcak kâğıt dokulu çizimler, her videoda efsane ile gerçeği ayıran dürüstlük.

## Format
- **Süre:** 6–9 dk (ilk videolar ~7 dk). Kısa versiyonlar: 45–60 sn dikey kesitler (aynı görseller, yeniden kadrajlanmış).
- **Yapı:** kanca (0–30 sn) → 3–5 bölüm (kontrol noktaları) → ters köşe/ders → kapanış geri çağırması.
- **Ritim:** görsel değişim ortalama ~2 sn (referans analizi). Anlatım gerektirdiğinde yavaşlar.

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
