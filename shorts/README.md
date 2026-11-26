# Shorts — Fasulye

Bu klasör kanalın **bağımsız (orijinal) Shorts** işlerini toplar. Uzun videolardan çıkan kesitler kendi video klasöründe durur (ör. `videos/001/shorts/`).

## Yapı
| Klasör / dosya | İçerik |
|---|---|
| `STRATEJI.md` | Shorts stratejisi, kararlar, kurallar |
| `arastirma/rakip_taramasi_2026-11.md` | Türkçe YouTube'da konu doygunluğu taraması |
| `fasulye-mahkemesi/` | **Seri 1: Fasulye Mahkemesi** (efsane çürütme) |
| `fasulye-mahkemesi/BOLUMLER.md` | Bölüm listesi, öncelik, durum |
| `fasulye-mahkemesi/SERI.md` | Seri formatı: kalıp, süre, kapak, karar damgası |
| `fasulye-mahkemesi/<NN>_<konu>/` | Her bölümün klasörü: `KAYNAKLAR.md`, `SENARYO.md`, `GORSEL_PROMPTLARI.md`, altyazı, kapak |
| `fikirler.md` | Diğer seri/format fikirleri (henüz başlamadı) |

## Uzun video kesitleri
- `videos/001/shorts/` — Prusya "Kahveyi koklayarak yakalayan polis" (hazır). Araç: `engine/tools/make_short.py`.

## Kurallar
- mp4 dosyaları git'e girmez (.gitignore); kapak, SRT ve metinler girer.
- Her bölümün "gerçek" kısmı senaryodan önce kaynakla doğrulanır (`KAYNAKLAR.md`).
- Rakip kanallar isimle hedef gösterilmez ("internette dolaşan…" denir).
