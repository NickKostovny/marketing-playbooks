# Recipe: cut share-ready clips from a long recording

Uses `tools/clip-cutter/`. About two minutes per clip on a laptop, most of it the speech model.

## 1. Transcribe the whole recording once

```bash
ffmpeg -i recording.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le work/source-16k.wav
whisper-cli -m work/models/ggml-small.en.bin -f work/source-16k.wav -l en -osrt -otxt -of work/transcript
```

Read the text transcript, not the video. Mark candidate moments with the approximate timestamp from the SRT.

## 2. Pick the moments

A clip is one idea, 60 to 90 seconds, that stands without the slides. Good signs: a question from the audience and its answer, a line the speaker repeats, a claim with a reason attached. Skip anything that needs the previous slide to make sense.

For each moment, write down: the speaker, a title in the speaker's words, a rough start and end, the first few words the clip should open on, and the last few words it should close on.

## 3. Write the spec

`clips.json`, one object per clip. See the docstring at the top of `precise-cuts.py`. Add a `fixes` list for domain terms the speech model gets wrong; read the first draft subtitles to find them.

Mark every clip of a person outside your company `"hold_for_consent": true`. Cut them anyway, so the ask can include the finished file.

## 4. Run

```bash
./render-all.sh clips.json out/ --brand "Company" --logo logo.png --logo-light logo-light.png \
  --footer "From the September webinar" --cta-url "example.com/page" \
  --end-line "1 h 34 min. Both talks and the audience Q&A." --end-line "Work email required."
```

Outputs per clip: `out/<id>.mp4` and `out/<id>-contact.png`, a contact sheet with one frame every five seconds.

## 5. Check

- Open every contact sheet. Look for a subtitle that runs off the card, a frame of the wrong speaker, or a stray token in the text.
- Play the first and last two seconds of each clip. The tool extends the end to the close of the sentence; make sure it did not extend into the next speaker.
- Loudness is normalised to -14 LUFS, stereo. Check one clip on phone speakers.

## 6. Post

Each clip is a separate post. The clip is the free sample; the end card sends people to the gated page. The page link goes in the first comment, not the body. Held clips wait for a yes.
