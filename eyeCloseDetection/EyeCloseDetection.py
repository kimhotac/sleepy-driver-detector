from eyeDetection.EyeDetection import EyeDetector
import abc

class EyeCloseDetector(EyeDetector, abc.ABC):
    def __init__(self):
        """
        EyeCloseDetector는 EyeDetector를 상속받아,
        왼쪽 및 오른쪽 눈의 감김 정도를 확률(0~1)로 예측하는 추상 클래스입니다.
        
        서브클래스는 반드시 `predict` 메서드를 구현해야 합니다.
        """
        super().__init__()
    
    @abc.abstractmethod
    def predict(self, eye_img):
        """
        눈 감김 정도를 예측합니다.

        Args:
            eye_img (np.ndarray): 단일 눈 이미지 (90x90, BGR 형식)

        Returns:
            float: 눈 감김 확률 (0.0 = 완전히 뜬 상태, 1.0 = 완전히 감긴 상태)
        """
        pass

    def eye_close_detecte(self, frame):
        """
        입력 프레임에서 왼쪽 및 오른쪽 눈 영역을 추출하고,
        각각의 눈 감김 확률을 반환합니다.

        Args:
            frame (np.ndarray): 전체 이미지 프레임 (BGR 형식)

        Returns:
            tuple[float, float]: (왼쪽 눈 감김 확률, 오른쪽 눈 감김 확률)
        """
        left_points, right_points = self.get_bounding_boxes(frame)

        
        if left_points is None:
            left_close_prob = -1

        else:
            left_img = self.crop_and_resize(frame, left_points)
            left_close_prob = self.predict(left_img)

        if right_points is None :
            right_close_prob = -1
            
        else:
            right_img = self.crop_and_resize(frame, right_points)
            right_close_prob = self.predict(right_img)

        return left_close_prob, right_close_prob