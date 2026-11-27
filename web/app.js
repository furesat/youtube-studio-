"use strict";

const el = id => document.getElementById(id);
const numbers = new Intl.NumberFormat("tr-TR", { maximumFractionDigits: 2 });
const percentages = new Intl.NumberFormat("tr-TR", { style: "percent" });
const fmt = value => value == null ? "—" : numbers.format(value);
const dates = new Intl.DateTimeFormat("tr-TR", { dateStyle: "medium", timeStyle: "short" });
let active;
let report;

function node(tag, text = "") {
  const element = document.createElement(tag);
  element.textContent = text;
  return element;
}

function showStatus(message, isError = false) {
  el("status").textContent = message;
  el("status").classList.toggle("error", isError);
}

async function request(path, options = {}) {
  const { method = "GET", body, signal, binary = false } = options;
  const headers = new Headers();
  if (body) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { method, headers, body, signal, cache: "no-store", credentials:"same-origin" });
  if (!response.ok) {
    if(response.status===401 && !["/api/login","/api/admin/unlock"].includes(path)) showLogin();
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.error ?? `İşlem tamamlanamadı (HTTP ${response.status}).`);
  }
  return binary ? response.blob() : response.json();
}

function updateMode() {
  const catalog = el("search").elements.mode.value === "catalog";
  el("catalog-fields").hidden = !catalog;
  el("manual-fields").hidden = catalog;
  for (const id of ["query", "region", "language"]) el(id).disabled = catalog;
  el("start").disabled = catalog && !el("topics").querySelector("input");
}

function options(kind, entries) {
  for (const { id, label } of entries) {
    const checkbox = node("input");
    checkbox.type = "checkbox";
    checkbox.value = id;
    const field = node("label");
    field.append(checkbox, node("span", label));
    el(kind).append(field);
  }
}

async function loadCatalog() {
  try {
    const catalog = await request("/api/catalog");
    options("topics", catalog.topics);
    options("markets", catalog.markets);
    for (const [id, field] of [["regions", "region"], ["languages", "language"]]) {
      for (const { [field]: code, label } of catalog.markets) {
        const option = node("option", label);
        option.value = code;
        el(id).append(option);
      }
    }
  } catch {
    el("topics").append(node("p", "Hazır konular yüklenemedi. Manuel sorgu yazabilirsin."));
  }
  updateMode();
}

function checked(id) {
  return Array.from(el(id).querySelectorAll("input:checked"), input => input.value);
}

function showRun(id) {
  el("run-id").value = id;
  const url = new URL(location.href);
  url.searchParams.set("run", id);
  history.replaceState(null, "", url);
  const local=/^9\d{15}$/.test(id);
  if(!local)el("run-link").href = "https://github.com/furesat/youtube-studio-/actions/runs/" + id;
  el("run-link").hidden = local;
}

async function watch(id, signal) {
  showRun(id);
  for (let attempt = 0; attempt < 90 && !signal.aborted; attempt++) {
    const query = new URLSearchParams({ id });
    const run = await request("/api/research?" + query, { signal });
    if (run.status === "completed") {
      showStatus("Araştırma sona erdi. Rapor hazırlanıyor…");
      query.set("result", "report");
      try {
        const data = await request("/api/research?" + query, { signal });
        displayReport(data, id);
        showStatus(run.source==="standalone" ? "Yerel worker raporu açıldı; eksik gözlemler raporda belirtilir." : run.conclusion === "success"
          ? "Araştırma tamamlandı."
          : "Çalıştırma eksik sona erdi. Kaydedilen raporu görüntülüyorsun.", run.source!=="standalone"&&run.conclusion !== "success");
      } catch (error) {
        if (signal.aborted) return;
        throw new Error("Supabase raporu açılamadı. " + error.message + (run.source==="standalone"?" Yerel worker kaydını kontrol edin.":" Ayrıntılar GitHub Actions kaydında."));
      }
      return;
    }
    showStatus(run.status === "in_progress" ? "YouTube verileri toplanıyor…" : "Araştırma sırada…");
    await new Promise(resolve => setTimeout(resolve, 6000));
  }
  if (!signal.aborted) showStatus("Araştırma sürüyor. Çalıştırma numarasıyla durumu yeniden açabilirsin.");
}

async function supervise(operation) {
  active?.abort();
  const controller = new AbortController();
  active = controller;
  el("results").hidden = true;
  report = null;
  try {
    await operation(controller.signal);
  } catch (error) {
    if (!controller.signal.aborted) showStatus(error.message, true);
  }
}

el("search").addEventListener("change", updateMode);
el("search").addEventListener("submit", event => {
  event.preventDefault();
  const isManual = el("search").elements.mode.value === "manual";
  const body = isManual ? {
    query: el("query").value.trim(),
    region: el("region").value.trim().toUpperCase(),
    language: el("language").value.trim(),
  } : { topics: checked("topics"), markets: checked("markets") };
  navigate("search");
  el("run-link").hidden = true;
  showStatus("Araştırma başlatılıyor…");
  el("start").disabled = true;
  void supervise(async signal => {
    try {
      const run = await request("/api/research", { method: "POST", body: JSON.stringify(body), signal });
      el("start").disabled = false;
      await watch(run.id, signal);
    } finally {
      updateMode();
    }
  });
});

el("resume").addEventListener("submit", event => {
  event.preventDefault();
  const id = el("run-id").value;
  showStatus("Çalıştırma açılıyor…");
  void supervise(signal => watch(id, signal));
});

el("load-history").addEventListener("click", async () => {
  const panel = el("research-history");
  el("load-history").disabled = true;
  try {
    const rows = await request("/api/research?result=history");
    panel.replaceChildren();
    panel.hidden = false;
    if (!rows.length) panel.append(node("p", "Henüz kayıtlı araştırma yok."));
    for (const row of rows) {
      const topics = [...new Set((row.context?.topics_markets ?? []).map(item => item.topic))];
      const entry = node("div");
      const label = dates.format(new Date(row.collected_at)) + " · " + topics.join(", ");
      const button = node("button", "Raporu aç");
      button.type = "button";
      button.className = "secondary";
      const available = Date.now() - new Date(row.collected_at).getTime() < 30 * 86400000;
      button.disabled = !available;
      button.addEventListener("click", () => void supervise(signal => watch(row.run_id, signal)));
      entry.append(node("p", label), available ? button : node("p", "YouTube raporunun saklama süresi doldu."));
      panel.append(entry);
    }
  } catch (error) {
    showStatus(error.message, true);
  } finally {
    el("load-history").disabled = false;
  }
});

function addRow(id, values) {
  const tr = node("tr");
  for (const value of values) {
    const td = node("td");
    td.append(value instanceof Node ? value : String(value ?? "—"));
    tr.append(td);
  }
  el(id).append(tr);
}

function detailFor(row) {
  const details = node("details");
  details.append(node("summary", "Aç"));
  for (const query of row.queries) {
    const suffix = query.error ? ` · ${query.error}` : query.has_more ? " · Daha fazla sonuç var" : "";
    details.append(node("p", `${query.query} · ${query.lookback_days??365} gün · ${query.order??"relevance"} · ${query.pages} sayfa${suffix}`));
  }
  if (row.video_ids.length === 0) return details;
  const list = node("ul");
  for (const id of row.video_ids) {
    const video = report.videos[id];
    const link = node("a", video.title ?? id);
    link.href = "https://www.youtube.com/watch?v=" + encodeURIComponent(id);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    const item = node("li");
    item.append(link, ` · ${video.channel_title ?? "—"} · ${fmt(video.views)} izlenme · ${fmt(video.subscribers)} abone · ${video.duration ?? "süre bilinmiyor"} · ${video.audio_language ?? video.default_language ?? "dil bilinmiyor"}`);
    list.append(item);
  }
  details.append(list);
  return details;
}

function filterOptions(target, entries) {
  const select = el(target);
  const all = node("option", "Tümü");
  all.value = "";
  select.replaceChildren(all);
  for (const [id, label] of entries) {
    const option = node("option", label);
    option.value = id;
    select.append(option);
  }
}

