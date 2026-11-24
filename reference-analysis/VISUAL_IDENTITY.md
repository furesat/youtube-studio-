# VISUAL_IDENTITY — Özgün görsel kimlik: 3 yön karşılaştırması

Panolar `identity/boards/` klasöründe. Hepsi bu projede koddan üretildi: kendi fırça motorumuz SVG çiziyor, Chrome ile PNG'ye çevriliyor. Referans videodan hiçbir görsel, renk değeri veya karakter alınmadı. Ücretli araç, abonelik ya da görüntü modeli kullanılmadı.

| Pano | İçerik |
|---|---|
| `01_genel_bakis.png` | Üç yön yan yana: anlatıcı (3 dönem), palet, font, sahne örnekleri |
| `02_karakter_A/B/C.png` | Her aile için kostüm/dönem, ölçek, 8 ifade, 8 poz |
| `03_paletler.png` | Rol bazlı paletler, HEX değerleri, WCAG kontrast ölçümü |
| `04_tipografi.png` | TR/DE/EN başlık + etiket, ğ/ş/İ/ß testi, elenen fontlar |
| `05_sahne_karsilastirma.png` | Aynı 5 sahne × 3 yön (adil karşılaştırma) |
| `06_cok_dilli.png` | Aynı kartlar TR / DE / EN |
| `boards/scenes/*.png` | 27 adet tam çözünürlüklü 1920×1080 test sahnesi |

## Referanstan korunan teknikler (görselleri değil)
- **İki dünya mizahı:** aynı karakter iki çağda. Tanınma kafa/yüz formundan gelir, değişen yalnızca saç ve kostüm.
- **Bölünmüş karşılaştırma kartı:** BUGÜN | GEÇMİŞ, ortada "=", altta kırmızı el yazısı vurgu.
- **Beyaz metin kartı + köşe ikonu**, grafikler (sayı doğrusu + kırmızı iğne + elle çizilmiş daire), kırmızı X ile yokluk vurgusu.
- **Katmanlı yeniden kullanım:** arka plan + karakter (poz/ifade/kostüm parametre) + nesne + efekt. Her sahne bir parametre setiyle yeniden üretilebiliyor; ~2 sn'lik sert kesme ritmi buna dayanıyor.
- **Tek vurgu kırmızısı** ve sıcak kâğıt zemini.

## Özgünlük kontrolü
| Referans | Bizim |
|---|---|
| Beyaz daire kafa + çubuk gövde | A: baş-gövde tek yumurta + atkı · B: yumuşak kare kafa + gözlük + kazak · C: iri kafa + bulut saç + çan gövde |
| Kürk + kırmızı kolye | Lif/deri sargı, örgü kemer, alın bandı, toka |
| Afrika savanı | Anadolu Neolitik esinli T-sütunlu tepe (kendi çizimimiz) |
| "SAME BRAIN" | "AYNI MERAK" (aynı kalıp, kendi metnimiz) |
| Siyah dolu eldiven eller | Açık renk yuvarlak eller |

## Değerlendirme (benim görsel değerlendirmem, öznel; izleyici testi yapılmadı)

| Ölçüt | A · Mürekkep & Kiremit | B · Kobalt Defter | C · Toprak Gouache |
|---|---|---|---|
| Siluet ayırt ediciliği (küçük ekranda) | **Çok yüksek** (yumurta + atkı) | Orta (gözlük) | Yüksek (bulut saç) |
| İfade gücü | **Yüksek**: büyük gözler, beyaz yüz | Orta: küçük göz bebekleri, gözlük arkasında | Yüksek: iri kafa |
| Poz esnekliği | Yüksek | **En yüksek** (uzun uzuvlar) | Düşük: kısa kollar, el hareketi sınırlı |
| Karakter–arka plan tutarlılığı | **Yüksek** (ikisi de konturlu) | Zayıf: konturlu karakter, konturuz zemin | Yüksek |
| İki dünya şakası | **Çok net** (aynı yumurta, farklı saç) | İyi (gözlüğün yokluğu şakaya dönüşüyor) | Orta (iki dönem birbirine çok benziyor) |
| Metin kontrastı | Kiremit 3,3:1 (yalnızca büyük başlık) | Mercan 2,5:1: **metinde kullanılamaz** | Kırmızı 5,2:1, en iyisi |
| Üretim maliyeti | Düşük | **En düşük** | Orta (gouache katmanları, kalın kontur) |
| Özgün "marka hissi" | Yüksek | Düşük (jenerik açıklayıcı video) | Yüksek, sıcak, "premium" |

**Önerim: A (Mürekkep & Kiremit) temel olsun, C'den iki öğe alınsın:** sahne kırmızısı #B83A2B (kontrastı daha iyi) ve yanaklardaki sıcak allık. B'yi bırakmayı öneriyorum; karakter ile arka plan dili birbirini tutmuyor. Karar sizin. A tek ayırt edici siluet, net ifade ve düşük maliyeti birlikte sunan yön.

## Dürüst sınırlar
- Bunlar **konsept panoları**, nihai çizim değil. Karakterler yalnızca önden çiziliyor; üç-çeyrek ve yan görünüş, el yakın planı ve özel aksesuarlar henüz yok.
- Sahneler kasıtlı olarak sınırlı nesneyle kuruldu. Profesyonel bölüm başına ~15–20 sahne tipi ve zengin nesne kütüphanesi gerekecek (bkz. SCENE_CATALOG tipleri).
- B'nin tarih öncesi saçı ve C'nin kısa kolları gibi zayıflıklar panolarda görünür bırakıldı; karar vermenize yardımcı olsun diye.
- Görüntü modeli kullanılmadı. İleride arka plan zenginliği için FLUX schnell (Apache-2.0, yerel) eklenebilir. Zorunlu değil, üretimi bekletmez.

## Yeniden üretim
`identity/` içinde: `ink.py` (fırça motoru), `chars.py` (karakterler), `palettes.py`, `scenes.py`, `compose.py` (test sahneleri), `boards.py` (panolar), `render.py` (Playwright + Chrome).
```
cd identity && python3 compose.py && python3 boards.py
```
Bağımlılık: Python 3 + Playwright + Chrome/Chromium. Fontlar `identity/fonts/` içinde, SIL OFL 1.1 lisans metinleriyle birlikte. Çıktılar SVG tabanlı ve deterministik (tohumlu); 4K için `render` ölçeği artırılabilir, vektör olduğu için kalite kaybı olmaz.
