# Statistics explainer review: the which-sigma checklist

What four review gates found on a Cpk explainer, turned into a gate. Use it on any piece that explains an index, a test, or a chart your reader computes for a living: Cpk and Ppk, control-chart rules, a t-test, a tolerance interval.

## The failure it prevents

The reader who computes this index every week reads one sentence that gets the statistics wrong and stops trusting the rest. My draft said Cpk describes the process "when nothing changes between batches." With one result per batch, the within-subgroup standard deviation comes from the moving range between consecutive batches. Batch-to-batch noise is in it. The sentence was wrong for exactly the data a biologics reader has, and it read fine to everyone who does not compute Cpk.

## Before drafting

- [ ] Write down the reader's data structure. Subgroups of several results, or one result per batch? Every formula and every "what it captures" sentence depends on it.
- [ ] Name a source for each formula, threshold, and table before the outline. A standards handbook first (NIST/SEMATECH), then a statistics vendor's documentation, then everything else.
- [ ] Check your own product's source of truth before the outline. If the product does not compute the index, the outline cannot assume it does.

## Which sigma

- [ ] Every formula says which standard deviation goes in it. Within-subgroup for Cp and Cpk, overall for Pp and Ppk. Say it next to the formula, not three sections later.
- [ ] Say how the within-subgroup value is estimated for the reader's data. Subgroups: average range over d2, or average standard deviation over c4. One result per batch: average moving range over 1.128.
- [ ] Describe what each value captures in the reader's terms. With one result per batch, within-subgroup captures batch-to-batch noise and changes little with slow drift. Overall adds the drift and the shifts.
- [ ] A spreadsheet example names its function's standard deviation. `STDEV.S` is the overall one, so that formula gives Ppk, not Cpk. Say so in the same sentence.

## One-sided limits

- [ ] One-sided limits get one-sided indices: Cpu or Cpl, Ppu or Ppl. Give a domain example of each. An impurity maximum is upper only. A purity minimum is lower only.
- [ ] Never compute a two-sided index against a limit the specification does not have.

## Thresholds

- [ ] Treat every threshold as a convention until a regulation's own text says otherwise. Find where it came from. The widely quoted 1.33 and 1.67 come from automotive supplier practice.
- [ ] Search the regulation's full text for the index name before writing what it requires. If it names no index or number, write that, and quote what it does ask for.
- [ ] No "many sites," "most companies," or "the industry standard" without a source. Cut the line or source it.

## Sample size

- [ ] Give a minimum from a named source, then the reader's reality. NIST puts the minimum at about 50 values and recommends 100 or more; a young biologics process may have far fewer batches.
- [ ] Every example obeys the post's own advice. My first spreadsheet example used 39 values, under the minimum the post had just stated. It became 100.
- [ ] Tell the reader to report the sample size with the index.

## Distribution and stability

- [ ] Say that all four indices assume normal data, Pp and Ppk included. A draft that only warns about Cpk implies Ppk is safe.
- [ ] Name the fix for non-normal data (a transformation, or an index made for non-normal data) and say that indices from the two are not comparable.
- [ ] Stability before capability. The control chart comes first, in the text and in the how-to steps.

## Arithmetic

- [ ] Recompute every number in code: worked examples, per-million tables, "1.33 times 3 is 4."
- [ ] Copy table values exactly as the source prints them. NIST's table row is 1.66, not 1.67.
- [ ] Label made-up numbers as illustrative.
- [ ] Check that every picture matches the math, including the thumbnail. The accented gap must be the nearer one.

## Before publishing

- [ ] Run the cold-read grader with a persona who computes this index weekly, and ask it to check each formula and each sigma against the reader's data structure.
- [ ] Re-run the gate on every line you fixed. A fix to one statistics sentence can break the next one.

## Words that signal the failure

"When nothing changes," "short-term" with no explanation of what that means for the reader's data, "always," "required," "the standard is," "industry standard," "most sites."