function displayReport(data, id) {
  report = data;
  el("download").dataset.runId = id;
  const markets = new Map(data.opportunities.map(row => [row.market_id, row.market]));
  const topics = new Map(data.opportunities.map(row => [row.topic_id, row.topic]));
  navigate("results");
  const detailErrors = Object.values(data.detail_errors).flat();
  el("report-meta").textContent = dates.format(new Date(data.collected_at)) + " · "
    + data.quota.successes.search + "/" + data.quota.attempts.search + " arama başarılı"
    + (detailErrors.length ? " · Eksik ayrıntılar: " + [...new Set(detailErrors)].join(", ") : "");
  filterOptions("topic-filter", topics);
  filterOptions("market-filter", markets);
  const declared=[...new Set(Object.values(data.videos).map(v=>v.audio_language??v.default_language??"unknown"))].sort();
  filterOptions("video-declared-language",declared.map(l=>[l,l==="unknown"?"Bilinmiyor":(batchCatalog?.languages[l]??l)]));
  el("video-include").value="";el("video-exclude").value="";
  renderRows();
  renderChannels(data.channel_samples??[]);
}

function renderRows() {
  const statuses = { complete: "Tamamlandı", no_query: "Sorgu yok", partial: "Kısmi", failed: "Başarısız" };
  const rows = report.opportunities.filter(row =>
    (!el("topic-filter").value || row.topic_id === el("topic-filter").value) &&
    (!el("market-filter").value || row.market_id === el("market-filter").value));
  renderComparison(rows);
  for (const id of ["observations", "reviews", "revenue"]) el(id).replaceChildren();
  for (const row of rows) {
    const label = `${row.topic} / ${row.market}`;
    const views = `${row.lookback_days??365} gün / ${row.search_order??"relevance"}`;
    addRow("observations", [label, statuses[row.search_status],
      `${fmt(row.sample_video_count)} / ${fmt(row.sample_channel_count)}`, views,
      row.queries.length ? detailFor(row) : "—"]);
    addRow("reviews", [label, fmt(row.review.score), percentages.format(row.review.coverage), row.review.source]);
  }
  if (!rows.length) {
    addRow("observations", ["Bu filtrelerle eşleşme yok."]);
    addRow("reviews", ["Bu filtrelerle eşleşme yok."]);
    addRow("revenue", ["Bu filtrelerle eşleşme yok."]);
  }
  for (const [id, label] of new Map(rows.map(row => [row.market_id, row.market]))) {
    for (const item of report.revenue_by_market[id]) {
      const format = item.format === "shorts" ? "Shorts" : "Uzun video";
      addRow("revenue", [label + " / " + format, fmt(item.views),
        ...["low", "base", "high"].map(band => item[band] == null ? "—" : fmt(item[band]) + " " + item.currency),
        item.rpm?.source ?? "RPM girilmedi"]);
    }
  }
}

for (const id of ["topic-filter", "market-filter"]) el(id).addEventListener("change", renderRows);

