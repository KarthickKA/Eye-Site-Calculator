# Eye Site Calculator — KT Document

## Project Overview

Eye Site Calculator is a **web-based eye health analysis and glasses recommendation system**. It uses a webcam photo to detect the user's face, analyze eye health indicators (redness, dryness, pupil symmetry), run interactive vision tests (Snellen acuity and Ishihara color blindness), detect face shape, recommend glasses frame styles, and overlay virtual glasses frames on the user's face.

Everything runs **100% locally** — no cloud APIs, no account, no subscriptions. All processing is done on-device with pre-trained local models.

## Business Purpose

The app exists as an accessible, free, privacy-friendly tool that helps users:

- Get a quick, playful look at their eye health (educational/entertainment value, not a medical diagnosis).
- Self-screen for common vision issues (visual acuity, color blindness).
- Discover which glasses frame styles suit their face shape.
- Preview frames virtually ("try before you buy") without visiting a store.

## Main Features

1. **Face Detection** — MediaPipe 468-landmark face detection (foundation for everything else).
2. **Eye Health Analysis** — redness level, dryness level, pupil symmetry score, with left/right eye close-ups.
3. **Visual Acuity Test** — interactive Snellen chart that walks the user down progressively smaller letter lines and returns a 20/XX score.
4. **Color Blindness Test** — six synthetic Ishihara-style plates; answers are scored and a color-vision type is reported.
5. **Face Shape Detection** — classifies Oval, Round, Square, Heart, or Oblong from geometric facial measurements.
6. **Glasses Recommendations** — rule-based frame style suggestions per face shape with reasons and descriptions.
7. **Virtual Try-On (AR)** — overlays six frame styles (rectangular, round, cat_eye, clubmaster, wayfarer, browline) aligned to the detected eyes, with rotation and a downloadable result image.

## Technology Stack

| Component | Technology | Role |
|---|---|---|
| Web UI | Streamlit (1.58.x) | Interactive web app, camera capture, tabs |
| Face detection | MediaPipe FaceLandmarker (0.10.35) | 468 facial landmarks from a local `.task` model |
| Image processing | OpenCV (4.13) | Image decode, color analysis, drawing overlays |
| Array math | NumPy | Pixel-level computations |
| Image I/O | Pillow | Snellen / Ishihara plate rendering |
| Python | 3.12 (in `venv/`) | Runtime |

## Project Architecture

Single-page Streamlit app. `app.py` is the entry point; the camera photo is decoded with OpenCV and passed to a chain of independent `modules/` classes. Streamlit keeps all state in the browser session via `st.session_state`.

```
camera photo
   -> modules/face_detector.FaceDetector.detect(image)  -> FaceLandmarkerResult
   -> modules/eye_health.EyeHealthAnalyzer.analyze()    -> {redness, dryness, pupil_symmetry, eye crops}
   -> modules/face_shape.FaceShapeDetector.detect_shape() -> {shape, confidence, measurements, outline image}
   -> modules/glasses_recommender.GlassesRecommender.recommend(shape) -> {frames, reason, descriptions}
   -> modules/virtual_tryon.VirtualGlassesOverlay.overlay_glasses()  -> image with frames drawn
   -> modules/visual_acuity.VisualAcuityTest.run_test()   (self-contained interactive tab)
   -> modules/color_blindness.ColorBlindnessTest.run_test() (self-contained interactive tab)
```

## Folder / File Structure

```
EyeSiteCalculator/
├── app.py                      # Main Streamlit app (7 tabs)
├── test_app.py                 # CLI test suite for all 7 phases
├── requirements.txt            # Python dependencies
├── PHASE_1_GUIDE.md            # Setup/Phase 1 explainer (historical)
├── README.md                   # Project readme
├── venv/                       # Python 3.12 virtual environment (gitignored)
├── models/
│   └── face_landmarker.task    # MediaPipe pre-trained model (3.7 MB)
├── modules/
│   ├── __init__.py
│   ├── face_detector.py        # Phase 1: MediaPipe wrapper
│   ├── eye_health.py           # Phase 2: redness/dryness/pupil symmetry
│   ├── visual_acuity.py        # Phase 3: Snellen chart test
│   ├── color_blindness.py      # Phase 4: Ishihara plates test
│   ├── face_shape.py           # Phase 5: face shape classification
│   ├── glasses_recommender.py  # Phase 6: frame recommendations
│   └── virtual_tryon.py        # Phase 7: AR glasses overlay
├── data/
│   └── glasses_styles.json     # Frame style database (kept in sync with recommender)
└── Documents/                  # This documentation
    ├── KT Document.md
    └── User Manual.md
```

## Important Modules / Components

