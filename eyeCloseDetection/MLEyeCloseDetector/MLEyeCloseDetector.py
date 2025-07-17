# MLEyeCloseDetector.py

import joblib
import cv2
import numpy as np
import os
from ..EyeCloseDetection import EyeCloseDetector

class MLEyeCloseDetector(EyeCloseDetector):
    def __init__(self):
        super().__init__()
        # 현재 파일 기준 절대 경로 구성
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "rf_model.pkl")
        self.model = joblib.load(model_path)

    def predict(self, eye_img):
        # 1. 이미지 전처리: 흑백 변환, 90x90 리사이즈, flatten
        gray = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (90, 90))
        flattened = resized.flatten().reshape(1, -1)

        # 2. 예측
        prediction = self.model.predict(flattened)[0]  # 0 or 1
        return prediction
