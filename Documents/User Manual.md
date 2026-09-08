# Eye Site Calculator — User Manual

## What Is This?

Eye Site Calculator is a free web app that checks your eyes and helps you pick glasses. You take a selfie with your webcam and the app:

- Tells you how **tired, dry, or red** your eyes look.
- Runs a **vision test** (the classic letter chart) and a **color blindness test**.
- Detects your **face shape** (oval, round, square, heart, oblong).
- Suggests **glasses frame styles** that suit your face.
- Lets you **try on glasses virtually** on your own photo.

Everything happens on your computer — your photo is never uploaded to the internet.

> **Important:** This app is for fun and education only. It is **not a medical diagnosis**. For real eye concerns, visit an optometrist or eye doctor.

## System Requirements

- A Windows (10/11), Mac, or Linux computer.
- Python 3.12 installed (for running the app).
- A webcam (built-in or USB).
- A modern browser (Chrome, Edge, Firefox).

## Installation

1. Download or copy the project folder `EyeSiteCalculator` to your computer.
2. Open **Command Prompt** or **PowerShell** and go to the project folder:

   ```
   cd C:\Users\YourName\Documents\EyeSiteCalculator
   ```

3. Create the app environment (only the first time):

   ```
   python -m venv venv
   ```

4. Turn it on:

   - PowerShell: `venv\Scripts\activate`
   - Command Prompt: `venv\Scripts\activate.bat`

5. Install the required parts:

   ```
   pip install -r requirements.txt
   ```

> If a `venv` folder already exists (with the green "(venv)" shown in your terminal after activating), you can skip steps 3–4.

## How to Start the App

1. Make sure the virtual environment is active (you see `(venv)` in your terminal).
2. Run:

   ```
   streamlit run app.py
   ```

3. Your browser opens automatically at `http://localhost:8501`.

4. Click **"Take a photo to begin"** and allow the camera when asked.

## Using the App

The app has **7 tabs**. Take a photo first, then explore each tab.

### 1. Face Detection
- Shows whether a face was found and how many landmark points were detected.
- **Expected output:** a green "Face Detected" message, or a red "No face detected" warning.

### 2. Eye Health
- Shows three numbers as percentages:
  - **Redness Level** — how red/tired your eyes look.
  - **Dryness Level** — how dry your tear film appears.
  - **Pupil Symmetry** — how balanced your pupils are.
- Below the numbers you'll see close-up views of your left and right eye.
- **What the colors mean:** green = healthy, blue = moderate, orange = high.
- **Outputs:** a percentage for each metric plus a short tip (e.g., "consider rest and hydration").

### 3. Visual Acuity Test
- A letter chart appears (like the doctor's eye chart).
- Press **"I can read this"** to go to the next (smaller) line, or **"Too small"** to stop.
- **Expected output:** your score, e.g. **20/20** (normal) or **20/40**.
- **Restart Test** lets you begin again.

### 4. Color Blindness Test
- Six colored plates appear one at a time.
- Type the **number you see** in each plate, then press **Next Plate** (or **Skip**).
- **Expected output:** a score (e.g. 6/6) and your color vision type, such as "Normal Color Vision (Trichromat)".

### 5. Face Shape
- Shows a photo of you with a green outline around your face.
- **Expected output:** your face shape (Oval, Round, Square, Heart, or Oblong), a confidence percentage, and facial measurements.

### 6. Glasses Recommendations
- Based on your face shape, lists frame styles that suit you, e.g. "Cat-Eye", "Rectangular", "Wayfarer".
- Each style has a short description of why it works for you.

### 7. Virtual Try-On
- Pick a frame style from the drop-down list.
- The app draws those glasses onto your photo, positioned over your eyes.
- **Expected output:** your photo side-by-side with the glasses version.
- Press **"Download Image with Glasses"** to save the picture as a PNG.

## Common User Errors

| Problem | What to do |
|---|---|
| "No face detected" | Stand in bright light, look straight at the camera, remove sunglasses. |
| Camera button does nothing | Allow camera permission in the browser; close other apps using the camera. |
| Clicked "Take Photo" but no picture | Restart the app and try again. |
| App won't start ("command not found") | Activate the virtual environment first (step 4 above). |
| Page looks broken / slow | Refresh the page; close other heavy apps. |

## Troubleshooting

- **"streamlit is not recognized"** — you forgot to activate the virtual environment (`venv\Scripts\activate`), or dependencies weren't installed (`pip install -r requirements.txt`).
- **Port 8501 already in use** — run `streamlit run app.py --server.port 8502`.
- **Model file missing error** — the file `models\face_landmarker.task` must exist. If it's missing, re-download the project folder.

## Frequently Asked Questions

**Q: Is this a medical diagnosis?**
A: No. It is educational/entertainment only. See an eye doctor for real concerns.

**Q: Does my photo get uploaded anywhere?**
A: No. Everything runs locally on your computer.

**Q: Does it work on my phone?**
A: Yes — open the same address on your phone's browser. You'll need a front camera.

**Q: How accurate is the eye health analysis?**
A: It's a rough heuristic estimate based on pixel colors and textures. Use it as a guide, not a medical result.

**Q: Can I use my own photo file instead of the camera?**
A: Not yet — the current version uses the camera only.

## Important Notes and Limitations

- Only one face can be analyzed at a time.
- Virtual glasses are a flat 2D overlay, not true 3D.
- If you already wear glasses, the overlay may not look right over them.
- The color blindness and vision tests are simplified versions of clinical tests.
