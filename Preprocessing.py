import numpy as np
import cv2

def crop_and_resize_eye(frame, bbox, padding=20, size=90):
    """
    입력 이미지에서 bounding box로 지정된 눈 영역을 잘라내고(padding 포함),
    지정된 크기로 리사이즈합니다.

    Args:
        frame (np.ndarray): 원본 이미지 (BGR 포맷, OpenCV 형식).
        bbox (tuple): (x, y, w, h) 형식의 bounding box.
        padding (int, optional): 잘라낼 때 사방에 추가할 여유 픽셀 수. 기본값 20.
        size (int, optional): 반환할 이미지의 한 변 크기 (정사각형). 기본값 90.

    Returns:
        np.ndarray or None: 크롭 & 리사이즈된 눈 이미지 (shape: [size, size, 3]).
            bbox가 None이면 None 반환.
    """
    if bbox is None:
        return None

    x, y, w, h = bbox
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + padding * 2, frame.shape[1] - x)
    h = min(h + padding * 2, frame.shape[0] - y)
    eye_img = frame[y:y+h, x:x+w]

    # size x size로 리사이즈 (비율 보존 X)
    eye_resized = cv2.resize(eye_img, (size, size))
    return eye_resized
