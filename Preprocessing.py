import numpy as np
import cv2

def crop_and_resize_eye(frame, eye_points, padding=20, size=90):
    if eye_points is None or len(eye_points) == 0:
        return None

    x, y, w, h = cv2.boundingRect(np.array(eye_points))
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + padding * 2, frame.shape[1] - x)
    h = min(h + padding * 2, frame.shape[0] - y)
    eye_img = frame[y:y+h, x:x+w]

    # 90x90 리사이즈 (비율 보존 X)
    eye_resized = cv2.resize(eye_img, (size, size))
    return eye_resized
