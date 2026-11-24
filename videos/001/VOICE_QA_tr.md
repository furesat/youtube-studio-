# 001 · Ses kalite kontrolü — "Yasli Adam 3", bölüm A (L001–L019)

Dosya: `New_tts_node-6.mp3` · 94,9 sn · eleven_v4 · Ölçüm: ffmpeg silencedetect (−38 dB, ≥0,25 sn), sherpa-onnx Whisper-small (tr), RMS seviyesi.
Tahmini süre (hece) 88,3 sn → gerçek 94,9 sn (**+%7,5**). Tüm video için öngörü ≈ 403 × 1,075 ≈ **433 sn** + kurguda eklenecek duraklamalar.

## Bulgular
| # | Sorun | Kanıt | Düzeltme |
|---|---|---|---|
| 1 | **Saniyeli duraklamalar uygulanmıyor.** `[pause, 1.5 seconds]`, `[pause, 1.8 seconds]` gibi etiketler tutmuyor | 44 boşluk: min 0,27 · medyan 0,41 · **max 0,75 sn**. "kahve içiyor" öncesi istenen 0,8 sn: hiç boşluk yok (76,4–80,5 kesintisiz). Son "masaydı"dan sonra yalnızca 0,7 sn | Saniyeler TTS promptundan çıkarıldı. Kesin süreler `PAUSES_tr.json`'da, **kurgu aşamasında sessizlik olarak eklenir.** TTS'te yalnızca `[pause]` ve `[long pause]` kullanılır |
| 2 | **Fazla "…" ve duraklama: kesik, robotik ritim** | Şehir listesi: her şehirden sonra 0,52–0,63 sn (istenen 0,3) → tek tek sayma hissi. "kaybeden taraf / yasaklayan oldu" 0,27 sn bölünmüş | "…" yalnızca gerçek vurgu anında (bölüm başına en fazla 3). Liste virgülle akıyor |
| 3 | **Fısıltı ve yumuşak kısımlar çok kısık** | "dikkatli tut" −26,0 dB, "Ve şüpheleniyor" −26,3 dB; gövde −16,5 dB → **~10 dB düşüş**, müzik altında kaybolur | `[whispers]` kaldırıldı → `[lower voice]` / `[conspiratorial]` (fısıltı tonu, normal seviye). Kurguda satır bazlı seviye eşitleme |
| 4 | **"Prusya" belirsiz: "Rusya" ya da "Prussia" duyuluyor** | Whisper 3 denemede "Rusya", "Prussia" | IPA ile yazıldı: `/ˈpɾusja/` |
| 5 | **"Yıl 1511. Mekke." kopuk; "Mekke" 0,47 sn'ye sıkışmış** | Tek kelimelik cümle + iki pause etiketi | "Yıl bin beş yüz on bir. Yer: Mekke." gibi doğal cümle |
| 6 | **Her satırda etiket değişimi: ton sürekli sıfırlanıyor** | 19 satırda 30+ etiket | Etiket yalnızca duygu değiştiğinde; bölüm başına ana ton + 4–6 vurgu |
| 7 | Sözsüz etiketler (`[chuckles]`) | Transkriptte görünmez; kulakla kontrol edilmeli | Az kullanıldı (bölüm başına en fazla 1) |

Doğru çıkanlar: metnin tamamı okunmuş, kelime atlama yok. "Kansu Gavri", "Hayır Bey", "Memlük", "âlimleri" doğru okunmuş. Toplam tempo hikâye anlatımına uygun.

## Kurgu için duraklama haritası
`PAUSES_tr.json`: satır sonundaki ek sessizlik (sn). `assemble.py` sesi hizaladıktan sonra uygular. TTS'in kendi doğal boşluğu (~0,4 sn) bunun içinde sayılır.

## Take 2 — prompt v3 (ONAYLANDI) · `audio/tr/part_A.mp3` · 93,96 sn
- `[long pause]` ≈ **2,05 sn** ("neyle ilgiliydi?" sonrası), `[pause]` ≈ 0,4–1,1 sn → etiketler artık çalışıyor.
- Ritim akıcı: şehir listesi tek nefeste (3,4 sn). "Yer: Mekke" doğal.
- Seviye: "dikkatli tut" −15,8 dB (düzeldi). **"Ve şüpheleniyor" hâlâ −25 dB** → kurguda +6 dB.
- Kulakla kontrol: "yasaklayan oldu" (Whisper "yasak viyan" duydu), "çöküyor" ("çöpüyor"), Prusya IPA ile "Prussia"ya kayıyor olabilir.
