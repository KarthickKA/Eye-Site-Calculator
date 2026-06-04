import cv2
import numpy as np
from typing import Any


class VirtualGlassesOverlay:
    """Overlay virtual glasses frames on face using landmarks."""

    def __init__(self):
        self.left_eye_index = 33
        self.right_eye_index = 263
        self.left_eye_outer = 33
        self.right_eye_outer = 263

    def overlay_glasses(
        self,
        image: np.ndarray,
        landmarks: Any,
        frame_type: str = 'rectangular'
    ) -> np.ndarray:
        """
        Overlay glasses on face.

        Args:
            image: np.ndarray input image
            landmarks: FaceLandmarkerResult with face landmarks
            frame_type: str (rectangular, round, cat_eye, clubmaster, wayfarer, browline)

        Returns:
            np.ndarray: image with glasses overlay
        """
        if not landmarks.face_landmarks:
            return image.copy()

        face_landmarks = landmarks.face_landmarks[0]
        h, w = image.shape[:2]

        left_eye = np.array([
            face_landmarks[self.left_eye_index].x * w,
            face_landmarks[self.left_eye_index].y * h
        ], dtype=np.float32)

        right_eye = np.array([
            face_landmarks[self.right_eye_index].x * w,
            face_landmarks[self.right_eye_index].y * h
        ], dtype=np.float32)

        eye_distance = np.linalg.norm(right_eye - left_eye)

        angle = np.degrees(np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]))

        frame_width = int(eye_distance * 1.5)
        frame_height = int(frame_width * 0.5)

        frame_img = self._create_frame(frame_type, frame_width, frame_height)

        center_x = int((left_eye[0] + right_eye[0]) / 2)
        center_y = int((left_eye[1] + right_eye[1]) / 2)

        result = self._overlay_frame(image, frame_img, center_x, center_y, angle)

        return result

    def _create_frame(self, frame_type: str, width: int, height: int) -> np.ndarray:
        """Create glasses frame shape."""
        frame = np.zeros((height, width, 4), dtype=np.uint8)

        if frame_type == 'rectangular':
            self._draw_rectangular_frame(frame)
        elif frame_type == 'round':
            self._draw_round_frame(frame)
        elif frame_type == 'cat_eye':
            self._draw_cat_eye_frame(frame)
        elif frame_type == 'clubmaster':
            self._draw_clubmaster_frame(frame)
        elif frame_type == 'wayfarer':
            self._draw_wayfarer_frame(frame)
        elif frame_type == 'browline':
            self._draw_browline_frame(frame)
        else:
            self._draw_rectangular_frame(frame)

        return frame

    def _draw_rectangular_frame(self, frame):
        """Draw rectangular glasses frame."""
        h, w = frame.shape[:2]
        lens_width = w // 3
        lens_height = h
        bridge_width = w // 6
        bridge_height = h // 3

        cv2.rectangle(frame, (0, 0), (lens_width, lens_height), (100, 150, 255, 200), 2)
        cv2.rectangle(frame, (2 * lens_width, 0), (w, lens_height), (100, 150, 255, 200), 2)

        bridge_x = lens_width
        bridge_y = (lens_height - bridge_height) // 2
        cv2.rectangle(frame, (bridge_x, bridge_y), (bridge_x + bridge_width, bridge_y + bridge_height),
                     (100, 150, 255, 200), 2)

    def _draw_round_frame(self, frame):
        """Draw round glasses frame."""
        h, w = frame.shape[:2]
        radius = h // 2
        gap = w // 6

        center_left = (radius, h // 2)
        center_right = (w - radius, h // 2)

        cv2.circle(frame, center_left, radius, (100, 150, 255, 200), 2)
        cv2.circle(frame, center_right, radius, (100, 150, 255, 200), 2)

        cv2.line(frame, (radius + radius, h // 2), (w - radius - radius, h // 2), (100, 150, 255, 200), 2)

    def _draw_cat_eye_frame(self, frame):
        """Draw cat-eye glasses frame."""
        h, w = frame.shape[:2]
        lens_width = w // 3
        lens_height = h

        pts_left = np.array([
            [0, int(lens_height * 0.3)],
            [lens_width, 0],
            [lens_width, lens_height],
            [0, int(lens_height * 0.7)]
        ], np.int32)

        pts_right = np.array([
            [2 * lens_width, 0],
            [w, int(lens_height * 0.3)],
            [w, int(lens_height * 0.7)],
            [2 * lens_width, lens_height]
        ], np.int32)

        cv2.polylines(frame, [pts_left], True, (100, 150, 255, 200), 2)
        cv2.polylines(frame, [pts_right], True, (100, 150, 255, 200), 2)

    def _draw_clubmaster_frame(self, frame):
        """Draw clubmaster glasses frame."""
        h, w = frame.shape[:2]
        lens_width = w // 3
        lens_height = h

        pts_left = np.array([
            [0, 0],
            [lens_width, 0],
            [lens_width, int(lens_height * 0.7)],
            [int(lens_width * 0.3), lens_height],
            [0, lens_height]
        ], np.int32)

        pts_right = np.array([
            [2 * lens_width, 0],
            [w, 0],
            [w, lens_height],
            [int(w - lens_width * 0.3), lens_height],
            [2 * lens_width, int(lens_height * 0.7)]
        ], np.int32)

        cv2.polylines(frame, [pts_left], True, (100, 150, 255, 200), 2)
        cv2.polylines(frame, [pts_right], True, (100, 150, 255, 200), 2)

    def _draw_wayfarer_frame(self, frame):
        """Draw wayfarer glasses frame."""
        h, w = frame.shape[:2]
        lens_width = w // 3
        lens_height = h

        pts_left = np.array([
            [0, 0],
            [lens_width, int(lens_height * 0.2)],
            [lens_width, lens_height],
            [0, int(lens_height * 0.8)]
        ], np.int32)

        pts_right = np.array([
            [2 * lens_width, int(lens_height * 0.2)],
            [w, 0],
            [w, int(lens_height * 0.8)],
            [2 * lens_width, lens_height]
        ], np.int32)

        cv2.polylines(frame, [pts_left], True, (100, 150, 255, 200), 2)
        cv2.polylines(frame, [pts_right], True, (100, 150, 255, 200), 2)

    def _draw_browline_frame(self, frame):
        """Draw browline glasses frame."""
        h, w = frame.shape[:2]
        lens_width = w // 3
        lens_height = h

        pts_left = np.array([
            [0, 0],
            [lens_width, 0],
            [lens_width, int(lens_height * 0.6)],
            [0, int(lens_height * 0.8)]
        ], np.int32)

        pts_right = np.array([
            [2 * lens_width, 0],
            [w, 0],
            [w, int(lens_height * 0.8)],
            [2 * lens_width, int(lens_height * 0.6)]
        ], np.int32)

        cv2.polylines(frame, [pts_left], True, (100, 150, 255, 200), 2)
        cv2.polylines(frame, [pts_right], True, (100, 150, 255, 200), 2)

    def _overlay_frame(self, image, frame_img, center_x, center_y, angle):
        """Overlay frame image on face image."""
        h, w = frame_img.shape[:2]

        matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)

        frame_rotated = cv2.warpAffine(
            frame_img,
            matrix,
            (w, h),
            borderMode=cv2.BORDER_REFLECT
        )

        x1 = max(0, center_x - w // 2)
        y1 = max(0, center_y - h // 2)
        x2 = min(image.shape[1], center_x + w // 2)
        y2 = min(image.shape[0], center_y + h // 2)

        fx1 = max(0, w // 2 - center_x)
        fy1 = max(0, h // 2 - center_y)
        fx2 = fx1 + (x2 - x1)
        fy2 = fy1 + (y2 - y1)

        if x1 < x2 and y1 < y2 and fx1 < fx2 and fy1 < fy2:
            frame_roi = frame_rotated[fy1:fy2, fx1:fx2]

            if frame_roi.shape[2] == 4:
                alpha = frame_roi[:, :, 3] / 255.0
                for c in range(3):
                    image[y1:y2, x1:x2, c] = (
                        image[y1:y2, x1:x2, c] * (1 - alpha) +
                        frame_roi[:, :, c] * alpha
                    )
            else:
                image[y1:y2, x1:x2] = frame_roi

        return image
