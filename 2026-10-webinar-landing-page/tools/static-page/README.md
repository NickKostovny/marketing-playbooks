# Static webinar page template

The two-section page from the ship log as a buildable template. Anonymised: speakers are placeholders, the partner logos and the product demo are left out, and the licensed font is swapped for the system stack. Everything else, the tokens, the layout, the facts strip, the register card and the speaker grid, is as shipped.

```bash
node build.mjs          # writes index.html from index.src.html
./deploy.sh             # builds, stages, deploys to a Vercel project (edit the project name)
```

Where the shipped page had the product demo and the hero figure, the template has comments marking the slot.
