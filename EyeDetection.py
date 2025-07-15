import mediapipe as mp
import cv2
import numpy as np

# 이미지에서 눈 부분을 감지하는 클래스
class EyeDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        # Mediapipe 좌/우 눈 인덱스
        self.RIGHT_EYE_IDX = [33, 133, 160, 159, 158, 157, 173, 246]
        self.LEFT_EYE_IDX  = [362, 263, 387, 386, 385, 384, 398, 466]

    def get_eye_bounding_boxes(self, frame):
        '''
        이미지 프레임에서 얼굴을 탐지하고, 
        왼쪽/오른쪽 눈의 bounding box 좌표를 반환합니다.

        Args:
            frame: COLOR 포맷의 이미지 프레임

        Returns:
            tuple: (오른쪽 눈 bounding box, 왼쪽 눈 bounding box)
                각 bounding box는 (x, y, w, h) 형태의 튜플입니다.
                (x, y)는 좌상단 좌표, w/h는 너비/높이입니다.
                얼굴이 감지되지 않으면 (None, None) 반환
        '''
        results = self.face_mesh.process(frame)
        if not results.multi_face_landmarks:
            return None, None  # 얼굴이 안 잡히면 None 반환

        landmarks = results.multi_face_landmarks[0].landmark
        ih, iw = frame.shape[:2]

        # 오른쪽 눈
        right_eye_points = np.array([
            [int(landmarks[i].x * iw), int(landmarks[i].y * ih)]
            for i in self.RIGHT_EYE_IDX
        ])
        right_bbox = cv2.boundingRect(right_eye_points)  # (x, y, w, h)

        # 왼쪽 눈
        left_eye_points = np.array([
            [int(landmarks[i].x * iw), int(landmarks[i].y * ih)]
            for i in self.LEFT_EYE_IDX
        ])
        left_bbox = cv2.boundingRect(left_eye_points)  # (x, y, w, h)

        return right_bbox, left_bbox
