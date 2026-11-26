# EDITING_KDENLIVE — düzenlenebilir proje

Kullanıcı videoyu elle düzeltmek isterse düz MP4 yerine **katmanlı Kdenlive projesi** kurulur. Kdenlive kullanıcının Mac'inde çalışır; Claude onu Kdenlive MCP araçlarıyla (`kdenlive__*`) yönetir.

## 001 projesi
- Dosya (Mac): `~/Downloads/youtube video/kahve_001_kdenlive/Kahve_001_TR.kdenlive` · kopya: `videos/001/kdenlive/Kahve_001_TR.kdenlive`
- Medya aynı klasörde: `sahneler_tr/`, `anlatim_tr_f/`, `muzik_ayarli/`, `efekt_ayarli/`, `altyazi_tr.srt`. Proje mutlak yollara bağlı: klasörü taşıma/yeniden adlandırma.
- Profil: 1920×1080, 30 fps, 402,87 sn. **v1 kurgusu** (61 sahne; 142 çekimlik v2 henüz eklenmedi).

| İz | İçerik |
|---|---|
| V1 | 61 sahne görseli (yazı katmanları gömülü), her klipte yavaş yakınlaşma (qtblend dönüşümü, giriş/çıkış dönüşümlü) |
| A1 | 61 anlatım klibi (sahne başına, kare hizalı, boşluksuz) |
| A2/A3 | 9 müzik klibi (−35,5 LUFS, iki şerit dönüşümlü; sahne bazlı kısma yok) |
| A4/A5 | 36 efekt klibi (iki şerit) |
| A6 | Ortam sesi (X08) |

## Kurulum yöntemi (tekrar kullanmak için)
1. Medyayı Linux'ta hazırla: sahne kareleri (`renders/<lang>/shots`), anlatımı sahne sınırlarından **örnek-hassas** kes (`atrim=start_sample:end_sample`), kare sınırlarına hizala (`round(cum*30)`), müzik/efekt kazançlarını dosyaya göm.
2. Zip → Mac'e gönder → aç.
3. `create_project` (1920×1080, 30 fps) → `import_folder` → `create_track` ×N.
4. Klip konumlarını **kare sınırlarından** hesapla (aksi halde 1 karelik boşluklar oluşur). `execute_batch` ile toplu `add_clip`.
5. `animate_scale` ile yavaş yakınlaşma: `zoom = max(0.03, min(0.10, 0.011 × süre))`, harita sahnesinde 0,04.
6. `save_project_as` → `validate_project`.
Asset/track kimlikleri oturuma özeldir; betikler her oturumda yeniden üretilir.
