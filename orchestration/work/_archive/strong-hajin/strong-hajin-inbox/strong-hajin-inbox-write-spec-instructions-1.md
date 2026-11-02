# [writer] SPEC 추가 지시 1 — 사용자 결정 반영 (2026-10-06)

브리프 `strong-hajin-inbox-write-spec-brief.md` 그대로 유효(allowed_paths 같음). 근거 = `_RESUME.md` §2 2026-10-06 마지막 세 행.

## SPEC-008
- OQ 처리(행은 남기고 「닫힘 — 사용자 결정 2026-10-06」 + 본문 계약에 반영):
  - 801 토큰 암호화 = env 의 **대칭키 하나**(Fernet 류) · 키 회전은 범위 밖
  - 802 슬랙 Socket Mode = **연동 전용 워커 새로**, 레플리카 1
  - 803 Gmail = **pull** (이미 §5) — 닫기만
  - 804 이번엔 **회사판만** — 개인판 redirect 는 범위 밖으로
  - 805 **보존·파기 없음 — 회사 데이터라 계속 보관**(D-49 를 대체하는 사용자 결정. 소프트 딜리트도 물리 삭제 없음)
  - 806·807 첨부 한도: **메일 보내기 25MB(Gmail 자체 한도) · 그 밖(카톡 수집 저장 · 슬랙 보내기) 50MB.** 카톡 동영상·음성은 저장 안 함(D-31). 한도 초과 카톡 첨부 = 「너무 큼 — 카톡에서 확인」 · 메일 25MB 초과 = 보내기 막음
  - 808 **사람마다 복제**(D-25)
- §4.5 로컬 redirect 는 지금 값 유지(`http://127.0.0.1:8000/...`)

## SPEC-009
- **DB 여는 방식 참조를 바꾼다**: kakaocli 가 아니라 **우리 mykakao 의 Mac 방식**을 따른다 — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/10-decision/decision-001-extraction-approach.md`(accepted · kakaocli 는 reference-only, 런타임 의존 없음) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/20-spec/spec-001-message-extraction.md`(사용자 ID 복구 절차 포함) · 로컬 코드 `/Users/kknaks/git/toy_pr2/mykakao`. **절차는 여전히 쓰지 마라** — 참조 한 줄 + 경계 입출력만(지금처럼)
- kakaocli 언급은 「참고」로 낮춘다(사이드카·의존 아님)
- OQ 처리: 901 **같은 Strong Hajin 데스크톱 앱에 수집을 더한다** — SPEC-006 「파일 권한 없음」 불변식(I-2)을 **개정 필요**로 명시(SPEC-006 파일은 고치지 말고 「SPEC-006 개정 필요」로 적기) · 902 폴링 **2초** · 903 mykakao SPEC-001 복구 절차 따름 · 904 기존 서명·공증 절차, 자동 업데이트 없음 · 905 상태 문구 「카카오톡을 읽을 수 없습니다 — 카카오톡 버전이 바뀌었을 수 있습니다」
- 첨부 한도 50MB

두 SPEC 버전 0.1.0 → 0.2.0, 변경 이력 한 줄. 끝나면 §9 로 보고.

## 추가 (코디 · 같은 판에 반영)
- SPEC-008 비밀값 절: 로컬은 **레포 규칙 `~/.config/<서비스>/env`** — `~/.config/google/env`(GOOGLE_OAUTH_* · GMAIL_PUBSUB_* · GOOGLE_PUBSUB_SA_KEY_FILE) · `~/.config/slack/env`(SLACK_*). `Makefile` 이 `SONIOX_ENV_FILE`·`THECONNECT_ENV_FILE` 과 같은 방식(`set -a; . 파일`)으로 읽는다(근거 `Makefile:2-9`). 운영은 k8s Secret → 차트 `secretRef`(`k8s_infra_mac/charts/strong-hajin/templates/back.yaml:48-50` · `worker.yaml:39-41`). 이름 규칙: 외부 서비스 값 = 서비스 접두어(예 `TDL_*`), 내부 설정 = `AX_*` — 토큰 암호화 키는 내부라 `AX_` 로
