# Recipe: a preview link reviewers can open, on a Vercel site behind SSO

Checked against Vercel's documentation on September 8, 2026. Button labels are quoted as written.

## The situation

Push a branch and Vercel builds a preview at a stable branch URL. On a team with Vercel Authentication (single sign-on) turned on, that URL asks every visitor to log in. Reviewers outside the Vercel team hit a wall. The Vercel MCP tools that mint bypass links refuse on SSO teams, so this needs the dashboard once.

## Steps

1. Push the branch. Confirm the deployment reached READY (MCP, dashboard, or the PR's Vercel check).
2. Open the deployment page in the Vercel dashboard: your project, **Deployments** in the sidebar, then the deployment for your commit.
3. Click **Share**. In the popover, set the dropdown to **Anyone with the link**. Copy the link.
4. Point the link at the page you want reviewed. The share token is a query parameter on the deployment host, so append the path before it:

   `https://<branch-host>.vercel.app/blog/<slug>?_vercel_share=<token>`

5. Test it in a private window or with a plain fetch. Expect one redirect (the token sets a cookie) and then a 200.

## Gotchas

- A share link belongs to a deployment. After the next push, recreate it from the new deployment page. Tell reviewers the link may change.
- To revoke, set the dropdown to **Only people with access**. All active links are listed under the project's **Deployment Protection** settings, **Access** section, **All Access**, then **Shareable Links**.
- Commit author matters. Previews from a commit whose author email is not a team member can sit BLOCKED. Set a real git identity before the first commit.
- Once the piece is live on the production domain, swap the share link for the real URL everywhere you posted it.
