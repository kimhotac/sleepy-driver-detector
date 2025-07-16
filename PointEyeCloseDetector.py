
class PointEyeCloseDetector(EyeCloseDetector):
    def __init__(self):
        super().__init__()
        self.THRESHOLD = 3
    
    def predict(self, points):
        x, y, w, h = points
        if h < self.THRESHOLD:
            prob = 1
        else:
            prob = 0
        return prob
    
    def eye_close_detecte(self, frame):
        """
        입력 프레임에서 왼쪽 및 오른쪽 눈을 감지하고,
        각각의 눈이 감겼는지 반환합니다.

        Args:
            frame (np.ndarray): 전체 이미지 프레임 (BGR 형식)

        Returns:
            tuple[float, float]: (왼쪽 눈 감김 확률, 오른쪽 눈 감김 확률)
        """
        left_points, right_points = self.get_bounding_boxes(frame)
        left_close_prob = self.predict(left_points)
        right_close_prob = self.predict(right_points)

        return left_close_prob, right_close_prob
