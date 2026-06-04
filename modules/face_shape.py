import cv2
import numpy as np
from typing import Any


class FaceShapeDetector:
    """Detect face shape from facial landmarks: oval, round, square, heart, oblong."""

    def __init__(self):
        self.face_outline_indices = [
            10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
            397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
            172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
        ]

    def detect_shape(self, image: np.ndarray, landmarks: Any) -> dict:
        """
        Detect face shape from image and landmarks.

        Returns:
            dict: {
                'shape': str (oval, round, square, heart, oblong),
                'confidence': 0-100,
                'measurements': dict with ratios and measurements,
                'image_with_outline': np.ndarray
            }
        """
        if not landmarks.face_landmarks:
            return {
                'shape': 'unknown',
                'confidence': 0,
                'measurements': {},
                'image_with_outline': image.copy()
            }

        face_landmarks = landmarks.face_landmarks[0]
        h, w = image.shape[:2]

        measurements = self._calculate_measurements(face_landmarks, h, w)

        shape, confidence = self._classify_shape(measurements)

        image_with_outline = self._draw_face_outline(
            image.copy(), face_landmarks, h, w, shape
        )

        return {
            'shape': shape,
            'confidence': confidence,
            'measurements': measurements,
            'image_with_outline': image_with_outline
        }

    def _calculate_measurements(self, landmarks, h, w):
        """Calculate facial measurements from landmarks."""
        measurements = {}

        forehead_left = np.array([landmarks[70].x * w, landmarks[70].y * h])
        forehead_right = np.array([landmarks[300].x * w, landmarks[300].y * h])
        measurements['forehead_width'] = np.linalg.norm(forehead_right - forehead_left)

        cheekbone_left = np.array([landmarks[210].x * w, landmarks[210].y * h])
        cheekbone_right = np.array([landmarks[430].x * w, landmarks[430].y * h])
        measurements['cheekbone_width'] = np.linalg.norm(cheekbone_right - cheekbone_left)

        jaw_left = np.array([landmarks[234].x * w, landmarks[234].y * h])
        jaw_right = np.array([landmarks[454].x * w, landmarks[454].y * h])
        measurements['jaw_width'] = np.linalg.norm(jaw_right - jaw_left)

        face_top = np.array([landmarks[10].x * w, landmarks[10].y * h])
        face_bottom = np.array([landmarks[152].x * w, landmarks[152].y * h])
        measurements['face_length'] = np.linalg.norm(face_bottom - face_top)

        face_center_x = (forehead_left[0] + forehead_right[0]) / 2
        face_left = np.array([landmarks[127].x * w, landmarks[127].y * h])
        face_right = np.array([landmarks[356].x * w, landmarks[356].y * h])
        measurements['face_width'] = np.linalg.norm(face_right - face_left)

        forehead_to_cheekbone = measurements['forehead_width'] / measurements['cheekbone_width']
        cheekbone_to_jaw = measurements['cheekbone_width'] / measurements['jaw_width']
        length_to_width = measurements['face_length'] / measurements['face_width']

        measurements['forehead_to_cheekbone_ratio'] = forehead_to_cheekbone
        measurements['cheekbone_to_jaw_ratio'] = cheekbone_to_jaw
        measurements['length_to_width_ratio'] = length_to_width

        return measurements

    def _classify_shape(self, measurements):
        """Classify face shape based on measurements."""
        lw_ratio = measurements['length_to_width_ratio']
        f2c = measurements['forehead_to_cheekbone_ratio']
        c2j = measurements['cheekbone_to_jaw_ratio']

        if lw_ratio > 1.5:
            if abs(f2c - 1.0) < 0.15 and abs(c2j - 1.0) < 0.15:
                return 'Oblong', 90
            else:
                return 'Oblong', 70

        if lw_ratio < 1.1:
            if f2c > 1.1 and c2j > 1.0:
                return 'Heart', 85
            elif abs(f2c - c2j) < 0.1:
                return 'Round', 90
            else:
                return 'Square', 85

        if 1.1 <= lw_ratio <= 1.5:
            if abs(f2c - c2j) < 0.15 and abs(f2c - 1.0) < 0.2:
                return 'Oval', 90
            elif f2c > 1.05 and c2j > 1.05:
                return 'Heart', 80
            elif abs(f2c - c2j) < 0.15:
                return 'Round', 75
            else:
                return 'Oval', 80

        return 'Oval', 60

    def _draw_face_outline(self, image, landmarks, h, w, shape):
        """Draw face outline and shape label on image."""
        outline_points = np.array([
            [int(landmarks[idx].x * w), int(landmarks[idx].y * h)]
            for idx in self.face_outline_indices
            if idx < len(landmarks)
        ], dtype=np.int32)

        cv2.polylines(image, [outline_points], True, (0, 255, 0), 3)

        text = f"Face Shape: {shape}"
        cv2.putText(
            image,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        return image