el("download").addEventListener("click", async () => {
  el("download").disabled = true;
  try {
    const id = el("download").dataset.runId;
    const blob = await request("/api/research?" + new URLSearchParams({ id, result: "zip" }), { binary: true });
    const url = URL.createObjectURL(blob);
    const link = node("a");
    link.href = url;
    link.download = "fasulye-" + id + ".zip";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (error) {
    showStatus(error.message, true);
  } finally {
    el("download").disabled = false;
  }
});

const initialRun = new URL(location.href).searchParams.get("run");
if (initialRun && /^[1-9]\d{0,15}$/.test(initialRun)) {
  showRun(initialRun);
  showStatus("Anahtarı girip Aç düğmesini seçerek bu çalıştırmayı görüntüleyebilirsin.");
}
updateMode();


let batchCatalog, batchController;
const selected = id => Array.from(el(id).selectedOptions, o => o.value);
function appendOption(id,value,label) { const opt=node("option",label);opt.value=value;el(id).append(opt); }
function flag(code) { return String.fromCodePoint(...[...code].map(c=>127397+c.charCodeAt(0))); }
async function initBatch() {
  try {
    batchCatalog = await request("/api/discovery-catalog");
    const names=new Intl.DisplayNames(["tr"],{type:"region"});
    for(const code of new Set(batchCatalog.markets.map(m=>m.region))) appendOption("batch-countries",code,flag(code)+" "+names.of(code));
    for(const [code,label] of Object.entries(batchCatalog.languages)) appendOption("batch-languages",code,label);
    for(const c of [...new Map([...batchCatalog.categories,...(batchCatalog.campaign?.categories??[])].map(c=>[c.id,c])).values()]) appendOption("batch-categories",c.id,c.label);
    el("region").replaceChildren();el("language").replaceChildren();
    for(const code of new Set(batchCatalog.markets.map(m=>m.region))) appendOption("region",code,flag(code)+" "+names.of(code));
    for(const [code,label] of Object.entries(batchCatalog.languages)) appendOption("language",code,label);
    el("region").value="TR";el("language").value="tr";
    for(const market of batchCatalog.markets) for(const id of ["trend-market","rpm-market","rpm-filter-market","review-market","cost-market","editorial-market","editorial-market-filter"]) appendOption(id,market.id,flag(market.region)+" "+market.label);
  } catch(e) { el("batch-status").textContent=e.message; }
}
function batchInput() {
  if(!batchCatalog) throw new Error("Katalog yüklenmedi.");
  const mode=el("batch-mode").value,languages=selected("batch-languages");
  const input={mode,countries:selected("batch-countries"),languages};
  if(mode==="controlled") return {...input,categories:selected("batch-categories"),comparison_axis:el("comparison-axis").value};
  if(mode!=="bulk") return {...input,categories:selected("batch-categories")};
  const topics=new Map();
  const raw=el("batch-topics").value.trim();
  const lines=raw.includes("|")?raw.split(/\r?\n/):raw.split(/[,\r\n]+/);
  for(const line of lines.map(s=>s.trim()).filter(Boolean)){
    const parts=line.split("|").map(s=>s.trim());
    if(parts.length===1){
      const normalized=parts[0].normalize("NFC").toLocaleLowerCase("tr");
      const known=batchCatalog.topics?.some(t=>[t.id,t.label,...t.aliases].some(s=>s.normalize("NFC").toLocaleLowerCase("tr")===normalized));
      if(known || languages.length!==1){if(!topics.has(parts[0]))topics.set(parts[0],{topic:parts[0],queries:{}});continue;}
      parts.push(languages[0],parts[0]);
    }
    if(parts.length!==3 || !batchCatalog.languages[parts[1]] || !parts[0] || !parts[2]) throw new Error("Her satırda konu | dil kodu | yerel sorgu gir veya tek dil seç.");
    if(!topics.has(parts[0])) topics.set(parts[0],{topic:parts[0],queries:{}});
    topics.get(parts[0]).queries[parts[1]]=parts[2];
  }
  return {...input,topics:[...topics.values()]};
}
el("batch-mode").addEventListener("change",()=>{
  const discovery=el("batch-mode").value!=="bulk";
  el("category-field").hidden=!discovery;el("bulk-field").hidden=discovery;
  el("controlled-field").hidden=el("batch-mode").value!=="controlled";
});
async function submitBatch(preview) {
  const button=el(preview?"batch-preview":"batch-submit");button.disabled=true;
  try {
    const data=await request("/api/batch"+(preview?"?preview=1":""),{method:"POST",body:JSON.stringify(batchInput())});
    el("batch-status").textContent=data.tasks+" görev · "+data.missing.length+" eksik pazar yerelleştirmesi"+(preview?" · Plan; henüz kuyruğa eklenmedi.":" · Kuyruğa kaydedildi.");
    if(preview&&data.methodology)el("batch-status").textContent+=" · Sabit yayın sınırı: "+data.methodology.anchor+" · "+data.methodology.axis;
    if(!preview) { el("batch-status").textContent += data.worker?.state==="dispatched"?" Worker başlatıldı.":" Zamanlanmış worker bekleniyor."; void watchBatch(data.id); }
  } catch(e) {el("batch-status").textContent=e.message;}
  finally {button.disabled=false;}
}
el("batch-preview").addEventListener("click",()=>void submitBatch(true));
el("batch-form").addEventListener("submit",e=>{e.preventDefault();void submitBatch(false);});
let taskBatchId,taskOffset=0,taskTotal=0;
async function loadBatchTasks(){
  if(!taskBatchId)return;
  try{const id=taskBatchId;const rows=await request("/api/batch?"+new URLSearchParams({id,tasks:"1",offset:String(taskOffset)}));if(id!==taskBatchId)return;el("batch-task-rows").replaceChildren();for(const t of rows){const actions=node("div");if(batchCatalog?.features?.queue_controls&&["queued","running","failed"].includes(t.status)){const retry=t.status==="failed";const button=node("button",retry?"Yeniden dene":"İptal");button.type="button";button.className="secondary";button.addEventListener("click",()=>void queueAction(retry?"retry_failed":"cancel",t.id));actions.append(button);}addRow("batch-task-rows",[t.topic+" / "+t.query,t.region+" / "+t.language,(t.lookback_days??365)+" gün / "+(t.search_order??"relevance"),t.status+(t.reused_at?" · önbellek":t.cancel_requested?" · iptal istendi":""),t.attempts,t.error_code,actions]);}el("batch-task-prev").disabled=taskOffset===0;el("batch-task-next").disabled=taskOffset+100>=taskTotal;}catch(e){el("batch-status").textContent=e.message;}
}
el("batch-task-details").addEventListener("toggle",()=>{if(el("batch-task-details").open)void loadBatchTasks();});
el("batch-task-prev").addEventListener("click",()=>{taskOffset=Math.max(0,taskOffset-100);void loadBatchTasks();});
el("batch-task-next").addEventListener("click",()=>{taskOffset+=100;void loadBatchTasks();});
async function watchBatch(id) {
  navigate("batch");
  taskBatchId=id;taskOffset=0;el("batch-task-details").hidden=false;
  el("queue-controls").hidden=!batchCatalog?.features?.queue_controls;
  compareBatchId=id;compareOffset=0;el("market-evidence").hidden=false;el("compare-topic").value="";el("compare-market").value="";el("compare-days").value="";if(el("market-evidence").open)void loadMarketEvidence();
  batchController?.abort();batchController=new AbortController();const {signal}=batchController;
  try {
    while(!signal.aborted){
      const b=await request("/api/batch?"+new URLSearchParams({id}),{signal});
      taskTotal=b.total;if(el("batch-task-details").open)void loadBatchTasks();
      const p=el("batch-progress");p.hidden=false;p.max=b.total||1;p.value=b.done+b.failed+(b.cancelled??0);
      el("queue-pause").disabled=!!b.paused;el("queue-resume").disabled=!b.paused;
      el("batch-status").textContent=b.label+" · "+b.done+"/"+b.total+" tamamlandı · "+b.running+" çalışıyor · "+b.queued+" sırada · "+b.failed+" başarısız"+(b.cancelled?" · "+b.cancelled+" iptal":"")+(b.paused?" · duraklatıldı":"")+(b.reused?" · "+b.reused+" tekrar kullanılan rapor":"");
      const container=el("batch-reports");container.replaceChildren();
      for(const runId of b.reports){const button=node("button","Raporu aç · "+runId);button.type="button";button.className="secondary";button.addEventListener("click",()=>void supervise(s=>watch(runId,s)));container.append(button);}
      if(b.done+b.failed+(b.cancelled??0)>=b.total) break;
      await new Promise(resolve=>setTimeout(resolve,15000));
    }
  } catch(e){if(!signal.aborted)el("batch-status").textContent=e.message;}
}
el("batch-history").addEventListener("click",async()=>{
  try{
    const rows=await request("/api/batch");const list=el("batch-list");list.replaceChildren();
    if(!rows.length)list.append(node("p","Henüz araştırma grubu yok."));
    for(const b of rows){const button=node("button",b.label+" · "+dates.format(new Date(b.created_at)));button.type="button";button.className="secondary";button.addEventListener("click",()=>void watchBatch(b.id));list.append(button);}
  }catch(e){el("batch-status").textContent=e.message;}
});
el("quota-load").addEventListener("click",async()=>{
  try{const q=await request("/api/quota");el("quota-status").textContent="Günlük sınır: "+q.daily_limit+" · "+(q.reservations.map(r=>r.day+": "+r.reserved).join(" · ")||"Rezervasyon yok")+" · "+q.scope;}catch(e){el("quota-status").textContent=e.message;}
});


let evidenceData;
const factors={demand:"İzleyici talebi",gap:"İçerik açığı",competition:"Rekabet",revenue:"Reklam geliri",cost:"Üretim maliyeti",cultural_fit:"Dil ve kültür uyumu",long_term:"Uzun vadeli potansiyel"};
for(const [key,label] of Object.entries(factors)){
  const wrap=node("div"), lab=node("label",label), input=node("input");
  lab.htmlFor=input.id="factor-"+key; input.type="number";input.min="0";input.max="100";input.step="any";
  wrap.append(lab,input);el("review-factors").append(wrap);
}
function marketLabel(id){return batchCatalog?.markets.find(m=>m.id===id)?.label??id;}
function renderComparison(rows) {
  const ids=new Set(rows.flatMap(r=>r.video_ids));
  const cap=el("video-max-subs").value;
  const period=Number(el("video-period").value),format=el("video-format").value;
  const include=el("video-include").value.trim().normalize("NFC").toLowerCase(),exclude=el("video-exclude").value.trim().normalize("NFC").toLowerCase(),language=el("video-declared-language").value;
  const matches=v=>{const raw=((v.title??"")+" "+(v.description??"")).normalize("NFC").toLowerCase();return (!include||raw.includes(include))&&(!exclude||!raw.includes(exclude))&&(!language||(v.audio_language??v.default_language??"unknown")===language);};
  const videos=[...ids].map(id=>report.videos[id]).filter(v=>v&&matches(v)&&(!cap||v.subscribers!=null&&v.subscribers<=Number(cap))&&(!period||(Date.parse(report.collected_at)-Date.parse(v.published_at)>=0&&Date.parse(report.collected_at)-Date.parse(v.published_at)<=period*86400000))&&(!format||durationGroup(v.duration)===format));
  const sort=el("video-sort").value;
  videos.sort((a,b)=>sort==="subscribers"?(a.subscribers??Infinity)-(b.subscribers??Infinity):sort==="date"?String(b.published_at??"").localeCompare(String(a.published_at??"")):(b.views??-1)-(a.views??-1));
  el("video-comparison").replaceChildren();
  for(const v of videos){
    const link=node("a",v.title??v.video_id);link.href="https://www.youtube.com/watch?v="+encodeURIComponent(v.video_id);link.target="_blank";link.rel="noopener noreferrer";
    const channel=node("a",v.channel_title??v.channel_id??"Bilinmiyor");channel.href="https://www.youtube.com/channel/"+encodeURIComponent(v.channel_id??"");channel.target="_blank";channel.rel="noopener noreferrer";
    const detail=node("details");detail.append(node("summary","İncele"),node("p",v.description??"Açıklama yok"),node("p","Kategori kodu: "+(v.category_id??"bilinmiyor")),node("p","Kanal kuruluşu: "+(v.channel_created_at?.slice(0,10)??"bilinmiyor")),node("p","Alaka: manuel inceleme gerekli. Shorts: doğrulanmadı."));
    addRow("video-comparison",[link,channel,fmt(v.views),fmt(v.subscribers),v.published_at?.slice(0,10),v.duration,v.audio_language??v.default_language??"Bilinmiyor",detail]);
  }
  if(!videos.length)addRow("video-comparison",["Eşleşen video yok."]);
}
for(const id of ["video-sort","video-max-subs","video-period","video-format","video-declared-language","video-include","video-exclude"])el(id).addEventListener("change",()=>{if(report)renderRows();});
function renderEvidence(){
  if(!evidenceData)return;
  for(const id of ["rpm-comparison","review-comparison","trend-list"])el(id).replaceChildren();
  el("trend-provider").textContent="Google Trends API: "+(evidenceData.trend_api==="configured"?"Yapılandırıldı":"Onay / erişim bekleniyor")+". Mutlak arama hacmi: bilinmiyor. CSV değerleri göreli ilgidir.";
  for(const item of evidenceData.trends){
    const button=node("button",item.topic+" · "+item.region+"/"+item.language+" · "+item.period_start+" – "+item.period_end);
    button.type="button";button.className="secondary";button.addEventListener("click",()=>void showTrend(item.id));el("trend-list").append(button);
  }
  if(!evidenceData.trends.length)el("trend-list").append(node("p","Henüz gerçek trend CSV verisi aktarılmadı."));
  const market=el("rpm-filter-market").value,format=el("rpm-filter-format").value,views=Number(el("rpm-filter-views").value);
  for(const row of evidenceData.rpm.filter(r=>(!market||r.market_id===market)&&(!format||r.format===format))){
    const s=row.scenarios.find(x=>x.views===views);if(!s)continue;
    addRow("rpm-comparison",[marketLabel(row.market_id),row.format==="shorts"?"Shorts":"Normal video",...["low","base","high"].map(k=>fmt(s[k])+" "+s.currency),s.production_cost==null?"Bilinmiyor":fmt(s.production_cost)+" "+s.currency,s.profit?["low","base","high"].map(k=>fmt(s.profit[k])+" "+s.currency).join(" / "):"Bilinmiyor",s.source+" · "+(row.source_date??"yayın tarihi bilinmiyor")+" · "+(row.source_checked_at??"doğrulama tarihi yok")+" · "+(row.reliability??"unspecified")]);
  }
  if(!el("rpm-comparison").children.length)addRow("rpm-comparison",["Kaynaklı RPM girdisi yok."]);
  for(const row of [...evidenceData.reviews].sort((a,b)=>(b.score??-1)-(a.score??-1))){
    addRow("review-comparison",[row.topic,marketLabel(row.market_id),fmt(row.score),percentages.format(row.coverage),{high:"Yüksek",medium:"Orta",low:"Düşük"}[row.coverage_band]??"Bilinmiyor",row.source]);
  }
  if(!evidenceData.reviews.length)addRow("review-comparison",["Henüz bağımsız değerlendirme yok."]);
}
async function loadEvidence(){
  try{evidenceData=await request("/api/evidence");renderEvidence();el("evidence-status").textContent="Kaynaklar güncellendi.";}
  catch(e){el("evidence-status").textContent=e.message;}
}
async function showTrend(id){
  try{
    const series=await request("/api/evidence?"+new URLSearchParams({id}));
    const box=el("trend-detail");box.replaceChildren(node("h3",series.topic),node("p",series.source));
    const wrap=node("div");wrap.className="table-scroll";const table=node("table"), body=node("tbody");
    for(const point of series.series){const row=node("tr");row.append(node("td",point.label),node("td",point.below_one?"<1":fmt(point.value)));body.append(row);}
    table.append(body);wrap.append(table);box.append(wrap);
  }catch(e){el("evidence-status").textContent=e.message;}
}
async function saveEvidence(body){
  await request("/api/evidence",{method:"POST",body:JSON.stringify(body)});await loadEvidence();
}
el("evidence-load").addEventListener("click",()=>void loadEvidence());
for(const id of ["rpm-filter-market","rpm-filter-format","rpm-filter-views"])el(id).addEventListener("change",renderEvidence);
el("trend-form").addEventListener("submit",async e=>{
  e.preventDefault();
  try{
    const market=batchCatalog?.markets.find(m=>m.id===el("trend-market").value),file=el("trend-csv").files[0];
    if(!market||!file||file.size>300000)throw new Error("Pazar ve 300 KB'dan küçük bir CSV gerekli.");
    await saveEvidence({kind:"trend",topic:el("trend-topic").value,region:market.region,language:market.language,source:el("trend-source").value,csv:await file.text()});
  }catch(error){el("evidence-status").textContent=error.message;}
});
el("rpm-form").addEventListener("submit",async e=>{
  e.preventDefault();
  try{await saveEvidence({kind:"rpm",market_id:el("rpm-market").value,format:el("rpm-format").value,currency:el("rpm-currency").value,low:Number(el("rpm-low").value),base:Number(el("rpm-base").value),high:Number(el("rpm-high").value),source:el("rpm-source").value,source_date:el("rpm-source-date").value||undefined,reliability:el("rpm-reliability").value});}
  catch(error){el("evidence-status").textContent=error.message;}
});
el("review-form").addEventListener("submit",async e=>{
  e.preventDefault();
  try{await saveEvidence({kind:"review",topic:el("review-topic").value,market_id:el("review-market").value,source:el("review-source").value,factors:Object.fromEntries(Object.keys(factors).filter(key=>el("factor-"+key).value!=="").map(key=>[key,Number(el("factor-"+key).value)]))});}
  catch(error){el("evidence-status").textContent=error.message;}
});
el("system-check").addEventListener("click",async()=>{
  const results=el("system-status");results.replaceChildren(node("p","Bağlantılar kontrol ediliyor."));
  const checks=await Promise.allSettled([request("/api/discovery-catalog"),request("/api/quota"),request("/api/research?result=history")]);
  results.replaceChildren();
  for(const [i,label] of ["Katalog","Supabase kuyruk kotası","Supabase araştırma geçmişi"].entries())results.append(node("p",label+": "+(checks[i].status==="fulfilled"?"Erişilebilir":checks[i].reason.message)));
  if(checks[0].status==="fulfilled"&&checks[0].value.features?.queue_controls){
    try{const health=await request("/api/queue");results.append(node("p","Sistem "+health.software_version+" · günlük rezervasyon "+health.reserved_today+"/"+health.daily_search_limit),node("p","Kuyruk: "+health.counts.queued+" bekleyen / "+health.counts.running+" çalışan / "+health.counts.expired_leases+" süresi dolan lease"),node("p","En eski bekleyen: "+(health.oldest_pending??"Yok")),node("p","Son rapor: "+(health.last_report??"Yok")),node("p","Son bilinen hata: "+(health.last_failure??"Bilinmiyor")));for(const w of health.workers)results.append(node("p",w.source+" · "+w.state+" · son heartbeat "+w.heartbeat_at));if(!health.workers.length)results.append(node("p","Worker heartbeat henüz kaydedilmedi."));}catch(e){results.append(node("p","Kuyruk sağlığı: "+e.message));}
  }
  if(checks[2].status==="fulfilled"&&checks[2].value.length){
    try{const id=checks[2].value[0].run_id,run=await request("/api/research?"+new URLSearchParams({id}));results.append(node("p",(run.source==="standalone"?"Yerel worker":"GitHub Actions")+" son kayıtlı çalışma: "+run.status+" / "+(run.conclusion??"bekliyor")));}
    catch(e){results.append(node("p","GitHub Actions: "+e.message));}
  }
});

let initialized=false,currentPage="search";
function showLogin(){
  active?.abort();batchController?.abort();
  clearEditorial();
  el("dashboard").hidden=true;el("account-bar").hidden=true;el("panel-footer").hidden=true;el("login-screen").hidden=false;
  el("login-status").textContent="Devam etmek için giriş yap.";
}
function navigate(page){
  currentPage=page;
  const evidence=["trend","rpm","review","system"].includes(page);
  for(const name of ["search","batch","history","editorial"])el("page-"+name).hidden=page!==name;
  el("results").hidden=page!=="results"||!report;
  el("page-evidence").hidden=!evidence;
  for(const name of ["trend","rpm","review","system"])el("evidence-"+name).hidden=page!==name;
  for(const button of document.querySelectorAll("[data-page]"))button.setAttribute("aria-current",button.dataset.page===page?"page":"false");
  el("panel-warning").hidden=true;
  if(page==="results"&&!report){el("panel-warning").hidden=false;el("panel-warning").textContent="Henüz açık rapor yok. Geçmişten bir rapor seç veya araştırma başlat.";}
  if(page==="editorial" && el("editorial-form").hidden)void loadEditorial(0);
  if(page==="history"){el("load-history").click();el("batch-history").click();}
  if(["trend","rpm","review"].includes(page))void loadEvidence();
}
for(const button of document.querySelectorAll("[data-page]"))button.addEventListener("click",()=>navigate(button.dataset.page));
el("history-slot").append(el("load-history"),el("research-history"));
el("groups-slot").append(el("batch-history"),el("batch-list"));
async function openDashboard(session){
  el("login-screen").hidden=true;el("dashboard").hidden=false;el("account-bar").hidden=false;el("panel-footer").hidden=false;
  el("admin-form").hidden=!!session.admin;
  el("audit-refresh").hidden=!session.admin;
  el("audit-status").textContent=session.admin_configured?"": "Giriş kayıtlarını açmak için Netlify'da FASULYE_ADMIN_TOKEN ayarlanmalı.";
  if(!session.audit_configured){el("audit-status").textContent+=" Supabase sunucu anahtarı eksik; giriş kaydı tutulamıyor.";}
  if(!initialized){initialized=true;await Promise.all([loadCatalog(),initBatch()]);}
  navigate("search");
  if(session.audit==="unavailable"){el("panel-warning").hidden=false;el("panel-warning").textContent="Oturum açık; giriş kaydı şu anda kaydedilemedi.";}
  if(session.admin)void loadAudit();
}
el("login-form").addEventListener("submit",async e=>{
  e.preventDefault();el("login-submit").disabled=true;
  try{
    const session=await request("/api/login",{method:"POST",body:JSON.stringify({password:el("login-password").value,remember:el("remember-device").checked,label:el("device-label").value})});
    el("login-password").value="";await openDashboard(session);
  }catch(e){el("login-status").textContent=e.message;}finally{el("login-submit").disabled=false;}
});
el("logout").addEventListener("click",async()=>{
  try{await request("/api/logout",{method:"POST"});location.reload();}catch(e){el("panel-warning").hidden=false;el("panel-warning").textContent=e.message;}
});
async function loadAudit(){
  try{
    const result=await request("/api/admin/logins");const s=result.summary;
    el("audit-metrics").replaceChildren(node("p","Son 90 gün: "+s.total_logins+" giriş · "+s.distinct_devices+" tarayıcı/cihaz · Son 24 saat: "+s.last_24h));
    el("audit-rows").replaceChildren();
    for(const entry of result.events)addRow("audit-rows",[dates.format(new Date(entry.signed_in_at)),entry.device_label||entry.device_id.slice(0,8),entry.browser+" / "+entry.platform,entry.remembered?"Evet":"Hayır"]);
    el("audit-status").textContent="En son 100 başarılı parola girişi. Cihaz kimliği kişiyi doğrulamaz.";
  }catch(e){el("audit-status").textContent=e.message;}
}
el("admin-form").addEventListener("submit",async e=>{
  e.preventDefault();
  try{await request("/api/admin/unlock",{method:"POST",body:JSON.stringify({password:el("admin-password").value})});el("admin-password").value="";el("admin-form").hidden=true;el("audit-refresh").hidden=false;await loadAudit();}
  catch(e){el("audit-status").textContent=e.message;}
});
el("audit-refresh").addEventListener("click",()=>void loadAudit());
void (async()=>{try{const session=await request("/api/session");if(session.authenticated)await openDashboard(session);else showLogin();}catch(e){el("login-status").textContent=e.message;}})();

function durationGroup(duration){
  const m=/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/.exec(duration??"");
  if(!m||!m.slice(1).some(Boolean))return "unknown";
  return Number(m[1]??0)*3600+Number(m[2]??0)*60+Number(m[3]??0)<=180?"short":"long";
}
el("priority-campaign").addEventListener("click",()=>{
  if(!batchCatalog?.campaign)return;
  el("batch-mode").value="campaign";el("batch-mode").dispatchEvent(new Event("change"));
  for(const id of ["batch-countries","batch-languages","batch-categories"])for(const option of el(id).options)option.selected=false;
  el("batch-preview").click();
});

function renderChannels(channels){
  const box=el("channel-library");box.replaceChildren();
  if(!channels.length){box.append(node("p","Bu raporda kanal yükleme örneklemi yok."));return;}
  for(const channel of channels){
    const details=node("details");const title=node("summary",(channel.channel_title??channel.channel_id)+" · "+fmt(channel.current_subscribers)+" mevcut abone");
    details.append(title,node("p","Kanal kuruluşu: "+(channel.channel_created_at?.slice(0,10)??"bilinmiyor")));
    const link=node("a","YouTube kanalını aç");link.href="https://www.youtube.com/channel/"+encodeURIComponent(channel.channel_id);link.target="_blank";link.rel="noopener noreferrer";details.append(link);
    if(channel.error)details.append(node("p","Eksik veri: "+channel.error));
    const list=node("ul");
    for(const v of channel.videos??[]){
      const item=node("li"),a=node("a",v.title??v.video_id);
      a.href="https://www.youtube.com/watch?v="+encodeURIComponent(v.video_id);a.target="_blank";a.rel="noopener noreferrer";
      item.append(a,document.createTextNode(" · "+(v.published_at?.slice(0,10)??"bilinmiyor")+" · "+fmt(v.views)+" izlenme · "+(v.duration??"süre bilinmiyor")));list.append(item);
    }
    details.append(list);box.append(details);
  }
}
const costs={voice:"Seslendirme",visuals:"Görsel üretimi",translation:"Çeviri",editing:"Kurgu",other:"Diğer"};
for(const [key,label] of Object.entries(costs)){
  const wrap=node("div"),lab=node("label",label),input=node("input");
  lab.htmlFor=input.id="cost-"+key;input.type="number";input.min="0";input.max="10000000";input.step="any";input.required=true;
  wrap.append(lab,input);el("cost-fields").append(wrap);
}
el("cost-form").addEventListener("submit",async e=>{
  e.preventDefault();
  try{await saveEvidence({kind:"cost",market_id:el("cost-market").value,format:el("cost-format").value,currency:el("cost-currency").value,source:el("cost-source").value,...Object.fromEntries(Object.keys(costs).map(k=>[k,Number(el("cost-"+k).value)]))});}
  catch(error){el("evidence-status").textContent=error.message;}
});

let compareBatchId,compareOffset=0,compareController;
async function loadMarketEvidence(){
  if(!compareBatchId)return;
  compareController?.abort();compareController=new AbortController();const {signal}=compareController;
  const query=new URLSearchParams({id:compareBatchId,compare:"1",offset:String(compareOffset)});
  for(const [key,id] of [["topic","compare-topic"],["market","compare-market"],["days","compare-days"]])if(el(id).value)query.set(key,el(id).value);
  el("compare-status").textContent="Karşılaştırma yükleniyor…";
  try{
    const data=await request("/api/batch?"+query,{signal});
    for(const [id,entries] of [["compare-topic",data.topics.map(t=>[t,t])],["compare-market",data.markets.map(m=>[m,marketLabel(m)])]]){
      const selected=el(id).value;filterOptions(id,entries);el(id).value=selected;
    }
    el("compare-rows").replaceChildren();
    for(const r of data.rows){
      const subject=node("div");subject.append(node("strong",r.topic),node("p",r.query));
      const source=(r.independent_trend_available?"Trend kaydı var":"Trend bilinmiyor")+" / "+(r.independent_review_available?"Bağımsız inceleme var":"İnceleme yok");
      let detail="Henüz veri yok";
      if(r.report_state==="expired_or_unavailable")detail="Rapor süresi dolmuş / erişilemiyor";
      if(r.report_run_id){detail=node("button","Örneklemi aç");detail.type="button";detail.className="secondary";detail.addEventListener("click",()=>void supervise(async s=>{await watch(r.report_run_id,s);if(report&&!s.aborted){el("topic-filter").value="queue-"+(r.source_task_id??r.id);renderRows();}}));}
      const count=r.sample_video_count==null?"Bilinmiyor":String(r.sample_video_count)+(r.has_more===true?" · devamı var":"");
      const missing=r.sample_video_count==null?"Bilinmiyor":"İzlenme verisi: "+(r.known_view_video_count??"?")+", abone verisi: "+(r.known_subscriber_video_count??"?")+" videoda mevcut";
      const status=({queued:"Sırada",running:"Çalışıyor",done:"Tamamlandı",failed:"Başarısız"})[r.status]??r.status;
      addRow("compare-rows",[subject,marketLabel(r.market_id),r.lookback_days+" gün / "+r.search_order+(r.window_anchor?" / "+r.window_anchor.slice(0,10):""),status+(r.reused_at?" · tekrar kullanılan rapor":"")+(r.error_code?" · "+r.error_code:""),count,missing,source,detail]);
    }
    el("compare-prev").disabled=compareOffset===0;el("compare-next").disabled=compareOffset+data.limit>=data.total;
    el("compare-status").textContent=data.total?"Görev "+(compareOffset+1)+"–"+Math.min(compareOffset+data.limit,data.total)+" / "+data.total+" · Arama hacmi bilinmiyor.":"Filtreye uyan görev yok.";
  }catch(e){if(!signal.aborted)el("compare-status").textContent=e.message;}
}
el("market-evidence").addEventListener("toggle",()=>{if(el("market-evidence").open)void loadMarketEvidence();});
el("compare-refresh").addEventListener("click",()=>void loadMarketEvidence());
for(const id of ["compare-topic","compare-market","compare-days"])el(id).addEventListener("change",()=>{compareOffset=0;void loadMarketEvidence();});
el("compare-prev").addEventListener("click",()=>{compareOffset=Math.max(0,compareOffset-50);void loadMarketEvidence();});
el("compare-next").addEventListener("click",()=>{compareOffset+=50;void loadMarketEvidence();});

const editorialStates = {
  draft: "Taslak", researching: "Araştırılıyor", ready: "Üretime hazır",
  in_production: "Üretimde", published: "Yayınlandı", archived: "Arşivlendi",
};
const editorialFormats = { undecided: "Karar verilmedi", shorts: "Shorts", long_form: "Uzun video" };
const editorialSourceKinds = { context: "Konu bağlamı", demand: "İzleyici ilgisi", coverage: "İçerik kapsamı" };
const editorialFields = {
  title: "editorial-name", market_id: "editorial-market", hypothesis: "editorial-hypothesis",
  narrative_angle: "editorial-angle", uncertainty: "editorial-uncertainty",
  format: "editorial-format", status: "editorial-state",
};
for (const [value, label] of Object.entries(editorialStates)) {
  appendOption("editorial-state", value, label);
  appendOption("editorial-state-filter", value, label);
}
let editorialOffset = 0, editorialNext = null, editorialEditing = null, editorialRead;

function clearEditorial() {
  editorialRead?.abort();
  closeEditorialForm();
  el("editorial-list").replaceChildren();
  el("editorial-status").textContent = "";
}

function editorialCard(candidate) {
  const card = node("article");
  card.className = "editorial-card";
  card.append(node("h3", candidate.title), node("p", [
    marketLabel(candidate.market_id), editorialStates[candidate.status], editorialFormats[candidate.format],
  ].join(" · ")));
  const cost = candidate.cost ? fmt(candidate.cost.amount) + " " + candidate.cost.currency + " · " + candidate.cost.basis : "Bilinmiyor";
  const detail = node("details");
  detail.append(node("summary", "Hipotez, anlatım ve kaynaklar"));
  const facts = node("dl");
  for (const [label, value] of [
    ["Pazar hipotezi", candidate.hypothesis], ["Özgün anlatım açısı", candidate.narrative_angle],
    ["Belirsizlik", candidate.uncertainty], ["Tahmini maliyet", cost],
  ]) facts.append(node("dt", label), node("dd", value));
  detail.append(facts);
  if (candidate.sources.length) {
    const sources = node("ul");
    for (const source of candidate.sources) {
      const item = node("li");
      const link = node("a", source.publisher);
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      item.append(link, node("span", " · " + source.checked_on + " · " + editorialSourceKinds[source.kind]), node("p", source.finding));
      sources.append(item);
    }
    detail.append(sources);
  } else {
    detail.append(node("p", "Bağımsız kaynak henüz eklenmedi."));
  }
  const edit = node("button", "Adayı düzenle");
  edit.type = "button";
  edit.className = "secondary";
  edit.addEventListener("click", () => openEditorialForm(candidate));
  const brief=node("button","Üretim brifini indir");brief.type="button";brief.className="secondary";
  brief.addEventListener("click",async()=>{
    brief.disabled=true;
    try{
      const data=await request("/api/editorial?"+new URLSearchParams({brief:candidate.id}));
      const url=URL.createObjectURL(new Blob([data.markdown],{type:"text/markdown;charset=utf-8"}));
      const link=node("a");link.href=url;link.download="fasulye-brief-"+candidate.id+".md";document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
      el("editorial-status").textContent="Güncel revizyonun üretim brifi indirildi.";
    }catch(error){el("editorial-status").textContent=error.message;}finally{brief.disabled=false;}
  });
  const actions=node("div");actions.className="editorial-actions";actions.append(edit,brief);card.append(detail,actions);
  if(batchCatalog?.features?.editorial_workflow)card.append(workflowPanel(candidate));
  return card;
}

async function loadEditorial(offset) {
  editorialRead?.abort();
  const reader = editorialRead = new AbortController();
  const params = new URLSearchParams({ offset, limit: 10 });
  for (const [key, id] of [["market_id", "editorial-market-filter"], ["status", "editorial-state-filter"]]) {
    if (el(id).value) params.set(key, el(id).value);
  }
  el("editorial-status").textContent = "Adaylar yükleniyor…";
  el("editorial-list").replaceChildren();
  el("editorial-prev").hidden = el("editorial-next").hidden = true;
  try {
    const data = await request("/api/editorial?" + params, { signal: reader.signal });
    if (reader.signal.aborted) return;
    editorialOffset = offset;
    editorialNext = data.next_offset;
    el("editorial-list").replaceChildren(...data.candidates.map(editorialCard));
    el("editorial-prev").hidden = !offset;
    el("editorial-next").hidden = editorialNext === null;
    el("editorial-status").textContent = data.candidates.length ? "" : "Bu görünümde henüz aday yok.";
  } catch (error) {
    if (!reader.signal.aborted) {
      el("editorial-status").textContent = error.message;
      const retry = node("button", "Tekrar dene");
      retry.type = "button";
      retry.className = "secondary";
      retry.addEventListener("click", () => void loadEditorial(offset));
      el("editorial-list").replaceChildren(retry);
    }
  }
}

function showEditorialCost() {
  const hasCost = el("editorial-amount").value !== "";
  el("editorial-cost-fields").hidden = !hasCost;
  el("editorial-currency").required = el("editorial-basis").required = hasCost;
}
function addEditorialSource(values = {}) {
  const container = el("editorial-sources");
  if (container.children.length >= 8) return;
  const source = el("editorial-source-template").content.firstElementChild.cloneNode(true);
  for (const input of source.querySelectorAll("[name]")) {
    if (input.name in values) input.value = values[input.name];
  }
  const add = el("editorial-add-source");
  source.querySelector("button").addEventListener("click", () => {
    source.remove();
    add.disabled = false;
    add.focus();
  });
  container.append(source);
  add.disabled = container.children.length >= 8;
  return source;
}
function closeEditorialForm() {
  editorialEditing = null;
  el("editorial-form").reset();
  el("editorial-form").hidden = true;
  el("editorial-backlog").hidden = false;
  el("editorial-new").hidden = false;
  el("editorial-sources").replaceChildren();
  el("editorial-add-source").disabled = false;
  el("editorial-form-status").hidden = true;
  el("editorial-form-status").textContent = "";
  showEditorialCost();
}
function openEditorialForm(candidate = null) {
  closeEditorialForm();
  editorialEditing = candidate;
  el("editorial-form-title").textContent = candidate ? "Adayı düzenle" : "Yeni aday";
  if (candidate) {
    for (const [key, id] of Object.entries(editorialFields)) el(id).value = candidate[key];
    if (candidate.cost) {
      for (const key of ["amount", "currency", "basis"]) el("editorial-" + key).value = candidate.cost[key];
    }
    for (const source of candidate.sources) addEditorialSource(source);
  }
  showEditorialCost();
  el("editorial-backlog").hidden = true;
  el("editorial-new").hidden = true;
  el("editorial-form").hidden = false;
  el("editorial-name").focus();
}
el("editorial-new").addEventListener("click", () => openEditorialForm());
el("editorial-cancel").addEventListener("click", () => {
  closeEditorialForm();
  el("editorial-new").focus();
});
el("editorial-add-source").addEventListener("click", () => addEditorialSource()?.querySelector("input").focus());
el("editorial-amount").addEventListener("input", showEditorialCost);
el("editorial-prev").addEventListener("click", () => void loadEditorial(Math.max(0, editorialOffset - 10)));
el("editorial-next").addEventListener("click", () => {
  if (editorialNext !== null) void loadEditorial(editorialNext);
});
for (const id of ["editorial-market-filter", "editorial-state-filter"]) {
  el(id).addEventListener("change", () => void loadEditorial(0));
}
el("editorial-form").addEventListener("submit", async event => {
  event.preventDefault();
  const editing = editorialEditing;
  const candidate = Object.fromEntries(Object.entries(editorialFields).map(([key, id]) => [key, el(id).value]));
  candidate.independent = el("editorial-independent").checked;
  candidate.cost = el("editorial-amount").value === "" ? null : {
    amount: el("editorial-amount").valueAsNumber,
    currency: el("editorial-currency").value, basis: el("editorial-basis").value,
  };
  candidate.sources = [...el("editorial-sources").children].map(source =>
    Object.fromEntries([...source.querySelectorAll("[name]")].map(input => [input.name, input.value])));
  el("editorial-save").disabled = el("editorial-cancel").disabled = true;
  const feedback = el("editorial-form-status");
  feedback.hidden = true;
  try {
    const body = editing ? { id: editing.id, revision: editing.revision, candidate } : candidate;
    await request("/api/editorial", { method: editing ? "PUT" : "POST", body: JSON.stringify(body) });
    closeEditorialForm();
    if (currentPage === "editorial" && !el("dashboard").hidden) {
      el("editorial-market-filter").value = el("editorial-state-filter").value = "";
      await loadEditorial(0);
      const status = el("editorial-status");
      if (currentPage === "editorial" && !el("dashboard").hidden) {
        status.textContent = ["Aday kaydedildi.", status.textContent].filter(Boolean).join(" ");
        el("editorial-new").focus();
      }
    }
  } catch (error) {
    feedback.hidden = false;
    feedback.textContent = error.message;
  } finally {
    el("editorial-save").disabled = el("editorial-cancel").disabled = false;
  }
});

let wikiSelectionLanguage=null;
el("wiki-language").addEventListener("change",()=>{wikiSelectionLanguage=null;el("wiki-page").replaceChildren(new Option("Önce ara",""));});
el("wiki-query").addEventListener("input",()=>{wikiSelectionLanguage=null;el("wiki-page").replaceChildren(new Option("Önce ara",""));});
el("wiki-search").addEventListener("submit",async e=>{
 e.preventDefault();const language=el("wiki-language").value,query=el("wiki-query").value;
 wikiSelectionLanguage=null;el("wiki-page").replaceChildren(new Option("Seçiniz",""));el("wiki-status").textContent="Makaleler aranıyor…";
 try{
  const result=await request("/api/wikimedia?search=1",{method:"POST",body:JSON.stringify({language,query})});
  if(el("wiki-language").value!==language||el("wiki-query").value!==query)return;
  for(const row of result.results)el("wiki-page").append(new Option(row.title,String(row.page_id)));
  wikiSelectionLanguage=language;el("wiki-status").textContent=result.results.length?"Doğru makaleyi elle seçin.":"Makale adayı bulunamadı.";
 }catch(err){el("wiki-status").textContent=err.message;}
});
async function loadWiki(){
 try{
  const p=await request("/api/wikimedia");const list=el("wiki-list");list.replaceChildren();
  for(const r of p.records){
   const item=node("p",r.topic+" · "+r.article_title+" · "+r.language+" · "+r.period_start+" – "+r.period_end+" · "+r.freshness);
   const detail=node("details");detail.append(node("summary","Günlük ham gözlemler"));
   const table=node("ul");for(const v of r.series)table.append(node("li",v.date+": "+(v.views===null?"Bilinmiyor":fmt(v.views))));
   detail.append(table,node("p",r.limitations),node("p","Kaynak: "+r.source_url),node("p","Alım: "+r.retrieved_at+" / "+r.license));
   list.append(item,detail);
  }
  if(!p.records.length)list.append(node("p","Henüz kanıt yok."));
  el("wiki-status").textContent="Kayıtlı bağımsız kanıtlar.";
 }catch(err){el("wiki-status").textContent=err.message;}
}
el("wiki-list-button").addEventListener("click",()=>void loadWiki());
el("wiki-collect").addEventListener("submit",async e=>{
 e.preventDefault();
 try{
  if(wikiSelectionLanguage!==el("wiki-language").value||!el("wiki-page").value)throw new Error("Önce doğru makaleyi seçin.");
  el("wiki-status").textContent="Gözlemler alınıyor…";
  await request("/api/wikimedia",{method:"POST",body:JSON.stringify({language:wikiSelectionLanguage,topic:el("wiki-topic").value,page_id:Number(el("wiki-page").value),start:el("wiki-start").value,end:el("wiki-end").value})});await loadWiki();
 }catch(err){el("wiki-status").textContent=err.message;}
});

async function queueAction(action,task_id,priority){
 if(!taskBatchId)return;
 const id=taskBatchId;
 const confirmNeeded=["cancel","retry_failed"].includes(action);
 if(confirmNeeded&&!window.confirm(action==="cancel"?"Seçili görevleri iptal et? Harcanan kota geri gelmez.":"Başarısız görevleri yeniden kuyruğa ekle? Yeni aramalar kota kullanabilir."))return;
 try{
  const input={id,action,...(task_id!==undefined?{task_id}:{}),...(priority!==undefined?{priority}:{}),...(confirmNeeded?{confirm:true}:{})};
  const result=await request("/api/queue",{method:"POST",body:JSON.stringify(input)});
  el("queue-action-status").textContent=result.changed+" kayıt değiştirildi; kota iadesi yok.";
  if(taskBatchId===id)void watchBatch(id);
 }catch(e){el("queue-action-status").textContent=e.message;}
}
for(const [id,action] of [["queue-pause","pause"],["queue-resume","resume"],["queue-cancel","cancel"],["queue-retry","retry_failed"]])el(id).addEventListener("click",()=>void queueAction(action));
el("queue-set-priority").addEventListener("click",()=>void queueAction("priority",undefined,Number(el("queue-priority").value)));

const workflowStages={discovered:"Aday keşfi",sources_collected:"Bağımsız kaynaklar",demand_evaluated:"Talep hipotezi",coverage_reviewed:"Pazar kapsamı",angle_validated:"Özgün açı ve olgular",cost_estimated:"Üretim maliyeti",experiment_ready:"Ön kayıtlı deney ve üretim planı",experiment_completed:"Yayın sonrası deney",long_form_decision:"Uzun video kararı"};
function downloadWorkflow(content,filename,type){
 const url=URL.createObjectURL(new Blob([content],{type})),a=node("a");a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function workflowPanel(candidate){
 const panel=node("details"),body=node("div");panel.append(node("summary","Araştırma ve deney iş akışı"),body);
 let loaded=false;
 async function load(){
  body.replaceChildren(node("p","İş akışı yükleniyor…"));
  try{
   const w=await request("/api/workflow?"+new URLSearchParams({candidate_id:candidate.id}));
   body.replaceChildren(node("p",w.events.length+"/9 aşama tamamlandı. Kayıtlar değiştirilemez."));
   const list=node("ol");for(const [id,title] of Object.entries(workflowStages))list.append(node("li",title+(w.events.some(e=>e.stage===id)?" · Kaydedildi":id===w.next_stage?" · Sıradaki":"")));body.append(list);
   const exports=node("div");exports.className="editorial-actions";
   for(const [label,ext,content,type] of [["Markdown indir","md",w.markdown,"text/markdown"],["JSON indir","json",JSON.stringify(w,null,2),"application/json"]]){
    const b=node("button",label);b.type="button";b.className="secondary";b.addEventListener("click",()=>downloadWorkflow(content,"fasulye-workflow-"+candidate.id+"-r"+w.events.length+"."+ext,type));exports.append(b);
   }body.append(exports);
   if(w.next_stage)body.append(workflowForm(w,load));
  }catch(e){body.replaceChildren(node("p",e.message));}
 }
 panel.addEventListener("toggle",()=>{if(panel.open&&!loaded){loaded=true;void load();}});
 return panel;
}
function workflowForm(w,refresh){
 const stage=w.next_stage,form=node("form"),fields=node("div"),status=node("p");form.className="editorial-form";status.setAttribute("role","status");
 form.append(node("h4",workflowStages[stage]),fields);
 const inputs={};
 function field(parent,key,label,{type="text",value="",options,required=true,min,max,step}={}){
  const wrap=node("label",label),input=node(options?"select":type==="textarea"?"textarea":"input");
  if(options)for(const [v,t] of options){const o=node("option",t);o.value=v;input.append(o);}
  else if(type!=="textarea")input.type=type;
  if(type==="textarea"){input.rows=2;input.maxLength=4000;}
  if(min!==undefined)input.min=String(min);if(max!==undefined)input.max=String(max);if(step!==undefined)input.step=String(step);
  if(type==="checkbox")input.checked=Boolean(value);else if(type!=="file")input.value=value;
  input.required=required;wrap.append(input);parent.append(wrap);return input;
 }
 function f(key,label,options){inputs[key]=field(fields,key,label,options);}
 function notes(keys){for(const [key,label] of keys)f(key,label,{type:"textarea"});}
 function value(input){return input.type==="checkbox"?input.checked:input.type==="number"?input.valueAsNumber:input.value;}
 const sourceInputs=[],claimInputs=[];
 if(stage==="discovered")notes([["origin","Fikrin kaynağı / nasıl bulundu?"]]);
 if(stage==="sources_collected"||stage==="demand_evaluated"){
  const old=w.events.find(e=>e.stage==="sources_collected")?.data.evidence.sources;
  const seeds=old??w.candidate.sources.map(s=>({...s,type:{context:"historical_context",demand:"general_interest",coverage:"market_coverage"}[s.kind],credibility:"unverified",direction:"unknown",independence_group:"",methodology:"",limitations:"",region:null,language:null,license:null}));
  if(!seeds.length)fields.append(node("p","Önce aday düzenleme ekranından bağımsız kaynak ekle."));
  const kindOptions=[["general_interest","Genel ilgi"],["search_interest","Arama ilgisi"],["youtube_demand","YouTube talebi (bağımsız kanıt)"],["historical_context","Tarihsel bağlam"],["market_coverage","Pazar kapsamı"],["editorial_fit","Editoryal uygunluk"]];
  function addSource(s={}){
   const box=node("fieldset");box.append(node("legend","Kaynak "+(sourceInputs.length+1)));
   const row={};
   for(const [key,label,opts] of [
    ["url","HTTPS kaynak adresi",{type:"url"}],["publisher","Yayıncı",{}],["checked_on","Kontrol tarihi",{type:"date"}],["type","Kanıt türü",{options:kindOptions}],["credibility","Güvenilirlik",{options:[["unverified","Doğrulanmadı"],["primary","Birincil"],["secondary","İkincil"]]}],
    ["independence_group","Bağımsızlık grubu (ortak dayanağı aynı adla belirt)",{}],["direction","Hipotez ilişkisi",{options:[["unknown","Bilinmiyor"],["supports","Destekliyor"],["contradicts","Çelişiyor"],["neutral","Nötr"]]}],
    ["finding","Bulgu",{type:"textarea"}],["methodology","Yöntem",{type:"textarea"}],["limitations","Sınırlamalar",{type:"textarea"}],["region","Ülke kodu (varsa)",{required:false}],["language","Dil kodu (varsa)",{required:false}],["license","Lisans (biliniyorsa)",{required:false}]])
    row[key]=field(box,key,label,{...opts,value:s[key]??(opts.options?opts.options[0][0]:"")});
   sourceInputs.push(row);fields.append(box);
  }
  for(const s of seeds)addSource(s);
  const add=node("button","Bağımsız kaynak ekle");add.type="button";add.className="secondary";add.addEventListener("click",()=>{if(sourceInputs.length<40)addSource();});fields.append(add);
  if(stage==="demand_evaluated"){f("conclusion","Sonuç",{options:[["inconclusive","Belirsiz"],["supports","Destekleniyor"],["contradicts","Çelişiyor"]]});notes([["reason","Gerekçe ve belirsizlik"]]);}
 }
 if(stage==="coverage_reviewed"){f("manual_review","Pazar kapsamını manuel inceledim",{type:"checkbox"});notes([["method","İnceleme yöntemi"],["findings","Bulgular"],["limitations","Sınırlamalar (az sonuç, boş pazar anlamına gelmez)"]]);}
 if(stage==="angle_validated"){
  f("angle","Özgün anlatım açısı",{type:"textarea",value:w.candidate.narrative_angle});
  f("original","Bu anlatım ve görsel yaklaşım özgündür",{type:"checkbox"});
  const sources=[...new Set(w.events.flatMap(e=>e.data?.evidence?.sources??[]).map(s=>s.url))];
  function addClaim(){
   const box=node("fieldset");box.append(node("legend","Olgu / kurgu "+(claimInputs.length+1)));
   const row={claim:field(box,"claim","İddia",{type:"textarea"}),kind:field(box,"kind","Tür",{options:[["verified_fact","Doğrulanmış olgu"],["creative_storytelling","Yaratıcı anlatım"],["unverified","Doğrulanmadı"]]}),source_url:field(box,"source_url","İncelenen kaynak",{required:false,options:[["","Yok"],...sources.map(u=>[u,u])]})};claimInputs.push(row);fields.append(box);
  }addClaim();const add=node("button","Olgu ekle");add.type="button";add.className="secondary";add.addEventListener("click",()=>{if(claimInputs.length<30)addClaim();});fields.append(add);
 }
 if(stage==="cost_estimated"){
  f("currency","Para birimi",{value:w.candidate.cost?.currency??"EUR"});
  for(const [k,l] of [["research_hours","İnsan araştırma saati"],["hourly_rate","Saat maliyeti"],["translation","Çeviri"],["voice","Ses"],["visuals","Görsel"],["editing","Kurgu"],["other","Diğer"]])f(k,l,{type:"number",min:0,max:10000000,step:"any"});
  notes([["basis","Maliyet dayanağı"]]);
 }
 if(stage==="experiment_ready"){
  f("format","Deney formatı",{options:[["shorts","Shorts"],["long_form","Uzun video"]]});
  notes([["hypothesis","Önceden belirlenen hipotez"],["primary_metric","Ana metrik (örneğin CTR)"],["success_rule","Önceden belirlenen değerlendirme kuralı"],["script_outline","Senaryo taslağı"],["scene_requirements","Sahne ihtiyaçları"],["thumbnail_concept","Kapak fikri"],["publication_checklist","Yayın kontrol listesi (her satır bir madde)"]]);
  f("observation_days","Gözlem süresi (gün)",{type:"number",min:1,max:90,step:1,value:7});
  f("proposed_long_form","Shorts ile ilişkili uzun video fikri",{type:"textarea",required:false});
 }
 if(stage==="experiment_completed"){
  f("published_at","Gerçek yayın zamanı (yerel saat)",{type:"datetime-local"});
  f("video_reference","Kendi video referansın",{});
  f("own_channel","Bu CSV kendi kanalıma ait; paylaşım yetkim var",{type:"checkbox"});
  f("csv","Normalize edilmiş YouTube Studio CSV",{type:"file"});
  fields.append(node("p","CSV başlığı: metric,period_start,period_end,value,unit,dimension_type,dimension_value. Boş değer bilinmiyor; 0 gerçek sıfır."));
  notes([["evaluation","Sonuç değerlendirmesi"],["limitations","Sınırlamalar"]]);
 }
 if(stage==="long_form_decision"){
  f("decision","Karar",{options:[["hold","Bekle"],["go","Uzun videoya geç"],["no_go","Devam etme"]]});
  notes([["reason","Deney ve kaynaklara dayalı gerekçe"]]);
  f("episode_outline","Özgün uzun video taslağı",{type:"textarea",required:false});
 }
 const confirm=field(form,"confirm","Bu aşamanın kaydını onaylıyorum (geri alınamaz)",{type:"checkbox"});
 const save=node("button","Aşamayı kaydet");save.type="submit";form.append(save,status);
 form.addEventListener("submit",async e=>{
  e.preventDefault();save.disabled=true;status.textContent="Kaydediliyor…";
  try{
   const data=Object.fromEntries(Object.entries(inputs).map(([k,input])=>[k,value(input)]));
   if(sourceInputs.length||stage==="sources_collected"||stage==="demand_evaluated")data.evidence={topic:w.candidate.title,hypothesis:w.candidate.hypothesis,sources:sourceInputs.map(row=>Object.fromEntries(Object.entries(row).map(([k,input])=>[k,["region","language","license"].includes(k)?value(input)||null:value(input)])))};
   if(stage==="angle_validated")data.claims=claimInputs.map(row=>({claim:value(row.claim),kind:value(row.kind),source_url:value(row.source_url)||null}));
   if(stage==="experiment_ready"){data.publication_checklist=data.publication_checklist.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);data.proposed_long_form=data.proposed_long_form||null;}
   if(stage==="experiment_completed"){const file=inputs.csv.files[0];if(!file||file.size>300000)throw new Error("300 KB altında CSV seç.");data.csv=await file.text();data.published_at=new Date(data.published_at).toISOString();data.source="owner_youtube_studio_csv";}
   if(stage==="long_form_decision")data.episode_outline=data.episode_outline||null;
   await request("/api/workflow",{method:"POST",body:JSON.stringify({candidate_id:w.candidate.id,candidate_revision:w.candidate.revision,expected_revision:w.events.length,stage,data,confirm:confirm.checked})});
   await refresh();
  }catch(err){status.textContent=err.message;save.disabled=false;}
 });
 return form;
}
