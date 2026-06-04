# Phase 1: Project Setup Complete

## What We Just Built

You now have a **fully functional Python environment** with all the ML/AI packages you need to detect faces and eyes. Let me explain each part:

---

## Part 1: Virtual Environment (venv)

**What is it?** A isolated Python workspace that keeps your project dependencies separate from your system Python.

**Why?** 
- Prevents package conflicts with other projects
- Makes your project reproducible on any Windows machine
- Easy to delete and recreate

**How it works:**
```
venv/
  Scripts/          <- Where pip installs .exe files (python.exe, pip.exe, etc)
  Lib/python3.12/   <- Where actual Python packages live
  pyvenv.cfg        <- Config file
```

When you run `. venv/Scripts/activate`, your shell uses the Python and packages INSIDE this folder, not your system Python.

---

## Part 2: requirements.txt (Your Dependencies)

This file lists every package your project needs:

```
streamlit>=1.38.0       # Web UI framework (like Flask, but for ML apps)
opencv-python>=4.10.0   # Computer vision library - read/write/process images
mediapipe>=0.10.35      # Google's ML toolkit - pre-trained models for face/hand/pose detection
numpy>=2.0.0            # Fast array math (used by OpenCV and MediaPipe)
pillow>=10.0.0          # Image file handling (PNG, JPG, etc)
```

**Why these versions?** Windows + Python 3.12 have specific wheel files (pre-compiled binaries). These exact versions are guaranteed to work.

---

## Part 3: modules/face_detector.py (Your First AI Module)

This class wraps MediaPipe's face detection. Let's break it down:

```python
import mediapipe as mp
import cv2

class FaceDetector:
    def __init__(self):
        # Load MediaPipe's face landmarker model
        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = mp.tasks.vision.FaceLandmarker
        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Configure the model
        options = FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="models/face_landmarker.task"  # Pre-trained ML model
            ),
            running_mode=VisionRunningMode.IMAGE,  # Process images (not video)
            num_faces=1                            # Only detect 1 face (faster)
        )
        
        # Create the detector
        self.detector = FaceLandmarker.create_from_options(options)
```

**What's a .task file?** It's a pre-trained neural network that Google trained on thousands of faces. It's free and runs locally (no API calls, no cloud).

**Line by line:**
1. `BaseOptions()` - tells MediaPipe where the model file is
2. `FaceLandmarkerOptions()` - configuration (how many faces, which mode, etc)
3. `create_from_options()` - initializes the model in RAM

---

## Part 4: app.py (Streamlit Web UI)

```python
st.title("👁 Eye Site Calculator")        # Page title

detector = FaceDetector()                  # Create detector instance once

uploaded = st.camera_input("Take a photo") # Show camera widget

if uploaded:
    # Convert camera bytes to NumPy array
    bytes_data = uploaded.getvalue()
    np_array = np.frombuffer(bytes_data, np.uint8)
    
    # Decode JPEG/PNG to OpenCV image (BGR format)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Run face detection
    result = detector.detect(image)
    
    # Show results
    if result.face_landmarks:
        st.success("Face Detected")
        st.write(f"Faces Found: {len(result.face_landmarks)}")
    else:
        st.error("No Face Found")
    
    # Display image
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
```

**Key concepts:**
- `st.camera_input()` - opens device camera in browser
- `np.frombuffer()` - converts bytes to numpy array (raw pixel data)
- `cv2.imdecode()` - decompresses JPEG to image array
- `cv2.cvtColor()` - converts BGR (OpenCV) → RGB (Streamlit expects this)

---

## How to Run Phase 1

**Windows PowerShell or Git Bash:**
```bash
cd c:\Users\YourName\Documents\EyeSiteCalculator
. venv\Scripts\activate
streamlit run app.py
```

**It will:**
1. Start a local web server (http://localhost:8501)
2. Open your browser automatically
3. Show camera widget + results

---

## What's Installed on Your Machine

```
pip list (inside venv):
- streamlit (web UI)
- opencv-python (image processing)
- opencv-contrib-python (extra OpenCV features)
- mediapipe (face detection model)
- numpy (fast math)
- pillow (image file I/O)
- + 30+ dependencies of the above
```

None of these are on your system Python. They live ONLY in `venv/Lib/python3.12/site-packages/`.

---

## Key Terms Explained

| Term | Meaning |
|------|---------|
| **venv** | Virtual environment - isolated Python workspace |
| **pip** | Package manager - downloads and installs Python packages |
| **wheels** | Pre-compiled Python packages (much faster than source) |
| **.task file** | Pre-trained neural network (MediaPipe format) |
| **NumPy array** | Fast array of numbers (shape: height × width × 3 channels) |
| **OpenCV** | Library for image: read, write, process, display |
| **MediaPipe** | Google's ML library - face/hand/pose detection |
| **Streamlit** | Turn Python scripts into interactive web apps in seconds |

---

## Next Steps (Phases 2-7)

1. **Phase 2:** Eye Health Detection (redness, dryness)
2. **Phase 3:** Visual Acuity Test (Snellen chart)
3. **Phase 4:** Color Blindness Test (Ishihara plates)
4. **Phase 5:** Face Shape Detection
5. **Phase 6:** Glasses Recommendations
6. **Phase 7:** Virtual Try-On (AR overlay)

---

## Files Created/Modified This Phase

- `requirements.txt` - Python dependencies (created)
- `venv/` - Virtual environment (created/fixed)
- Verified `app.py` works ✓
- Verified `modules/face_detector.py` works ✓
- Verified `models/face_landmarker.task` exists ✓

---

**You're now ready to test the app and move to Phase 2!**
