# Recipe: lock a Vimeo embed to your domain

Why: a page that unlocks a player after a form still has to ship the player URL to the browser. Anyone who reads the page payload has it. Domain-level embed privacy makes the URL play only inside pages on the domains you list.

Labels below are as they read on September 23, 2026. Vendor UIs move; check the current help article if a label is missing.

1. Open the video on Vimeo. Go to **Settings**, then **Privacy**.
2. Under **Where can this be embedded?** choose **Specific domains**.
3. Add your production domain. Add both the apex and the `www` host if you serve both. Do not add preview or review hosts unless you accept that anyone who finds those pages can play the video.
4. Save.

Verify, in a fresh browser session:

- Load the player URL (`https://player.vimeo.com/video/<id>`) directly. You should see a privacy notice, not the video.
- Load your production page and pass the gate. The video plays.
- Load a preview or review copy on another host. The video does not play. This is the lock working, not a bug to fix.

Two notes:

- The embed still works with the standard `<iframe>` code from the **Share** dialog. No token or signed URL is needed.
- If you also use the video host's own page as a fallback link anywhere, the video's **Who can watch** setting is a separate control. Set it to match.
