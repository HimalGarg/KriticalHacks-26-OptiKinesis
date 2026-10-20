<div align="center">

# OptiKinesis

### Hands-free computer control with an ordinary webcam

Move your head to move the cursor. Blink to click. Speak or type with a gaze-friendly keyboard.
Find answers and read the web in large, clean text, powered by **TinyFish**.

**Head-pose cursor** · **Blink-to-click** · **5-point calibration** · **Smart keyboard** · **Voice typing** · **TinyFish web reader** · **Emergency SOS**

</div>

---

## Why

People living with ALS, spinal cord injuries, cerebral palsy and other motor
conditions often keep full use of their minds but lose the use of their hands.
Specialist eye-tracking hardware is expensive and hard to get. OptiKinesis turns
the webcam that is already in a laptop into a complete hands-free input system,
with no extra hardware.

---

## Features

| Feature | What it does |
|---|---|
| **Head-pose cursor** | MediaPipe Face Landmarker tracks 478 facial points. The direction your head points moves the OS cursor, smoothed so it stays steady. |
| **5-point calibration** | On first launch you turn comfortably toward five dots: the center and each corner. The cursor map is fitted to your own range of movement, even if you can turn further one way than the other. **F9** re-centers in one step. |
| **Blink-to-click** | A deliberate blink clicks where you were pointing. Very short and very long eye closures are ignored, and a short lock after each click prevents double clicks. |
| **Floating control pill** | A small always-on-top pill shows live tracking status and expands into large Voice, Keyboard, Camera, Web, SOS and Settings buttons. It never steals focus from the app you're using. |
| **Smart on-screen keyboard** | Full QWERTY that types into whatever app is in front. A **word suggestions** row finishes words in one blink, and a **Speak** button turns speech into text. |
| **Web: Find answers** | Ask a question by typing or speaking and see the top results as big, blink-friendly cards. *(TinyFish Search)* |
| **Web: Read this page** | Turns the page open in your browser into large, clean, ad-free text with big scroll and text-size buttons. *(TinyFish Fetch)* |
| **Voice commands** | "find …", "what is …", "read this page", reminders, alarms and email. |
| **Emergency SOS** | WhatsApp message, call via Twilio, or dial emergency numbers, each needing a deliberate double activation. |
| **Caregiver safety** | **F12** pauses everything, moving the mouse into a screen corner stops cursor control, and **Esc** cancels calibration. |

---

## TinyFish integration

