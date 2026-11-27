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
  el("run-link").href = "https://github.com/furesat/youtube-studio-/actions/runs/" + id;
  el("run-link").hidden = false;
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
        showStatus(run.conclusion === "success"
          ? "Araştırma tamamlandı."
          : "Çalıştırma eksik sona erdi. Kaydedilen raporu görüntülüyorsun.", run.conclusion !== "success");
      } catch (error) {
        if (signal.aborted) return;
        throw new Error("Supabase raporu açılamadı. " + error.message + " Ayrıntılar GitHub Actions kaydında.");
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
});
async function submitBatch(preview) {
  const button=el(preview?"batch-preview":"batch-submit");button.disabled=true;
  try {
    const data=await request("/api/batch"+(preview?"?preview=1":""),{method:"POST",body:JSON.stringify(batchInput())});
    el("batch-status").textContent=data.tasks+" görev · "+data.missing.length+" eksik pazar yerelleştirmesi"+(preview?" · Plan; henüz kuyruğa eklenmedi.":" · Kuyruğa kaydedildi.");
    if(!preview) { el("batch-status").textContent += data.worker?.state==="dispatched"?" Worker başlatıldı.":" Zamanlanmış worker bekleniyor."; void watchBatch(data.id); }
  } catch(e) {el("batch-status").textContent=e.message;}
  finally {button.disabled=false;}
}
el("batch-preview").addEventListener("click",()=>void submitBatch(true));
el("batch-form").addEventListener("submit",e=>{e.preventDefault();void submitBatch(false);});
let taskBatchId,taskOffset=0,taskTotal=0;
async function loadBatchTasks(){
  if(!taskBatchId)return;
  try{const rows=await request("/api/batch?"+new URLSearchParams({id:taskBatchId,tasks:"1",offset:String(taskOffset)}));el("batch-task-rows").replaceChildren();for(const t of rows)addRow("batch-task-rows",[t.topic+" / "+t.query,t.region+" / "+t.language,(t.lookback_days??365)+" gün / "+(t.search_order??"relevance"),t.status,t.attempts,t.error_code]);el("batch-task-prev").disabled=taskOffset===0;el("batch-task-next").disabled=taskOffset+100>=taskTotal;}catch(e){el("batch-status").textContent=e.message;}
}
el("batch-task-details").addEventListener("toggle",()=>{if(el("batch-task-details").open)void loadBatchTasks();});
el("batch-task-prev").addEventListener("click",()=>{taskOffset=Math.max(0,taskOffset-100);void loadBatchTasks();});
el("batch-task-next").addEventListener("click",()=>{taskOffset+=100;void loadBatchTasks();});
async function watchBatch(id) {
  navigate("batch");
  taskBatchId=id;taskOffset=0;el("batch-task-details").hidden=false;
  compareBatchId=id;compareOffset=0;el("market-evidence").hidden=false;el("compare-topic").value="";el("compare-market").value="";el("compare-days").value="";if(el("market-evidence").open)void loadMarketEvidence();
  batchController?.abort();batchController=new AbortController();const {signal}=batchController;
  try {
    while(!signal.aborted){
      const b=await request("/api/batch?"+new URLSearchParams({id}),{signal});
      taskTotal=b.total;if(el("batch-task-details").open)void loadBatchTasks();
      const p=el("batch-progress");p.hidden=false;p.max=b.total||1;p.value=b.done+b.failed;
      el("batch-status").textContent=b.label+" · "+b.done+"/"+b.total+" tamamlandı · "+b.running+" çalışıyor · "+b.queued+" sırada · "+b.failed+" başarısız";
      const container=el("batch-reports");container.replaceChildren();
      for(const runId of b.reports){const button=node("button","Raporu aç · "+runId);button.type="button";button.className="secondary";button.addEventListener("click",()=>void supervise(s=>watch(runId,s)));container.append(button);}
      if(b.done+b.failed>=b.total) break;
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
    addRow("review-comparison",[row.topic,marketLabel(row.market_id),fmt(row.score),percentages.format(row.coverage),{high:"Yüksek",medium:"Orta",low:"Düşük"}[row.confidence],row.source]);
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
  if(checks[2].status==="fulfilled"&&checks[2].value.length){
    try{const id=checks[2].value[0].run_id,run=await request("/api/research?"+new URLSearchParams({id}));results.append(node("p","GitHub Actions son kayıtlı çalışma: "+run.status+" / "+(run.conclusion??"bekliyor")));}
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
      if(r.report_run_id){detail=node("button","Örneklemi aç");detail.type="button";detail.className="secondary";detail.addEventListener("click",()=>void supervise(async s=>{await watch(r.report_run_id,s);if(report&&!s.aborted){el("topic-filter").value="queue-"+r.id;renderRows();}}));}
      const count=r.sample_video_count==null?"Bilinmiyor":String(r.sample_video_count)+(r.has_more===true?" · devamı var":"");
      const missing=r.sample_video_count==null?"Bilinmiyor":"İzlenme verisi: "+(r.known_view_video_count??"?")+", abone verisi: "+(r.known_subscriber_video_count??"?")+" videoda mevcut";
      const status=({queued:"Sırada",running:"Çalışıyor",done:"Tamamlandı",failed:"Başarısız"})[r.status]??r.status;
      addRow("compare-rows",[subject,marketLabel(r.market_id),r.lookback_days+" gün / "+r.search_order,status+(r.error_code?" · "+r.error_code:""),count,missing,source,detail]);
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
  card.append(detail, edit);
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
