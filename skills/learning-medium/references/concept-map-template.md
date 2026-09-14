# Concept Map Template

When generating the end-of-conversation concept map, use this as a structural template. Adapt the data to match the actual conversation content.

## Data Structure

Before rendering, assemble the conversation's concepts into this structure:

```javascript
const mapData = {
  title: "Domain: [topic explored]",
  date: "[conversation date]",
  concepts: [
    {
      id: "unique_id",
      label: "Short Concept Name",
      definition: "One sentence definition in plain language",
      status: "anchored" | "introduced" | "flagged",
      // anchored = understood and connected
      // introduced = explained but not fully probed
      // flagged = gap for future exploration
    }
  ],
  priorKnowledge: [
    {
      id: "prior_id",
      label: "Existing Concept",
      // These are things Nick already knew that new concepts were anchored to
    }
  ],
  connections: [
    {
      source: "concept_id",
      target: "concept_id_or_prior_id",
      label: "relationship description", // e.g., "enables", "contradicts", "builds on", "analogous to"
    }
  ],
  coreSummary: "The 1-2 sentence model Nick articulated at the end"
};
```

## Implementation Notes

- Use d3 force simulation for layout
- Import d3: `import * as d3 from 'd3'`
- Use React refs to manage the SVG container
- Node radius should scale slightly with connection count (more connected = more central)
- Edge labels should appear on hover or be positioned along the edge
- Use Tailwind for the legend and info panel, d3 for the graph itself
- Click a node to see its definition in a side panel or tooltip
- The map should be readable at a glance — if there are more than 12-15 nodes, consider grouping by sub-topic

## Color Palette (use CSS variables for theme compatibility)

```
Anchored nodes:  var(--color-emerald, #059669) with 20% opacity fill, full opacity stroke
Introduced nodes: var(--color-amber, #d97706) with 20% opacity fill, full opacity stroke
Flagged nodes:   var(--color-red, #dc2626) with 20% opacity fill, full opacity stroke
Prior knowledge: transparent fill, dashed stroke in var(--color-slate, #64748b)
Edges:           var(--color-slate, #94a3b8) at 40% opacity
Edge labels:     var(--color-slate, #64748b) at 70% opacity, small font
```

## Layout Guidance

- Graph takes 70% width, info panel takes 30%
- Info panel shows: title, date, core summary, and clicked node detail
- Legend at bottom of info panel
- Responsive: on narrow screens, info panel moves below graph
