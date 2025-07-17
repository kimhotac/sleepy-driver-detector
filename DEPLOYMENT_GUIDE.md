# 🚀 SleepyDriver PyPI 배포 가이드

이 가이드는 SleepyDriver 라이브러리를 PyPI에 배포하는 방법을 단계별로 설명합니다.

## 📋 사전 준비

### 1. PyPI 계정 생성

1. [PyPI](https://pypi.org/) 방문
2. 계정 생성
3. 이메일 인증 완료
4. 2FA 설정 (권장)

### 2. TestPyPI 계정 생성 (테스트용)

1. [TestPyPI](https://test.pypi.org/) 방문
2. 계정 생성 (PyPI와 별도)

### 3. API 토큰 생성

1. PyPI → Account settings → API tokens
2. "Add API token" 클릭
3. Token name: `sleepy-driver`
4. Scope: "Entire account" (첫 업로드) 또는 "Project: sleepy-driver"
5. 생성된 토큰 저장 (한 번만 표시됨!)

## 🛠️ 로컬 환경 설정

### 1. 필요한 도구 설치

```bash
# 빌드 도구 설치
pip install build twine

# 또는 dev 의존성으로 일괄 설치
pip install -e .[dev]
```

### 2. 프로젝트 정리

```bash
# 임시 파일 정리
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.egg-info" -type d -exec rm -rf {} +
rm -rf build/ dist/
```

### 3. 버전 확인 및 업데이트

```bash
# pyproject.toml과 setup.py에서 버전 확인
# 버전 형식: 1.0.0, 1.0.1, 1.1.0 등
```

## 🔨 패키지 빌드

### 1. 빌드 실행

```bash
# 소스 배포판과 휠 생성
python -m build

# 생성된 파일 확인
ls -la dist/
# sleepy_driver-1.0.0-py3-none-any.whl
# sleepy-driver-1.0.0.tar.gz
```

### 2. 빌드 결과 검증

```bash
# 패키지 내용 확인
python -m zipfile -l dist/sleepy_driver-1.0.0-py3-none-any.whl

# 메타데이터 확인
python -m twine check dist/*
```

## 🧪 테스트 배포 (TestPyPI)

### 1. TestPyPI에 업로드

```bash
# TestPyPI 업로드
python -m twine upload --repository testpypi dist/*

# 인증 정보 입력
# Username: __token__
# Password: [TestPyPI API 토큰]
```

### 2. TestPyPI에서 설치 테스트

```bash
# 가상환경 생성
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# test_env\Scripts\activate   # Windows

# TestPyPI에서 설치
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sleepy-driver

# 기능 테스트
python -c "from sleepy_driver import quick_detector; print('Import success!')"
sleepy-driver-demo --list-models
```

## 🌟 프로덕션 배포 (PyPI)

### 1. 최종 점검

```bash
# 최신 코드인지 확인
git status
git log --oneline -5

# 테스트 실행
python -m pytest tests/ -v

# 문서 확인
cat README.md
```

### 2. PyPI 업로드

```bash
# 실제 PyPI 업로드
python -m twine upload dist/*

# 인증 정보 입력
# Username: __token__
# Password: [PyPI API 토큰]
```

### 3. 업로드 성공 확인

```bash
# PyPI 페이지 확인
# https://pypi.org/project/sleepy-driver/

# 실제 설치 테스트
pip install sleepy-driver
sleepy-driver-demo --version
```

## 🔄 업데이트 배포

### 1. 버전 업데이트

```python
# pyproject.toml
version = "1.0.1"  # 1.0.0 → 1.0.1

# setup.py (사용 중인 경우)
version="1.0.1"
```

### 2. 변경사항 문서화

```markdown
# CHANGELOG.md 또는 README.md에 추가

## [1.0.1] - 2024-01-15

### Fixed

- 좌우 눈 감지 순서 수정
- 에러 메시지 표시 개선

### Added

- CLI 명령어 추가 옵션
```

### 3. 재빌드 및 업로드

```bash
# 이전 빌드 파일 삭제
rm -rf dist/ build/

# 새로 빌드
python -m build

# 업로드
python -m twine upload dist/*
```

## 🛡️ 보안 및 모범 사례

### 1. API 토큰 관리

```bash
# ~/.pypirc 파일 생성 (선택적)
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...
```

### 2. 환경변수 사용

```bash
# 토큰을 환경변수로 설정
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcC...

# 업로드
python -m twine upload dist/*
```

### 3. GitHub Actions (CI/CD)

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
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: "3.8"
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 📝 체크리스트

### 배포 전 체크리스트

- [ ] 모든 테스트 통과
- [ ] README.md 업데이트
- [ ] 버전 번호 증가
- [ ] CHANGELOG 작성
- [ ] 의존성 확인
- [ ] 라이선스 파일 포함
- [ ] .gitignore에 dist/, build/ 포함

### 배포 후 체크리스트

- [ ] PyPI 페이지 확인
- [ ] `pip install sleepy-driver` 테스트
- [ ] CLI 명령어 테스트
- [ ] 문서 링크 확인
- [ ] GitHub 릴리즈 태그 생성

## 🚨 문제 해결

### 일반적인 오류

1. **"File already exists"**

   ```bash
   # 버전 번호를 올리고 다시 빌드
   ```

2. **"Invalid credentials"**

   ```bash
   # API 토큰 재확인
   # Username: __token__ (정확히 입력)
   ```

3. **"Package validation failed"**
   ```bash
   # twine check로 사전 검증
   python -m twine check dist/*
   ```

### 도움말 링크

- [PyPI 공식 가이드](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine 문서](https://twine.readthedocs.io/)
- [Python 패키징 가이드](https://packaging.python.org/)

## 🎉 축하합니다!

성공적으로 배포가 완료되면:

1. 사용자들이 `pip install sleepy-driver`로 설치 가능
2. CLI 명령어 `sleepy-driver-demo` 사용 가능
3. PyPI 통계에서 다운로드 수 확인 가능

**이제 전 세계 개발자들이 당신의 라이브러리를 사용할 수 있습니다! 🌍✨**