| Module | Class | Responsibility |
|---|---|---|
| `face_detector.py` | `FaceDetector` | Loads `models/face_landmarker.task`, converts BGR→RGB, runs `FaceLandmarker.detect`, returns the raw result object. |
| `eye_health.py` | `EyeHealthAnalyzer` | Extracts left/right eye crops from landmarks; HSV red-mask redness, Laplacian-variance dryness, Hough-circle pupil symmetry. All scores clamped to 0–100. |
| `visual_acuity.py` | `VisualAcuityTest` | Renders Snellen lines with Pillow; button-driven line progression stored in `st.session_state`. |
| `color_blindness.py` | `ColorBlindnessTest` | Draws 6 synthetic Ishihara plates as colored circle digits; tallies answers; classifies color vision. |
| `face_shape.py` | `FaceShapeDetector` | Computes forehead/cheekbone/jaw widths, face length/width, ratio-based classification into 5 shapes. |
| `glasses_recommender.py` | `GlassesRecommender` | Static lookup of frame styles + reasons per shape; falls back to 'unknown' recommendations. |
| `virtual_tryon.py` | `VirtualGlassesOverlay` | Computes eye centers + interpupillary distance, builds a 4-channel frame image, rotates it to face angle, alpha-blends it onto the photo. |

## Application Flow

1. User opens the app → Streamlit starts, model loads from disk.
2. User allows camera and takes a photo (`st.camera_input`).
3. Bytes are decoded to a BGR NumPy array.
4. Face detection runs once; the result is reused by every tab (analysis is not repeated per tab except face shape, which is re-run for the recommendation tab).
5. Each tab renders its results; interactive tests (acuity, color blindness) manage their own `st.session_state`.
6. Virtual try-on lets the user pick a frame style and download the composited PNG.

## Database Details

None. No database — no user data is stored or transmitted.

## APIs / Integrations

None. All functionality is local. The only external artifact is the MediaPipe model downloaded at setup time (`face_landmarker.task`).

## Environment Variables / Configuration

- No environment variables are required.
- `requirements.txt` pins dependency floors; the working `venv` already contains everything.
- The MediaPipe model path (`models/face_landmarker.task`) is relative to the project root — always run the app from the project root.

## Installation / Setup

```powershell
cd C:\Users\AardhraaAsus19\Documents\EyeSiteCalculator
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

The model file is expected at `models/face_landmarker.task`. If missing:

```powershell
cd models
curl -LO https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

## Build and Run Commands

There is no compile step for a Python app.

```powershell
venv\Scripts\python.exe -m streamlit run app.py
```

Opens at `http://localhost:8501`.

## Testing Instructions

Run the bundled CLI test suite from the project root:

```powershell
venv\Scripts\python.exe test_app.py
```

Covers all 7 phases. If a camera is present it captures a real frame; if not, camera-dependent phases are skipped and remaining phases still run. **Observed status (2026-08-14): 7/7 phases PASS.**

Headless smoke test of the web app:

```powershell
venv\Scripts\python.exe -m streamlit run app.py --server.headless=true --server.port=8501
# then:  Invoke-WebRequest http://localhost:8501/_stcore/health  -> 200 "ok"
```

## Deployment Information

- Runs as a local desktop web app; no deployment pipeline exists.
- Because it is fully local, it can be copied to any Windows machine with Python 3.12 + the venv and run as-is (models folder included).
- For sharing with others, host on a Streamlit Community Cloud / VM, but note camera access then requires HTTPS.
- A standalone Windows executable could be produced with PyInstaller, but this is not set up.

## Important Technical Decisions

- **Local-only processing**: no cloud APIs, preserving privacy and offline capability.
- **MediaPipe over a hand-rolled detector**: pre-trained 468-landmark model, no training data needed.
- **Rule-based face-shape classification**: geometric ratios instead of ML for transparency and zero training cost.
- **Synthetic Ishihara plates**: generated programmatically with Pillow so no image assets are required.
- **Reuse a single detection result** across tabs to keep the app fast and consistent.
- **Streamlit session state** for multi-step interactive tests.

## Common Issues and Troubleshooting

| Issue | Fix |
|---|---|
| "No face detected" | Better lighting, face straight to camera, remove sunglasses/obstructions. |
| Camera not working | Check browser permissions, restart the app, close other camera apps. |
| Model file not found | Ensure `models/face_landmarker.task` exists (download command above). |
| Deprecated `use_column_width` | Already replaced with `use_container_width` in `app.py`. |
| Out of memory | Close other apps, lower camera resolution. |
| MediaPipe XNNPACK / feedback-manager warnings on stderr | Harmless noise; ignore. |
| Port 8501 in use | Start with `--server.port=<other>` or stop the conflicting process. |

## Maintenance / Development Guidelines

- Add new frame styles by implementing a `_draw_<style>_frame()` method in `virtual_tryon.py` and registering it in `_create_frame()`.
- Tune eye-health thresholds at the top of `eye_health.py` (`red_lower1`, `red_upper1`, etc.).
- Keep `data/glasses_styles.json` in sync with `glasses_recommender.py` if either is changed.
- After changing any module, re-run `test_app.py`; keep all 7 phases passing.
- Do not commit the `venv/` folder or `__pycache__/` (already gitignored).

## Important Dependencies

- `streamlit>=1.38.0`
- `opencv-python>=4.10.0.84` (and `opencv-contrib-python` present in the venv)
- `mediapipe>=0.10.35`
- `numpy>=2.0.0`
- `pillow>=10.0.0`

## Known Limitations

- Detects only one face.
- Virtual try-on is a 2D overlay, not true 3D AR.
- Does not account for existing glasses (occlusion).
- Eye health metrics are heuristic (HSV masking, texture variance) and not a medical diagnosis.
- Synthetic Ishihara plates are simplified approximations of real plates.
- Accuracy varies with image quality, lighting, and angle.
