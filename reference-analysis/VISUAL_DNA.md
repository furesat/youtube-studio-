# VISUAL_DNA — Görsel kimlik analizi

Kanıt: `reference_frames/key_frames/*` (tam çözünürlük) ve `contact_sheets/`. HEX değerleri k-means (kare örneklemesi) ile ölçüldü; kare başvuruları parantez içinde.

## 1. Renk paletleri

**Genel (389 sahne örneği, ağırlıklı):** beyaz #FDFEFE %24,8 · tan toprak #B28C60 %13,0 · gök mavisi #AAD0DC %9,5 · kuru çim #DBB779 %7,8 · koyu toprak #946247 %7,6 · açık gök #BDE0EE %7,1 · koyu kahve #665642 %5,9 · siyah kontur #0C0A0C %5,1 · gri #C6C3BF %5,1.

**Dünya başına palet** (ölçülen baskın renkler):

| Dünya | Renkler |
|---|---|
| Savana gündüz (14,4 sn / 15,6 sn) | zemin #B28D61, gök #AED4DB, kontur #281C13, kulübe #846142, çim #DDBD7A |
| Gece ateş (10,4 sn) | gece #040B15, kaya #5E4C38 / #6C6259, ateş #FB920E |
| Hastane bookend (1,0 sn) | pastel yeşil #C5E1D4, #DBE7E8, beyaz #FDFDFD, kontur #040404 |
| Modern oturma odası (27,2 sn) | duvar #F1D4AC, kanepe/gri #7B818B, zemin #DAA874 |
| Kulübe içi (41,1 sn) | #8A6040, #714B2F, #BA9059 |
| Ofis/veri simsarı (216 sn) | gri #C9C9CA, #9B9DA1, lacivert takım #3F4049 |
| Beyaz kart | #FEFEFE %97, yazı #1F1F1F |

**Vurgu renkleri:** ateş turuncusu #FB8B28 / #E97F3F · kırmızı el yazısı etiketi #B42E34 (SAME BRAIN) · kırmızı çarpı #D34949 · beyin pembesi #F2A2A8 · kolye kırmızısı · sponsor mavisi (UI, "60% OFF", rozet) · onay işareti yeşili.

**Karakter renkleri:** kürk #936F56 / #694B38, saç #2E2520, kontur #140A07 – #190707. Yüz/kafa: neredeyse saf beyaz (gölge: kafanın altında açık gri-mavi yarım ay).

**Zemin kâğıdı:** %24 beyaz → yaklaşık #FDFEFE, saf #FFFFFF değil. Bazı beyaz kartlarda zemin üzerinde çok silik "hayalet" desen görünüyor (53. sahne civarı); sıkıştırma artefaktı olması muhtemel, bilinçli doku olduğuna dair kanıt yok.

## 2. Çizim tekniği ve çizgi kalınlığı

