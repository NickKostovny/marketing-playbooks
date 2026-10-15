// Assemble index.html from index.src.html. The shipped build inlined a wordmark SVG and two
// licensed font weights as data URIs; this public version inlines a text wordmark and uses the system stack.
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const src = readFileSync(path.join(root, 'index.src.html'), 'utf8');
const mark = '<span style="font-size:18px;font-weight:500;letter-spacing:-0.01em">yourbrand</span>';
const out = src.replace('<!--FONTS-->', '').replace(/<!--WORDMARK-->/g, mark);
writeFileSync(path.join(root, 'index.html'), out);
console.log('wrote index.html', (out.length / 1024).toFixed(0) + ' KB');
