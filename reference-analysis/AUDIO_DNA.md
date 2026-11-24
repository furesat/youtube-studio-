# AUDIO_DNA — Ses ve anlatım

Yöntem: ses 16 kHz mono çıkarıldı; VAD (Silero) + Whisper small.en (int8, sherpa-onnx) ile 90 segmentlik transkript; FFmpeg `ebur128`, `silencedetect`; spektrogram incelemesi (`reference_frames/motion_strips/spectrogram_0-40s.png`). **Ben sesi dinleyemedim**; aşağıdakiler ölçüm ve transkriptten çıkarımdır. Ton/duygu hakkında yalnızca metinden ve spektrogramdan çıkarılabilen şeyleri yazdım.

## 1. Tempo (ölçülen)

- 2.919 kelime / 774,9 sn = **≈226 kelime/dk** (tüm süre dahil). Konuşma segmentleri içinde ≈237 kelime/dk. Açılış (0–26 sn): 114 kelime / 26,4 sn ≈ 259 kelime/dk.
- Sessizlik: −38 dB altı ≥0,25 sn duraksama sadece **19 adet** (medyan 0,31 sn, p90 0,56 sn, maks 1,31 sn). 50 ms'lik karelerin %88'i −40 dBFS üstü. Yani cümle araları çok kısa, kurgu "nefes kırpılmış".
- Not: ASR doğruluğu tam değil; kelime sayısı ±%3 sapabilir.

## 2. Ses karakteri (spektrogram + seviye)

- Düşük frekanslı (40–300 Hz) enerji güçlü: yakın mikrofon / yüksek bas vurgulu ses işlemesi izlenimi. Cümle aralarında spektrogram koyuya düşüyor; sürekli bir müzik yatağı **görünmüyor**. Çok kısık müzik/efekti dışlayamam.
- Seviye: −14,0 LUFS (YouTube normalizasyon hedefi), LRA 2,5 LU → dinamik aralık dar, güçlü sıkıştırma; tepe −0,9 dBFS.
- Sonuç: üretim hedefi olarak "−14 LUFS, kuru ses, sıkı kurgu" kopyalanabilir.

## 3. Cümle yapısı

- 252 cümle; ortalama 11,6 kelime, medyan 11; p10–p90 = 6–18; %27'si ≤8 kelime, yalnızca %1,2'si ≥25 kelime; en uzun 26.
- Kısa-sert cümleler ("It was the day you were born."), ardından açıklayıcı orta uzunlukta cümle; paragraf sonunda kısa bir kanca.
- "You/your" 175 kez (2.919 kelimenin ~%6'sı): ikinci tekil şahısta anlatım. Soru işareti yalnızca 4 yerde.

## 4. Hikâye anlatım teknikleri (transkriptten)

1. **Paradoksla açılış:** "hayatının en tehlikeli günü zaten yaşandı ve hiçbirini hatırlamıyorsun".
2. **Yanlış inanışı çürütme:** "30'da ölürlerdi" → "bu bir ortalama".
3. **Üç "söz" (open loop):** 0:40 civarında "tam şu yaştasın" vaadi; ardından 19–20, 33, 50–60 yaş olarak üç kez ödeme (476 sn, 579–593 sn, 682–709 sn).
4. **Kontrol noktası yapısı:** "ilk kontrol noktası, ikinci, üçüncü, kimsenin geçemediği son".
5. **Geri çağırma:** "Remember that" 8 kez; ayak izi hikâyesi iki parçaya bölünüp (135–171 sn ve 340–360 sn) geri dönüyor.
6. **Bookend:** açılış cümlesi (en tehlikeli gün) kapanışta (757–766 sn) birebir tekrar ediliyor, anlamı dönüşmüş olarak.
7. **Doğrudan izleyici sorusu:** "Take a guess" ardından beklenmedik veri (5 yaşında yiyecek bulan Hadza çocukları).
8. **Karmaşık konuyu basitleştirme:** büyükanne hipotezi tek bir saha anlatımı (kimin yiyecek getirdiği tartıldı) + tek sonuç cümlesi; istatistik "ortalama aşağı çekildi" benzetmesi ile.
9. **Duygusal zirve:** 78.000 yıllık çocuk mezarı, "başı yumuşak bir şeyin üzerinde" ayrıntısıyla.
10. **Mizah:** kısa, kuru karşılaştırma ("kız arkadaşının ailesinin faturasını ödemek"). Çoğunlukla görsel mizah (komik karakter ifadeleri) taşıyor, metin ağırbaşlı.

## 5. Sponsor entegrasyonu (öğrenilecek, birebir kopyalanmayacak)

- 0:48 kısa duyuru, 3:22–4:43 ana okuma (≈80 sn, süre içinde %10,3), 12:50 kısa teşekkür. Ana okuma, hikâyenin temasına (saklanmak=güvenlik) köprü kuruyor; "şimdi atalarımıza dönelim" ile bitiyor. Bu sırada görsel mod değişiyor (beyaz zemin, sunucu çubuk adam, UI ekranı).

## 6. Müzik ve ses efektleri

Doğrulanamadı (dinleyemiyorum, spektrogramda sürekli yatak yok). **Kanıtsız iddiada bulunmuyorum.** Kendi sistemimiz için karar: kısık, tek döngülü müzik yatağı (−28/−30 LUFS civarı) + sade efekt kütüphanesi (CC0), referanstan öğrenilen "kuru ses" ilkesini koruyarak.

## 7. Türkçe için aktarım ilkeleri

- Türkçe sondan eklemeli (kaba gözlem, ölçülmedi): aynı bilgi genelde daha az ama daha uzun kelimeyle söylenir; 226 kelime/dk hedef yerine **~180–200 kelime/dk** (Türkçe) ile başla, sahne başına 6–8 kelime planla.
- Cümle başına 10–12 kelime, kısa-uzun dönüşümlü.
- "Sen" hitabı (ikinci tekil) aynen korunabilir.
- Üç aşamalı söz–ödeme yapısı, bookend ve "hatırla" geri çağırması kendi senaryolarımızda yeniden kullanılabilir (kendi konularımızla).
