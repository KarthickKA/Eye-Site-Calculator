# Eye Site Calculator

A complete **eye health analysis** and **glasses recommendation system** built with Python, OpenCV, and MediaPipe. Analyze your eyes, get personalized glasses recommendations, and virtually try on frames — all **100% free and local** (no cloud APIs, no subscriptions).

> **Documentation**
> - [Knowledge Transfer (KT) Document](Documents/KT%20Document.md) — for developers taking over this project
> - [User Manual](Documents/User%20Manual.md) — for end users

## Features

### 1. Face Detection
Detect facial features using MediaPipe's 468-landmark face detection model. Foundation for all other features.

### 2. Eye Health Analysis
- **Redness Detection:** Identifies tired or irritated eyes
- **Dryness Detection:** Analyzes tear film quality
- **Pupil Symmetry:** Checks left-right pupil balance

### 3. Visual Acuity Test
Interactive Snellen chart test to measure vision quality (20/20, 20/40, etc.).

### 4. Color Blindness Test
Ishihara-style color blindness screening to detect:
- Normal color vision (trichromat)
- Red-green color blindness (protanopia/deuteranopia)
- Blue-yellow color blindness (tritanopia)

### 5. Face Shape Detection
Automatically classify your face shape:
- Oval
- Round
- Square
- Heart
- Oblong

### 6. Glasses Recommendations
Get personalized frame style recommendations based on your face shape:
- Cat-Eye
- Rectangular
- Round
- Clubmaster
- Wayfarer
- Browline
- And more!

### 7. Virtual Try-On (AR)
Try on virtual glasses frames in real-time. See how different styles look on your face before buying.

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Web UI** | Streamlit | Fast prototyping, no frontend needed |
| **Face Detection** | MediaPipe | Pre-trained 468-landmark model, no training required |
| **Image Processing** | OpenCV | Efficient, open-source, Windows-compatible |
| **Array Math** | NumPy | Fast numerical computations |
| **Image I/O** | Pillow | Handle PNG, JPEG, and other formats |

### Why No Cloud APIs?
- **Privacy:** All processing happens locally on your device
- **Speed:** No network latency, instant analysis
- **Cost:** 100% free, no subscriptions or API charges
- **Reliability:** Works offline after initial setup

---

## Prerequisites

- **OS:** Windows 11 (or Windows 10), macOS, Linux
- **Python:** 3.12
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 500MB for dependencies + models
- **Camera:** Built-in or USB webcam (required for photos)

## Installation

### Step 1: Get the Project

```bash
cd C:\Users\<your-user>\Documents\EyeSiteCalculator
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # On Windows
# source venv/Scripts/activate  # On macOS/Linux
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify the Model File

Ensure `models/face_landmarker.task` exists (about 3.7 MB). If missing:

```bash
cd models
curl -LO https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## Usage

### Basic Workflow

1. **Take a Photo**
   - Click the camera button
   - Allow browser access to camera
   - Click "Take Photo" to capture

2. **Select Feature**
   - Choose from 7 tabs at the top
   - Each tab shows different analysis

3. **Get Results**
   - View instant analysis and recommendations
   - Download results if available

### Feature-Specific Instructions

#### Eye Health Analysis
- Shows redness, dryness, and pupil symmetry scores
- Includes closeup views of eyes
- Provides health recommendations

#### Visual Acuity Test
- Click through progressively smaller letter sizes
- Select "I can read this" or "Too small"
- Get your visual acuity score (20/20, 20/40, etc.)

#### Color Blindness Test
- View 6 Ishihara color test plates
- Enter the number you see (or skip)
- Get diagnosis of color vision type

#### Face Shape & Recommendations
- Automatic face shape detection
- See measurement breakdown
- Get frame style recommendations
- Includes detailed descriptions

#### Virtual Try-On
- Select a frame style from dropdown
- See live preview on your face
- Try different styles instantly
- Download the result

---

## How to Test

Run the bundled CLI test suite (covers all 7 feature phases):

```bash
python test_app.py
```

Expected result: `7 PASSED, 0 FAILED`. If no camera is available, camera-dependent phases are skipped and the remaining phases still run.

Quick headless smoke test:

```bash
streamlit run app.py --server.headless=true --server.port=8501
# http://localhost:8501/_stcore/health  should return 200 "ok"
```

---

## Project Structure

