import { crc32 } from "node:zlib";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

function csvCell(value) {
  let s = value == null ? "" : String(value);
  if (typeof value === "string" && (/^[\t\r\n]/.test(s) || /^[=+@-]/.test(s.trimStart()))) s = "'" + s;
  return '"' + s.replaceAll('"', '""') + '"';
}
function csv(columns, rows) {
  return "\uFEFF" + [columns, ...rows.map(row => columns.map(key => row[key]))].map(row => row.map(csvCell).join(",")).join("\r\n") + "\r\n";
}
export async function exportReport(report) {
  const serialized = JSON.stringify(report, null, 2);
  const template = await readFile(resolve(process.cwd(), "engine/tools/opportunity_engine/dashboard.html"), "utf8");
  const files = {
    "report.json": serialized + "\n",
    "opportunities.csv": csv(["topic_id","topic","market_id","market","region","language","search_status","sample_video_count","sample_channel_count","known_view_video_count","known_subscriber_video_count","sample_total_known_views","demand","competition","channel_fit","coverage","score","source"], report.opportunities.map(row => ({...row,...row.review}))),
    "videos.csv": csv(["topic_id","market_id","video_id","title","published_at","channel_id","channel_title","views","subscribers"], report.opportunities.flatMap(row => row.video_ids.map(id => ({topic_id:row.topic_id,market_id:row.market_id,...report.videos[id]})))),
    "revenue.csv": csv(["market_id","format","views","currency","rpm_low","rpm_base","rpm_high","rpm_source","low","base","high"], Object.entries(report.revenue_by_market).flatMap(([market_id, scenarios]) => scenarios.map(s => ({market_id,...s,...Object.fromEntries(Object.entries(s.rpm ?? {}).map(([k,v])=>["rpm_"+k,v]))})))),
    "dashboard.html": template.replace("__REPORT_JSON__", () => serialized.replaceAll("<", "\\u003c")),
  };
  return zipFiles(files);
}
export function zipFiles(files) {
  const local = [], central = [];
  let offset = 0, centralSize = 0;
  for (const [name,text] of Object.entries(files)) {
    const filename = Buffer.from(name), data = Buffer.from(text);
    const crc = crc32(data);
    const h = Buffer.alloc(30), c = Buffer.alloc(46);
    h.writeUInt32LE(0x04034b50,0); h.writeUInt16LE(20,4); h.writeUInt16LE(0x800,6);
    h.writeUInt16LE(33,12); h.writeUInt32LE(crc,14); h.writeUInt32LE(data.length,18);
    h.writeUInt32LE(data.length,22); h.writeUInt16LE(filename.length,26);
    c.writeUInt32LE(0x02014b50,0); c.writeUInt16LE(20,4); c.writeUInt16LE(20,6);
    c.writeUInt16LE(0x800,8); c.writeUInt16LE(33,14); c.writeUInt32LE(crc,16);
    c.writeUInt32LE(data.length,20); c.writeUInt32LE(data.length,24);
    c.writeUInt16LE(filename.length,28); c.writeUInt32LE(offset,42);
    local.push(h,filename,data); central.push(c,filename);
    offset += h.length + filename.length + data.length; centralSize += c.length + filename.length;
  }
  const end = Buffer.alloc(22), count = Object.keys(files).length;
  end.writeUInt32LE(0x06054b50,0); end.writeUInt16LE(count,8); end.writeUInt16LE(count,10);
  end.writeUInt32LE(centralSize,12); end.writeUInt32LE(offset,16);
  return Buffer.concat([...local,...central,end]);
}
