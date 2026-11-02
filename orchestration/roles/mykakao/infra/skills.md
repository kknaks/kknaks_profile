# @mykakao-infra — 기술 스택

- Docker + docker compose (redis `7-alpine` + codex worker)
- open-kknaks worker (RedisBroker) + codex CLI (Linux 바이너리 `.codex-tools/`)
- Bash 스크립트 (`setup.sh`·`run.sh`) — 현재 macOS 전제
- Python venv (`run.sh` 가 만든다)

## 핵심 원칙
- 최소 변경 · 자격증명은 레포 밖 · 못 한 검증은 못 했다고 쓴다
