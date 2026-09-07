# @mykakao-infra — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: `git branch --show-current` → `README.md` 의 「AI 요약 파이프라인」 절 → compose·스크립트 통독

## 탐색 경로 (레포 루트 기준)
```
docker-compose.yml     # redis + codex worker (backend·DB 없음)
Dockerfile.worker      # open-kknaks worker 이미지
worker/run.py          # codex provider worker 기동 (cwd=/project)
setup.sh               # codex CLI 설치 + 인증 복사 + trust 등록 + .env 생성
run.sh                 # venv → 의존성 → 키 복구 → uvicorn
.env.example           # NAMESPACE/QUEUES/REDIS_URL/CONCURRENCY/WORK_DIR
backend/summarize.py   # (읽기만) 큐 설정이 맞물리는 반대편
```

## 금지 사항
- `backend/`·`frontend/` 수정 금지 · 문서 SoT 수정 금지
- git commit·push·PR 금지 · 실제 자격증명 커밋 금지
