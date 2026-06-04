# 👁 Eye Site Calculator

A complete **eye health analysis** and **glasses recommendation system** built with Python, OpenCV, and MediaPipe. Analyze your eyes, get personalized glasses recommendations, and virtually try on frames—all **100% free and local** (no cloud APIs, no subscriptions).

## Features

### 1. 📸 Face Detection
Detect facial features using MediaPipe's 468-landmark face detection model. Foundation for all other features.

### 2. 👁 Eye Health Analysis
- **Redness Detection:** Identifies tired or irritated eyes
- **Dryness Detection:** Analyzes tear film quality
- **Pupil Symmetry:** Checks left-right pupil balance

### 3. 📊 Visual Acuity Test
Interactive Snellen chart test to measure vision quality (20/20, 20/40, etc.).

### 4. 🎨 Color Blindness Test
Ishihara-style color blindness screening to detect:
- Normal color vision (trichromat)
- Red-green color blindness (protanopia/deuteranopia)
- Blue-yellow color blindness (tritanopia)

### 5. 👤 Face Shape Detection
Automatically classify your face shape:
- Oval
- Round
- Square
- Heart
- Oblong

### 6. 👓 Glasses Recommendations
Get personalized frame style recommendations based on your face shape:
- Cat-Eye
- Rectangular
- Round
- Clubmaster
- Wayfarer
- Browline
- And more!

### 7. 🥽 Virtual Try-On (AR)
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
- ✓ **Privacy:** All processing happens locally on your device
- ✓ **Speed:** No network latency, instant analysis
- ✓ **Cost:** 100% free, no subscriptions or API charges
- ✓ **Reliability:** Works offline after initial setup

---

## Installation

### System Requirements
- **OS:** Windows 11 (or Windows 10)
- **Python:** 3.12
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 500MB for dependencies + models

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/EyeSiteCalculator.git
cd EyeSiteCalculator
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
. venv\Scripts\activate  # On Windows
# or
source venv/Scripts/activate  # On macOS/Linux
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

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

## Project Structure

```
EyeSiteCalculator/
├── app.py                           # Main Streamlit app (7 tabs)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── PHASE_1_GUIDE.md                # Detailed Phase 1 explanation
│
├── venv/                            # Virtual environment (ignored by git)
│
├── models/
│   └── face_landmarker.task         # MediaPipe pre-trained model (3.7 MB)
│
├── modules/
│   ├── face_detector.py             # Phase 1: Face detection wrapper
│   ├── eye_health.py                # Phase 2: Eye health analysis
│   ├── visual_acuity.py             # Phase 3: Snellen chart test
│   ├── color_blindness.py           # Phase 4: Color blindness test
│   ├── face_shape.py                # Phase 5: Face shape detection
│   ├── glasses_recommender.py       # Phase 6: Frame recommendations
│   └── virtual_tryon.py             # Phase 7: AR glasses overlay
│
├── data/
│   └── glasses_styles.json          # Frame recommendations database
│
├── assets/
│   └── (reserved for UI assets)
│
└── .gitignore                       # Git ignore rules
```

---

## How It Works

### Phase 1: Face Detection
- Uses MediaPipe's FaceLandmarker to detect 468 facial landmarks
- Provides foundation for all downstream features
- Returns: face landmarks, face outline, feature positions

### Phase 2: Eye Health
- Extracts left and right eye regions from landmarks
- Analyzes HSV color space for red channel dominance (redness)
- Calculates texture variance using Laplacian (dryness)
- Detects pupils using Hough circles
- Compares pupil sizes for symmetry

### Phase 3: Visual Acuity
- Generates Snellen chart programmatically
- Displays progressively smaller letter sizes
- Tracks last readable line
- Returns visual acuity score (20/20, 20/40, etc.)

### Phase 4: Color Blindness
- Creates synthetic Ishihara test plates
- Uses color theory to generate plates
- Scores user answers against known correct answers
- Determines color vision type

### Phase 5: Face Shape
- Extracts key landmarks (face outline, jaw, cheekbone, forehead)
- Calculates geometric ratios:
  - Length vs width
  - Jaw width vs cheekbone width
  - Forehead vs jaw proportions
- Classifies face shape using rule-based logic

### Phase 6: Glasses Recommendations
- Looks up recommended frames for detected face shape
- Provides descriptions and reasoning
- Simple rule-based mapping (no ML needed)

### Phase 7: Virtual Try-On
- Calculates eye center positions from landmarks
- Determines frame size based on eye distance
- Calculates rotation angle from eye positions
- Creates frame shape (rectangular, round, cat-eye, etc.)
- Overlays and blends frame on image
- Handles rotation and positioning

---

## Key Algorithms Explained

