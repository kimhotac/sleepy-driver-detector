# 👥 팀 워크플로우 가이드

## 🌿 브랜치 전략 (간단함!)

우리 팀의 Git 브랜치는 아주 간단합니다:

```
main       ← 안정 버전 (팀원들이 작업)
└── infra  ← 배포 전용 (배포 담당자만)
```

## 👨‍💻 팀원들 (일반 개발자)

### 일반적인 개발 과정

```bash
# 1. 메인 브랜치에서 작업
git checkout main
git pull origin main

# 2. 코드 수정 및 커밋
# (sleepy_driver/ 폴더 안의 파일들 수정)
git add .
git commit -m "fix: 눈 감지 정확도 개선"

# 3. 푸시
git push origin main

# 끝! 매우 간단함 😊
```

### 주의사항

- ❌ `infra` 브랜치는 건드리지 마세요
- ✅ `main` 브랜치에서만 작업하세요
- ✅ 평소처럼 개발하면 됩니다

## 🚀 배포 담당자 (인프라 관리자)

### 배포 과정

```bash
# 1. main의 최신 변경사항을 infra로 가져오기
git checkout main
git pull origin main

git checkout infra
git merge main

# 2. 버전 업데이트 (필요 시)
# pyproject.toml에서 version = "1.0.1" → "1.0.2"

# 3. infra 브랜치에 푸시 → 자동 배포!
git push origin infra
```

### 자동 배포 프로세스

1. **infra 브랜치 푸시** → GitHub Actions 자동 실행
2. **테스트 실행** → Python 3.8~3.11에서 검증
3. **패키지 빌드** → wheel + tar.gz 생성
4. **PyPI 자동 업로드** → 전 세계 사용자가 설치 가능
5. **슬랙/이메일 알림** (설정 시)

## 📋 브랜치별 역할

| 브랜치  | 역할      | 접근 권한        | 자동 동작      |
| ------- | --------- | ---------------- | -------------- |
| `main`  | 개발 작업 | 👥 모든 팀원     | 없음           |
| `infra` | 배포 관리 | 🚀 배포 담당자만 | PyPI 자동 배포 |

## 🎯 배포 시나리오

### 시나리오 1: 버그 수정 배포

```bash
# 팀원이 main에 버그 수정 커밋
# 배포 담당자가 배포 결정
git checkout main && git pull
git checkout infra && git merge main
git push origin infra  # → 자동 배포!
```

### 시나리오 2: 새 기능 배포

```bash
# 1. 버전 업데이트
# pyproject.toml: version = "1.0.0" → "1.1.0"

# 2. 배포
git add pyproject.toml
git commit -m "bump: version 1.1.0"
git push origin infra  # → 자동 배포!
```

### 시나리오 3: 긴급 배포

```bash
# GitHub에서 Actions → "🚀 Publish to PyPI" → "Run workflow"
# 수동으로 즉시 배포 가능
```

## 🔒 권한 설정 (GitHub)

### 브랜치 보호 규칙

```
infra 브랜치:
- ✅ 배포 담당자만 푸시 가능
- ✅ PR 없이 직접 푸시 허용
- ✅ GitHub Actions 자동 실행

main 브랜치:
- ✅ 모든 팀원 푸시 가능
- ✅ 자유로운 협업 환경
```

## 📊 배포 모니터링

### 배포 상태 확인

1. **GitHub Actions**: https://github.com/your-repo/actions
2. **PyPI 페이지**: https://pypi.org/project/sleepy-driver/
3. **다운로드 통계**: PyPI에서 확인 가능

### 배포 성공 알림

```bash
# 배포 완료 시 자동으로 생성되는 정보:
📦 Package: sleepy-driver
🏷️ Version: 1.0.1
🔗 PyPI: https://pypi.org/project/sleepy-driver/
🌿 Branch: infra

### 설치 방법
pip install sleepy-driver
sleepy-driver-demo
```

## 🆘 문제 해결

### Q: 배포가 실패했어요!

**A**: GitHub Actions 탭에서 오류 로그 확인 → 배포 담당자에게 문의

### Q: 잘못된 버전을 배포했어요!

**A**: 새 버전으로 다시 배포 (PyPI는 동일 버전 덮어쓰기 불가)

### Q: main과 infra가 달라졌어요!

**A**: `git checkout infra && git merge main`으로 동기화

---

**🎉 이 워크플로우의 장점:**

- ✅ **팀원들은 main에서만 작업** → 매우 간단
- ✅ **배포는 자동화** → 실수 방지
- ✅ **권한 분리** → 안전한 배포 관리
- ✅ **브랜치 최소화** → Git 초보자도 쉬움
