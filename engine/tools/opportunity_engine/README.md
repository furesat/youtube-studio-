# Fasulye Opportunity Engine

Fasulye’nin yayın fikirlerini YouTube’da yerel sorgularla araştırır. Başlangıç kataloğu Türkiye (TR/tr), Almanya (DE/de) ve ABD (US/en) için dört Fasulye konusu içerir. Katalog, raporlar ve asistan bağlantısı aynı araştırma motorunu kullanır.

## Web panelini Netlify’a bağlama

1. Bu depoyu Netlify’da **Import an existing project** ile bağla. Yayın dalı `main`. Derleme komutu ve yayın dizini depo kökündeki `netlify.toml` dosyasından gelir.
2. Netlify → Environment variables bölümünde aşağıdaki dört değişkeni **Functions** kapsamında tanımla ve yeniden deploy et.

   | Değişken | Değer |
   |---|---|
   | `FASULYE_ACCESS_TOKEN` | Panel ve kişisel MCP istemcileri için yeni bir erişim anahtarı. Örneğin `openssl rand -hex 32` ile üret. |
   | `FASULYE_GITHUB_TOKEN` | Yalnızca `furesat/youtube-studio-` deposuna erişebilen fine-grained GitHub token. Depo izni **Actions: Read and write**. |

   | `SUPABASE_URL` | `https://niihqywncuwxfxipkgte.supabase.co` |
   | `SUPABASE_SECRET_KEY` | Supabase API Keys bölümünde Netlify için oluşturulmuş ayrı `sb_secret_` anahtarı. Secret / Functions kapsamında. |

3. GitHub Actions secrets bölümüne aynı proje için **ayrı** bir `SUPABASE_SECRET_KEY` ekle. `YOUTUBE_API_KEY` GitHub’da **Settings → Secrets and variables → Actions** altında kalır. Panelde **Panel erişim anahtarı** alanına `FASULYE_ACCESS_TOKEN` değerini gir.
4. **Manuel sorgu** ile bir arama metni ve ülke/dil kodlarını gir veya **Hazır konular** sekmesinden konu ve pazar seç. Çalıştırma numarasıyla başka bir zamanda aynı raporu açabilirsin.

Panelde çalıştırma durumunu, kaynak video bağlantılarını, bağımsız puanı ve gelir senaryolarını görebilirsin. ZIP arşivi Supabase raporundan istek üzerine üretilir; GitHub Artifact kotası kullanılmaz. YouTube raporları en fazla 30 gün, bağımsız araştırma bağlamı ise geçmişte tutulur. GitHub’daki **Rapor biçimlerini doğrula** adımı, dosyaların çalıştırıcıda oluşup oluşmadığını gösterir. Yerel çalıştırma çıkışlarını 30 gün içinde sil veya güncelle.

## ChatGPT ve Claude bağlantısı

`https://NETLIFY-SITE/mcp` adresi dört araç sunar. `list_research_catalog` konu ve pazarları getirir. `start_youtube_research` bir sorgu veya seçilmiş konu ve pazarlarla araştırmayı başlatır ve çalıştırma numarası verir. `get_research_result` durumu ve hazır olduğunda video bağlantılarıyla sınırlı bir özeti okur. `list_research_history` son 50 araştırmanın bağımsız bağlamını getirir. Tam rapor için paneli kullan.

**Claude Code ve Bearer başlığı destekleyen MCP istemcileri.** `FASULYE_ACCESS_TOKEN` değerini bir ortam değişkeni olarak tanımladıktan sonra şu komutu kullanabilirsin.

```sh
claude mcp add --transport http fasulye https://NETLIFY-SITE/mcp \
  --header "Authorization: Bearer ${FASULYE_ACCESS_TOKEN}"
```

**ChatGPT web ve claude.ai için OAuth.** Kullandığın hesap veya çalışma alanında özel MCP bağlantısı açık olmalı. Netlify’da, aşağıdaki **Functions** değişkenlerini ekleyerek Auth0 gibi uyumlu bir sağlayıcıdan giriş etkinleştirilebilir. Panelin erişim anahtarıyla çalışması için bu üç değişken isteğe bağlıdır.

| Değişken | Değer |
|---|---|
| `FASULYE_OAUTH_ISSUER` | Giriş sağlayıcısının HTTPS issuer adresi, sonunda `/`. Sağlayıcı RS256 anahtarlarını `/.well-known/jwks.json` üzerinden sunmalı. |
| `FASULYE_OAUTH_RESOURCE` | Panelin tam HTTPS MCP adresi, örneğin `https://NETLIFY-SITE/mcp`. |
| `FASULYE_OAUTH_SUBJECT` | Bağlanmasına izin verdiğin tek hesabın sağlayıcıdaki `sub` kimliği. |

