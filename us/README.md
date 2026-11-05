# Civics 128 — US civics test study kit (2025 version)

Independent study kit for the 2025 civics test: all 128 USCIS questions as audio, a printable
PDF with 5 timed practice tests, and free reference pages.

Live site: https://skeeder1.github.io/civics-128/

## What is in this repository

- `index.html` — product page
- `questions/` — all 128 questions with the acceptable answers
- `practice-test/` — free 20-question scored practice test (runs in the browser)
- `audio/` — what the audio kit contains and a free 4-question excerpt
- `passing-score/`, `65-20/`, `study-plan/` — reference pages
- `sitemap.xml`, `robots.txt` — indexing

The paid files (7 MP3 themes, 31-page PDF, 5 practice tests) are **not** in this repository. They are
delivered after checkout. The excerpt and a 4-page PDF sample are free here.

## Sources and licences

- **Questions and acceptable answers**: USCIS form M-1778 (09/25), *128 Civics Questions and Answers
  (2025 version)*, https://www.uscis.gov/sites/default/files/document/questions-and-answers/2025-Civics-Test-128-Questions-and-Answers.pdf — published by the U.S. government, public domain.
- **Scoring rules and 65/20 exception**: USCIS Policy Alert PA-2025-24 (20 Oct 2025) and the
  M-1778 text published by USCIS.
- **Everything else** (audio narration, practice tests, distractor options, page copy, design) is
  original to this kit.

This kit is **not affiliated with, endorsed by, or connected to** USCIS, DHS or any government
agency. It is not a government document. The questions themselves are free at uscis.gov; you pay for the
audio version and the practice tests, not for access to the questions.

## Answers that change

The President, Vice President, Speaker of the House and Chief Justice change with elections and
appointments; your senators, representative, governor and state capital depend on where you live.
They are flagged everywhere in this kit and were last checked on 5 November 2026.
Official updates: https://www.uscis.gov/citizenship/testupdates

## Rebuilding

The site is generated from the USCIS list — no question text is typed by hand:

```
cd src
python3 parse_official.py   # USCIS PDF text -> q_official.json (asserts 128 questions)
python3 build_q.py          # cleaning + distractor checks -> q.json
python3 build_audio.py      # 7 MP3 themes + excerpt (edge-tts, en-US)
python3 build_pdf.py        # 31-page printable PDF
python3 build_sample.py     # 4-page free sample
python3 build_site.py       # pages, sitemap, robots
```
