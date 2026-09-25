// IFRAME MODE (use when the extension refuses scripts on the post URL itself).
// Run on https://www.linkedin.com/feed/ . Replace __POST_ID__ (a urn:li:share id). Loads the post in a same-origin
// iframe, scrapes reactors + comments from the frame, then navigates the PARENT to receiver.py (which 302s back to /feed/).
// In a browser_batch: [js(ad A), navigate(/feed/), js(ad B), navigate(/feed/), ...]
await (async()=>{const P='__POST_ID__';const s=ms=>new Promise(r=>setTimeout(r,ms));
if(!/linkedin\.com$/.test(location.hostname))return{err:'run this on linkedin.com'};
let f=document.getElementById('__scrapeFrame');if(f)f.remove();
f=document.createElement('iframe');f.id='__scrapeFrame';f.style.cssText='position:fixed;left:0;top:0;width:1200px;height:900px;z-index:99999;background:#fff';
f.src='/feed/update/urn:li:share:'+P+'/';document.body.appendChild(f);
let doc=null,cb=null,loaded=false;
for(let i=0;i<40;i++){await s(500);try{doc=f.contentDocument;}catch(e){return{err:e.message};}if(!doc)continue;
  loaded=!!doc.querySelector('.feed-shared-update-v2, .update-components-text, .update-components-actor');
  cb=doc.querySelector('button[aria-label$="reactions"], button[aria-label$="reaction"]');if(cb)break;if(loaded&&i>14)break;}
if(!doc)return{post:P,err:'frame never loaded'};
const h=cb?parseInt((cb.getAttribute('aria-label')||'').replace(/[^\d]/g,''),10):0;
const op=doc.querySelector('button.social-details-reactors-facepile__reactions-modal-button')||cb;
let rows=[],note='';
if(op){op.click();let m=null;for(let i=0;i<25&&!m;i++){await s(400);m=doc.querySelector('.social-details-reactors-modal');}
  if(m){const box=m.querySelector('.social-details-reactors-modal__content')||m;let last=-1,st=0;
    for(let i=0;i<80;i++){const b=[...m.querySelectorAll('button')].find(b=>/show more results/i.test(b.innerText));if(b)b.click();else box.scrollTop=box.scrollHeight;await s(900);const n=m.querySelectorAll('li').length;if(n===last){if(++st>=3)break;}else{st=0;last=n;}}
    const D=/^[•·]?\s*(1st|2nd|3rd\+?)(\s+degree connection)?$/;
    rows=[...m.querySelectorAll('li')].map(li=>{const a=li.querySelector('a[href*="/in/"], a[href*="/company/"]');const t=li.innerText.split('\n').map(x=>x.trim()).filter(Boolean);const im=li.querySelector('img.reactions-icon');const rest=t.slice(1).filter(x=>!/^View .* profile$/.test(x)&&!D.test(x));const dg=(t.find(x=>D.test(x))||'').replace(/^[•·]\s*/,'').replace(/\s+degree connection$/,'');return{name:t[0]||'',degree:dg,headline:rest.join(' | '),reaction:im?im.alt:'',profile:a?a.href.split('?')[0]:'',is_company:!!(a&&/\/company\//.test(a.href))};}).filter(r=>r.name);
    m.querySelector('.artdeco-modal__dismiss, button[aria-label="Dismiss"]')?.click();} else note='modal did not open';}
else note=loaded?'0 reactions':'post not loaded';
let comments=[],ch=0;
const ccb=[...doc.querySelectorAll('button')].find(b=>/^\d[\d,]*\s+comments?$/i.test((b.innerText||'').trim())||/\d+\s+comments?/i.test(b.getAttribute('aria-label')||''));
if(ccb){ch=parseInt(((ccb.getAttribute('aria-label')||ccb.innerText)).replace(/[^\d]/g,''),10)||0;ccb.click();await s(1500);
  for(let i=0;i<40;i++){const mo=[...doc.querySelectorAll('button')].find(b=>/load more comments|previous replies|more replies|see more comments/i.test(b.innerText||''));if(!mo)break;mo.click();await s(1200);}
  comments=[...doc.querySelectorAll('article.comments-comment-entity, .comments-comment-item')].map(e=>{const a=e.querySelector('a[href*="/in/"], a[href*="/company/"]');const nm=(e.querySelector('.comments-comment-meta__description-title, .comments-post-meta__name-text, .comments-comment-meta__name')?.innerText||'').trim();const hl=(e.querySelector('.comments-comment-meta__description-subtitle, .comments-post-meta__headline')?.innerText||'').trim();const tx=(e.querySelector('.comments-comment-item__main-content, .update-components-text')?.innerText||'').trim();return{name:nm,headline:hl,profile:a?a.href.split('?')[0]:'',text:tx.slice(0,600),is_reply:!!e.closest('.comments-comment-item__replies, .comments-replies-list')};}).filter(r=>r.name);}
const pl={post_id:P,post_url:'https://www.linkedin.com/feed/update/urn:li:share:'+P+'/',captured:new Date().toISOString(),headline_count:h,rows,comments_headline:ch,comments,mode:'iframe'};
f.remove();
const u='http://127.0.0.1:8871/save?name=reactors-'+P+'.json&d='+encodeURIComponent(JSON.stringify(pl));
location.href=u;await s(700);
return{post:P,headline:h,captured:rows.length,comments_headline:ch,comments:comments.length,note,urlKB:Math.round(u.length/1024)};})();
