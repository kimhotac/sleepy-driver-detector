# MLEyeCloseDetector.py

import joblib
import cv2
import numpy as np
from ..EyeCloseDetection import EyeCloseDetector

class MLEyeCloseDetector(EyeCloseDetector):
    def __init__(self):
        self.model = joblib.load("eye_close_model.pkl")

    def predict(self, eye_img):
        # 1. 이미지 전처리: 흑백 변환, 90x90 리사이즈, flatten
        gray = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (90, 90))
        flattened = resized.flatten().reshape(1, -1)

        # 2. 예측
        prediction = self.model.predict(flattened)[0]  # 0 or 1
        return prediction