- **Kontur:** neredeyse siyah (#0C0A0C civarı), organik, hafif titrek; vektör düz çizgi değil. 1080p'de iskelet çizgi kalınlığı medyan ~4,4 px, p10 ~2 px, p90 ~12 px (kalın karakter konturları ve kapüşon/kafa çevresi). Çubuk adamın gövdesi/uzuvları ince; baş çevresi kalın.
- **Dolgu:** düz renk + hafif gölge (kafanın altında gri-mavi gölge; kürk üzerinde kıl dokusu kısa fırça darbeleri). Arka planlar daha "boyalı": gökyüzü gradyanı, çim darbeleri, toprak doku.
- **Stil karması:** çubuk adam (modern dünya) çıplak kontur + beyaz kafa; tarih öncesi karakterler aynı kafa formu ama saç, kürk, kolye ve doku ile zenginleştirilmiş. Bu çift katmanlı kimlik videonun görsel şakasının temeli (bugün|50.000 yıl önce kıyası).

## 3. Karakter anatomisi ve oranları (ölçüm: 15,4 sn kare, 1920×1080)

- **Modern çubuk adam:** kafa çapı ≈ 215 px, toplam boy ≈ 610 px → kafa boyun ~%35'i (yaklaşık 2,8 kafa boyu). İnce çubuk gövde, "Y" kollar, eller siyah dolu (eldiven benzeri) daireler, ayaklar çizgi.
- **Tarih öncesi karakter:** kafa genişliği ≈ 190 px, görünür boy ≈ 450 px → ~2,4 kafa boyu (daha "chibi"). Dağınık saç, kürk elbise, ince çizgi bacak/kol.
- **Yüz ifadeleri:** büyük göz (tam daire + küçük siyah göz bebeği), ince kaş, tek çizgi ağız; ifade sadece kaş eğimi + ağız + göz bebeği yönüyle ayrışıyor (şaşkın, endişeli, kurnaz sırıtma, mutlu kapalı göz, öfke). Kaş/ağız çok sade, ama göz bebeği yönü (sağ/sol/yukarı) ile bakış anlatılıyor.
- **Karakter seti:** (1) çubuk adam anlatıcı, (2) beyaz önlüklü bilim insanı kadın, (3) safari şapkalı kâşif, (4) hamile/anne/büyükanne/çocuk/erkek avcı tarih öncesi aile, (5) kapüşonlu "kötü adam" ve takım elbiseli simsar, (6) Tanzanya bölümünde kızıl toprak sahnesi: kırmızı desenli ve mor örtülü figürler, safari şapkalı araştırmacı.
- **Pozlar:** durma, oturma, koşma, mızrak atma, bebek taşıma, yatma, el kaldırma, işaret etme, baş üstü ters düşme (komik anlar). Pozlar ayrı ayrı çizilmiş, rig/iskelet yok (kareler arası poz değişimi hep sert kesme).

## 4. Perspektif ve derinlik

- Çoğu dış mekân sahnesi **yan görünüş yatay şerit**: üstte gökyüzü (~%30), ufuk çizgisi, altta zemin. Derinlik ölçek farkı ve üst üste binen katmanlarla (kulübeler arkada, ateş+karakter önde) veriliyor; gerçek 3 boyutlu perspektif yok.
- İç mekân (kulübe, oturma odası, sınıf, market): hafif tek noktalı perspektif; sınıf ve market sahnelerinde belirgin kaçış çizgileri.
- Yakın plan portre sahnelerinde karakter kadrajı %60-100 doldurur ve arka plan bulanık/boş (ör. 436,5 sn civarı hunter yakın planı, 547 sn).

## 5. Nesne yerleşimi ve ölçek

- Üç parçalı yatay yerleşim yaygın: sol = çevre (kulübe), orta = ana karakter, sağ = ateş/ikincil karakterler (15,6 sn karesi).
- Ateş halkası neredeyse her kamp sahnesinde alt orta-sağda, karakter grubunun ayakları hizasında → görsel çapa.
- Büyük sembolik nesneler (kum saati, sepet, kerte direği) beyaz zeminde ekranı %50-70 dolduruyor.

## 6. Tipografi

- **Kart başlıkları:** el yazısı, TÜM BÜYÜK HARF, ince fırça/kalem; ölçüm (98 sn "BIGGER PROBLEM" kartı): cap-height ≈ 100 px (1080p'de ekran yüksekliğinin ~%9'u), kelime aralığı geniş, harfler arası hafif açık, yatayda ekranın ~%45'ini kaplıyor, dikey olarak tam ortada.
- **Etiketler:** "TODAY | 50,000 YEARS AGO" üstte siyah ~70 px; "SAME BRAIN" altta kırmızı #B42E34, ~75 px cap-height, el yazısı, daha kalın.
- **Grafik içi:** "30", "AVG", "PEAK", "EATEN/GATHERED" el yazısı; eksen etiketleri küçük.
- **Sponsor bloğu:** logo (inkexplainer promosyon kartı) kendi sans fontunda; UI ekran görüntüleri gerçek ürün arayüzü.
- Font adı kanıtlanamaz; açık kaynak karşılık için bkz. TOOLS_AND_COSTS (Patrick Hand / Caveat / Gaegu SIL OFL tabanlı denemeler önerilir, doğrulanmamıştır).

## 7. Görsel hiyerarşi ve boşluk

- Beyaz kartlarda tek nesne/tek cümle: yoğun negatif boşluk, odak merkezde. Köşede küçük ikon (sağ üst) bölüm "bağlamı" taşır (taş, ateş, bebek, ayak izi, at).
- Sahnelerde ana karakter ekranın orta üçte birinde; ikincil karakterler yarım boy küçük, arka planda.
- Renk kontrastı sahneye göre: sıcak toprak + soğuk gök (savana), tamamen sıcak monokrom (kulübe), tamamen soğuk koyu (gece/scam), gri nötr (kurumsal tehdit).
- Soru/vurgu sembolleri: kırmızı soru işareti, kırmızı çarpı, kırmızı daire/yıldız patlaması; hepsi aynı kırmızıya yakın.

## 8. Özgün kimlik için kaçınılacaklar

Referansın çubuk adam + kürklü tarih öncesi karakter ikilemini, belirli kolye/kürk tasarımını, kendi sahne kompozisyonlarını, "SAME BRAIN" gibi birebir kartları ve sponsor tasarımını kopyalamayacağız. Bizden alınacak ilke: **iki dünyalı karakter kimliği, katmanlı tekrar kullanım, el yazısı kart sistemi, kırmızı tek vurgu rengi** gibi yöntemler; görseller, karakterler ve renk değerleri özgün olacak (bkz. PRODUCTION_PIPELINE.md §Kimlik).
