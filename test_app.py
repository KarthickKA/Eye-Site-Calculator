import cv2
import numpy as np
from modules.face_detector import FaceDetector
from modules.eye_health import EyeHealthAnalyzer
from modules.visual_acuity import VisualAcuityTest
from modules.color_blindness import ColorBlindnessTest
from modules.face_shape import FaceShapeDetector
from modules.glasses_recommender import GlassesRecommender
from modules.virtual_tryon import VirtualGlassesOverlay
import os

print("=" * 80)
print("EYE SITE CALCULATOR - COMPREHENSIVE TEST SUITE")
print("=" * 80)

test_results = {
    'Phase 1: Face Detection': None,
    'Phase 2: Eye Health': None,
    'Phase 3: Visual Acuity': None,
    'Phase 4: Color Blindness': None,
    'Phase 5: Face Shape': None,
    'Phase 6: Glasses Recommendations': None,
    'Phase 7: Virtual Try-On': None
}

detector = FaceDetector()
eye_analyzer = EyeHealthAnalyzer()
color_test = ColorBlindnessTest()
face_shape_detector = FaceShapeDetector()
glasses_recommender = GlassesRecommender()
glasses_overlay = VirtualGlassesOverlay()

print("\n1. Testing Phase 1: Face Detection")
print("-" * 80)

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("ERROR: Camera not available. Skipping camera-based tests.")
    print("Creating synthetic face image instead...")

    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 200
    cv2.putText(test_image, "Unable to use camera", (150, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    print("SKIP: Camera-based testing requires live camera")
    test_results['Phase 1: Face Detection'] = "SKIP - No camera"
else:
    print("Camera detected. Capturing test image...")
    ret, test_image = camera.read()
    camera.release()

    if ret:
        print(f"[OK] Test image captured: {test_image.shape}")

        face_landmarks = detector.detect(test_image)

        if face_landmarks.face_landmarks:
            num_faces = len(face_landmarks.face_landmarks)
            num_landmarks = len(face_landmarks.face_landmarks[0])
            print(f"[OK] Face detection PASSED")
            print(f"  - Faces detected: {num_faces}")
            print(f"  - Landmarks per face: {num_landmarks}")
            test_results['Phase 1: Face Detection'] = "PASS"

            print("\n2. Testing Phase 2: Eye Health Analysis")
            print("-" * 80)
            try:
                eye_results = eye_analyzer.analyze(test_image, face_landmarks)
                print(f"[OK] Eye Health Analysis PASSED")
                print(f"  - Redness Level: {eye_results['redness_level']}%")
                print(f"  - Dryness Level: {eye_results['dryness_level']}%")
                print(f"  - Pupil Symmetry: {eye_results['pupil_symmetry']}%")
                test_results['Phase 2: Eye Health'] = "PASS"
            except Exception as e:
                print(f"[FAIL] Eye Health Analysis FAILED: {str(e)[:100]}")
                test_results['Phase 2: Eye Health'] = f"FAIL - {str(e)[:50]}"

            print("\n3. Testing Phase 5: Face Shape Detection")
            print("-" * 80)
            try:
                shape_results = face_shape_detector.detect_shape(test_image, face_landmarks)
                print(f"[OK] Face Shape Detection PASSED")
                print(f"  - Face Shape: {shape_results['shape']}")
                print(f"  - Confidence: {shape_results['confidence']}%")
                print(f"  - Measurements:")
                for key, value in list(shape_results['measurements'].items())[:3]:
                    print(f"    - {key}: {value:.1f}")
                test_results['Phase 5: Face Shape'] = "PASS"

                print("\n6. Testing Phase 6: Glasses Recommendations")
                print("-" * 80)
                try:
                    rec_results = glasses_recommender.recommend(shape_results['shape'])
                    print(f"[OK] Glasses Recommendations PASSED")
                    print(f"  - Face Shape: {shape_results['shape']}")
                    print(f"  - Recommended Frames: {', '.join(rec_results['recommendations'])}")
                    print(f"  - Reason: {rec_results['reason']}")
                    test_results['Phase 6: Glasses Recommendations'] = "PASS"
                except Exception as e:
                    print(f"[FAIL] Recommendations FAILED: {str(e)[:100]}")
                    test_results['Phase 6: Glasses Recommendations'] = f"FAIL"

                print("\n7. Testing Phase 7: Virtual Try-On (AR)")
                print("-" * 80)
                try:
                    frame_types = ['rectangular', 'round', 'cat_eye']
                    for frame_type in frame_types:
                        result = glasses_overlay.overlay_glasses(test_image, face_landmarks, frame_type)
                        print(f"[OK] Frame style '{frame_type}' applied successfully")
                    print(f"[OK] Virtual Try-On PASSED")
                    print(f"  - Tested {len(frame_types)} frame styles")
                    test_results['Phase 7: Virtual Try-On'] = "PASS"
                except Exception as e:
                    print(f"[FAIL] Virtual Try-On FAILED: {str(e)[:100]}")
                    test_results['Phase 7: Virtual Try-On'] = f"FAIL"

            except Exception as e:
                print(f"[FAIL] Face Shape Detection FAILED: {str(e)[:100]}")
                test_results['Phase 5: Face Shape'] = f"FAIL"
        else:
            print("[FAIL] No face detected in test image")
            print("  Suggestion: Ensure your face is clearly visible and well-lit")
            test_results['Phase 1: Face Detection'] = "FAIL - No face detected"
    else:
        print("[FAIL] Failed to capture image from camera")
        test_results['Phase 1: Face Detection'] = "FAIL - Camera error"

print("\n3. Testing Phase 3: Visual Acuity Test")
print("-" * 80)
try:
    acuity_test = VisualAcuityTest()
    chart = acuity_test.create_snellen_chart(0)
    print(f"[OK] Snellen Chart Generation PASSED")
    print(f"  - Chart size: {chart.shape}")
    print(f"  - Chart created for all lines: {len(acuity_test.snellen_lines)} lines available")
    test_results['Phase 3: Visual Acuity'] = "PASS"
except Exception as e:
    print(f"[FAIL] Visual Acuity FAILED: {str(e)[:100]}")
    test_results['Phase 3: Visual Acuity'] = f"FAIL"

print("\n4. Testing Phase 4: Color Blindness Test")
print("-" * 80)
try:
    cb_test = ColorBlindnessTest()
    for i in range(len(cb_test.plates)):
        plate = cb_test.create_ishihara_plate(i)
        if plate is not None and plate.size > 0:
            print(f"[OK] Ishihara Plate {i+1} created: {plate.shape}")
    print(f"[OK] Color Blindness Test PASSED")
    print(f"  - Total plates: {len(cb_test.plates)}")
    test_results['Phase 4: Color Blindness'] = "PASS"
except Exception as e:
    print(f"[FAIL] Color Blindness Test FAILED: {str(e)[:100]}")
    test_results['Phase 4: Color Blindness'] = f"FAIL"

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for v in test_results.values() if v and v.startswith("PASS"))
failed = sum(1 for v in test_results.values() if v and v.startswith("FAIL"))
skipped = sum(1 for v in test_results.values() if v and v.startswith("SKIP"))

for phase, result in test_results.items():
    status = "[OK]" if result and result.startswith("PASS") else "[FAIL]" if result and result.startswith("FAIL") else "[SKIP]"
    print(f"{status} {phase}: {result}")

print("\n" + "=" * 80)
print(f"TOTAL: {passed} PASSED, {failed} FAILED, {skipped} SKIPPED out of {len(test_results)} phases")
print("=" * 80)

if failed == 0:
    print("\n[OK] ALL TESTS PASSED! App is ready to use.")
else:
    print(f"\n[WARN] {failed} test(s) failed. See details above.")

print("\nTo run the Streamlit app:")
print("  streamlit run app.py")
print("\n" + "=" * 80)