Sağlayıcıda API kaynak tanımlayıcısını MCP adresiyle aynı yap, RS256 imzayı ve Authorization Code + PKCE akışını kullan. Auth0’da **Resource Parameter Compatibility Profile** ayarını ve seçtiğin istemcinin desteklediği DCR veya CIMD kaydını etkinleştir. Ardından ChatGPT **Plugins → Add custom MCP server** veya Claude **Settings → Connectors → Add custom connector** bölümüne MCP adresini ekle ve OAuth ile giriş yap. Sağlayıcı yapılandırması senin hesabında yapılır. [ChatGPT özel MCP bağlantısı](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) · [Auth0 MCP kaynak ayarı](https://support.auth0.com/center/s/article/mcp-audience-error-with-auth0) · [Claude Code MCP](https://code.claude.com/docs/en/mcp)

## GitHub Actions ve yerel çalıştırma

Actions → **Fasulye Opportunity Engine** → **Run workflow**. Alanlar boşken katalog çalışır. `topics` ve `markets` alanları virgülle ayrılmış kimlikleri, `query` seçeneği ise `region` ve `language` ile manuel aramayı alır. Aynı yöntem API üzerinden de çalışır. Repo dalı birleştirildikten sonra normal çalıştırma hedefi `main` olur. Araştırma, panel veya asistan isteği de dahil olmak üzere talep üzerine başlar.

Python 3.9+ kullanılır. Ek Python paketi gerekmez. Depo kökünden çalıştır.

```sh
python3 -m engine.tools.opportunity_engine --plan
python3 -m engine.tools.opportunity_engine --topics fork,sleep --markets tr,de
python3 -m engine.tools.opportunity_engine --query 'Geschichte der Gabel' --region DE --language de
python3 -m unittest discover -s engine/tools/opportunity_engine/tests -v
npm ci
npm test
npm run build
```

Yerel canlı araştırma için `YOUTUBE_API_KEY` ortam değişkenini tanımla. `--plan` anahtarsız çalışır ve sorgu/bütçe planını gösterir. `--config /path/config.json` alternatif katalog, `--output /path/reports` ayrı bir çıktı dizini seçer. Paneli ve sunucu işlevlerini yerelde birlikte açmak için Node.js 22.18+ ile Netlify CLI üzerinden `netlify dev` kullan.

## Katalog, kota ve ölçümler

- [config.json](config.json) ülke, dil, konular, yerel sorgular ve arama sınırlarını tanımlar. Bir konu için pazara özel birden fazla sorgu eklenebilir. Anahtar kelimeler insan tarafından yerelleştirilir.
- Varsayılan plan 12 arama isteği ve istek başına en fazla 25 sonuçtur. Çalıştırma tavanları 30 arama isteği ve ayrı ayrıntı kotasında 200 birimdir. Google varsayılan olarak günlük ayrı bir arama kotası ve diğer uç noktalar için genel kota tanımlar. Ek sonuç sayfası ayrı aramadır. Aynı parametrelerle yapılan aramalar çalıştırma içinde yeniden kullanılır. Video ve kanal ayrıntıları 50’lik gruplarla alınır. Google, API projesinin başka çalıştırmalarda harcadığı kotayı da sayar. [YouTube kota dokümanı](https://developers.google.com/youtube/data/determine_quota_cost)
- **Talep göstergesi** seçilen örnekteki bilinen toplam video izlenmesidir. Kapsama karşılaştırmak için bilinen izlenmeye sahip video sayısına bak. İzlenmeler video başına herkese açık yaşam boyu toplamdır. Arama hacmi, dönem içindeki izlenmeler ve izleyici ülkesi için ayrı veri gerekir.
- **Rekabet göstergesi** örnekteki farklı video ve kanal sayılarıyla birlikte her videonun kanalına ait herkese açık abone sayısıdır. Başlık ve bağlantılar yakın konuları elle incelemeye yardımcı olur. Ülke arama sonucu erişilebilirliğini, dil ise alaka tercihini belirler. Sonuçlarda başka diller de çıkabilir. [YouTube arama dokümanı](https://developers.google.com/youtube/data/reference/rest/v3/search/list)
- Tamamlanan bir arama sıfır sonuç döndürebilir. Başarısız arama veya tanımsız sorgu için örnek sayıları boş kalır. Eksik istatistikler JSON’da `null`, CSV’de boş, panelde `—` görünür. Kısmi rapor yazılır ve araç API hatası varsa başarısız çıkış kodu verir. Örnek sonuçları sıralama ve sayfa sınırından etkilenir.

## Puan ve RPM girdileri

YouTube’un geliştirici kuralları API verilerinden özel performans puanları üretmeyi kısıtlar. Fasulye’nin 0–100 fırsat puanı bu yüzden editörün YouTube API dışından verdiği talep, rekabet ve kanal uyumu girdilerini kullanır. `reviews.<konu>.<pazar>` altına `demand`, `competition`, `channel_fit` ve girdilerin kaynağını anlatan `source` eklenir. Talep ve kanal uyumunda yüksek değer avantaj, rekabette yüksek değer daha fazla rekabet anlamına gelir. [YouTube geliştirici kuralları](https://developers.google.com/youtube/terms/developer-policies#e-handling-youtube-data-and-content)

```text
Puan = (0,40 × talep + 0,35 × (100 − rekabet) + 0,25 × kanal uyumu)
Kapsam = girilen ölçütlerin toplam ağırlığı
```

Girdilerin tümü mevcutsa denklem doğrudan uygulanır. Kapsam en az %75 ise yalnızca mevcut kalemler kullanılır ve ağırlıklı toplam kapsam değerine bölünür. Daha düşük kapsamda puan boş kalır. Puan ağırlıkları ve kapsam eşiği yapılandırılabilir.

`revenue.rpm_by_market.<pazar>.<long_form|shorts>` altına `low`, `base`, `high` ve varsayımın `source` alanını ekle. RPM, seçilen para biriminde 1.000 izlenme başına gelirdir. Senaryo tutarı `izlenme hedefi / 1.000 × RPM` ile hesaplanır. Shorts hedefi, gelir hesabına esas etkileşimli izlenmedir. İlk katalogda bağımsız puan ve RPM girdileri boş bırakılmıştır.

## Çıktılar

| Dosya | İçerik |
|---|---|
| `report.json` | Sorgu bazında durum, kota, video ayrıntıları, bağımsız puan ve gelir senaryoları |
| `opportunities.csv` | Konu/pazar satırları ve veri kapsamı |
| `videos.csv` | Her konu/pazara bağlı bulunan videolar |
| `revenue.csv` | Pazar ve format için RPM girdileri ve hedef senaryoları |
| `dashboard.html` | Arşiv açıldığında tarayıcıda çevrimdışı çalışan filtreli panel |

## Supabase entegrasyonu ve doğrulama

- Tek hedef proje: `niihqywncuwxfxipkgte`. Şema: [supabase/schema.sql](supabase/schema.sql), uygulanan migrasyon: `20261127004923`.
- `fasulye_runs` bağımsız konu, pazar, dil, ülke, editoryal değerlendirme ve RPM senaryolarını; `fasulye_reports` geçici API raporunun tamamını tutar. Tek RPC işleminde yazılır; GitHub run ID ve attempt ile yeniden çalıştırma korunur.
- RLS açık. Anon ve authenticated rollerinin tablo/RPC erişimi yok. Secret key yalnızca GitHub Actions ve Netlify Functions ortamında bulunur, frontend'e verilmez. Ayrı anahtarlar oluştur, kaynak koduna veya loglara yazma. Netlify paneli mevcut erişim anahtarı/OAuth ile korunur.
- Cron her 15 dakikada dolmak üzere olan raporları siler; okuma da `expires_at` sınırını kontrol eder. ZIP kopyalarını yerelde 30 gün dolmadan sil veya güncelle. Eski GitHub arşivleri yeni sistemde okunmaz.
- Kurulum sonrası Actions üzerinden bir manuel sorgu çalıştır. Step özetinde Supabase kayıt onayını, Supabase SQL Editor'da gerçek satırları, panelde aynı run ID ile raporu ve ZIP'i, MCP üzerinden `get_research_result` sonucunu doğrula. Canlı test yapılmadan tamamlandı kabul etme.

```sql
select run_id, collected_at, expires_at,
       (select count(*) from jsonb_object_keys(report->'videos')) as videos
from public.fasulye_reports order by collected_at desc;
```

Yerel kullanımda `--persist` isteğe bağlıdır. Geçerli `GITHUB_RUN_ID` ve sunucu secret key gerektirir. CI testleri üretim veritabanına sahte veri yazmaz.

## Opportunity Engine 2.0

- **Pazarlar:** [catalog_v2.json](catalog_v2.json), 23 dil, 36 ülke-dil pazarı, 11 kategori, 253 kategori sorgusu ve dört ortak konuda 92 yerelleştirilmiş sorgu (toplam 345). Ülke ve dil ayrı filtrelenir. Bir arama ülkesi gerçek izleyici coğrafyasını göstermez. Bilinen çatal, takvim, uyku ve lale çılgınlığı konuları seçili dillerde otomatik yerelleştirilir. Özel konular için MCP asistanı hedef dillerde doğal sorgular oluşturup `enqueue_research_batch` çağrısına verir; panelde `konu | dil | sorgu` biçimi, tek dilde virgül/satır listesi desteklenir. Bilinmeyen dilde sorgu uydurulmaz; eksik yerelleştirme açıkça bildirilir. Genel amaçlı otomatik çeviri servisi entegre değildir.
- **Kuyruk:** `fasulye_batches`, `fasulye_tasks`, `fasulye_queue_budget`, `fasulye_manual_reservations`. 30 arama/gün ortak uygulama rezervasyonu (Los Angeles günü), en fazla 10 görev/worker; üç deneme, 30 dakikalık lease, kota/bağlantı hatalarında gecikmeli yeniden deneme. Aynı gün aynı toplu istek idempotent. Günlük 30 arama, gerçek Google Cloud kotası değil; diğer istemcilerin harcamaları bilinmez. Rezervasyonlar ihtiyatlıdır ve gerçekleşmeyen çağrılar için de tutulabilir. Worker sekiz saatte bir, manuel Actions `queue=true` ile ve yeni grup eklendiğinde GitHub dispatch başarılıysa hemen çalışır. Boş kuyruk API kotası kullanmaz. 396 keşif görevi ilk günden bitmez. GitHub Actions kullanım sınırını hesabında kontrol et.
- **REST:** `GET /api/discovery-catalog` (public); `POST /api/batch?preview=1`, `POST /api/batch`, `GET /api/batch[?id=...]`, `GET /api/batch?id=...&tasks=1&offset=0`, `GET /api/quota`, `GET /api/evidence[?id=...]`, `POST /api/evidence` (mevcut bearer koruması). Eski API/ZIP akışı korunur.
- **MCP:** `list_discovery_catalog`, `preview_batch`, `enqueue_research_batch`, `get_batch_status`, `list_research_batches`, `get_queue_budget`, `get_independent_evidence`, `get_trend_series`, `save_independent_evidence`, `list_batch_tasks`, `list_report_videos` mevcut dört araca eklenir (toplam 15 araç). Asistan yeni konuları yerel dillere uyarlamalı ve kaynakları açıkça belirtmeli. Örnek: discovery modu, countries ve languages dizileri, categories: history/psychology/science. Arama örneklemi toplam YouTube video sayısı veya mutlak talep değildir.
- **Trendler:** Google Trends'in [resmi CSV dışa aktarımı](https://support.google.com/trends/answer/4365538) ile tek sorgulu zaman serisi içe aktarılır; normalize 0–100 göstergesi, mutlak arama hacmi değildir. <1 değeri sansürlenmiş olarak saklanır. Kaynağı, ülke/dili, tarihleri ve arama türünü belirt. [Alpha API](https://developers.google.com/search/apis/trends) onayı bekliyor; adapter arayüzü hazır, gerçek API çağrısı henüz yok. Ücretsiz yardımcı kaynak olarak [Trending now](https://support.google.com/trends/answer/3076011) CSV'si (ayrı sinyal) veya [Wikimedia Analytics](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/) makale ziyaretleri araştırılabilir; ikisi de YouTube arama hacmi değildir. Ücretli sağlayıcı veya resmi olmayan scraping yok.
- **RPM:** [rpm_benchmarks.json](rpm_benchmarks.json), 72 üçüncü taraf senaryo varsayımı (36 pazar × iki format). RevenueLab [ülke referansları](https://www.revenuelab.fyi/geo) ve [Shorts model tahminleri](https://www.revenuelab.fyi/youtube-shorts-revenue-by-country) (CC BY 4.0); mümkün olan ülkelerde AIR Media-Tech'in [2025 Shorts örneklem ortalamaları](https://air.io/en/monetization/what-rpm-can-you-expect-from-shorts-in-2026). Orta değer yayınlanan referans, düşük/yüksek = 0,5×/1,5× duyarlılık varsayımı (istatistiksel aralık değil). 10K, 100K, 1M, 10M varsayımsal izlenme. 72 kaynaklı girdi canlı veritabanında doğrulandı. YouTube tarafından onaylanan gelir verileri değil; hedef izleyici ülkesi varsayımıdır, arama pazarı/dil eşittir izleyici coğrafyası denmez. Girdiler düzenlenebilir, mevcut kaynaklı değerleri otomatik seed üzerine yazmaz. YouTube API izlenmelerinden rakip geliri hesaplanmaz. Gerçek arama talebi bilinmiyorsa null.
- **Bağımsız puan:** talep %20, içerik açığı %20, rekabet %15 (ters), gelir %15, maliyet %10 (ters), kültür uyumu %10, uzun vade %10. Kaynak zorunlu. Kapsam %75 altı puan yok; %90 altı yüksek güven yok. Bu, veri kapsamı etiketi, istatistiksel güven aralığı değildir. API verilerinden otomatik fırsat puanı türetilmez. Ham video karşılaştırmasında izlenme, abone, yayın tarihi, süre ve API'nin beyan ettiği dil ayrı ayrı gösterilir; dil bilgisi yoksa bilinmiyor. Konu/dil uygunluğu editör değerlendirmesidir. Otomatik semantik konu açığı ölçümü yok.
- **Veritabanı:** [supabase/](supabase/) altındaki ek SQL migrasyonları (katalog sürüm 2 dahil) mevcut tablo ve rapor saklama kurallarını korur; RLS ve yalnızca sunucu rolü. [ACCOUNT.md](supabase/ACCOUNT.md) özel depo hesap hatırlatma notudur. Anahtarları hiçbir belgeye yazma.

### Gerçek doğrulama (27.11.2026)

- V1: [45920022444](https://github.com/furesat/youtube-studio-/actions/runs/45920022444), 25 benzersiz video Supabase'e kaydedildi.
- V2 kuyruk: [45920719622](https://github.com/furesat/youtube-studio-/actions/runs/45920719622), gerçek üç pazarda 75 benzersiz video, 3/3 görev tamamlandı. Grup: `8d2ec11e-4f81-46de-95d8-0a257e5b64bb`. SQL okuma doğrulandı. Testte kullanılan geçici push tetikleyicisi kaldırıldı.
- Netlify: `studioyout` doğru repo; [ortam değişkenleri](https://app.netlify.com/projects/studioyout/configuration/env) içinde `SUPABASE_SECRET_KEY` Functions kapsamıyla ayrıca gereklidir. GitHub Secrets anahtarını buraya kaynak koduyla aktarma. Ayrı secret tercih edilir. Deploy sonrası panel erişim anahtarı ile geçmiş, grup, rapor, kota ve kanıt ekranlarının canlı okumasını kontrol et.
- Trend CSV gerçek kaynak sağlanana kadar boş; bağımsız değerlendirmeler kaynak girilene kadar boş. Test fixture'ları üretim DB'ye yazılmaz.

- [CI doğrulama 45921318678](https://github.com/furesat/youtube-studio-/actions/runs/45921318678): Python, Node testleri (CSV, RPM, batch, MCP ve DOM bağları) ve web derlemesi başarılı. Bu testler canlı panel oturumunun yerine geçmez.

## Opportunity Engine 3.0 (geliştirme dalı)

- `catalog_v3.json`: sekiz öncelikli pazarda 14 kategori, kategori ve dil başına iki doğal ifade. Varsayılan derin keşif 8 pazar × 10 kategori × 4 profil = 320 bağımsız görev: 365 gün relevance, 90 gün alternatif relevance, 30 gün viewCount, 7 gün date. Günlük 30 arama rezervasyonu korunur. Her görev bir API sayfası (en fazla 50 video); tüm YouTube envanteri değildir. Diğer 23 dilin mevcut 2.0 keşfi korunur; 3.0 profilleri bulunmayan diller açıkça eksik görünür.
- Ham API alanları: başlık, açıklamanın ilk 600 karakteri, kategori kimliği, beyan edilen ses/video dili, süre, yayın tarihi, kanal kuruluş tarihi, güncel abone ve izlenme. Alaka ve Shorts statüsü doğrulanmamışsa manuel inceleme gerekir. 3 dakikalık süre filtresi kesin Shorts tanımı değildir. Son 25 yükleme örneklemi, küçük abone sayısı açıklanmış en fazla iki kanala ait; performans derecesi yok. Veriler araştırma anına aittir, abone sayısı yayın tarihindeki sayı değildir. Arama bölgesi izleyici demografisi değildir.
- Google'ın [API politikaları](https://developers.google.com/youtube/terms/developer-policies) ve [özel türetilmiş metrik izinleri](https://developers.google.com/youtube/terms/derived-metrics-policy): rakip izlenme toplamı/dönüşüm oranı veya otomatik başarı puanı üretme. Ham veri ayrı, bağımsız kaynak girdisi ayrı. API verisi en fazla 30 gün. [Arama seçenekleri](https://developers.google.com/youtube/data/reference/rest/v3/search/list), [kota](https://developers.google.com/youtube/data/determine_quota_cost) ve [Shorts tanımı](https://support.google.com/youtube/answer/15424877).
- Talep: Google Trends CSV ve bağımsız değerlendirme mevcut; Alpha API onayı bekliyor. Google Ads [Keyword Planner API](https://developers.google.com/google-ads/api/docs/keyword-planning/overview), [historical metrics](https://developers.google.com/google-ads/api/docs/keyword-planning/generate-historical-metrics) teknik olarak mümkün fakat Google Ads hesabı/OAuth, uygun geliştirici tokenı ve kota gerekir; Google Search hacmi YouTube arama hacmi değildir. Canlı Ads entegrasyonu yapılmadı; ücretli servis kullanılmadı.
- RPM için kaynak tarihi (bilinmiyorsa null), kontrol tarihi ve kaynak türü. AIR verileri 2025 örneklemidir, 23.01.2026 yayını; RevenueLab yönlendirici modeldir ve yayın tarihi doğrulanmamışsa bilinmiyor. Kâr senaryoları yalnız bağımsız RPM ve kullanıcının sağladığı aynı para birimindeki ses/görsel/çeviri/kurgu/diğer maliyetler ile hesaplanır; vergi öncesi, garanti değil. Eksik maliyet veya farklı para birimi = bilinmiyor. API izlenmelerinden rakip kazancı türetilmez.
- Panel oturumu: mevcut `FASULYE_ACCESS_TOKEN` giriş parolası. Hatırlanan tarayıcı 90 gün; parola tarayıcı depolamasına yazılmaz. Secure, HttpOnly, SameSite=Strict imzalı cookie; `FASULYE_GITHUB_TOKEN` ile alan ayrımlı imzalama, token rotasyonu oturumları geçersiz kılar. MCP bearer erişimi korunur. Oturum kapanınca cookie silinir; stateless token için tekil sunucu tarafı iptal listesi henüz yok. Ayrı `FASULYE_ADMIN_TOKEN` (panel/GitHub tokenından farklı ve güçlü) giriş kayıtlarını korur. Login audit yalnız `SUPABASE_SECRET_KEY` Netlify Functions ortamında yapılandırıldığında çalışır. İsteğe bağlı cihaz etiketi, rastgele tarayıcı kimliği, zaman, tarayıcı ve OS; IP/parola tutulmaz, 90 gün temizliği etkin. Aynı parolayı paylaşan kişilerin gerçek kimliği doğrulanamaz. Netlify ortam değişkenleri: https://app.netlify.com/projects/studioyout/configuration/env .
- [DEVELOPMENT_REPORT.md](../../../DEVELOPMENT_REPORT.md) doğrulanan ilerlemeyi ve engelleri açıklar.

## 3.1 pazar karşılaştırması

Araştırma grubu açıldığında **Pazar ve konu karşılaştırması** bölümünde konu, ülke/dil pazarı ve yayın dönemi filtrelenebilir. Arama örneklemi, eksik alanlar, bağımsız trend/değerlendirme varlığı ve süresi dolmamış kaynak rapor ayrı gösterilir. Rapor içindeki başlık/açıklama dahil et ve hariç tut filtreleri kelime eşleşmesidir; semantik doğrulama değildir. Tek sorgu da artık en fazla 50 video ister. MCP: `compare_market_evidence`; API: `GET /api/batch?id=...&compare=1&topic=...&market=...&days=365&offset=0`. Mevcut yetkilendirme ve 30 günlük saklama sınırı korunur.

Gerçek 320 görevli kampanya: `7d1e1f6c-d5ac-4243-9e9d-66d421e20409`. İlk 10 görev [45924619213](https://github.com/furesat/youtube-studio-/actions/runs/45924619213) ile tamamlandı; 499 benzersiz video. Kalanlar zamanlanmış worker ile işlenir. Bulgular için DEVELOPMENT_REPORT.md dosyasına bakın. Bağımsız kanıt bulunmadıkça talep veya içerik açığı kararı üretilmez.

### 3.2 — Editoryal iş listesi

Panelde **Editoryal iş listesi → Yeni aday**. Her aday için ülke ve dil pazarı, o pazarda sınanacak hipotez, özgün anlatım açısı, format ve doğrulanması gereken noktalar girilir. Maliyet bilinmiyorsa alanı boş bırak. Maliyet girildiğinde tutar, para birimi ve tahmin dayanağı birlikte kaydedilir. Aynı fikri farklı pazarlarda sınamak için her pazar için ayrı aday aç.

Kaynak başına yayıncı, bağımsız HTTPS adresi, inceleme tarihi, kanıt türü ve kendi cümlelerinle bulgunun hipotezle ilişkisini kaydet. Konu bağlamı, izleyici ilgisi ve pazardaki içerik kapsamı farklı kanıt türleridir. Bir kaynak bir iddiayı destekleyebilir, zayıflatabilir veya açık bırakabilir. Editör bunu bulgu ve belirsizlik alanlarına yazar. Kaynak adresleri otomatik açılmaz veya içe aktarılmaz ve kaynakların güvenilirliği editör tarafından değerlendirilir. Taslak ve araştırma durumunda kaynak eklemek isteğe bağlıdır. Üretime hazır, üretimde veya yayınlandı durumları en az bir kaynak gerektirir. Durum ve pazar filtreleriyle listeyi daraltabilir, aday kartından düzenleyebilir veya arşivleyebilirsin.

Adaylarda YouTube API kayıtları ve bunlardan türetilen metrikler için alan veya rapordan aktarım yoktur. YouTube bağlantıları kaynak olarak kabul edilmez. Serbest metinde de API içeriğini, rakiplerin metinlerini ve API verisinden çıkarılmış değerlendirmeleri kullanma. Adaylar editoryal kayıt olarak saklanır ve arşivlenebilir. Süreli YouTube raporları ve giriş kayıtlarının mevcut temizliği devam eder. [YouTube API geliştirici politikaları](https://developers.google.com/youtube/terms/developer-policies/)

| REST | İşlem |
| --- | --- |
| `GET /api/editorial?market_id=de&status=draft&offset=0&limit=10` | Filtreler isteğe bağlıdır. Yanıt `candidates` ve `next_offset` döner. |
| `POST /api/editorial` | Yeni aday oluşturur ve `201` ile kaydı döner. |
| `PUT /api/editorial` | `{id, revision, candidate}` ile alanların tamamını günceller. Eski bir revizyon `409` döner. Güncel adayı listeden açıp düzenle. |

`candidate` alanları `title`, `market_id`, `hypothesis`, `narrative_angle`, `format` (`shorts`, `long_form`, `undecided`), `cost` (bilinmiyorsa `null`, aksi halde `{amount,currency,basis}`), `uncertainty`, `status` (`draft`, `researching`, `ready`, `in_production`, `published`, `archived`), `sources` (en çok sekiz adet `{publisher,url,checked_on,kind,finding}`, türler `demand`, `coverage`, `context`) ve `independent: true` değeridir. Aynı şema MCP araçlarında kullanılır. `list_editorial_candidates` filtreleri kabul eder, `create_editorial_candidate` adayı doğrudan alır, `update_editorial_candidate` ise REST ile aynı güncelleme zarfını alır.

REST mevcut panel oturumu veya bearer ile korunur. Tarayıcı oturumlu yazmalar aynı kaynaktan yapılır. MCP mevcut erişim kontrolünü kullanır. Yayından önce [editorial_backlog.sql](supabase/editorial_backlog.sql) migrasyonunu hedef projeye uygula. Tabloda RLS açıktır ve okuma, oluşturma ve güncelleme yalnızca sunucu rolüne verilmiştir. Ek ortam değişkeni veya dış servis gerekmez.

## 3.3 üretim brifi

Editoryal iş listesinde **Üretim brifini indir** düğmesi adayın güncel revizyonunu Markdown olarak dışa aktarır. İçerik, pazar hipotezi, format, bağımsız kaynaklar, maliyet ve eksik doğrulamalar ayrı gösterilir. Kaynak varlığı doğruluk veya talep garantisi değildir. API: `GET /api/editorial?brief=<uuid>` (yetkilendirme gerekir). MCP: `get_editorial_production_brief` (salt okuma; YouTube kotası harcamaz). Brif bir senaryo değildir; editoryal doğrulama gerekir.

## V4 security migration (draft)

Set a new independent Functions-only `FASULYE_SESSION_SECRET` (generate with `openssl rand -hex 32`; never commit it). It must differ from the panel, admin and GitHub credentials. Deploy only after checks pass and owner approval. With the new secret, existing panel/admin cookies are deliberately invalidated once; sign in again. Rotating the GitHub token then no longer rotates the session key. Rotating the panel password or session secret invalidates sessions. An unset secret preserves legacy behavior during rollout; a nonempty invalid secret fails closed. Keep the dedicated secret configured after rollout: removing it can re-enable legacy signatures until their original expiry. Logout currently clears cookies only; per-session server-side revocation is still outstanding. Do not remove the secret as a routine rollback. If reverting code, coordinate credential rotation to invalidate legacy sessions.


### Controlled research (V4 draft)
Use batch mode `controlled`, with comparison_axis `window`, `order` or `variant` (default window). An optional ISO UTC millisecond window_anchor is fixed for all queries; default is current UTC midnight. This compares publication bounds, not historical snapshots of YouTube rankings. One page of up to 50 results per query; absence of results is not absence of competition. Before enabling enqueue, apply controlled_campaigns.sql in a test environment, run full tests, upgrade every worker, obtain approval and set FASULYE_CONTROLLED_CAMPAIGNS=1 in Functions. Disable the flag to stop new controlled campaigns; drain existing ones before rolling back workers. No production migration has been applied.

### Standalone worker and atomic queue (V4 draft)
The existing queue is shared with GitHub Actions. Apply and verify `atomic_queue.sql` after existing migrations in an isolated database, then enable `FASULYE_ATOMIC_QUEUE=1` for upgraded workers. Standalone mode requires that flag, the existing server-only Supabase secret and YouTube API key. From repository root: `python3 -m engine.tools.opportunity_engine.standalone_worker --check-config`, then `--once` or `--poll-seconds 300`. Config check performs no network calls. SIGTERM/SIGINT stops new polls after the current batch returns; lease expiry recovers abandoned claims. Local IDs use reserved 16-digit 9-prefix namespace, readable in the panel without GitHub. No external service or installation performed. Legacy Actions execution remains supported with flag unset. Do not mix old workers with controlled campaigns; atomic mode only fences participating workers. Keep quota cap 30, and confirm actual Google project quotas separately. Rollback: stop standalone workers and disable flag before reverting code; leave additive functions installed until approved removal.

### Independent Wikimedia evidence (V4 draft)
After applying and verifying wikimedia_evidence.sql in an isolated database, enable FASULYE_WIKIMEDIA_EVIDENCE=1 in Functions only with owner approval. Search article candidates, manually select one, and collect at most 90 days of worldwide language-edition article views; missing days are null. The provider sends an identifying User-Agent, uses fixed hosts, and stores CC0 observations, source URL, date, method and limitations. No automatic topic relevance, national viewer inference or YouTube demand estimate. Google Trends CSV remains independent; Alpha API access is still pending. Disable the flag for rollback without deleting evidence.

### Isolated queue migrations and regression (V4 draft)
Migration order after existing queue/profile/shared budget/evidence/market evidence files: controlled_campaigns.sql, atomic_queue.sql, wikimedia_evidence.sql, queue_controls.sql. Test in a fresh disposable PostgreSQL 16 Docker container named database fasulye_test: set FASULYE_TEST_PG_CONTAINER to its container ID, run `python engine/tools/opportunity_engine/supabase/tests/run_isolated.py`. The runner refuses an existing application schema and does not use a production URL; pg_cron is omitted in fixture only. Tests exercise SQL functions, RLS/grants, atomic idempotency, cancellation, cross-batch reuse, concurrent claims and daily cap. Queue pause blocks future claims, cancellation of running work completes cooperatively, no quota refunded. Cached evidence points to original expiring report, not a new archive. Do not apply to production until reviewed and every worker is upgraded. Rollback: stop new writes/workers and disable new feature gates; keep additive columns/functions and data pending owner review.

### Queue controls and worker service examples (V4 draft)
After queue_controls.sql is reviewed and applied, set FASULYE_QUEUE_CONTROLS=1 for Functions and worker environment (Actions variable for GitHub worker). The authenticated API and MCP permit explicit pause/resume, priority, cancellation and retry, and expose actual stored heartbeats. Running cancellation is cooperative; spent reservations are not refunded. Standalone report IDs never require GitHub. See deploy/*.example for systemd and launchd examples; copy configuration outside the repo with restricted permissions and substitute absolute paths. Nothing is installed or activated by this change. Stop local services and disable flags before reverting workers. Heartbeat records are telemetry, not proof of upstream health.

Dashboard: controlled campaign selection supports preview without enqueue activation; queue management controls appear when queue-controls flag is enabled. Cached observations show original report source. Local worker reports do not link to GitHub Actions.


### Server-side session revocation (optional)
Apply `supabase/session_revocation.sql` in an approved migration, configure dedicated `FASULYE_SESSION_SECRET`, then enable `FASULYE_SESSION_REVOCATION=1` in Functions. Old sessions must log in again. Database outages reject protected cookie access; logout failure is visible and retryable. Never disable the registry after activation without owner-approved signing-key rotation; old signed cookies could otherwise become valid again. Bearer credentials remain independently authorized. Registry stores only session IDs and times; review expired-record retention separately.

### Optional shared detail budget
Apply `supabase/detail_budget.sql` before setting `FASULYE_SHARED_DETAIL_BUDGET=1` in Actions and standalone/manual environments. The existing 30 search reservations/day remain unchanged. The additional app ceiling is 6000 one-unit videos/channels/playlistItems requests per Pacific calendar day (conservative headroom under legacy 100-unit search accounting; not the project's actual Google Cloud allocation). Verify project quota in the console before activation. Each uncached attempted detail request reserves first; failed calls consume their reservation. In shared mode manual non-persist runs also need Supabase and reserve searches. Direct external clients and ungated older code are outside this ledger; coordinate rollout. No quota was increased or changed in production.
