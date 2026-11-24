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
- **Süreklilik:** prompt bloğundaki `Continuity:` satırına uy (aynı mekân, ışık, kostüm, kamera tarafı).
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
