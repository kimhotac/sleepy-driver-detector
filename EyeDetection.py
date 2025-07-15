import mediapipe as mp

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
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            return None, None  # 얼굴이 안 잡히면 None 반환

        landmarks = results.multi_face_landmarks[0].landmark
        # 오른쪽 눈
        right_eye_points = [(int(landmarks[i].x * frame.shape[1]), int(landmarks[i].y * frame.shape[0])) for i in self.RIGHT_EYE_IDX]
        right_x = [pt[0] for pt in right_eye_points]
        right_y = [pt[1] for pt in right_eye_points]
        right_bbox = (min(right_x), min(right_y), max(right_x), max(right_y))

        # 왼쪽 눈
        left_eye_points = [(int(landmarks[i].x * frame.shape[1]), int(landmarks[i].y * frame.shape[0])) for i in self.LEFT_EYE_IDX]
        left_x = [pt[0] for pt in left_eye_points]
        left_y = [pt[1] for pt in left_eye_points]
        left_bbox = (min(left_x), min(left_y), max(left_x), max(left_y))

        return right_bbox, left_bbox
