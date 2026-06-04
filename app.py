import streamlit as st
import cv2
import numpy as np

from modules.face_detector import FaceDetector

st.title("👁 Eye Site Calculator")

detector = FaceDetector()

uploaded = st.camera_input(
    "Take a photo"
)

if uploaded:

    bytes_data = uploaded.getvalue()

    np_array = np.frombuffer(
        bytes_data,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    result = detector.detect(
        image
    )

    if result.face_landmarks:

        st.success(
            "Face Detected"
        )

        st.write(
            f"Faces Found: {len(result.face_landmarks)}"
        )

    else:

        st.error(
            "No Face Found"
        )

    st.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )
    )