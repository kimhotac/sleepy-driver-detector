# 📝 SleepyDriver 변경 로그

## [1.1.2] - 2024-12-19

### 🎨 UI 대폭 개선

#### 원라이너 API 글자 크기 확대

- **문제**: 원라이너 API(`start_detection`)의 글자가 너무 작아 멀리서 안 보임
- **해결**: 모든 텍스트 크기를 2-3배 확대
  ```python
  # 기본 텍스트: 1.0 → 2.2 (120% 증가)
  # 모델명: 0.6 → 1.8 (200% 증가)
  # 눈 상태: 0.6 → 1.8 (200% 증가)
  # 두께: 2 → 5-6 (150-200% 증가)
  ```

#### 졸음 경고 효과 강화

- **깜빡이는 빨간 배경** 추가
- **중앙 대형 경고 메시지** "DROWSINESS DETECTED!" (3.0 크기)
- **깜빡이는 두꺼운 테두리** (8-15px)
- **지속 시간 표시** 추가

### 📋 적용 범위

- ✅ 원라이너 API (`start_detection()`)
- ✅ CLI 도구 (`sleepy-driver-demo`)
- ✅ 로컬 `examples/demo.py` (이미 적용됨)

---

## [1.1.1] - 2024-12-19

### 🐛 버그 수정

#### 좌우 눈 표시 오류 해결

- **문제**: 원라이너 API(`start_detection`)에서 좌우 눈 상태가 반대로 표시되는 버그
- **원인**: 거울 모드에서 화면 좌우와 해부학적 좌우의 매핑 오류
- **수정**: 화면 기준으로 올바른 매핑 적용

  ```python
  # 수정 전 (잘못됨)
  left_eye = "C" if result.left_eye_closed else "O"    # L = 실제 왼쪽 눈
  right_eye = "C" if result.right_eye_closed else "O"  # R = 실제 오른쪽 눈

  # 수정 후 (올바름)
  left_eye = "C" if result.right_eye_closed else "O"   # L = 화면 왼쪽 (사용자 오른쪽 눈)
  right_eye = "C" if result.left_eye_closed else "O"   # R = 화면 오른쪽 (사용자 왼쪽 눈)
  ```

### 📝 참고사항

- 로컬 `examples/demo.py`는 이미 올바르게 구현되어 있었음
- CLI 및 직접 코딩 시에는 영향 없음
- 원라이너 API만 해당하는 버그였음

---

## [1.1.0] - 2024-12-19

### 🚀 주요 신기능 추가

#### 원라이너 API

- **`start_detection()`**: 1줄로 바로 웹캠 졸음 감지 시작!
- **`webcam_detection()`**: start_detection의 별칭
- **`simple_detector()`**: 기본 설정으로 감지기 생성

#### 사용 예시

```python
# 기존 방식 (23줄)
from sleepy_driver import quick_detector
import cv2
detector = quick_detector('mlp')
cap = cv2.VideoCapture(0)
# ... 복잡한 while 루프 ...

# 새로운 방식 (2줄!)
from sleepy_driver import start_detection
start_detection('mlp')
```

### ✨ 개선사항

#### 사용성 향상

- **윈도우 최적화**: DirectShow 자동 사용으로 카메라 호환성 향상
- **자동 에러 처리**: 친절한 오류 메시지와 해결 방법 제시
- **의존성 가이드**: 모델별 필요한 패키지 설치 안내

#### UI/UX 개선

- **일시정지 기능**: 스페이스바로 일시정지/재생
- **경고 표시**: 졸음 감지 시 빨간 테두리 표시
- **상태 정보**: 실시간 눈 상태 및 지속 시간 표시
- **모델 정보**: 사용 중인 모델명 화면에 표시

#### CLI 개선

- **간소화**: 원라이너 API 사용으로 CLI 코드 대폭 단순화
- **안정성**: 에러 처리 및 사용자 경험 개선

### 📦 새로운 예제 파일

- **`examples/simple_usage.py`**: 원라이너 API 사용법 완전 가이드
- 6가지 다양한 사용 예제 포함

### 🔧 기술적 개선

- **크로스 플랫폼**: 윈도우/맥/리눅스 자동 최적화
- **메모리 관리**: 리소스 정리 개선
- **에러 복구**: 카메라 연결 실패 시 자동 재시도

### 📚 문서 업데이트

- **README.md**: 원라이너 API 사용법 추가
- **코드 주석**: 더 자세한 설명 추가

---

## [1.0.0] - 2024-12-18

### 🎉 최초 릴리스

#### 핵심 기능

- **4가지 AI 모델**: OpenCV, RandomForest, CNN, MediaPipe
- **실시간 감지**: ~30 FPS 웹캠 처리
- **크로스 플랫폼**: Windows, macOS, Linux, Raspberry Pi

#### API

- **DrowsinessDetector**: 메인 감지기 클래스
- **quick_detector()**: 빠른 설정 함수
- **ModelRegistry**: 모델 관리 시스템

#### CLI 도구

- **sleepy-driver-demo**: 설치 후 바로 사용 가능

#### 패키징

- **PyPI 배포**: `pip install sleepy-driver`
- **선택적 의존성**: `[ml]`, `[dl]`, `[all]` 옵션
- **GitHub Actions**: 자동 배포 파이프라인

#### 문서

- **포괄적인 README**: 설치부터 고급 사용법까지
- **사용 예제**: 다양한 통합 시나리오
- **성능 벤치마크**: 모델별 속도/정확도 비교

---

### 📝 버전 규칙

- **Major (X.0.0)**: 호환성을 깨는 변경
- **Minor (1.X.0)**: 새로운 기능 추가 (하위 호환)
- **Patch (1.1.X)**: 버그 수정 및 소규모 개선

### 🔗 링크

- **PyPI**: https://pypi.org/project/sleepy-driver/
- **GitHub**: https://github.com/your-org/sleepy-driver
- **문서**: https://sleepy-driver.readthedocs.io/
