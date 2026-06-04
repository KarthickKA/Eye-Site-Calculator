import streamlit as st
import cv2
import numpy as np

from modules.face_detector import FaceDetector
from modules.eye_health import EyeHealthAnalyzer
from modules.visual_acuity import VisualAcuityTest
from modules.color_blindness import ColorBlindnessTest
from modules.face_shape import FaceShapeDetector
from modules.glasses_recommender import GlassesRecommender
from modules.virtual_tryon import VirtualGlassesOverlay

st.set_page_config(page_title="Eye Site Calculator", layout="wide")

st.title("👁 Eye Site Calculator")
st.write("A complete eye health analysis and glasses recommendation system. 100% free and local (no cloud APIs).")

detector = FaceDetector()
eye_analyzer = EyeHealthAnalyzer()
acuity_test = VisualAcuityTest()
color_test = ColorBlindnessTest()
face_shape_detector = FaceShapeDetector()
glasses_recommender = GlassesRecommender()
glasses_overlay = VirtualGlassesOverlay()


def process_camera_input(uploaded_file):
    """Convert Streamlit camera input to OpenCV image."""
    bytes_data = uploaded_file.getvalue()
    np_array = np.frombuffer(bytes_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image


tabs = st.tabs([
    "📸 Face Detection",
    "👁 Eye Health",
    "📊 Visual Acuity",
    "🎨 Color Blindness",
    "👤 Face Shape",
    "👓 Glasses Recommendations",
    "🥽 Virtual Try-On"
])

st.sidebar.write("---")
st.sidebar.write("### About")
st.sidebar.write(
    "Eye Site Calculator analyzes your eye health and recommends glasses frames based on your face shape. "
    "All processing is done locally on your device - no data is sent to any servers."
)

uploaded = st.camera_input("Take a photo to begin")

if uploaded:
    image = process_camera_input(uploaded)

    face_landmarks = detector.detect(image)

    with tabs[0]:
        st.subheader("Face Detection Results")

        if face_landmarks.face_landmarks:
            st.success("✓ Face Detected")
            st.write(f"Landmarks detected: {len(face_landmarks.face_landmarks[0])} points")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_column_width=True)
        else:
            st.error("✗ No face detected. Please ensure your face is clearly visible.")

    with tabs[1]:
        st.subheader("Eye Health Analysis")

        if face_landmarks.face_landmarks:
            results = eye_analyzer.analyze(image, face_landmarks)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Redness Level",
                    f"{results['redness_level']}%",
                    delta=None,
                    delta_color="normal"
                )
                if results['redness_level'] > 60:
                    st.warning("High redness detected. Consider rest and hydration.")
                elif results['redness_level'] > 30:
                    st.info("Moderate redness. Your eyes may be slightly tired.")
                else:
                    st.success("Low redness. Eyes look healthy!")

            with col2:
                st.metric(
                    "Dryness Level",
                    f"{results['dryness_level']}%",
                    delta=None,
                    delta_color="normal"
                )
                if results['dryness_level'] > 60:
                    st.warning("High dryness detected. Use eye drops and stay hydrated.")
                elif results['dryness_level'] > 30:
                    st.info("Moderate dryness. Consider using lubricating drops.")
                else:
                    st.success("Tear film looks healthy!")

            with col3:
                st.metric(
                    "Pupil Symmetry",
                    f"{results['pupil_symmetry']}%",
                    delta=None,
                    delta_color="normal"
                )
                if results['pupil_symmetry'] > 90:
                    st.success("Pupils are well-balanced.")
                else:
                    st.info("Minor pupil asymmetry detected.")

            if results['left_eye_image'] is not None and results['right_eye_image'] is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Left Eye**")
                    st.image(cv2.cvtColor(results['left_eye_image'], cv2.COLOR_BGR2RGB),
                            use_column_width=True)
                with col2:
                    st.write("**Right Eye**")
                    st.image(cv2.cvtColor(results['right_eye_image'], cv2.COLOR_BGR2RGB),
                            use_column_width=True)
        else:
            st.error("Face not detected. Please take a clearer photo.")

    with tabs[2]:
        st.subheader("Visual Acuity Test (Snellen Chart)")
        acuity_test.run_test()

    with tabs[3]:
        st.subheader("Color Blindness Test (Ishihara Plates)")
        color_test.run_test()

    with tabs[4]:
        st.subheader("Face Shape Analysis")

        if face_landmarks.face_landmarks:
            results = face_shape_detector.detect_shape(image, face_landmarks)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.image(cv2.cvtColor(results['image_with_outline'], cv2.COLOR_BGR2RGB),
                        use_column_width=True)

            with col2:
                st.metric("Face Shape", results['shape'], f"{results['confidence']}% confidence")

                st.write("#### Measurements")
                for key, value in results['measurements'].items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value:.1f}")

        else:
            st.error("Face not detected. Please take a clearer photo.")

    with tabs[5]:
        st.subheader("Glasses Recommendations")

        if face_landmarks.face_landmarks:
            face_shape_result = face_shape_detector.detect_shape(image, face_landmarks)
            shape = face_shape_result['shape']

            recommendations = glasses_recommender.recommend(shape)

            st.write(f"### Based on your {shape.title()} face shape:")
            st.write(recommendations['reason'])

            st.write("#### Recommended Frame Styles:")
            for i, frame in enumerate(recommendations['recommendations'], 1):
                st.write(f"{i}. **{frame}** - {recommendations['descriptions'][frame]}")

        else:
            st.error("Face not detected. Please take a clearer photo.")

    with tabs[6]:
        st.subheader("Virtual Glasses Try-On")

        if face_landmarks.face_landmarks:
            frame_type = st.selectbox(
                "Select a frame style:",
                ["rectangular", "round", "cat_eye", "clubmaster", "wayfarer", "browline"],
                format_func=lambda x: x.replace("_", " ").title()
            )

            result_image = glasses_overlay.overlay_glasses(image, face_landmarks, frame_type)

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Original**")
                st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_column_width=True)

            with col2:
                st.write("**With Glasses**")
                st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_column_width=True)

            st.download_button(
                label="Download Image with Glasses",
                data=cv2.imencode('.png', result_image)[1].tobytes(),
                file_name=f"glasses_tryon_{frame_type}.png",
                mime="image/png"
            )

        else:
            st.error("Face not detected. Please take a clearer photo.")

else:
    st.info("📷 Click the camera button above to start analyzing your eyes!")
    st.write(
        """
        ### Features:
        - **Face Detection:** Detect and analyze facial features
        - **Eye Health:** Analyze redness, dryness, and pupil symmetry
        - **Visual Acuity:** Test your vision with Snellen chart
        - **Color Blindness:** Test for color vision deficiency
        - **Face Shape:** Detect your face shape (oval, round, square, heart, oblong)
        - **Glasses Recommendations:** Get frame style suggestions
        - **Virtual Try-On:** See how different glasses look on you

        ### How it works:
        1. Take a photo with your camera
        2. Select a feature from the tabs above
        3. Get instant analysis and recommendations
        """
    )
