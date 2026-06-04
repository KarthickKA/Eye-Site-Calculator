import cv2
import numpy as np
from typing import Any


class EyeHealthAnalyzer:
    """Analyze eye region for health indicators: redness, dryness, pupil symmetry."""

    def __init__(self):
        self.left_eye_indices = list(range(33, 133))
        self.right_eye_indices = list(range(362, 462))

    def analyze(self, image: np.ndarray, landmarks: Any) -> dict:
        """
        Analyze eye health from image and face landmarks.

        Returns:
            dict: {
                'redness_level': 0-100,
                'dryness_level': 0-100,
                'pupil_symmetry': 0-100,
                'left_eye_image': np.ndarray,
                'right_eye_image': np.ndarray
            }
        """
        if not landmarks.face_landmarks:
            return {
                'redness_level': 0,
                'dryness_level': 0,
                'pupil_symmetry': 0,
                'left_eye_image': None,
                'right_eye_image': None
            }

        face_landmarks = landmarks.face_landmarks[0]
        h, w = image.shape[:2]

        left_eye_img = self._extract_eye_region(image, face_landmarks, self.left_eye_indices, h, w)
        right_eye_img = self._extract_eye_region(image, face_landmarks, self.right_eye_indices, h, w)

        left_redness = self._detect_redness(left_eye_img) if left_eye_img is not None else 0
        right_redness = self._detect_redness(right_eye_img) if right_eye_img is not None else 0
        redness_level = int((left_redness + right_redness) / 2)

        left_dryness = self._detect_dryness(left_eye_img) if left_eye_img is not None else 0
        right_dryness = self._detect_dryness(right_eye_img) if right_eye_img is not None else 0
        dryness_level = int((left_dryness + right_dryness) / 2)

        pupil_symmetry = self._detect_pupil_symmetry(
            left_eye_img, right_eye_img
        ) if left_eye_img is not None and right_eye_img is not None else 0

        return {
            'redness_level': min(100, max(0, redness_level)),
            'dryness_level': min(100, max(0, dryness_level)),
            'pupil_symmetry': min(100, max(0, pupil_symmetry)),
            'left_eye_image': left_eye_img,
            'right_eye_image': right_eye_img
        }

    def _extract_eye_region(self, image, landmarks, eye_indices, h, w, margin=20):
        """Extract eye region from image using landmarks."""
        try:
            points = np.array([
                [int(landmarks[i].x * w), int(landmarks[i].y * h)]
                for i in eye_indices
                if i < len(landmarks)
            ])

            if len(points) == 0:
                return None

            x_min = max(0, points[:, 0].min() - margin)
            x_max = min(w, points[:, 0].max() + margin)
            y_min = max(0, points[:, 1].min() - margin)
            y_max = min(h, points[:, 1].max() + margin)

            if x_max <= x_min or y_max <= y_min:
                return None

            return image[y_min:y_max, x_min:x_max].copy()
        except Exception:
            return None

    def _detect_redness(self, eye_image):
        """
        Detect redness in eye region.
        High red channel + low blue/green = redness.
        Returns 0-100 score.
        """
        if eye_image is None or eye_image.size == 0:
            return 0

        hsv = cv2.cvtColor(eye_image, cv2.COLOR_BGR2HSV)

        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([170, 100, 100])
        red_upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        red_pixels = cv2.countNonZero(red_mask)
        total_pixels = red_mask.size

        if total_pixels == 0:
            return 0

        redness_ratio = (red_pixels / total_pixels) * 100
        return min(100, int(redness_ratio * 2))

    def _detect_dryness(self, eye_image):
        """
        Detect dryness by analyzing texture variance.
        Dry eyes have low texture variation (less tear film).
        Returns 0-100 score (100 = very dry).
        """
        if eye_image is None or eye_image.size == 0:
            return 0

        gray = cv2.cvtColor(eye_image, cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()

        dryness = max(0, 100 - (variance * 2))
        return min(100, int(dryness))

    def _detect_pupil_symmetry(self, left_eye, right_eye):
        """
        Detect pupil size and position symmetry.
        Returns 0-100 score (100 = perfectly symmetric).
        """
        if left_eye is None or right_eye is None:
            return 0

        left_pupil = self._detect_pupil(left_eye)
        right_pupil = self._detect_pupil(right_eye)

        if left_pupil is None or right_pupil is None:
            return 50

        left_radius = left_pupil[1]
        right_radius = right_pupil[1]

        if left_radius == 0 or right_radius == 0:
            return 50

        size_ratio = min(left_radius, right_radius) / max(left_radius, right_radius)
        symmetry = int(size_ratio * 100)

        return min(100, max(0, symmetry))

    def _detect_pupil(self, eye_image):
        """
        Detect pupil circle using Hough circle detection.
        Returns (x, y, radius) or None.
        """
        if eye_image is None or eye_image.size == 0:
            return None

        gray = cv2.cvtColor(eye_image, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=5,
            maxRadius=50
        )

        if circles is not None and len(circles[0]) > 0:
            return tuple(circles[0][0])

        return None
