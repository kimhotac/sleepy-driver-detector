import numpy as np
import cv2

def crop_and_resize_eye(frame, bbox, size=90):
    """
    주어진 프레임에서 bounding box 영역(눈 부분)을 주변 여유 공간과 함께 잘라내어,
    지정한 크기의 정사각형 이미지로 리사이즈합니다.

    Args:
        frame (np.ndarray): 입력 이미지 (OpenCV BGR 형식).
        bbox (tuple): (x, y, w, h) 형태의 bounding box 좌표.
        size (int, optional): 반환할 정사각형 이미지의 한 변 크기. 기본값은 90.

    Returns:
        np.ndarray or None: 크롭 및 리사이즈된 눈 이미지 (shape: [size, size, 3]).
            bbox가 None이면 None을 반환합니다.
    """
    if bbox is None:
        return None

    x, y, w, h = bbox
    x1 = max(x - h//2, 0)
    y1 = max(y - w//2, 0)
    x2 = min(x + w + h//2, frame.shape[1])
    y2 = min(y + h + w//2, frame.shape[0])
    eye_crop = frame[y1:y2, x1:x2]
    eye_resized = cv2.resize(eye_crop, (size, size))
    return eye_resized