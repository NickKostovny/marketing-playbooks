# Technical content review: the incumbent-posture checklist

What a product manager with an engineering background taught me in one 20-minute call, turned into a gate. Use it on any piece that names a protocol, a standard, or a system your reader already runs.

## The failure it prevents

A technical reader who owns the incumbent tool reads one line that misdescribes it, or one line that tells them to rip it out, and discounts the entire product before the second paragraph. Engineers read nuance and decide fast. That is a bad behavior and a real one.

## Before drafting

- [ ] Name the reader's incumbent tool (historian, LIMS, ELN, spreadsheet, homegrown script). Write down what it does well. That list goes in the piece first.
- [ ] Decide the message at the product level, not the protocol level. "We read whatever interface a system already exposes" beats "we use protocol X."
- [ ] Pull the product's own integration list and check every vendor-to-protocol claim against it. My own LinkedIn post had one wrong.

## While drafting

- [ ] Credit the incumbent before locating the friction. "A historian does its job well. It is the plant's long-retention record." Then say precisely where the time goes.
- [ ] Locate friction in a task, not in a system. Not "the historian is the problem" but "getting a complete, batch-labeled record of a run into the analysis tool."
- [ ] Hedge every mechanism claim to what is defensible. Compression is a setting. Batch context exists in some historians and is often unconfigured. Write it that way.
- [ ] End sections on data availability or the reader's outcome, never on skipping a system.
- [ ] Give the reader a personal win, including the person who gets asked to pull the data.
- [ ] Say the protocol is one path among several, and that the reader does not have to operate it.

## Before publishing

- [ ] Run the cold-read grader with the incumbent tool written into the persona.
- [ ] Send the draft to a domain reviewer in a public channel with no one-hour deadline. Reviewers who gate technical content are busy; a weekly rhythm beats "posting tomorrow."
- [ ] Test the reviewer's SEO hypotheses with data before adopting them. Ten minutes settles most of them.

## Words that trigger the failure

"Instead of," "bypass," "skip," "versus," "legacy," "no longer need," "without the historian." Each one implies the reader made a bad choice.
