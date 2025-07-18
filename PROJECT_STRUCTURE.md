# 📂 SleepyDriver 프로젝트 구조

## 🎯 프로젝트 개요

**운전자 피로도 분석 시스템** - 영상 기반 눈 감김 분석을 통한 실시간 피로도 판단 라이브러리

### 📋 프로젝트 목적

- **운전자의 눈이 감겼는가를 이진 분류**
- **눈을 감은 시간이 몇 초인지 정량 분석**
- **실시간 운전자 피로도 분석 모듈의 통합 라이브러리 구축**
- **스마트카 연계**: ADAS 및 자율주행 시스템의 운전자 모니터링 기능 강화
- **사회적 효과**: 사고 예방 AI 구현 가능
- **기술 학습 효과**: 실시간 영상 처리, 시계열 데이터 분석, Vision 기반 분류 등 산업 적용력 높은 실전형 경험

### 👥 팀원 구성

- **김진현**: AIHub 기반 딥러닝 모델 설계 및 적외선 딥러닝 라벨 정리, PyTorch GPU 리서치, 적외선 모델 구현 및 학습, 오류 디버깅 지원 (infrared_mlp_model.py)
- **김호탁**: 전처리 모듈 구축 및 구조 기획, 좌표 기반 눈 감김 판별 알고리즘 구현, 딥러닝 모델 학습 및 통합, 상속 구조 정리 및 패키지화 주도 (point_model.py)
- **박준규**: OpenCV 기반 접근법 개발, 디렉토리 정리 및 구조 패키지화, 졸음 검출 모듈 구현, PyPI 라이브러리 배포 주도 (opencv_model.py)
- **안승현**: Mediapipe 기반 좌표 추출 및 눈 감김 판별 알고리즘 구현, Kaggle 데이터 기반 딥러닝 모델 개발 및 최적화, PyTorch GPU 환경 세팅 및 적외선 모델 학습 참여 (mlp_model.py)
- **윤선아**: 데이터 수집 및 머신러닝 모델 (SVM, XGBoost, RandomForest) 개발 전반 수행, 모델 최적화 및 적용(ml_model.py)

## 🎯 배포용 권장 구조

```
SleepyDriver/
├── 📄 README.md                    # 프로젝트 소개 (PyPI에서 보여짐)
├── 📄 LICENSE                      # MIT 라이선스
├── 📄 pyproject.toml               # 최신 패키징 설정
├── 📄 setup.py                     # 하위 호환성 (선택사항)
├── 📄 MANIFEST.in                  # 포함할 파일 목록
├── 📄 .gitignore                   # Git 무시 파일
├── 📄 DEPLOYMENT_GUIDE.md          # 배포 가이드
│
├── 📁 sleepy_driver/               # 메인 패키지
│   ├── 📄 __init__.py             # 공개 API
│   ├── 📄 cli.py                  # CLI 명령어
│   ├── 📁 core/                   # 핵심 인터페이스
│   ├── 📁 models/                 # 감지 모델들 (+ .pth, .pkl 파일)
│   ├── 📁 eye/                    # 눈 타겟팅
│   └── 📁 drowsiness/             # 졸음 분석
│
├── 📁 examples/                    # 사용 예제
│   ├── 📄 demo.py                 # 기본 데모
│   └── 📄 custom_model_example.py # 커스텀 모델 예제
│
├── 📁 tests/                       # 테스트 (선택사항)
│   ├── 📄 test_models.py
│   └── 📄 test_api.py
│
├── 📁 docs/                        # 문서 (선택사항)
│   └── 📄 api.md
│
├── 📁 .github/                     # GitHub Actions
│   └── 📁 workflows/
│       └── 📄 publish.yml         # 자동 배포
│
├── 📁 dist/                        # 빌드 결과 (gitignore)
└── 📁 _legacy/                     # 개발 과정 백업 (gitignore)
```

## 🚀 브랜치 전략

### 1. 메인 브랜치

```bash
main/master  # 배포용 안정 버전
└── 포함: sleepy_driver/, examples/, README.md, LICENSE 등
└── 제외: _legacy/, 개발 임시 파일들
```

