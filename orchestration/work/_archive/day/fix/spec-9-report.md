# fix-spec-9 결과 보고 — 저장소 정정 3(환경 = 컨테이너 · 환경 폴더 없음)

## 상태: done

근거 = `fix/correction-storage-3.md` 결정 1 ~ 6 · planner 줄(사용자 2026-11-11 「daydev / dayprod 이렇게 컨테이너 만들고」 · 「일단 그렇게 했다고 가정하고 코드 짜면 안 돼? 그럼 환경 설정값만 내가 주면 되는 거 아니야?」). 컨테이너 이름 `daydev` · `dayprod` 만 적었고 계정 이름 · 주소는 적지 않았다. 커밋 · push 0. D = `products/day/40-architecture/deployment.md` · S4 = `products/day/20-spec/spec-004-internal-chat.md`.

## 고친 자리

| 문서:줄 | 내용 |
|---|---|
| D `:19` · `:20` | 머리 — 「적지 않는 값」에서 컨테이너는 `daydev` · `dayprod` 만 예외 · **정정 3 개정 줄**(7판 사용자 확정 「맨 위 = 환경 폴더」 · 8판 「환경 폴더 그대로」를 사용자가 컨테이너 분리로 바꿈 · 아직 없음 · 사용자가 인프라 요청) |
| D `:171` | env 표 — dev 컨테이너 = `daydev` · prod = `dayprod`(아직 없음 · prod 값은 prod 배포 때 사용자) |
| D `:184` | 「저장소 · 환경」 — 환경 = 컨테이너 · 설정값 · 코드 · 시험은 특정 이름 가정 안 함 · **지금 실제 상태(처음 만든 컨테이너 하나 · `daydev` · `dayprod` 없음 · 사용자 요청)** · 없으면 `ContainerNotFound` = 503 |
| D `:185` | 「경로」 — 컨테이너 안 `{용도}/{병원 id}/…` · 환경 폴더 없음(옛 `{환경}/…` 취소선) |
| D `:187` | 「로컬 개발」 — 경로 모양 `{용도}/{병원 id}/…` · 옛 로컬 키와 같은 모양 |
| D `:189` | 「키」 — 모양 검사만 · 「키의 환경」 검사 없앰 · 환경은 컨테이너가 정함 |
| D `:190` | 「dev ↔ prod」 — dev `daydev` · prod `dayprod` 설정상 · 같은 관리 ID 면 권한상 서로 읽음(사실만) · 생성 · 권한 = 사용자가 인프라 요청 |
| D `:196` | 「prod」 — `dayprod` · 같은 구조 |
| D `:223` | Blob 준비 행 — `daydev` · `dayprod` 아직 없음 · 사용자 요청 |
| D `:239` | 미결 — 「파일 저장소 컨테이너 `daydev` · `dayprod`」(아직 없음 · 생성 + 권한 · 없는 동안 503 · 생기면 설정 그대로) · 사용자가 인프라 담당에게 요청 |
| S4 `:32` | 머리 개정 ⑤ — 키 `{환경}/chat/…` 취소선 → 정정 3(`chat/{병원 id}/…` 그대로 · 서버는 자기 환경 컨테이너만) |
| S4 `:417` | §3 「키」 — `chat/{hospital_id}/…` · 환경 폴더 없음 · 모양 검사만 · 로컬 기존 키 그대로 읽힘(「옛 키 안 읽음」 문제 없어짐 — 결정 6) |
| S4 `:565` | 프로토와 다른 곳 — 컨테이너 = 환경 · 키 `chat/…` |
| S4 `:613` | C-A26 — 키 `chat/{병원 id}/…` · 「컨테이너 이름은 설정에서만」 단언 · 「다른 환경 키 · 옛 키」 갈래 삭제 |
| S4 `:614` | C-A27 ⓑ — 컨테이너 `daydev` 안 `chat/{병원 id}/…`(생긴 뒤) |
| `spec-000-data-model.md:31` · `:1089` · `:1161` | 키 설명 `{용도}/…` · `identity/…` · `chat/…`(환경 = 컨테이너) |
| `log.md` | 9판 1줄 |
| `wp-plan.md:21` · `:168` · `:177` · `:182` · `:184` · `:187` · 실물 몫 | WP-BE-4 — 환경 접두 · 환경 `check_key` · 옛 키 거절 걷어 냄(지금 코드 모양 그대로) · 컨테이너 이름은 설정에서만 · `dev.env` = 안내문 주소 + `daydev` + `blob` · `prod.env` 값 없음 · 시험의 환경 폴더 단언 걷어 냄 · 실물 경로 `daydev` 안 `chat/…` |

`system.md` 는 경로를 적지 않아(「deployment.md 절」 링크만) 바꿀 것 없음.

## 옛 문장 grep

`grep -rn "{APP_ENV}/\|{환경}/\|dev/chat\|맨 위 = 환경\|키의 환경\|키 환경\|환경 폴더\|{env}/chat\|다른 환경 키\|prod/…"` → `products/day` + `wp-plan.md` 에서 취소선 · 「정정 3」 · 「환경 폴더 없음」 설명 문장을 빼면 **`log.md` 의 7판 · 8판 이력 줄 2개만** 남는다(이력 — 그대로 둠). 살아 있는 계약 문장 0.

## Delivery #241

v3 결과 계약(Target Delta · A13 · Review Surface)에 `경로 {환경}/{용도}/{병원 id}/…` 가 적혀 있었다 → **계약이 바뀌므로 version 을 올렸다**(정정 문서 규칙).

| 항목 | 값 |
|---|---|
| contract_version | **4**(scope delta 기록 — 더해진 범위 없음) |
| risk | L3 그대로 |
| contract_digest | `sha256:9b26269c4930837b2c44fac19fb457197cd6bc5c927d05f58f6fe8fe55111a9d` |
| plan_digest | `sha256:8a037f7aea63361a1d9b4ab01e969c7ebfdc46bf126e2fc3a457d0397ed69c6c`(v3 승인 stale) |
| 승인 | **적용함**(`human` · `kknaksss` · 근거 = 위 사용자 인용) |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| next_action | `prepare-spec-baseline` |

바꾼 것: Target Delta 파일 저장소 줄(환경 = 컨테이너 · 키 `{용도}/…` · 이름 확정) · A12(키 모양 · 설정에서만) · A13(`daydev` 안 경로 · 생긴 뒤) · Review Surface(8판에서 알린 옛 표시 — 「이름 = 코디 기본값」 · 「사용자 미결」 — 도 같이 바로잡음) · Non-Goals(「옛 키 옮기기」 · 「dev/prod 컨테이너 분리」 → 「컨테이너 생성 · 권한(인프라)」) · Execution(predeploy · dependencies · open questions). request = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v4.request.json`.

## 검증

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0.
