// Print an HTML file to PDF through Chrome's DevTools protocol (the CLI --print-to-pdf hangs on this Mac).
// usage: node tools/print-cdp.mjs <abs html path> <out prefix>
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
const CH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const [, , htmlPath, outPrefix] = process.argv;
const ud = mkdtempSync(path.join(tmpdir(), 'chrome-cdp-'));
const port = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn(CH, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${ud}`, `--remote-debugging-port=${port}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function waitPort() { for (let i = 0; i < 150; i++) { try { const r = await fetch(`http://127.0.0.1:${port}/json/version`); if (r.ok) return; } catch {} await sleep(200); } throw new Error('chrome did not start'); }
try {
  await waitPort();
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const pending = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result); } };
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 816, height: 1400, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'file://' + htmlPath });
  for (let i = 0; i < 60; i++) { const { result } = await send('Runtime.evaluate', { expression: 'document.readyState === "complete" && document.fonts.status === "loaded"', returnByValue: true }); if (result.value) break; await sleep(200); }
  await sleep(300);
  const heights = (await send('Runtime.evaluate', { expression: '[...document.querySelectorAll(".sheet")].map(e => Math.round(e.getBoundingClientRect().height)).join(",")', returnByValue: true })).result.value;
  const fonts = (await send('Runtime.evaluate', { expression: '[...document.fonts].filter(f => f.status === "loaded").map(f => f.family + " " + f.weight).join("; ")', returnByValue: true })).result.value;
  console.log('sheet heights (px @ 720px content width):', heights);
  console.log('fonts loaded:', fonts);
  const m = { marginTop: 0.5, marginBottom: 0.5, marginLeft: 0.5, marginRight: 0.5, displayHeaderFooter: false };
  async function pdf(name, params) { const r = await send('Page.printToPDF', { printBackground: false, preferCSSPageSize: true, ...m, ...params }); writeFileSync(`${outPrefix}-${name}.pdf`, Buffer.from(r.data, 'base64')); console.log('wrote', `${outPrefix}-${name}.pdf`); }
  await pdf('letter-nobg', { paperWidth: 8.5, paperHeight: 11 });                       // print preview, Background graphics OFF
  await pdf('letter-bg', { paperWidth: 8.5, paperHeight: 11, printBackground: true });   // Background graphics ON
  await pdf('a4-nobg', { paperWidth: 8.27, paperHeight: 11.69, preferCSSPageSize: false }); // A4 tray, backgrounds OFF
  ws.close();
} finally { chrome.kill(); rmSync(ud, { recursive: true, force: true }); }
