import { copyFile, mkdir } from "node:fs/promises";

const dist = new URL("./dist/", import.meta.url);
await mkdir(dist, { recursive: true });
await Promise.all(["index.html", "styles.css", "app.js"].map(name =>
  copyFile(new URL(name, import.meta.url), new URL(name, dist))));