```
EyeSiteCalculator/
├── app.py                           # Main Streamlit app (7 tabs)
├── test_app.py                      # CLI test suite for all 7 phases
├── requirements.txt                 # Python dependencies
├── PHASE_1_GUIDE.md                 # Phase 1 setup explainer
├── README.md                        # This file
├── venv/                            # Virtual environment (ignored by git)
├── models/
│   └── face_landmarker.task         # MediaPipe pre-trained model (3.7 MB)
├── modules/
│   ├── face_detector.py             # Phase 1: Face detection wrapper
│   ├── eye_health.py                # Phase 2: Eye health analysis
│   ├── visual_acuity.py             # Phase 3: Snellen chart test
│   ├── color_blindness.py           # Phase 4: Color blindness test
│   ├── face_shape.py                # Phase 5: Face shape detection
│   ├── glasses_recommender.py       # Phase 6: Frame recommendations
│   └── virtual_tryon.py             # Phase 7: AR glasses overlay
├── data/
│   └── glasses_styles.json          # Frame recommendations database
├── assets/                          # Reserved for UI assets
└── Documents/                       # Project documentation
    ├── KT Document.md               # Developer knowledge transfer
    └── User Manual.md               # End-user guide
```

---

## Configuration

### Modifying Glasses Recommendations
Edit `data/glasses_styles.json`:

```json
{
  "face_shape": ["Frame1", "Frame2", "Frame3"]
}
```

### Adding New Frame Styles
Edit `modules/virtual_tryon.py`, add method:

```python
def _draw_custom_frame(self, frame):
    # Your frame drawing code
    pass
```

Then add to `_create_frame()` method.

### Tuning Eye Health Thresholds
Edit `modules/eye_health.py`:

```python
red_lower1 = np.array([0, 100, 100])      # HSV lower bound for red
red_upper1 = np.array([10, 255, 255])     # HSV upper bound for red
```

---

## How It Works (Summary)

1. **Face Detection** — MediaPipe `FaceLandmarker` returns 468 landmarks per face.
2. **Eye Health** — eye regions are cropped from landmarks; redness via HSV red-mask ratio, dryness via Laplacian variance, pupil symmetry via Hough circles.
3. **Visual Acuity** — Snellen chart lines rendered with Pillow; the user steps down until "Too small".
4. **Color Blindness** — six synthetic Ishihara plates scored against known answers.
5. **Face Shape** — forehead/cheekbone/jaw widths and face length-to-width ratios classify the shape.
6. **Glasses Recommendations** — rule-based mapping from shape to frame styles.
7. **Virtual Try-On** — frame image sized from interpupillary distance, rotated to eye angle, alpha-blended over the photo.

---

## Troubleshooting

### "No face detected"
- Ensure good lighting (avoid backlighting)
- Position face straight toward camera
- Remove sunglasses or face obstructions
- Try a different angle

### "Camera not working"
- Check browser permissions (allow camera)
- Restart Streamlit app
- Try a different browser
- Verify camera is not in use by another app

### "Out of memory"
- Close other applications
- Reduce image size
- Increase available RAM

### "Model file not found"
The `face_landmarker.task` file should be in `models/`. See Installation Step 4 for the download command.

### "streamlit is not recognized"
Activate the virtual environment (`venv\Scripts\activate`) and confirm dependencies are installed (`pip install -r requirements.txt`).

### Port 8501 already in use
Run with `streamlit run app.py --server.port 8502`.

---

## Limitations & Future Work

### Current Limitations
- Detects only 1 face (can be extended to multiple)
- 2D frame overlay (not true 3D AR)
- Does not account for existing glasses (occlusion)
- Eye health metrics are heuristic, not a medical diagnosis

### Potential Improvements
- 3D face mesh for better geometry
- Support for multiple faces
- Integration with real 3D glasses models
- Machine learning for face shape confidence
- Prescription lens visualization
- Contact lens recommendation
- Eye disease detection (cataracts, glaucoma awareness)

---

## Deployment

- Runs as a local desktop web app; no deployment pipeline is required.
- Fully local, so the whole folder (including `models/`) can be copied to another machine with Python 3.12 and the venv.
- For public hosting, a Streamlit Community Cloud deployment or a VM works; note that camera access over the web requires HTTPS.

---

## Performance Notes

| Operation | Time | Hardware |
|-----------|------|----------|
| Face detection | 100-200ms | CPU (Intel i5, 8GB RAM) |
| Eye health analysis | 50-100ms | CPU |
| Face shape detection | 30-50ms | CPU |
| Frame overlay | 50-100ms | CPU |

All processing is CPU-based (no GPU required).

---

## FAQ

**Q: Is this medical diagnosis?**
A: No. This tool is for educational and entertainment purposes only. For actual eye health concerns, consult an optometrist or eye doctor.

**Q: Does it work on mobile?**
A: Yes! Streamlit works on mobile browsers. Just open the same URL on your phone.

**Q: Can I use my own images instead of camera?**
A: Currently, only camera input is supported. You can modify `app.py` to add file upload:
```python
uploaded_file = st.file_uploader("Upload image", type=['jpg', 'png'])
if uploaded_file:
    image = cv2.imdecode(...)
```

**Q: Can I run this offline?**
A: Yes! After initial setup, everything runs locally without internet.

**Q: How accurate are the results?**
A: Accuracy varies by image quality, lighting, and angles. Use as a guide, not medical diagnosis.

---

## License

MIT License — Free to use, modify, and distribute.

**Made for eye health awareness. Completely free and open source.**
