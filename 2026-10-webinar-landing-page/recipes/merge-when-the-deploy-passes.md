# Merge a PR when the deploy check passes, without polling by hand

Five production merges in an afternoon, each the same loop.

```bash
# 1. Fresh branch off the remote main, in a worktree
git fetch origin main
git checkout -b claude/<slug> origin/main

# 2. Edit, build, commit
npm run build
git commit -am "..."

# 3. Push and open the PR with an explicit head.
#    A worktree branch tracks origin/main until the first push -u, and the
#    GitHub CLI aborts on a branch whose upstream is main.
git push -u origin claude/<slug>
gh pr create --head claude/<slug> --base main --title "..." --body "..."

# 4. Background loop: exit when the deploy check leaves "pending", pass or fail.
until s=$(gh pr checks <n> | grep -i '^Vercel' | awk -F'\t' '{print $2}') \
      && [ -n "$s" ] && [ "$s" != "pending" ]; do sleep 20; done; echo "VERCEL $s"

# 5. On pass, squash-merge. Do not pass --delete-branch under a worktree.
gh pr merge <n> --squash --subject "... (#<n>)"

# 6. Background loop: exit when production serves the change.
until curl -sL https://example.com/path | grep -q "a string only the new version has"; do sleep 20; done
```

Notes:

- Step 4 exits on fail too. A loop that only exits on pass hangs forever on a broken build.
- An advisory AI review check often finishes after the deploy. Decide up front whether it blocks. Here it does not.
- A site that redirects `www` to the bare domain returns 308 to a plain `curl`. Use `-L` in step 6 or you will wait on a redirect.
- Turbopack refuses a symlinked `node_modules` in a worktree. `cp -c -R ../main/node_modules node_modules` is a copy-on-write clone on APFS and takes seconds.
