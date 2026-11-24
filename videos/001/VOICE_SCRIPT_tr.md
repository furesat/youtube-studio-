# 001 · Seslendirme senaryosu (duygu + duraklama) · TR v2

**Ses:** ElevenLabs "Yasli adam 2" (`0lx1MjCizLSqpSJueqVC`), önceki deneme "Yasli adam" (`x6MH8NM5Cgf2UNidRBXE`) · **Model:** `eleven_v4`
**Hedef süre:** görsel plan 403 sn (~6:43). Duraklamalar dahil ses hedefi **~7:00–7:20**. Sahne süreleri gerçek sese göre yeniden hesaplanır.
**Karakter:** Yaşlı, bilge, kuru esprili bir hikâyeci. Bir kahvehanede, elinde fincan, torunlarına anlatır gibi. Espriyi bastırmaz, gülümseyerek söyler. Ciddi yerlerde sesini alçaltır.

## Notasyon
- `[warmly]`, `[mischievously]` … → duygu/ton etiketi. Bir sonraki etikete kadar geçerli.
- Bekleme süreleri (saniye) aşağıdaki tabloda ve `PAUSES_tr.json`da. **TTS promptunda saniye yazılmaz** (v4 uygulamıyor); kurguda sessizlik olarak eklenir. Promptta yalnızca `[pause]` / `[long pause]`.
- `…` kısa düşünme, `—` vurgu öncesi nefes. BÜYÜK HARF = tek kelime vurgu.

## Duraklama haritası (sahne geçişleriyle)
| Yer | Süre | Neden / sahne |
|---|---|---|
| L001 sonu | 0,8 sn | S001→S002, fincan, buhar |
| L003 içinde şehir adları arası | 0,3 sn × 4 | harita iğneleri tek tek düşer (S003) |
| L004 sonu | 0,8 sn | hükümdarlar ve fincan (S004) |
| L006 sonu | **1,5 sn** | bölüm geçişi → "MEKKE · 1511" kartı |
| L007 "Mekke." sonrası | 0,8 sn | kuruluş planı (S006) |
| L011 "Ve şüpheleniyor." öncesi | 0,6 sn | Hayır Bey'in yan bakışı (S010) |
| L013 "Kahve yasak." öncesi | 0,7 sn | kırmızı X damgası (S012) |
| L016 "kahve içiyor" öncesi | 0,8 sn | ironi, sultan fincanla (S014) |
| L019 "Sorun masaydı." öncesi | 0,6 sn, sonrası **1,8 sn** | masa motifi + bölüm geçişi |
| L020 sonu | 1,0 sn | İstanbul kuruluş (S017) |
| L023 "Sonuç:" sonrası | 0,5 sn | kuyruk (S019) |
| L027 sonu | **1,2 sn** | ton değişimi: Murad geliyor |
| L028 sonu | 1,0 sn | Murad'ın girişi (S024) |
| L031 "Tahmin et." sonrası | **1,2 sn** | izleyiciye cevap boşluğu → yeniçeriler (S026) |
| L034 sonu | 0,8 sn | boş sokak gerilimi (S029) |
| L036 sonu | 1,0 sn | "EFSANE?" damgası (S031) |
| L038 sonu | 0,8 sn | masa motifi tekrar (S033) |
| L041 sonu | **2,0 sn** | bölüm geçişi → "LONDRA · 1675" |
| L045 sonu | 0,8 sn | ferman (S039) |
| L049 sonu | **1,8 sn** | "10 GÜN" + bölüm geçişi → Prusya |
| L053 sonu | 0,8 sn | bira çorbası esprisi oturur |
| L056 sonu | 0,8 sn | kahve koklayıcı |
| L057 sonu | **1,8 sn** | bölüm geçişi → İsveç |
| L061 sonu | 1,0 sn | demlik cenazesi espri boşluğu |
| L063 sonu | 1,0 sn | ikizler yaşlandı |
| L065 sonu | **1,8 sn** | bölüm geçişi → Viyana |
| L068 sonu | 0,8 sn | "EFSANE" damgası |
| L069 sonu | **2,0 sn** | kapanışa geçiş |
| L072 sonu | 1,0 sn | düşünme anı |
| L074 sonu | 1,2 sn | son espri öncesi |
| L075 "Sultanlar denedi." / "Krallar denedi." | 0,6 sn + 0,6 sn | ritmik kapanış |
| Toplam | **≈ 38 sn** | |

## Ses promptu (bölümler hâlinde gönderilir)
Gönderilen tam metin: `VOICE_PROMPT_tr_A.txt` (L001–L019), `_B.txt` (L020–L041), `_C.txt` (L042–L075).
