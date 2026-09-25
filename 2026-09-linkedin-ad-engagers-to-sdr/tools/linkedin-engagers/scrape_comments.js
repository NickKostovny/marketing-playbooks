// Run on a FRESH page load (after reactors). Expands comments/replies, sends comments-<id>.json to receiver.py
// only when there are comments. Never throws.
await (async () => {
  const POST_ID = '__POST_ID__';
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  await sleep(2000);
  const cbtn = [...document.querySelectorAll('button')].find(b => /^\d[\d,]*\s+comments?$/i.test((b.innerText||'').trim()) || /\d+\s+comments?/i.test(b.getAttribute('aria-label')||''));
  const headline = cbtn ? parseInt(((cbtn.getAttribute('aria-label')||cbtn.innerText)).replace(/[^\d]/g,''),10) : 0;
  if (cbtn) { cbtn.click(); await sleep(1500); }
  for (let i = 0; i < 40; i++) {
    const more = [...document.querySelectorAll('button')].find(b => /load more comments|previous replies|more replies|see more comments/i.test(b.innerText||''));
    if (!more) break; more.click(); await sleep(1200);
  }
  const items = [...document.querySelectorAll('article.comments-comment-entity, .comments-comment-item')];
  const rows = items.map(it => {
    const a = it.querySelector('a[href*="/in/"], a[href*="/company/"]');
    const name = (it.querySelector('.comments-comment-meta__description-title, .comments-post-meta__name-text, .comments-comment-meta__name')?.innerText || '').trim();
    const hl = (it.querySelector('.comments-comment-meta__description-subtitle, .comments-post-meta__headline')?.innerText || '').trim();
    const text = (it.querySelector('.comments-comment-item__main-content, .update-components-text')?.innerText || '').trim();
    return { name, headline: hl, profile: a ? a.href.split('?')[0] : '', text: text.slice(0, 600),
             is_reply: !!it.closest('.comments-comment-item__replies, .comments-replies-list') };
  }).filter(r => r.name);
  if (rows.length) {
    const payload = { post_id: POST_ID, post_url: location.href.split('?')[0], captured: new Date().toISOString(), headline_count: headline, rows };
    // transfer: navigate to the local receiver (start `python3 receiver.py 8871` first). The receiver saves the
  // file, then holds its reply 2s, so this page stays alive long enough to return the result below.
  location.href = 'http://127.0.0.1:8871/save?name=comments-' + POST_ID + '.json&d=' + encodeURIComponent(JSON.stringify(payload));
  await sleep(700);
  }
  return {post: POST_ID, headline, captured: rows.length};
})();
