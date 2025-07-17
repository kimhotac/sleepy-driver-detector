import cv2
import numpy as np

from ..EyeCloseDetection import EyeCloseDetector

class OpencvEyeCloseDetector(EyeCloseDetector):
    """
    순수 OpenCV 기술만을 사용하여 눈의 개폐 상태를 판단하는 구현체입니다.
    입력: 90x90 크기의 눈 이미지(컬러 또는 흑백, 반드시 1장)
    출력: 0.0(완전히 뜸) ~ 1.0(완전히 감음)
    """
    def __init__(self):
        super().__init__()
        # 눈을 떴는지, 감았는지 임계값
        self.EDGE_DENSITY_MIN = 5.0 
        self.EDGE_DENSITY_MAX = 30.0

        # 밝기 분산 임계값
        self.VARIANCE_MIN = 300.0
        self.VARIANCE_MAX = 1500.0

    def predict(self, eye_img):
        # 1. 이미지 흑백으로 통일 : 색상 노이즈를 제거하고 밝기 정보만 남겨 주요 특징을 더 명확하게 분석
        """
        흑백은 밝기 정보만 남기므로, 눈꺼풀/동공/속눈썹 등 주요 특징 명확히 드러남
        OpenCV 이미지 처리 함수(에지, 블러, 히스토그램 등)은 흑백 이미지에서 동작 잘 됨
        컬러는 조명/피부색/카메라 화이트밸런스 등에 따라 너무 많이 변함
        색상 정보는 노이즈가 될 수 있음
        밝기 정보만으로도 눈 감김 판단에 충분
        따라서, 경계/선/원 등 구조적 특징으로 안정적 추출 가능
        """

        # shape: (높이, 너비, 채널수) → 컬러
        # shape: (높이, 너비) → 흑백
        gray_eye = eye_img
        if len(eye_img.shape) == 3: # 컬러인 경우에는 흑백으로 전환
            gray_eye = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)

        # 2-1) 명암 대비 향상 및 노이즈 제거 : 조명/피부색 등 환경에 상관없이 눈 경계가 잘 보이도록 하기 위함
        # 명암 대비(CLAHE) : 픽셀 밝기 분포 제한하는 라이브러리
        """
        clipLimit : 픽셀 밝기 분포 제한 파라미터
        ex) 1.0 ~ 4.0
        - 값 작을수록 : 원본에 가까움
        - 값 클수록 : 경계 뚜렷하지만 노이즈 커질 수 있음

        tileGridSize : 픽셀 그룹화 
        ex) (4, 4), (8, 8), (16, 16)
        - 값 작을수록 : 세밀하게(경계 뚜렷)
        - 값 클수록 : 넓게(전체적으로)
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        preprocessed_img = clahe.apply(gray_eye)

        # 2-2) 가우시안 블러(노이즈 제거) : 불필요한 점, 잡음 등 노이즈를 흐리게 만들어 분석 정확도를 높이기 위함
        """
        첫 번째 파라미터 : 타겟 이미지
        두 번째 파라미터 : 블러 커널 크기
        ex) (3, 3), (5, 5), (7, 7), (9, 9)
        - 값 작을수록 : 원본에 가까움(노이즈 제거↓, 경계 선명)
        - 값 클수록 : 더 부드러움(노이즈 제거↑, 경계 뭉개짐)
        """
        preprocessed_img = cv2.GaussianBlur(preprocessed_img, (5, 5), 0) # (9, 9)는 별로임 (3, 3) 나름 괜찮은듯 (5, 5)도 나름 정확한듯

        # 3. 홍채(동공) 검출: 동공(원)이 보이면 무조건 '눈을 떴다'로 확정하기 위함
        """
        HoughCircles 함수는 이미지에서 '원'을 찾아주는 알고리즘입니다.
        동공(홍채)은 눈을 떴을 때만 보이는 검은 원이므로, 원이 검출되면 '눈을 떴다'로 판단합니다.
        - dp: 누적기 해상도 비율 (1.0~2.0)
          - 값이 작을수록 더 정밀하게 원을 찾음(속도↓, 정확도↑) -> 아무래도 정확한게 가장 중요한 것 같아서 최소값으로!
          - 값이 크면 빠르지만 대충 찾음(속도↑, 정확도↓)
        - minDist: 검출된 원들 사이의 최소 거리(픽셀)
          - 값이 작으면 겹치는 원이 많이 검출됨(중복 검출↑)
          - 값이 크면 일부 원을 놓칠 수 있음(중복 검출↓)
        - param1: 내부 Canny 엣지 검출 임계값(1차 경계 검출)
          - 값이 크면 경계가 뚜렷한 원만 검출
        - param2: 원 검출 민감도(2차 임계값)
          - 값이 작으면 더 많은 원을 검출(노이즈↑)
          - 값이 크면 확실한 원만 검출(노이즈↓)
        - minRadius/maxRadius: 찾을 원의 반지름 범위(픽셀)
          - 값이 작으면 작은 원까지 검출(노이즈↑)
          - 값이 크면 큰 원만 검출(노이즈↓)
        """
        circles = cv2.HoughCircles(
            preprocessed_img, cv2.HOUGH_GRADIENT,
            dp=1.0, minDist=50, param1=50, param2=30,
            minRadius=7, maxRadius=20
        )
        if circles is not None:
            # 동공(원)이 검출되면, 눈을 확실히 뜬 상태로 간주하여 0.0 반환
            return 0.0

        # 4. 가로 에지(눈 감김 실선) 분석 : 눈을 감으면 생기는 강한 가로선을 감지해 감김 상태를 판단하기 위함
        """
        Sobel 필터는 이미지에서 '선(경계)'을 찾아주는 연산입니다.
        sobel_y는 세로 방향 밝기 변화(=가로선)를 감지합니다.
        - ksize: 커널 크기(3, 5, 7 등)
          - 값이 크면 더 두꺼운 선, 값이 작으면 더 얇은 선 감지
        - np.mean(np.absolute(sobel_y)): 전체 이미지에서 가로선의 강도를 평균
          - 값이 높을수록 강한 가로선(=눈 감음)
          - 값이 낮을수록 약한 가로선(=눈 뜸)
        - edge_score: 감은 눈/뜬 눈의 edge_density 값 범위를 0~1로 정규화
          - 값이 1.0에 가까울수록 눈 감음, 0.0에 가까울수록 눈 뜸
        """
        sobel_y = cv2.Sobel(gray_eye, cv2.CV_64F, 0, 1, ksize=5)
        edge_density = np.mean(np.absolute(sobel_y))
        edge_score = (edge_density - self.EDGE_DENSITY_MIN) / (self.EDGE_DENSITY_MAX - self.EDGE_DENSITY_MIN)
        edge_score = np.clip(edge_score, 0.0, 1.0)

        # 5. 밝기 분산 분석 : 눈을 감으면 단색(분산↓), 뜨면 다양한 밝기(분산↑)로 감김 상태를 보조적으로 판단하기 위함
        """
        np.var(gray_eye)는 이미지의 밝기 값이 얼마나 다양한지(분산)를 계산합니다.
        - 눈을 감으면(=눈꺼풀) 거의 단색(밝기 분산↓)
        - 눈을 뜨면(=동공, 흰자, 피부 등) 밝기 차이가 커짐(밝기 분산↑)
        - variance_score: 감은 눈/뜬 눈의 분산 값 범위를 0~1로 정규화
          - 값이 1.0에 가까울수록 눈 감음, 0.0에 가까울수록 눈 뜸
        """
        variance = np.var(gray_eye)
        variance_score = (variance - self.VARIANCE_MIN) / (self.VARIANCE_MAX - self.VARIANCE_MIN)
        variance_score = 1.0 - np.clip(variance_score, 0.0, 1.0)

        # 6. 최종 점수 융합 (가로선 0.7, 분산 0.3) : 여러 신호(가로선, 밝기 분산)를 종합해 감김 정도를 최종적으로 산출하기 위함
        """
        최종적으로, 두 특징(가로선, 밝기 분산)을 가중 평균하여 감김 점수를 산출합니다.
        - final_score = 0.7 * edge_score + 0.3 * variance_score
          - edge_score(가로선): 눈 감김의 가장 강력한 신호(가중치↑)
          - variance_score(밝기 분산): 보조적 신호(가중치↓)
        - np.clip: 결과가 0.0~1.0 범위를 벗어나지 않게 보정
        - 값이 1.0에 가까울수록 눈 감음, 0.0에 가까울수록 눈 뜸
        """
        final_score = 0.7 * edge_score + 0.3 * variance_score
        result = np.clip(final_score, 0.0, 1.0) 
        if (result <= 0.95): return 0
        return 1
        