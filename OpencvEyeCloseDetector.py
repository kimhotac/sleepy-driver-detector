from EyeCloseDetection import EyeCloseDetector

class OpencvEyeCloseDetector(EyeCloseDetector):
    def predict(self, eye_img):
        return