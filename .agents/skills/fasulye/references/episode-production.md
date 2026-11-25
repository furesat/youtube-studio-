# FASULYE bölüm üretimi

BOONIE, meraklı yetişkinlere tarih ve bilimde şaşırtıcı, kaynaklı hikâyeler anlatır. Uzun bölüm hedefi 6–9 dakika. Dikey kısa kesitler istenirse 45–60 saniye hedefle ve görseli yeniden kadrajla. Ana bölümde ilk 30 saniyede cevaplanabilir soru veya paradoks, ardından 3–5 kontrol noktası, ters köşe ya da sonuç ve girişteki imgeye geri dönüş kullan. Kısa bir bölüm isteğine bu ritmi ölçekle.

## Üretim sırası ve teslimler

| Aşama | Teslim ve karar |
|---|---|
| Konu ve araştırma | `videos/NNN/RESEARCH.md`. Önce mevcut bölüm numaralarını kontrol et. Tek cümlelik tez, iddia/kaynak tablosu ve tam kaynak künyeleri yaz. |
| Senaryo | `SCRIPT.md`. Sırayla `**L001** ...` kimlikleri. Mevcut iş akışında taslağı kullanıcı incelemesine çıkar. |
| Anlatım | `NARRATION.txt`. Aynı kimliklerle `L001|...`. Ses için sayıları ve kısaltmaları aç. Zor telaffuzu ve ses yönetimi notlarını ayrıca tut. |
| Sahne planı | `SCENES.json` → `IMAGE_PROMPTS.md` ve `STORYBOARD.md`. Her sahne anlatım satırlarına bağlı. Görsel işlevi, odak, karakter, katman ve süreklilik tarifli. |
| Çizim | Gereken ana sahneleri ve T01'i üret. Türevleri kaynak sahneden, kartları motorla kur. Seçilen dosyaları ve eksikleri `STATUS.json` ile kaydet. |
| Ses ve montaj | Onaylı ses, satır hizalaması, önizleme, MP4 ve ayrı SRT. İstenirse editör zaman çizelgesi. |
| Yayına hazırlık | `TITLE_THUMBNAIL.md`, birleşik kapak, son ses üzerinden gerçek bölüm başlangıçları ve açıklama kaynakları. |
| Kapanış | İstenen çıktıları kontrol et. `STATUS.json` içindeki durumu ve bir sonraki somut adımı güncelle. Yayını kullanıcı yapar, `published` yalnız doğrulanan yayını gösterir. |

Yeni bölüm açarken 001'den dosya yapısını al. İçerik, ses, kimlik, tarih veya tamamlandı işaretini yeni bölüme taşımadan önce yeni çalışmanın verileriyle doldur. Mevcut bir bölümde önceki onayları ve dosyaları koru. Üretim aşaması tamamlandığında ilgili dosyalarla `STATUS.json` birlikte kaydedilir. Büyük ve yerel üretim dosyaları için deponun `.gitignore` kuralları uygulanır.

## Araştırma ve anlatım

- Konu seçiminde güçlü merak sorusu, en az üç güvenilir kaynak bulabilme, çizilebilirlik ve mizah potansiyelini değerlendir. Tarih, sayı, kişi, neden-sonuç, atfedilen söz ve görseldeki tarihsel iddia için ayrı kanıt ara. Birincil belge, arşiv veya araştırma varsa önce ona git. Künyeye bağlantı ve varsa sayfa/yer işareti ekle.
- 001'in örnek düzeni **belgeli**, **tartışmalı** ve **efsane** işaretleridir. Kaynaklar ayrışırsa görüşleri ve ayrışan noktayı yaz. Efsaneyi “anlatılana göre” gibi bir ifadeyle anlat ve gerekiyorsa görselde motorun damgasıyla işaretle. Destek bulamadığın ayrıntıyı çıkar veya açıkça belirsiz bırak. Bölümün başlığı ve kapağı da iddia seviyesine uysun.
- BOONIE izleyiciye “sen” diye hitap eder. Kuru espri kısa, cümlenin sonuna yakın ve sakin. Ölüm, şiddet ve din anlatılırken mizah geri çekilir. Hedef 125–140 sözcük/dakika, çoğu cümle 8–14 sözcük. Birkaç cümlede bir kısa vurgu cümlesi, bölüm sonlarında açık döngü, son 20 saniyede tek cümlelik sonuç ve küçük bir geri çağırma.
- `SCRIPT.md` yazılı biçim ve altyazı kaynağıdır. `NARRATION.txt` ses için doğal okunuştur. Örneğin senaryodaki “IV. Murad, 1633” ses metninde “Dördüncü Murad, bin altı yüz otuz üç” olur. TTS duygu etiketlerini ve IPA denemelerini `VOICE_PROMPT_<lang>_*.txt` gibi ses yönetimi dosyalarında tut. Yazılı senaryoya veya SRT'ye taşınmaz.
- TR asıl metindir. DE/EN istenirse `SCRIPT_de.md`, `NARRATION_de.txt` gibi dil dosyaları ve `overlay.de` / `overlay.en` kullan. Espriyi yerelleştir, süreyi gerçek sese göre tekrar hizala, kutulara sığmayı ve `İ/ı/ğ/ş/ß` gliflerini kontrol et.

## Teslim kontrolü

- **Editoryal:** Kanca sonda karşılığını buluyor. Tarihler, alıntılar, çizilen ayrıntılar ve başlık kaynaklarla tutarlı. Efsane/tartışma işaretleri ses ve ekranda anlaşılır.
- **Görsel:** BOONIE dönüş sayfasına uyuyor. Aynı mekân, kostüm ve odak ardışık sahnelerde eşleşiyor. Görsel tabanlar metinsiz. Damga, harita etiketi ve başlık yüzü veya ana nesneyi kapatmıyor.
- **Ses/SRT:** Onaylı kayıtta satır atlaması, yanlış telaffuz, ses seviyesi veya duraklama sorunu yok. SRT gerçek sesle uyumlu ve okunabilir. İsimler ve karakterler doğru. Baş ve son zamanlarla birlikte bölüm geçişleri dinlenmiş.
- **Kurgu/kapak:** Tam montajda eksik kart, kayıp ses ve istemsiz kırpma yok. Açılış ile kapanış ve uzun planlar gerçek oynatmada kontrol edilmiş. Kapak telefon boyutunda okunuyor. Çıktı adları ve durum gerçek dosyalarla eşleşiyor. Geçici önizleme, doğrulanmamış dosya veya bekleyen onayı teslimde belirt.
