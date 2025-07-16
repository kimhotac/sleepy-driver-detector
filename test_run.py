import cv2
from MLEyeCloseDetector import MLEyeCloseDetector

# 테스트할 이미지 불러오기_뜬 눈
eye_img = cv2.imread("test_eye_120.png")

# 모델 객체 생성
detector = MLEyeCloseDetector()

# 예측
result = detector.predict(eye_img)

# 결과 출력
print("예측 결과:", "감은 눈" if result == 0 else "뜬 눈")



# 테스트할 이미지 불러오기_감은 눈
eye_img = cv2.imread("test_eye_544.png")

# 모델 객체 생성
detector = MLEyeCloseDetector()

# 예측
result = detector.predict(eye_img)

# 결과 출력
print("예측 결과:", "감은 눈" if result == 0 else "뜬 눈")