### 2. 개발 브랜치

```bash
develop      # 개발용 브랜치
└── 포함: 모든 파일 (_legacy 포함)
└── 실험, 테스트, 기존 코드 백업 등
```

## 📦 배포 준비 체크리스트

### 필수 파일

- [ ] `sleepy_driver/` - 메인 패키지
- [ ] `README.md` - 프로젝트 설명
- [ ] `LICENSE` - 라이선스
- [ ] `pyproject.toml` - 패키지 설정
- [ ] `MANIFEST.in` - 포함 파일 목록

### 선택 파일

- [ ] `examples/` - 사용 예제
- [ ] `tests/` - 단위 테스트
- [ ] `docs/` - 추가 문서
- [ ] `.github/workflows/` - CI/CD

### 제외 파일 (.gitignore)

- [ ] `_legacy/` - 개발 과정 백업
- [ ] `dist/`, `build/` - 빌드 임시 파일
- [ ] `__pycache__/` - Python 캐시
- [ ] `.DS_Store` - OS 임시 파일

## 🔄 Git 워크플로우

### 현재 상태 정리

```bash
# 1. 현재 모든 변경사항 커밋
git add .
git commit -m "feat: PyPI 배포 준비 완료"

# 2. 태그 생성 (배포 버전)
git tag v1.2.0
git push origin v1.2.0
```

### 배포용 브랜치 생성 (선택사항)

```bash
# 1. 배포용 브랜치 생성
git checkout -b release/v1.2.0

# 2. 불필요한 파일 제거 (이미 .gitignore 설정됨)
git rm -r _legacy/ --cached  # Git에서만 제거, 로컬은 유지

# 3. 깔끔한 배포용 커밋
git commit -m "release: v1.2.0 PyPI 배포용"
git push origin release/v1.2.0
```

## 📊 패키지 크기 최적화

### 현재 크기 분석

```bash
# 전체 패키지 크기
du -sh dist/sleepy_driver-1.2.0-py3-none-any.whl  # ~7.8MB

# 가장 큰 파일들
find sleepy_driver/ -type f -size +1M -exec ls -lh {} \;
```

### 크기 구성 (예상)

- 📄 PyTorch 모델 (.pth): ~2MB × 3개 = ~6MB
- 📄 RandomForest 모델 (.pkl): ~1.8MB
- 📄 Python 코드: ~0.1MB
- **총 크기: ~7.8MB** ← 적당한 크기!

## 🎯 배포 모범 사례

### 1. 버전 관리

```python
# pyproject.toml
version = "1.2.0"  # 메이저.마이너.패치

# 버전 업그레이드 예시
1.2.0 → 1.2.1  # 버그 수정
1.2.1 → 1.3.0  # 새 기능 추가
1.3.0 → 2.0.0  # 대규모 변경 (Breaking Change)
```

### 2. 릴리즈 노트

```markdown
## v1.2.0 (2025-07-17)

### ✨ Features

- 5가지 AI 모델 지원 (OpenCV, ML, MLP, Point, Infrared)
- CLI 도구 (`sleepy-driver-demo`)
- 실시간 졸음 감지 (~30 FPS)
- 원라이너 API (`start_detection()`)

### 📦 Dependencies

- opencv-python>=4.5.0
- mediapipe>=0.10.0
- Optional: torch, scikit-learn
```

### 3. 지속적 통합 (CI/CD)

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          python -m build
          python -m twine upload dist/*
```

## 🌟 추천 설정

현재 구조가 이미 매우 좋습니다! 추가로 고려할 점:

1. **GitHub 리포지토리 연동** - PyPI에서 소스코드 링크
2. **자동 테스트** - GitHub Actions으로 PR마다 테스트
3. **문서 사이트** - Read the Docs 연동
4. **버전 자동화** - `bump2version` 도구 사용

하지만 **현재 상태로도 완벽하게 배포 가능**합니다! 🚀

## 📞 연락처

- **GitHub**: https://github.com/kimhotac/sleepy-driver-detector
- **이메일**: junju404@naver.com (박준규)
