# Fasulye Opportunity Engine

Fasulye’nin yayın fikirlerini YouTube’da yerel sorgularla araştırır. Başlangıç kataloğu Türkiye (TR/tr), Almanya (DE/de) ve ABD (US/en) için dört Fasulye konusu içerir. Katalog, raporlar ve asistan bağlantısı aynı araştırma motorunu kullanır.

## Web panelini Netlify’a bağlama

1. Bu depoyu Netlify’da **Import an existing project** ile bağla. Yayın dalı `main`. Derleme komutu ve yayın dizini depo kökündeki `netlify.toml` dosyasından gelir.
2. Netlify → Environment variables bölümünde aşağıdaki iki değişkeni **Functions** kapsamında tanımla ve yeniden deploy et.

   | Değişken | Değer |
   |---|---|
   | `FASULYE_ACCESS_TOKEN` | Panel ve kişisel MCP istemcileri için yeni bir erişim anahtarı. Örneğin `openssl rand -hex 32` ile üret. |
   | `FASULYE_GITHUB_TOKEN` | Yalnızca `furesat/youtube-studio-` deposuna erişebilen fine-grained GitHub token. Depo izni **Actions: Read and write**. |

3. `YOUTUBE_API_KEY` GitHub’da **Settings → Secrets and variables → Actions** altında kalır. Panelde **Panel erişim anahtarı** alanına `FASULYE_ACCESS_TOKEN` değerini gir.
4. **Manuel sorgu** ile bir arama metni ve ülke/dil kodlarını gir veya **Hazır konular** sekmesinden konu ve pazar seç. Çalıştırma numarasıyla başka bir zamanda aynı raporu açabilirsin.

Panelde çalıştırma durumunu, kaynak video bağlantılarını, bağımsız puanı ve gelir senaryolarını görebilirsin. ZIP arşivi GitHub Actions çalıştırmasına yüklenir ve 14 gün saklanır. Arşiv yüklemesi kota nedeniyle başarısız olursa panelde çalıştırma bağlantısı ve raporun erişilemediği bilgisi görünür. GitHub’daki **Rapor biçimlerini doğrula** adımı, dosyaların çalıştırıcıda oluşup oluşmadığını gösterir. Yerel çalıştırma çıkışlarını 30 gün içinde sil veya güncelle.

## ChatGPT ve Claude bağlantısı

`https://NETLIFY-SITE/mcp` adresi üç araç sunar. `list_research_catalog` konu ve pazarları getirir. `start_youtube_research` bir sorgu veya seçilmiş konu ve pazarlarla araştırmayı başlatır ve çalıştırma numarası verir. `get_research_result` durumu ve hazır olduğunda video bağlantılarıyla sınırlı bir özeti okur. Tam rapor için paneli veya GitHub çalıştırma sayfasını kullan.

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