[TinyFish](https://tinyfish.ai) provides web infrastructure for AI agents.
OptiKinesis uses two of its APIs to make the web usable for someone who clicks
by blinking, where every click costs effort.

### What it powers

**1. Find answers (TinyFish Search API)**

A normal search page needs many precise clicks: the search box, scrolling,
dodging ads and picking a link. In OptiKinesis the user says or types a
question, and the **Search API** returns structured results. They're shown as six
large cards with the site, title and a short preview. One blink on a card opens
that page in the reader.

**2. Read this page (TinyFish Fetch API)**

Cookie banners, pop-ups and tiny text are hard to deal with using head movement
and blinks. "Read this page" takes the address of the page open in the browser.
The **Fetch API** returns its main content as clean markdown, which OptiKinesis
shows in a large-print reader. Big **Up / Down** buttons scroll, **A+ / A−**
change the text size, and the size is remembered.

### How it works

```
 Question (typed or spoken)                Page open in Chrome / Edge / Brave / Firefox
            │                                              │
            ▼                                              ▼
 GET  https://api.search.tinyfish.ai        address copied from the browser
      ?query=…                                (only when a browser is in front;
            │                                  clipboard restored afterwards)
            │                                              │
            ▼                                              ▼
   JSON results: title, url,                 POST https://api.fetch.tinyfish.ai
   snippet, site_name                             { "urls": [...], "format": "markdown" }
            │                                              │
            ▼                                              ▼
   Large answer cards  ── blink on a card ──▶  Clean markdown ──▶ large-print reader
```

* **Client:** [`web_assist.py`](web_assist.py) calls the REST endpoints with
  `requests` and an `X-API-Key` header. It doesn't use the official SDK,
  because that SDK needs Python 3.11+ while MediaPipe pins this project to
  Python 3.10.
* **Reader cleanup:** images, link targets and stray HTML are removed, so the
  reader shows readable text only.
* **UI:** the `WebPanel` class in [`desktop_overlay.py`](desktop_overlay.py)
  runs requests on a background thread, so the overlay never freezes. Every
  control is a large, blink-clickable button.
* **Voice:** spoken searches such as "find wheelchair ramps near me" or
  "what is ALS", and "read this page", go straight to the Web panel.
* **Errors in plain language:** rate limits, pages that need a login, blocked
  sites and lost connections each show a clear message instead of failing
  silently.
* **Graceful fallback:** without an API key, the panel explains how to enable
  it, and voice searches open Google in the browser instead.

### Setup

1. Create an API key at <https://agent.tinyfish.ai/api-keys>.
2. Add it to `.env` (copy `.env.example` first):
   ```
   TINYFISH_API_KEY=your-key-here
   ```
3. Restart OptiKinesis. **Web** appears on the control pill.

Search and Fetch have free tiers: 30 searches and 150 pages per minute,
12,000 searches and 1,000 pages per day.

**Privacy:** search queries and page addresses are sent to TinyFish. Page
content is never uploaded from your machine, and pages behind a login can't be
read.

---

## How it works

```
Webcam ──▶ MediaPipe Face Landmarker (478 points)
              │                         │
              ▼                         ▼
     Head pose (yaw, pitch)     Eye openness (both eyes)
              │                         │
     5-point calibration map     Deliberate-blink detector
              │                         │
              ▼                         ▼
     Mouse mover (~65 Hz)       Click router: overlay button or OS click
              │                         │
              └──────────┬──────────────┘
                         ▼
              PyQt5 overlay (never takes focus)
     Pill · Keyboard · Camera · Web (TinyFish) · SOS · Settings
```

| Layer | Technology |
|---|---|
| Face tracking | MediaPipe Face Landmarker (Tasks API) |
| Camera and image processing | OpenCV |
| Overlay UI | PyQt5: frameless, translucent, always-on-top, non-activating windows |
| Cursor and keystrokes | PyAutoGUI |
| Web answers and reader | TinyFish Search and Fetch APIs |
| Voice typing | sounddevice and SpeechRecognition (Google web speech) |
| Optional browser dashboard | Flask |

---

## Getting started

**Requirements:** Windows, a webcam, and Python **3.10**.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env      # then fill in only the keys you need
.\.venv\Scripts\python.exe main.py
```

On first launch, follow the 5-point calibration: turn comfortably toward each
dot and hold still. Then move your head to move the cursor and blink to click.
By default a single deliberate blink clicks; this can be changed in Settings.

| Caregiver key | Action |
|---|---|
| **F9** | Re-center the cursor on the current head position |
| **F12** | Pause or resume control |
| **Esc** / **F12** | Cancel a running calibration |

Keystrokes typed through the on-screen keyboard never trigger these keys.

Optional browser dashboard (binds to `127.0.0.1` only):

```powershell
.\.venv\Scripts\python.exe main.py --web
```

**Optional integrations** (`.env`): `TINYFISH_API_KEY` for the Web panel,
Twilio for SOS calls, and SMTP for email voice commands.

---

## Tests

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
.\.venv\Scripts\python.exe -m unittest discover -v
```

The suite covers the blink detector, calibration math, TinyFish client (with
fake HTTP sessions), word suggestions, voice typing, voice commands, fatigue
monitor and web API.

---

## Project structure

```
├── main.py               # Entry point: camera loop, head pose, blinks, mouse mover, hotkeys, settings, Flask
├── desktop_overlay.py    # PyQt5 overlay: pill, keyboard, Web panel, calibration screen, click router
├── head_calibration.py   # 5-point calibration and personal head-angle → screen map
├── blink_detector.py     # Deliberate-blink state machine
├── web_assist.py         # TinyFish Search/Fetch client, reader cleanup, browser-address capture
├── word_suggestions.py   # Word completion for the on-screen keyboard
├── speech_input.py       # Voice typing for the keyboard's Speak button
├── voice_commands.py     # Voice command parsing and actions
├── fatigue_monitor.py    # Blink-rate fatigue monitor
├── templates/, static/   # Optional web dashboard
├── tests/                # unittest suites
└── face_landmarker.task  # MediaPipe face model
```

Developer notes for contributors and coding agents are in
[`AGENTS.md`](AGENTS.md), [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) and
[`OVERLAY_UI_MAP.md`](OVERLAY_UI_MAP.md).

---

## Privacy and safety

- Camera frames are processed in memory and never saved.
- Voice typing records only while the Speak button is active and sends that
  clip to Google's speech service. Audio is never stored.
- Word suggestions use a built-in word list and never learn what you type.
- API keys live in `.env`, which is never committed.
- Emergency actions need a deliberate second activation.