### Redness Detection
```
1. Extract eye region
2. Convert BGR → HSV (Hue, Saturation, Value)
3. Create red color mask: H ∈ [0-10] ∪ [170-180]
4. Count red pixels / total pixels
5. Scale to 0-100 score
```

### Dryness Detection
```
1. Extract eye region
2. Convert to grayscale
3. Apply Laplacian edge detection
4. Calculate variance (low variance = dryness)
5. Invert: high variance = wet, low variance = dry
```

### Face Shape Classification
```
1. Extract 468 face landmarks
2. Calculate measurements:
   - Forehead width, Cheekbone width, Jaw width
   - Face length, Face width
3. Calculate ratios
4. Apply decision rules:
   - If length >> width → Oblong
   - If length ≈ width + other metrics → Square/Round/Heart
   - Else → Oval
```

### Virtual Try-On Positioning
```
1. Find left and right eye positions from landmarks
2. Calculate distance between eyes = frame width
3. Calculate rotation angle = atan2(right_eye - left_eye)
4. Create frame image in memory
5. Rotate frame by angle
6. Position at midpoint between eyes
7. Blend using alpha blending
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
red_lower = np.array([0, 100, 100])      # HSV lower bound for red
red_upper = np.array([10, 255, 255])     # HSV upper bound for red
```

---

## Limitations & Future Work

### Current Limitations
- Detects only 1 face (can be extended to multiple)
- 2D frame overlay (not true 3D AR)
- Does not account for existing glasses (occlusion)
- Limited test data for accuracy claims

### Potential Improvements
- [ ] 3D face mesh for better geometry
- [ ] Support for multiple faces
- [ ] Integration with real 3D glasses models
- [ ] Machine learning for face shape confidence
- [ ] Prescription lens visualization
- [ ] Contact lens recommendation
- [ ] Eye disease detection (cataracts, glaucoma awareness)

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
The `face_landmarker.task` file should be in `models/`. If missing:

```bash
cd models
wget https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

---

## Performance Notes

| Operation | Time | Hardware |
|-----------|------|----------|
| Face detection | 100-200ms | CPU (Intel i5, 8GB RAM) |
| Eye health analysis | 50-100ms | CPU |
| Face shape detection | 30-50ms | CPU |
| Frame overlay | 50-100ms | CPU |

All processing is CPU-based (no GPU required). Faster with newer CPUs or GPUs.

---

## Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- [ ] Improve face shape detection accuracy
- [ ] Add more frame styles
- [ ] Optimize performance
- [ ] Improve eye health analysis
- [ ] Better color blindness testing
- [ ] Documentation improvements

---

## License

MIT License - Free to use, modify, and distribute.

---

## Citation

If you use this project in research or publication:

```bibtex
@software{eyesitecalculator,
  title = {Eye Site Calculator},
  author = {Your Name},
  year = {2026},
  url = {https://github.com/yourusername/EyeSiteCalculator}
}
```

---

## Support

### Getting Help
- Check `PHASE_1_GUIDE.md` for detailed explanations
- Review inline code comments
- Check GitHub Issues for common problems
- Submit an issue with:
  - Error message (full traceback)
  - Steps to reproduce
  - System info (Python version, OS, RAM)

### Reporting Bugs
Create an issue with:
- Title: Brief description
- Description: What happened vs expected
- Reproduction: Steps to reproduce
- Screenshots: Visual proof (optional)

---

## Roadmap

### Version 1.0 (Current)
- ✅ Face detection
- ✅ Eye health analysis
- ✅ Visual acuity test
- ✅ Color blindness test
- ✅ Face shape detection
- ✅ Glasses recommendations
- ✅ Virtual try-on

### Version 1.1 (Q3 2026)
- [ ] Multiple face support
- [ ] Better frame positioning
- [ ] More frame styles
- [ ] Performance optimizations

### Version 2.0 (Q4 2026)
- [ ] 3D face reconstruction
- [ ] Eye disease awareness
- [ ] Prescription estimation
- [ ] Mobile app (React Native)

---

## Acknowledgments

- **MediaPipe:** Pre-trained models and face detection
- **OpenCV:** Image processing library
- **Streamlit:** Web app framework
- **NumPy/Pillow:** Supporting libraries

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

**Q: What's the frame overlay quality?**
A: Currently 2D overlay. For better results, consider updating to 3D face mesh in future versions.

**Q: Can I run this offline?**
A: Yes! After initial setup, everything runs locally without internet.

**Q: How accurate are the results?**
A: Accuracy varies by image quality, lighting, and angles. Use as a guide, not medical diagnosis.

---

**Made with ❤️ for eye health awareness. Completely free and open source.**

**[⭐ Star this project if you find it helpful!](https://github.com/yourusername/EyeSiteCalculator)**

