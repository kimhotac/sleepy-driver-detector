import cv2
import time

class SleepDetection:
    def __init__(self, model_name='Opencv', drowsy_threshold_ms=1000):
        # 동적 임포트를 사용하여 필요한 모델만 로드
        if model_name == 'Opencv':
            from eyeCloseDetection.OpencvEyeCloseDetector.OpencvEyeCloseDetector import OpencvEyeCloseDetector
            self.detector = OpencvEyeCloseDetector()
        elif model_name == 'InfraredMLP':
            from eyeCloseDetection.InfraredMLPEyeCloseDetector.InfraredMLPEyeCloseDetector import InfraredMLPEyeCloseDetector
            self.detector = InfraredMLPEyeCloseDetector()
        elif model_name == 'MLEye':
            from eyeCloseDetection.MLEyeCloseDetector.MLEyeCloseDetector import MLEyeCloseDetector
            self.detector = MLEyeCloseDetector()
        elif model_name == 'MLP':
            from eyeCloseDetection.MLPEyeCloseDetector.MLPEyeCloseDetector import MLPEyeCloseDetector
            self.detector = MLPEyeCloseDetector()
        elif model_name == 'Point':
            from eyeCloseDetection.pointEyeCloseDetector.PointEyeCloseDetector import PointEyeCloseDetector
            self.detector = PointEyeCloseDetector()
        else:
            raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")
        
        self.drowsy_threshold_ms = drowsy_threshold_ms  # 졸음 임계값 (밀리초)
        self.closed_start_time = None  # 눈 감기 시작 시간
        self.drowsy_accum_time = 0    # 졸음 누적 시간 (ms)
        self.total_closed_time = 0  # 총 감김 시간 초기화

    def video_to_frames(self, video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames

    def webcam_stream(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
        cap.release()

    def detect_eye_close(self, frame):
        # 왼쪽/오른쪽 눈 감김 확률 반환 (0:뜸, 1:감음, -1:감지실패 -> 예외처리)
        left, right = self.detector.eye_close_detecte(frame)
        
        # 하나라도 감지 실패한 경우
        if left == -1 or right == -1:
            return -1  # 예외처리
        
        # 두 눈 모두 감은 경우
        if left == 1 and right == 1:
            return 1  # 졸음 카운트 증가
        
        # 두 눈 모두 뜬 경우
        if left == 0 and right == 0:
            return 0  # 정상, 카운트 초기화
        
        # 한쪽만 감은 경우 (하나라도 감겼다면)
        return -1  # 예외처리, 카운트 유지

    def run_on_video(self, video_path):
        frames = self.video_to_frames(video_path)
        for frame in frames:
            self._process_frame(frame)

    def run_on_webcam(self):
        for frame in self.webcam_stream():
            self._process_frame(frame)

    def _process_frame(self, frame):
        current_time = time.time()
        left, right = self.detector.eye_close_detecte(frame)

        # 양쪽 다 감음(1): 감기 시작/누적
        if left == 1 and right == 1:
            if self.closed_start_time is None:
                self.closed_start_time = current_time  # 감기 시작 시간 기록
            self.drowsy_accum_time = (current_time - self.closed_start_time) * 1000  # 누적 시간 계산

        # 양쪽 다 뜸(0): 초기화
        elif left == 0 and right == 0:
            self.closed_start_time = None  # 시작 시간 초기화
            self.drowsy_accum_time = 0     # 누적 시간 초기화

        # 그 외(-1, 한쪽만 감음): 이전 값 유지 (아무것도 하지 않음)

        # 졸음 임계점 도달 시 알림
        if self.drowsy_accum_time >= self.drowsy_threshold_ms:
            print(f"[경고] 졸음 운전 감지! (감김 시간: {self.drowsy_accum_time:.0f}ms)")
            # 여기서 알람, 로그, UI 등 추가 가능
            self.drowsy_accum_time = 0  # 한 번 알림 후 초기화
            self.closed_start_time = None

    def detect(self, frame):
        # 단일 프레임에 대한 감김 여부 반환 (테스트용)
        return self.detect_eye_close(frame)

    def run(self):
        # 여러 인덱스에서 사용 가능한 카메라 자동 탐색
        selected_index = None
        for idx in range(5):
            cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    selected_index = idx
                    cap.release()
                    break
                cap.release()
        if selected_index is None:
            print("사용 가능한 카메라를 찾을 수 없습니다.")
            exit(1)
        print(f"카메라 인덱스 {selected_index}를 사용합니다.")
        cap = cv2.VideoCapture(selected_index, cv2.CAP_AVFOUNDATION)
        print("웹캠이 시작되었습니다. 'q'를 누르면 종료됩니다.")
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("프레임 읽기 실패")
                break
            # 프레임 좌우반전(사용자 경험 개선)
            frame = cv2.flip(frame, 1)
            
            frame_count += 1
            
            # 눈 감김 판정 및 시간 누적
            current_time = time.time()
            result = self.detect_eye_close(frame)
            
            if result == 1:  # 눈 감음
                if self.closed_start_time is None:
                    self.closed_start_time = current_time  # 감기 시작 시간 기록
            elif result == 0:  # 눈 뜸
                self.closed_start_time = None  # 시작 시간 초기화
                self.total_closed_time = 0     # 누적 시간 초기화
            # result == -1인 경우는 상태 유지
            
            # 현재 연속 감김 시간 계산
            if self.closed_start_time is not None:
                self.total_closed_time = (current_time - self.closed_start_time) * 1000  # ms로 변환
            
            # 눈 상태 정보 표시 (디버깅용)
            left, right = self.detector.eye_close_detecte(frame)
            status_text = f"L:{left} R:{right} Time:{self.total_closed_time:.0f}ms"
            cv2.putText(frame, status_text, (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            
            # 경고 메시지 표시
            if self.total_closed_time >= self.drowsy_threshold_ms:
                cv2.putText(frame, "졸음!", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 5, cv2.LINE_AA)
            # 실시간 프레임 출력
            cv2.imshow("SleepDetection - Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    sd = SleepDetection()
    sd.run()