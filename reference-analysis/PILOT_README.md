# PILOT — "Tarladan Önce Tapınak? — Göbeklitepe" (60 sn)

## Teslim edilenler
| Ne | Nerede |
|---|---|
| **1080p MP4 (temiz)**: TR 60,4 sn · DE 58,8 sn · EN 62,1 sn | `pilot/out/<dil>/pilot_<dil>_1080p.mp4` |
| İnceleme sürümü (altyazılı, "GEÇİCİ ZAMANLAMA" etiketli) | `pilot/out/<dil>/pilot_<dil>_inceleme_altyazili.mp4` |
| Storyboard (PDF + PNG sayfaları) | `pilot/out/<dil>/storyboard_<dil>.pdf` |
| Altyazı | `pilot/out/<dil>/pilot_<dil>.srt` |
| **Düzenlenebilir proje** | `pilot/pilot.py` (sahneler), `pilot/script.json` (3 dilde metin + kaynaklar), `pilot/scene_plan.json`, `pilot/build.py` |
| Editör zaman çizelgesi | `pilot/timeline/pilot_<dil>_fcp7.xml` (DaVinci Resolve / Premiere içe aktarım) + `.otio` |
| Katmanlar (görsel ve metin ayrı) | `pilot/layers/art/*.png`, `pilot/layers/text_tr|de|en/*_txt.png` (şeffaf) |
| Karakter | `identity/boards/fasulye/`: dönüş sayfası, 15 ifade, 16 poz, 5 kostüm, 9 efekt, komik tepkiler + 35 tekil şeffaf PNG |
| Kütüphane | `identity/boards/library/`: 30 nesne (+ tekil şeffaf PNG), 9 mekân (1920×1080) |

## Zamanlama: GEÇİCİDİR
Ses yok. Süreler `voice` katmanının **estimate** sağlayıcısıyla hece sayısından tahmin edildi (TR 5,6 hece/sn). Bu **nihai ses senkronu değildir**. Gerçek ses gelince:
1. `voice_config.json` içinde dilin `provider` alanını değiştir (ör. ücretli bir TTS adaptörü veya `external` ile stüdyo kaydı).
2. `python3 pilot/build.py tr` komutunu çalıştır. Çekim süreleri yeni ses sürelerinden yeniden hesaplanır, görseller değişmez.

## Ritim
30 çekim, ortalama ~2,0 sn (TR 2,01 · DE 1,96 · EN 2,07). Referanstaki ~2 sn başlangıç noktası olarak alındı. Anlatımın gerektirdiği yerde ritim bilerek değiştirildi:
- **Hızlı dizi:** "Tekerlek yok. Metal yok. Yazı yok." üç ardışık durum değişimi, her biri ~0,9 sn.
- **Uzun nefes:** alıntı kartı ~3 sn; kapanış gecesi ~4 sn, son 1,2 sn sessiz.

Kesmeler sert. Hareket hissini, referanstaki gibi aynı kompozisyon üzerindeki durum değişimleri veriyor: kırmızı X, kabartmaların sırayla belirmesi, ev temelinin ortaya çıkması.

## Düzenleme
- **Metin:** `script.json` (anlatım) veya `pilot.py` içindeki `TXT` (ekrandaki yazılar). Diller ayrı; DE ve EN otomatik sığdırılıyor (gerçek font ölçümü).
- **Sahne:** `pilot.py` içinde her çekim bir fonksiyon. Karakter: `F.g(x, y, ölçek, poz, ifade, kostüm, view=front|tq|side|back, flip=)`; nesne: `l.obj(ad, x, y, ölçek)`; mekân: `l.loc(ad)`; efekt: `fx(ad, x, y)`.
- **Yeniden üretim:** `python3 pilot/build.py all`, ardından `python3 pilot/export_timeline.py`.
- **Gerekenler:** Python 3, `pip install playwright pillow opentimelineio otio-fcp-adapter`, Chrome, FFmpeg. Chrome yolu otomatik bulunur; gerekirse `CHROME_PATH` ortam değişkeniyle verilir.

## Doğrulanan gerçekler ve kaynaklar
Tüm kaynaklar `script.json` → `sources` içinde.
- Radyokarbon tarihi: en eski yapılar MÖ 9500–9000 → anlatımda "MÖ 9500 civarı".
- Sütunlar ~5,5–6 m'ye kadar → anlatımda dikkatli ifadeyle "beş metreyi aşan".
- Ocakta ~7 m yarım kalmış sütun (DAI).
- 1963 İstanbul–Chicago yüzey araştırması; Smithsonian'a göre taşlar Orta Çağ mezarlığına ait sanıldı. DAI ise ekibin malzemeyi Neolitik olarak tanımladığını ama önemini kaçırdığını yazıyor. Anlatım iki kaynakla da uyumlu tutuldu: "mezar taşı sanıp geçti".
- 1994: Klaus Schmidt "mezar taşlarını" T biçimli sütun olarak tanıdı.
- Yorum değişikliği: bugünkü ekip ev yapıları ve su tesisatlarına dayanarak alanı yerleşim olarak yorumluyor.
- 2018 UNESCO; 2021 itibarıyla %5'ten azı kazılmış.
- Stonehenge'den kabaca 6.000 yıl önce.
- "Yaban domuzu" bu oturumda bir kaynakla doğrulanamadığı için anlatımdan çıkarıldı; kabartmalar tilki, akbaba ve yılan.
- Zaman çizgisi (S13) yaklaşık ölçekli; bilimsel grafik değil.

## Dürüst sınırlar
- Ses, müzik ve ses efekti yok. MP4'te sessiz bir ses izi var (editör uyumluluğu için).
- Çizimler kodla üretilen vektör illüstrasyonlar (SVG → PNG). Kare kare karakter animasyonu yok; bu, referansın statik-kesme diliyle uyumlu bilinçli bir tercih.
- FCP7 XML üretildi ama **DaVinci/Premiere'de içe aktarma bu oturumda test edilmedi.**
- Karakterler gerçek kişilere benzetilmedi. "Klaus Schmidt" sahnesinde (S15) yalnızca jenerik arkeolog kostümü var.
