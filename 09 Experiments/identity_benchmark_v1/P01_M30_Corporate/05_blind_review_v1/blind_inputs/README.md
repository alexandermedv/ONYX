# Blind inputs

No image files are copied into this directory. `blind_mapping.json` records immutable absolute source paths, and the local app reads each candidate only when its blind route is requested. This keeps the 36 source benchmark artifacts unchanged and avoids accidental duplicate or renamed candidate files.
