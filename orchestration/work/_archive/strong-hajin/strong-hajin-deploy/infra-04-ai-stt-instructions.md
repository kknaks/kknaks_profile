# [infra 2차] AI 대화 · STT · 회의실 연결 (2026-10-01, 사용자 지시 「다 연결」)

## A. STT·회의실 키 → `strong-hajin-secret` (지금)
- 원천(사용자 Mac): `~/.config/soniox/env`(SONIOX_API_KEY) · `~/.config/theconnect/env`(TDL_EMAIL·TDL_PASSWORD)
- 코드가 읽는 키 전수: `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy grep -n 'SONIOX\|TDL_' -- backend/src` — TDL_BASE_URL·TDL_COMPANY_ID 등 기본값이 없는 게 있으면 로컬 설정(`config/projects/strong-hajin.json` local_dev env_files, 코드 기본값)에서 찾고, 없으면 멈추고 질문
- 값은 **파이프로만**: 로컬 env 파일을 읽어 `kubectl create secret generic strong-hajin-secret --from-env-file=/dev/stdin --dry-run=client -o yaml | kubectl apply -f -` 식으로. 화면·파일·리포트 출력 금지. 기존 시크릿의 다른 키가 있으면 보존
- back·worker 재시작(rollout restart) → 실측: STT 토큰 발급 API 1회 성공(응답 코드만) · 회의실 조회 API 1회 성공

## B. AI(codex) — 사용자 로그인 뒤
- 사용자가 전용 인증을 만든다: `CODEX_HOME=~/strong-hajin-deploy-data/codex-home codex login --device-auth` → `~/strong-hajin-deploy-data/codex-home/auth.json`
- 그 파일이 생기면(코디가 알린다) 같은 파이프 방식으로 strong-hajin-prod codex-home PVC 에 덮고 worker 재시작 → AX 턴 1회 실측(워커 로그 성공)
- 이 인증은 Strong Hajin 전용 — mediness·사용자 로컬 `~/.codex` 와 공유하지 않는다(refresh token 회전)

## 보고
`report-infra-deploy.md` 에 §A·§B 추가(명령은 값 가림). A 끝나면 한 번, B 끝나면 완료 두 채널.
