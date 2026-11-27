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
  if (!["/api/catalog","/api/discovery-catalog"].includes(path)) {
    const token = el("token").value.trim();
    if (!token) {
      el("token").focus();
      throw new Error("Panel erişim anahtarını gir.");
    }
    headers.set("Authorization", "Bearer " + token);
  }
  if (body) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { method, headers, body, signal, cache: "no-store" });
  if (!response.ok) {
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
    details.append(node("p", `${query.query} · ${query.pages} sayfa${suffix}`));
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
  el("results").hidden = false;
  const detailErrors = Object.values(data.detail_errors).flat();
  el("report-meta").textContent = dates.format(new Date(data.collected_at)) + " · "
    + data.quota.successes.search + "/" + data.quota.attempts.search + " arama başarılı"
    + (detailErrors.length ? " · Eksik ayrıntılar: " + [...new Set(detailErrors)].join(", ") : "");
  filterOptions("topic-filter", topics);
  filterOptions("market-filter", markets);
  renderRows();
}

function renderRows() {
  const statuses = { complete: "Tamamlandı", no_query: "Sorgu yok", partial: "Kısmi", failed: "Başarısız" };
  const rows = report.opportunities.filter(row =>
    (!el("topic-filter").value || row.topic_id === el("topic-filter").value) &&
    (!el("market-filter").value || row.market_id === el("market-filter").value));
  for (const id of ["observations", "reviews", "revenue"]) el(id).replaceChildren();
  for (const row of rows) {
    const label = `${row.topic} / ${row.market}`;
    const views = `${fmt(row.sample_total_known_views)} (${fmt(row.known_view_video_count)} videoda)`;
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
void loadCatalog();

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
    for(const c of batchCatalog.categories) appendOption("batch-categories",c.id,c.label);
  } catch(e) { el("batch-status").textContent=e.message; }
}
function batchInput() {
  if(!batchCatalog) throw new Error("Katalog yüklenmedi.");
  const mode=el("batch-mode").value,languages=selected("batch-languages");
  const input={mode,countries:selected("batch-countries"),languages};
  if(mode==="discovery") return {...input,categories:selected("batch-categories")};
  const topics=new Map();
  const raw=el("batch-topics").value.trim();
  const lines=raw.includes("|")?raw.split(/\r?\n/):raw.split(/[,\r\n]+/);
  for(const line of lines.map(s=>s.trim()).filter(Boolean)){
    const parts=line.split("|").map(s=>s.trim());
    if(parts.length===1 && languages.length===1) parts.push(languages[0],parts[0]);
    if(parts.length!==3 || !batchCatalog.languages[parts[1]] || !parts[0] || !parts[2]) throw new Error("Her satırda konu | dil kodu | yerel sorgu gir veya tek dil seç.");
    if(!topics.has(parts[0])) topics.set(parts[0],{topic:parts[0],queries:{}});
    topics.get(parts[0]).queries[parts[1]]=parts[2];
  }
  return {...input,topics:[...topics.values()]};
}
el("batch-mode").addEventListener("change",()=>{
  const discovery=el("batch-mode").value==="discovery";
  el("category-field").hidden=!discovery;el("bulk-field").hidden=discovery;
});
async function submitBatch(preview) {
  const button=el(preview?"batch-preview":"batch-submit");button.disabled=true;
  try {
    const data=await request("/api/batch"+(preview?"?preview=1":""),{method:"POST",body:JSON.stringify(batchInput())});
    el("batch-status").textContent=data.tasks+" görev · "+data.missing.length+" eksik pazar yerelleştirmesi"+(preview?" · Plan; henüz kuyruğa eklenmedi.":" · Kuyruğa kaydedildi.");
    if(!preview) void watchBatch(data.id);
  } catch(e) {el("batch-status").textContent=e.message;}
  finally {button.disabled=false;}
}
el("batch-preview").addEventListener("click",()=>void submitBatch(true));
el("batch-form").addEventListener("submit",e=>{e.preventDefault();void submitBatch(false);});
async function watchBatch(id) {
  batchController?.abort();batchController=new AbortController();const {signal}=batchController;
  try {
    while(!signal.aborted){
      const b=await request("/api/batch?"+new URLSearchParams({id}),{signal});
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
void initBatch();
