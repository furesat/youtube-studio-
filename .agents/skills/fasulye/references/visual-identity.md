# BOONIE çizim ve kapak kılavuzu

## Model ve dünya

Her görsel oturumunda [dönüş sayfasını](../assets/fasulye/01_donus_sayfasi.png) ve [ifadeleri](../assets/fasulye/02_ifadeler.png) görsel girdi olarak kullan. İstenen hareket için [pozlar](../assets/fasulye/03_pozlar.png), dönem için [kostümler ve efektler](../assets/fasulye/04_kostum_efekt.png), mizah için [komik tepkiler](../assets/fasulye/05_komik_tepkiler.png) yardımcı olur.

- Baş ve gövde üstü hafif daralan tek yumurta/fasulye formu. Gövde 1,0 birim, bacak 0,27. Gövde #FFFAF0, sağ gölge #E7DFD0 ve ince tarama. Burun ve boyun çizme.
- Yüz üst üçte birde. İki büyük yuvarlak beyaz göz, ince kontur, küçük siyah bebek ve beyaz ışık noktası. Kısa ince kaş, tek çizgi ağız ve belli belirsiz şeftali yanak. Dönüşe göre üç çeyrekte uzak göz küçülür, yanda tek göz görünür, arkada yüz görünmez.
- Modern imza, tepede soru işareti gibi tek perçem ve #E4572E düğümlü atkı. Önden atkının ucu sağa düşer. Yan ve arka görünümde sarkışı dönüş sayfasından eşleştir. İnce dirsekli kollar, küçük açık renk yuvarlak eller, ince bacaklar ve siyah oval ayakkabılar.
- Kostüm bir katmandır. Dönem kostümü silueti ve yüzü korur. Kostüm panosunda tarih öncesi saç/alın bandı, arkeolog şapkası, bilim gözlüğü ve 1900 kasketi bazı imza öğelerini örter veya değiştirir. İstenen görünüm için aynı kostümün tekil referansına bak. Mevcut Kahve sahnesi atkıyı açıkça koruyorsa o sahnenin tarifini izle. Kahve bölümünün kostüm anahtarları kendi `fasulye_costumes` sözlüğündedir.
- Dünyadaki diğer insanlar da aynı fasulye anatomisini kullanır. Saç, sakal, giysi, başlık ve renk ayırt eder. Çocuk yaklaşık %60 boyda, yaşlı hafif eğik olabilir. Gerçek tarihî kişileri dönem giysileriyle yorumla. 001'in kahve koklayıcısındaki burun yalnız o sahneye yazılmış bir gag.
- BOONIE meraklı, hafif şüpheci ve sakin. Tepkiyi göz, kaş ve duruşla ver. Ter damlası, şok çizgisi, soru işareti, buhar ve benzeri efektleri anlatım ihtiyacına göre kullan.

## Mürekkep & Kiremit

| Rol | Renk |
|---|---|
| Kâğıt / mürekkep | `#F7F1E5` / `#1D1A17` |
| Atkı / kırmızı yazı, X, damga / ikincil turkuaz | `#E4572E` / `#B83A2B` / `#2A7F7A` |
| Gök / toprak / taş | `#CFE2E3`, `#EEF3EC` / `#D9B27C`, `#B98A55` / `#B9AFA2`, `#8E8478` |
| Gece / ateş / iç mekân | `#17233A`, `#2C3B57` / `#F28C28`, `#FFD166` / `#F2DCC2`, `#C99A6B` |

Değişken kalınlıkta, hafif titrek mürekkep çizgisi, düz renk, gölge tarafında ince çapraz tarama ve az sıcak kâğıt greni. Anime/chibi, 3B, gradyan, fotogerçekçilik, neon ve vektör-ikon düzlüğünden kaçın. Mekânı yatay derinlik şeritleriyle kur ve arka planı karakterden sakin tut. 16:9 sahnede ana özne orta üçte birde, geniş planda karakter kadraj yüksekliğinin %35–55'i, yakın planda baş yaklaşık %60'ı. Üst %12 ve alt %15 bantlarını yazı için sakin bırak. Mevcut kompozisyonun odak noktasını ve önceki sahnenin ışığını, eşya yönünü ve kostümünü kontrol et.

