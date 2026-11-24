# NARRATION_GUIDE — senaryo ve anlatım

Kaynak analiz: `reference-analysis/AUDIO_DNA.md`. Referanstan **teknikler** alınır, cümleler alınmaz.

## Ses ve ton
- "Sen" diye hitap: izleyiciyi hikâyenin içine koy.
- Kuru mizah: espri cümlenin sonunda, kısa ve vurgusuz gelir. Gülme efekti yok, abartı yok.
- Ciddi anlarda (ölüm, şiddet, din) mizah geri çekilir.
- Dürüstlük: efsane ise "anlatılana göre", tartışmalıysa "bu hikâyenin ne kadarı gerçek, bilinmiyor". Kanalın imzası bu.

## Tempo
- Hedef ~125–140 kelime/dk (Türkçe). Tahmin: 5,6 hece/sn.
- Cümle 8–14 kelime. Her 3–4 cümlede bir 2–5 kelimelik vurgu cümlesi.
- Paragraf sonu = kanca (bir soru, ters köşe ya da "Ama bir sorun var.").

## Yapı kalıpları
1. **Kanca (≤30 sn):** paradoks veya şaşırtıcı iddia + "bunun nedeni sandığın şey değil".
2. **Açık döngü:** başta sorulan soru sonda cevaplanır.
3. **Kontrol noktaları:** bölümler yer/tarih başlığıyla ayrılır (beyaz kart).
4. **Geri çağırma:** girişteki bir imge kapanışta anlam değiştirerek döner.
5. **Ders:** son 20 sn'de tek cümlelik sonuç + izleyiciye dönük küçük espri.

## NARRATION.txt kuralları (ses sağlayıcısına giden metin)
- Her satır bir cümle grubu, başında kimlik: `L001|...`
- Sayılar okunacağı gibi: "1633" → "bin altı yüz otuz üç". Kısaltma yok. "IV. Murad" → "Dördüncü Murad".
- Duraksama: satır sonu = kısa nefes. `…` = uzun duraksama (≤0,6 sn).
- Yabancı isimlerin okunuşu parantezde değil, `PRONUNCIATION` bölümünde verilir.

## Çok dillilik
- DE/EN uyarlama birebir çeviri değildir. Espriler yerelleştirilir, süre ±%10 içinde tutulur.
- Almanca metin genelde %10–15 uzun çıkar. Sahne süreleri sesten yeniden hesaplanır.

## ElevenLabs v4 ses promptu kuralları (001 testinden, bkz. videos/001/VOICE_QA_tr.md)
- `[pause, N seconds]` **uygulanmıyor** (ölçülen boşluk en fazla ~0,75 sn). Kesin duraklama `PAUSES_<lang>.json` ile kurguda eklenir. Promptta yalnızca `[pause]` / `[long pause]`.
- `…` ve `[pause]` az kullanılır (bölüm başına ≤3). Fazlası kesik, robotik ritim yapar. Listeler virgülle akar.
- `[whispers]` ve `[softly]` ~10 dB kısık çıkıyor. Yerine `[lower voice]` / `[conspiratorial]` kullanılır.
- Etiket yalnızca duygu değişince yazılır. Her cümleye etiket koymak tonu sıfırlar.
- Yanlış okunan özel isimler IPA ile yazılır: Prusya `/ˈpɾusja/`, Kolschitzky `/kɔlˈʃɪtski/`.
- Tek kelimelik cümlelerden kaçınılır ("Mekke."). Bunun yerine "Yer: Mekke." gibi doğal bir cümle kurulur.
