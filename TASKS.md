# TASKS.md — OptiKinesis

Temporary progress and handoff notes. Update before finishing or handing off.
Durable knowledge belongs in `PROJECT_CONTEXT.md`.

## Current state

All features described in `README.md` are implemented, including the TinyFish
Web panel (answer cards and the clean reader), word suggestions and voice
typing on the on-screen keyboard.

## Verification

- `$env:PYTHONDONTWRITEBYTECODE="1"; .\.venv\Scripts\python.exe -m unittest discover`:
  Ran 79 tests, OK.
- The TinyFish Search and Fetch APIs were verified with a real key. Voice
  recognition was verified with synthesized speech.

**Not yet verified:** a full session with a real user under head tracking,
covering calibration feel, the Web panel and voice typing with live speech.

## Next steps

1. Run a real-user session and record the results here.
2. Decide the default number of blinks per click (currently 1).
3. Make each SOS action report real success or failure.