Shantell Sans 700/800 başlık, 500 etiket. Büyük harfte Türkçe `İ / I` ayrımını ve dile göre taşmayı kontrol et. Tarihî palet örneği olarak 001'de Osmanlı/Orta Doğu için kiremit, safran, lacivert, bakır ve krem, Avrupa için kahverengi ahşap, gri-mavi ve koyu yeşil kullanılır. Panolardaki A/B/C karşılaştırmalarından **A** yönünü, yazıda ise güncel kılavuzdaki #B83A2B'yi izle.

## ImageGen akışı

1. Mevcut bölümü sürdürürken `IMAGE_PROMPTS.md` içinden sahnenin tam bloğunu, `Referanslar` listesini ve `CONTINUITY` satırını al. Dönüş sayfasına ek olarak ilgili tekil PNG'yi ve belirtilen önceki onaylı sahne karelerini görsel girdi yap. Yeni sahnede kimlik, dönem kostümü, eylem, ifade, kompozisyon, kamera, arka plan, palet, hikâye işlevi ve süreklilik ver. Bir istem kendi başına uygulanabilsin.
2. Ana sahneleri mevcut akışa göre ChatGPT ImageGen ile üret. Kılavuzdaki genel stil tarifi `IMAGE_GENERATION_GUIDE.md` §4 ve `engine/tools/prompts.py` içindedir. ZIP ile çalışırken şu kısa başlangıcı sahne talimatlarıyla genişletebilirsin.

   > Hand-drawn editorial cartoon in warm ink with slightly uneven line weight, flat colors, subtle crosshatching and warm paper grain. BOONIE matches the supplied turnaround: one off-white egg-shaped head-body, round white eyes, single curled tuft and knotted terracotta scarf for the modern look. Landscape 16:9 with calm top 12% and bottom 15%. No letters, numbers, captions, logos, signatures or watermarks.

3. Tabelaları boş bırak. Repo görsel kılavuzuna göre dini yapı ve sembol çizme. Şiddeti ima düzeyinde tut. Gerçek 16:9 kadrajı kontrol et. Eski istemlerdeki 1792×1024 tam 16:9 değildir. Kırpmayı ve metin bantlarını 1920×1080 montaj önizlemesinde kontrol et.
4. Seçilecek sahne çıktısını `videos/NNN/images/NNN_Sxxx_vK.png` adıyla kaydet. Bir hata varsa çalışan öğeleri koruyup hatayı hedefleyen bir düzeltme yap, sürümü artır. `_final` kilidi varsa aracın o dosyayı seçtiğini hesaba kat. Tek tek perçem/göz/siluet, poz, atkı, ışık ve obje sürekliliğini, metinsizliği ve kadrajı kontrol et.

## YouTube kapağı

`TITLE_THUMBNAIL.md` içinde başlık, açıklama, kaynaklar, bölüm zamanları ve kapak kompozisyonunu birlikte tut. Merkezde BOONIE'nin okunabilir silueti ve tek bir hikâye nesnesi olsun. Telefonda küçültülmüş görünümde yüz, nesne ve ayrı yazı katmanı okunmalı. 001 örneği, solda fincanı tutan büyük üç çeyrek BOONIE, sağda kavuklu IV. Murad silueti ve üst sağda mühür alanı. “YASAK!” bir 001 örneğidir. 1–2 kelimelik yazı için Shantell Sans 800, kırmızı #B83A2B ve gerekirse açık kontur kullan.

Metinsiz tabanı `images/NNN_T01_v1.png` olarak sakla. Üretim planında bileşik kapak yolu `renders/thumbnail_tr.png` olarak tanımlı. İncelenen `assemble.py` T01'i birleştirmiyor. Kapak yazısını ayrı bir tasarım/kurgu katmanında yerleştir ve istenen yayın dosyasını ayrıca dışa aktar. 1280×720, bu paketin mobil önizleme ve teslim için önerdiği 16:9 boyuttur. `STATUS.json` içindeki `images.thumbnail` işareti yalnızca T01 girdisinin bulunduğunu gösterir.
