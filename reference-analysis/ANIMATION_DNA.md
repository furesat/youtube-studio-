# ANIMATION_DNA — Animasyon ve kurgu

Tüm sayılar `frac.json`/`events.json` düzeyindeki kare farkı analizinden (384×216 gri, eşik 25) ve kenar-süreklilik sınıflandırmasından geldi. Görsel kanıt: `reference_frames/motion_strips/`.

## 1. Gerçek FPS ve çözünürlük
1920×1080, 30 fps sabit. (Kaynağın özgün fps değeri bu yeniden kodlanmış dosyadan çıkarılamaz.)

## 2. Ana bulgu: ana hikâye tamamen statik görüntü + sert kesme

- Kareler arası fark: karelerin %91'i ≈ 0.
- 389 sahne; sahne sınırı olan kesmeler **tek karelik** (geçiş kareleri yok): ana hikâyede (0–207 sn ve 283–770 sn) hiç solma, itme, zoom geçişi yok.
- Sahne içinde karakter, ateş, arka plan sabit. (14,6 → 15,4 sn: eşik üstü değişen piksel = 0.)
- Ortalama sahne 1,99 sn; medyan 1,8 sn. Hız ritmi neredeyse metronom: p10–p90 = 1,3–2,8 sn.

## 3. "Hareket hissi" nasıl yaratılıyor

1. **Değişim sıklığı:** her ~1,6 sn'de bir görsel değişim (389 kesme + 96 durum değişimi / 775 sn).
2. **Aynı arka plan, farklı karakter durumu:** kesme sonrası arka plan korunup karakter pozu/ifadesi değişiyor (ör. 558,37 → 558,43 sn: aynı kamp, avcı pozu değişimi). Bu, kareyi "hareket" gibi okutuyor.
3. **Tek karelik ekleme/çıkarma:** kırmızı X (290,43→290,50 sn), "SAME BODY"→"SAME BRAIN" etiketi (16,63→16,70 sn), buzdağı suyu mavileşir (30,53→30,60 sn), konuşma balonları belirir (461,87→461,97 sn). Toplam 17 ekleme, 5 çıkarma, 74 küçük değişim (≈65'i sponsor bloğunda).
4. **Anlatımla eşleşen illüstrasyon seçimi:** ortalama 7,5 kelime/sahne; sahne değişimi cümle içindeki isim/eylem değişimine denk geliyor (bkz. SCENE_CATALOG `narration_estimated`).
5. **Ölçek değişimi** (kafa-yakın plan ↔ geniş çekim) kesmeyle sağlanıyor; zoom animasyonu yok (yalnızca 3 sahnede ölçülebilir ölçek değişimi).

## 4. Çok kareli animasyon yalnızca sponsor bloğunda

- Konum: 48,4 sn (giriş), 207,9–281,3 sn (ana sponsor), 770,6 sn (çıkış). 24 animasyonlu geçiş, 8–36 kare (0,27–1,2 sn).
- Tür: **itme/kaydırma (push/slide)** — örnek: 217,9–218,3 sn bir gazete ekranının üstten itilip yerini çubuk adam sahnesinin alması; 268,6–269,0 sn yatay itme (`motion_strips/sponsor_push_and_popin_268-279s.jpg`).
- Giriş animasyonu: UI ekran görüntüsü, "419 → 420+ DATA BROKERS" sayaç rozeti, kod kutusu, "60% OFF", garanti rozeti sırayla beliriyor (ease ile ~0,4–1 sn). Hepsi **ögelerin üst üste eklenmesi (katman ekleme)**.
- Sunucu çubuk adam sabit, yalnızca göz/ağız/kaş poz değişimi (kısa tek kare swap'ları; ör. 269,3 sn'de göz kırpma).

## 5. Katman oluşum sırası (gözlenen)

Ana hikâye: arka plan + karakterler + nesneler **tek karede** birlikte geliyor (sıralı pop-in yok). Sponsor/UI: (1) çubuk adam, (2) ekran görüntüsü, (3) rozet/etiket, (4) CTA — sırayla katman ekleme.

## 6. Karakter giriş-çıkışı

Ana hikâyede karakter girişi **yok**: sahne değişince karakter zaten orada. Karakterin sahneye girmesini "gösteren" bir animasyon yok; yeni sahne/poz = yeni giriş.

## 7. Tekrarlanan teknikler

- Bookend: açılış (0–2,4 sn hastane) ve kapanış (761–765 sn hastane) aynı arka planla.
- "Kontrol noktası": yol + tabela kartı (soru işareti → onay işareti) üç kez.
- Strike/X: kırmızı çarpı ile yokluk vurgusu.
- Bugün|50.000 yıl önce bölünmüş ekran ve ardından aynı pozda iki karakter.
- Aynı oda arka planı (modern kanepe) 8+ kez farklı poz.

## 8. İzleyici dikkatini koruyan yöntemler

1. Sahnelerin %93'ü 3 sn'den kısa (362/389); yalnızca 3 sahne ≥5 sn (en uzun 12,8 sn). Beyaz kart + büyük metin genelde 2–3 sn.
2. Kart ↔ illüstrasyon ↔ grafik dönüşümü: beyaz zemin kartı yoğun sahnelerden sonra "nefes" veriyor.
3. Beklenmedik komik görseller (ör. 34,2 sn'de baş aşağı düşen karakter).
4. Renk-dünya değişimi: gece/gündüz/iç mekân ardışıklığı.

## 9. Ses–görüntü senkronu

Sahne sınırları ASR cümle sınırlarıyla her zaman çakışmıyor; cümle içinde de sahne değişiyor. Kesin kelime-sahne senkron oranını ölçemedim: elimde kelime-düzeyi zaman damgası yok, yalnızca tahmini dağılım. Ölçülen yüksek düzey: ortalama 7,5 kelime/sahne, 252 cümle, ortalama 11,6 kelime; yani cümle başına ≈1,5 sahne.

## 10. Yerel araçlarla yeniden üretim

- Remotion: her sahne `<Sequence from durationInFrames={Math.round(sec*30)}>` içinde `<Img>` katmanları; "sert kesme" = ek geçiş yok.
- Durum değişimi: aynı `<Sequence>` içinde ikinci `<Sequence>` ile overlay (X, etiket, balon).
- Sponsor/UI şablonu: `spring()` ile ek katman girişi; push geçişi `@remotion/transitions` `slide()` (lisans: Remotion free license şartı için bkz. TOOLS_AND_COSTS).
- FFmpeg yedek: `-loop 1 -t <dur>` ile görüntüden klip, `concat` + `xfade=transition=slideleft` yalnızca sponsor segmentinde.
