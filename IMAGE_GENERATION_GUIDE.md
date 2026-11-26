# IMAGE_GENERATION_GUIDE — ChatGPT ImageGen protokolü

Bu dosya, görsel üreten oturum (ChatGPT) için **zorunlu** talimattır.

## 0. Oturum başlangıcı
1. `AGENTS.md`, `STYLE_GUIDE.md`, `CHARACTER_BIBLE.md` dosyalarını oku.
2. İlgili videonun `videos/NNN/IMAGE_PROMPTS.md` dosyasını aç. Her sahne bloğu **tek başına kullanılabilir** tam bir prompttur.
3. Oturumun ilk mesajında karakter referanslarını yükle (kullanıcı sağlar):
   - `character-references/fasulye/01_donus_sayfasi.png` (zorunlu)
   - `character-references/fasulye/02_ifadeler.png`
   - sahnenin istediği ek referanslar (prompt bloğunda `References:` satırı)
4. `videos/NNN/STATUS.json` → `images.missing` listesindeki sahneleri sırayla üret.

## 1. Üretim kuralları
- **Format:** yatay 16:9 (1536×864 veya 1792×1024).
- **Görselde metin yok:** harf, rakam, tabela yazısı, filigran, imza yok. Tabelalar boş bırakılır.
- **Karakter tutarlılığı:** Fasulye her zaman dönüş sayfasındaki gibi. Atkı rengi, saç perçemi ve göz stili değişmez. Diğer insanlar da fasulye anatomisinde.
- **Stil:** el yapımı mürekkep konturu + düz renk + ince tarama + sıcak kâğıt dokusu. 3B, anime, fotogerçekçi değil.
- **Kompozisyon:** alt %15 ve üst %12 bandı sade bırak (metin katmanı için).
- **Süreklilik:** prompt bloğundaki `CONTINUITY:` satırına uy. `Referanslar` satırında "(süreklilik)" diye işaretli önceki sahne görsellerini de yükle (aynı mekân, ışık, kostüm).
- **Hassas içerik:** dini mekânlar ve semboller çizilmez. Şiddet ima edilir, gösterilmez (ör. kılıç kında).

## 2. Dosya isimlendirme (otomatik eşleştirme buna dayanır)
`NNN_Sxxx_vK.png` → ör. `001_S014_v1.png`
- `NNN` video numarası, `Sxxx` sahne kimliği (prompt bloğunun başlığında), `vK` deneme numarası.
- En yüksek `vK` otomatik seçilir. Belirli bir sürümü kilitlemek için `001_S014_final.png`.
- Kayıt yeri: `videos/NNN/images/`
- Eşleştirme toleransı: `S14`, `s014`, `scene14`, `sahne_14` da tanınır, ama standart ad tercih edilir.

## 3. Kalite kontrol (her görselden sonra)
- [ ] Fasulye referansla aynı mı (perçem, atkı, göz)?
- [ ] Görselde metin yok mu?
- [ ] 16:9 mu, alt-üst bantlar sade mi?
- [ ] Önceki sahneyle aynı mekân ve ışık mı?
- [ ] Stil düz ve mürekkep çizimi mi (3B gölge veya parlama yok)?
Biri bozuksa aynı promptu "keep everything, fix: …" diye düzeltme notuyla tekrar üret, `v2` olarak kaydet.

## 4. Ortak stil bloğu (her promptun içinde zaten var)
```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colors with light diagonal ink hatching on shadow sides, subtle warm paper grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no photorealism, no text, no letters, no numbers, no watermark. 16:9 landscape.
```


## 5. Ara çekimler (v2) — 30'arlı partiler
Ara çekim promptları: `videos/NNN/IMAGE_PROMPTS_v2.md` (kısa alternatif: `IMAGE_PROMPTS_v2_kisa.md`). Ana sahne görselleri repoda yoktur; küçük kopyaları `videos/NNN/images_ref/NNN_Sxxx_ref.jpg`.
ChatGPT'ye her parti için (yeni sohbette) verilecek metin:
```
GitHub'daki furesat/youtube-studio- reposunu kullanacaksın.
Önce oku: AGENTS.md, IMAGE_GENERATION_GUIDE.md, CHARACTER_BIBLE.md, videos/NNN/IMAGE_PROMPTS_v2.md
GÖREV: IMAGE_PROMPTS_v2.md'deki şu ara çekimleri üret: <30 kod>
KURALLAR:
- Her görsel için o başlığın altındaki kod bloğunu EKSİKSİZ prompt olarak kullan.
- Ana sahne referansını videos/NNN/images_ref/NNN_Sxxx_ref.jpg dosyasından al (örn. S005b → 001_S005_ref.jpg): aynı yer, ışık, renk, kostüm; kadraj belirgin farklı.
- Fasulye varsa character-references/fasulye/01_donus_sayfasi.png ve 02_ifadeler.png referans.
- Görselde hiçbir yazı/harf/rakam/logo yok. 16:9, üst/alt kenar sakin. Aynı çizim stili.
- Her görselden sonra dosya adını yaz: NNN_SxxxB_v1.png. Ana sahneyle neredeyse aynı çıkarsa veya yazı varsa yeniden üret.
```
Kapak ve kanal görselleri: `videos/NNN/youtube/kapak_promptu.txt`, `channel/kanal_gorsel_promptlari.txt` (görseller yazısız; yazıyı motor ekler).
