// Paste into javascript_tool on a logged-in LinkedIn post page (Nick's Chrome). Replace __POST_ID__.
// Opens the reactors modal, pages it, sends reactors-<id>.json to receiver.py.
// In a browser_batch: navigate(post) -> this script -> navigate(next). No wait step needed. Never throws.
await (async () => {
  const POST_ID = '__POST_ID__';
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await sleep(2000);
  const countBtn = document.querySelector('button[aria-label$="reactions"], button[aria-label$="reaction"]');
  const headline = countBtn ? parseInt((countBtn.getAttribute('aria-label')||'').replace(/[^\d]/g,''),10) : 0;
  const opener = document.querySelector('button.social-details-reactors-facepile__reactions-modal-button') || countBtn;
  if (!opener) return {post: POST_ID, headline: 0, captured: 0, note: 'no reactions button'};
  opener.click();
  let modal = null;
  for (let i = 0; i < 25 && !modal; i++) { await sleep(400); modal = document.querySelector('.social-details-reactors-modal'); }
  if (!modal) return {post: POST_ID, headline, captured: 0, note: 'modal did not open'};
  const box = modal.querySelector('.social-details-reactors-modal__content') || modal;
  let last = -1, stable = 0;
  for (let i = 0; i < 80; i++) {
    const btn = [...modal.querySelectorAll('button')].find(b => /show more results/i.test(b.innerText));
    if (btn) btn.click(); else box.scrollTop = box.scrollHeight;
    await sleep(900);
    const n = modal.querySelectorAll('li').length;
    if (n === last) { if (++stable >= 3) break; } else { stable = 0; last = n; }
  }
  const DEG = /^[•·]?\s*(1st|2nd|3rd\+?)(\s+degree connection)?$/;
  const rows = [...modal.querySelectorAll('li')].map(li => {
    const a = li.querySelector('a[href*="/in/"], a[href*="/company/"]');
    const txt = li.innerText.split('\n').map(s => s.trim()).filter(Boolean);
    const img = li.querySelector('img.reactions-icon');
    const name = txt[0] || '';
    const rest = txt.slice(1).filter(t => !/^View .* profile$/.test(t) && !DEG.test(t));
    const deg = (txt.find(t => DEG.test(t)) || '').replace(/^[•·]\s*/, '').replace(/\s+degree connection$/, '');
    return { name, degree: deg, headline: rest.join(' | '), reaction: img ? img.alt : '',
             profile: a ? a.href.split('?')[0] : '', is_company: !!(a && /\/company\//.test(a.href)) };
  }).filter(r => r.name);
  const payload = { post_id: POST_ID, post_url: location.href.split('?')[0], captured: new Date().toISOString(), headline_count: headline, rows };
  // transfer: navigate to the local receiver (start `python3 receiver.py 8871` first). The receiver saves the
  // file, then holds its reply 2s, so this page stays alive long enough to return the result below.
  location.href = 'http://127.0.0.1:8871/save?name=reactors-' + POST_ID + '.json&d=' + encodeURIComponent(JSON.stringify(payload));
  await sleep(700);
  modal.querySelector('.artdeco-modal__dismiss, button[aria-label="Dismiss"]')?.click();
  return {post: POST_ID, headline, captured: rows.length};
})();
