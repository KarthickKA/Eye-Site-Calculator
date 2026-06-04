import mediapipe as mp
import cv2


class FaceDetector:

    def __init__(self):

        BaseOptions = mp.tasks.BaseOptions

        FaceLandmarker = mp.tasks.vision.FaceLandmarker

        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions

        VisionRunningMode = mp.tasks.vision.RunningMode

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="models/face_landmarker.task"
            ),
            running_mode=VisionRunningMode.IMAGE,
            num_faces=1
        )

        self.detector = FaceLandmarker.create_from_options(
            options
        )

    def detect(self, image):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(
            mp_image
        )

        return result