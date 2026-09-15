# P01 blind review v1

This is a local, read-only presentation layer for the 36 official P01 qualifier outputs: 12 participants across BUS_01, BUS_06 and BUS_09. It does not generate, copy, resize, crop, normalize or otherwise modify benchmark images.

`blind_mapping.json` is the secret fixed mapping, generated with seed `20260912`. The browser receives only scene, candidate letter and image bytes; it has no route that exposes model names, source paths or the mapping. The score file contains no model name.

FLUX Kontext uses its effective qualifier: original `flux_kontext_qualifier_v1` for BUS_01 and `flux_kontext_repair_v1` for BUS_06/BUS_09. Ideogram uses the three official `P01_BUS_*_IDEOGRAM.jpg` files; its raw batches are excluded.

## Run

```powershell
& 'C:\Users\ME\miniconda3\envs\onyx_qa\python.exe' .\app\app.py --port 8765
```

Open `http://127.0.0.1:8765`. Use `I`, `R`, `S`, or `C` to select a score row, `1`–`5` to set its score, and `Enter` to save and proceed. Clicking an image opens it at browser scale only.

Scores are atomically written to `blind_review_scores.csv` after every save. `Finish review` is accepted only after all 36 entries have complete ratings; it records a completion marker and does not reveal the mapping or create rankings.

## Verification

```powershell
& 'C:\Users\ME\miniconda3\envs\onyx_qa\python.exe' .\app\build_review.py --verify
& 'C:\Users\ME\miniconda3\envs\onyx_qa\python.exe' .\app\test_blind_review.py
```
