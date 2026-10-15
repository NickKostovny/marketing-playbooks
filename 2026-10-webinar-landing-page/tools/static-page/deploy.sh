#!/bin/zsh
# Build, stage, deploy to a public Vercel project. Only the project's clean alias is public;
# per-deploy hash URLs sit behind team SSO.
set -e
cd "$(dirname "$0")"
node build.mjs
mkdir -p deploy && rm -rf deploy/index.html deploy/media
cp index.html deploy/
[ -d media ] && cp -R media deploy/media
cd deploy
vercel link --yes --project YOUR-PROJECT >/dev/null
vercel deploy --prod --yes
