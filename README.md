# 🚗 SleepyDriver - AI 기반 졸음 감지 라이브러리

[![PyPI version](https://badge.fury.io/py/sleepy-driver.svg)](https://badge.fury.io/py/sleepy-driver)
[![Python](https://img.shields.io/pypi/pyversions/sleepy-driver)](https://pypi.org/project/sleepy-driver/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SleepyDriver**는 운전자의 졸음 상태를 AI(컴퓨터 비전)로 감지하는 파이썬 라이브러리입니다. 5가지 다양한 감지 모델을 지원하며, 간단한 API로 프로젝트에 쉽게 통합할 수 있습니다.

## ✨ 주요 기능

- 🎯 **5가지 감지 모델**: OpenCV, 머신러닝(RF), 딥러닝(CNN), MediaPipe, 적외선 기반
- ⚡ **실시간 처리**: 웹캠에서 실시간 졸음 감지 (~30 FPS)
- 🔧 **간단한 API**: 3줄의 코드로 졸음 감지 시스템 구축
- 📦 **플러그인 아키텍처**: 사용자 정의 모델 쉽게 추가 가능
- 🛡️ **안정성**: 강력한 에러 처리와 의존성 관리
- 🖥️ **CLI 지원**: 설치 후 바로 사용 가능한 명령행 도구

## 🚀 빠른 시작

### 설치

```bash
pip install sleepy-driver
```

### 코드 사용법 (초간단!)

```python
from sleepy_driver import start_detection
start_detection('mlp')  # MLP 모델로 바로 시작
# start_detection('ml', threshold_ms=2000)  # ML 모델, 2초 임계값
# start_detection('opencv')  # OpenCV 모델
# start_detection('point')  # MediaPipe 모델
# start_detection('infrared')  # 적외선 모델
```

## 📋 지원 모델

| 모델         | 설명                           | 장점              | 의존성       |
| ------------ | ------------------------------ | ----------------- | ------------ |
| **opencv**   | OpenCV 기반 전통적 컴퓨터 비전 | 빠름, 의존성 적음 | 없음         |
| **ml**       | RandomForest 머신러닝          | 균형잡힌 성능     | scikit-learn |
| **mlp**      | CNN 딥러닝                     | 높은 정확도       | PyTorch      |
| **point**    | MediaPipe 랜드마크             | 실시간성 우수     | 없음         |
| **infrared** | 적외선 CNN 딥러닝              | 야간 감지 우수    | PyTorch      |

## 📊 성능 벤치마크

| 모델      | 평균 FPS | 정확도 | 메모리 사용량 |
| --------- | -------- | ------ | ------------- |
| OpenCV    | ~35 FPS  | 85%    | ~50MB         |
| ML (RF)   | ~30 FPS  | 90%    | ~100MB        |
| MLP (CNN) | ~28 FPS  | 95%    | ~200MB        |
| Point     | ~40 FPS  | 80%    | ~30MB         |
| Infrared  | ~25 FPS  | 92%    | ~250MB        |

_테스트 환경: MacBook Pro M1, 720p 웹캠_

## 👥 라이브러리 소개

**운전자 피로도 분석 시스템** - 영상 기반 눈 감김 분석을 통한 실시간 피로도 판단 라이브러리

### 🎯 라이브러리 목적

- **운전자의 눈이 감겼는가를 이진 분류**
- **눈을 감은 시간이 몇 초인지 정량 분석**
- **사회적 효과**: 사고 예방 AI 구현 가능
- **기술 학습 효과**: 실시간 영상 처리, 시계열 데이터 분석, Vision 기반 분류 등 산업 적용력 높은 실전형 경험

### 👨‍💻 개발 팀

| 이름       | 역할                                                                                                                                                  | GitHub                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **김진현** | AIHub 기반 딥러닝 모델 설계 및 적외선 딥러닝 라벨 정리, PyTorch GPU 리서치, 적외선 모델 구현 및 학습, 오류 디버깅 지원                                | [@JinhyeonK](https://github.com/JinhyeonK)       |
| **김호탁** | 전처리 모듈 구축 및 구조 기획, 좌표 기반 눈 감김 판별 알고리즘 구현, 딥러닝 모델 학습 및 통합, 상속 구조 정리 및 패키지화 주도                        | [@kimhotac](https://github.com/kimhotac)         |
| **박준규** | OpenCV 기반 접근법 개발, 디렉토리 정리 및 구조 패키지화, 졸음 검출 모듈 구현, PyPI 라이브러리 배포 주도                                               | [@ParkJunGyu26](https://github.com/ParkJunGyu26) |
| **안승현** | Mediapipe 기반 좌표 추출 및 눈 감김 판별 알고리즘 구현, Kaggle 데이터 기반 딥러닝 모델 개발 및 최적화, PyTorch GPU 환경 세팅 및 적외선 모델 학습 참여 | [@asho227](https://github.com/asho227)           |
| **윤선아** | 데이터 수집 및 머신러닝 모델 (SVM, XGBoost, RandomForest) 개발 전반 수행, 모델 최적화 및 적용                                                         | [@dotoriysa](https://github.com/dotoriysa)       |

## 🛠️ 개발자 가이드

### 로컬 개발 설정

```bash
# 저장소 클론
git clone https://github.com/kimhotac/sleepy-driver-detector.git
cd sleepy-driver-detector

# 개발 의존성 설치
pip install -e .[dev]

# 테스트 실행
pytest tests/

# 코드 포맷팅
black sleepy_driver/
flake8 sleepy_driver/
```

### 패키지 빌드

```bash
# 빌드 도구 설치
pip install build twine

# 패키지 빌드
python -m build

# PyPI 업로드 (관리자만)
twine upload dist/*
```

## 🤝 기여하기

1. [Fork 저장소](https://github.com/kimhotac/sleepy-driver-detector/fork)
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- [MediaPipe](https://mediapipe.dev/) - 얼굴 랜드마크 감지
- [OpenCV](https://opencv.org/) - 컴퓨터 비전 라이브러리
- [PyTorch](https://pytorch.org/) - 딥러닝 프레임워크
- [scikit-learn](https://scikit-learn.org/) - 머신러닝 라이브러리

## 🆘 지원 및 문의

- 📖 **문서**: [GitHub README](https://github.com/kimhotac/sleepy-driver-detector#readme)
- 🐛 **버그 리포트**: [GitHub Issues](https://github.com/kimhotac/sleepy-driver-detector/issues)
- 💬 **디스커션**: [GitHub Discussions](https://github.com/kimhotac/sleepy-driver-detector/discussions)
- 📧 **이메일**: junju404@naver.com (박준규)

---

**⚠️ 주의사항**: 이 라이브러리는 보조 도구로만 사용하세요. 실제 운전 시에는 항상 안전을 최우선으로 하고, 졸음을 느끼면 즉시 안전한 곳에 정차하여 휴식을 취하세요.
