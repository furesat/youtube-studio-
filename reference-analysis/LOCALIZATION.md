# LOCALIZATION — TR öncelikli, DE ve EN hazır

## İlke: görsel ile metin ayrı katman
Çizimlerde gömülü yazı yok. Tüm kart, etiket ve grafik metinleri sahne planında dil anahtarıyla tutulur ve render sırasında yazılır (bkz. `identity/compose.py` içindeki `TXT` sözlüğü ve `06_cok_dilli.png`). Bir bölüm başka dile çevrilirken yalnızca **metin + ses + zamanlama** yeniden üretilir; varlıklar ve kompozisyon aynı kalır.

## Dil kuralları
| Konu | TR | DE | EN |
|---|---|---|---|
| Büyük harf | `i→İ`, `ı→I`: CSS/SVG'de `lang="tr"` ver veya metni elle büyük yaz | `ß` büyük harfte `SS` (fontlarda ẞ çoğu zaman yok) | — |
| Sayı biçimi | 11.600 · %40 | 11.600 · 40 % | 11,600 · 40% |
| Metin uzunluğu | temel | Testte en uzun (karşılaştırma kartında "VOR 11.600 JAHREN"; metin kartında %14 küçük punto gerekti) | TR'ye yakın |
| Konuşma hızı (tahmin) | 5,6 hece/sn | 5,0 | 4,6 |
| Hitap | "sen" | "du" | "you" |

## Uygulama kuralları
- Başlık kutusuna sığdırma: kart şablonunda üst sınır genişlik %86. Taşarsa önce punto küçülür (en çok −%15), sonra iki satıra bölünür.
- Font seçimi yalnızca TR+DE glifleri tam olan fontlardan: Shantell Sans, Playpen Sans, Mali, Baloo 2, Nunito (tam); Kalam, Patrick Hand, Caveat (yalnızca ẞ eksik). Fredoka, Gochi Hand, Delius ve Sniglet elendi (ğ/ş yok).
- Mizah çevirisi: kelime oyunları birebir çevrilmez, her dilde yerelleştirilmiş replik yazılır. Sahne süresi ses süresinden yeniden hesaplanır, bu yüzden dil başına kurgu otomatik uyar.
- Kültürel bağlam: TR versiyonunda Anadolu örnekleri öne çıkabilir; DE ve EN'de aynı sahne korunur, açıklama replikleri uyarlanır.
