# day-mobile-v2 Delivery #262 · #263 v2 재결속 — 결과 보고

## 상태: blocked — harness 가 머지 전 커밋을 baseline 으로 받지 않는다 (우회 안 함)

두 Issue 모두 **변경 없음**이다. v1(contract_version 1 · baseline `ccede286` · plan_digest 그대로) 상태이고, 승인 receipt 는 적용하지 않았다. 문서 수정 · 커밋도 없다.

## 막힌 것

| 항목 | 값 |
|---|---|
| 요청 baseline | 워크트리 HEAD `7d19831719d3984a272ae91d56e2b75348a67b54`(브랜치 `kknaksss/day-mobile-v2-spec` · PR mediness#955 · 머지 전) |
| fetched `origin/main` | `ccede2866d006607509c5e34bdad33079fa9dffd`(`7d198317` 은 origin/main 의 조상이 아님 — 머지 안 됨) |
| 명령 | `uv run mediness start-delivery --request <main|fcm>.v2.request.json --mediness-repo <워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2 --github-repo MediSolveAIDev/CENTURION_DAY --plan --json` |
| 출력(둘 다 · rc=2) | `{"error": "requested SPEC baseline is not the fetched latest origin/main revision", "status": "conflict"}` |
| 코드 근거 | `tools/harness/src/mediness_harness/workflow.py:917-928` — `baseline = fresh_origin_main(...)` 를 받는다. `--plan` 은 Issue 를 찾지 않아(`existing` 없음) 이 조건에서 멈춘다. `--apply` 도 `:1042-1045` 「new or changed Contract baseline is not the fetched latest origin/main revision」에서 멈춘다. 계약이 바뀌므로(`contract_changed`) 머지 전 커밋은 어느 경로로도 baseline 이 될 수 없다 |

`--apply` 는 실행하지 않았다. 위 코드상 GitHub 쓰기 전에 같은 conflict 로 멈추기 때문이다. 규칙상(delivery-workflow 「SPEC 은 fetch 한 latest origin/main 의 exact Git object 에서 읽는다」)도 우회 대상이 아니다.

## 풀 방법 (코디 · 사용자 판단)

1. **권장** — 스펙 PR #955 를 머지한다. 그 뒤 같은 key 로 아래 요청 파일의 `spec_baseline_revision` 만 새 `origin/main`(머지 SHA)으로 바꿔 `--plan` → `--apply` 를 실행한다. 요청 내용은 준비돼 있다.
2. 머지 전에 Issue 문구라도 고쳐야 하면, `spec_baseline_revision = ccede286`(지금 origin/main)으로 v2 를 결속하는 방법이 harness 상 가능하다. 다만 baseline 은 여전히 옛 계약이라 머지 뒤 v3 재결속이 또 필요하다. 이번 브리프의 「baseline = 7d198317」과 달라 실행하지 않았다.

## 준비된 v2 요청 (반영 항목 체크)

파일: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-day-mobile-v2-spec/55c97167-02b2-4ce4-8179-785d92dc4074/scratchpad/delivery/{main,fcm}.v2.request.json`(같은 key · `contract_version 2` · `scope_delta` 있음 · baseline 칸 = `7d198317…` — 머지 뒤 SHA 로 바꿀 것).

| 반영 항목 | #262 | #263 |
|---|---|---|
| A2 `can*` = 서비스 거절 규칙 정본(웹 템플릿과 같을 필요 없음) | ✓ A2 · Target Delta M-4/5 | — |
| A3 호출 취소 확인 창 없음 · 복귀 · 점유 띠 · 방 목록 재묶음 · 「담당의 미정」 누름 | ✓ A3 | — |
| M-6 본문 「{방} · 호출 취소」 · 그 호출이 완전히 닫힐 때만 · 일부 줄 취소 = 알림 없음 · 원래 알림 닫기(read_at · 앱 · 웹 tag) · 웹 = OS 알림만 | ✓ Target Delta M-6 · A4 · Non-Goals(웹 목록 · 종 화면) | ✓ 채널 「원장 호출」에 호출 취소 |
| 단계 시작 조건 = 의존 표(P1 · P2 · P3 · P4 승인 즉시 병렬 · P5 = P1 뒤만 · P6 = P2 · P3 · P4 뒤 · P7 = P5 · P6 뒤) — 직렬 없음(W-15) | ✓ execution.phases · dependencies | ✓ F1 · F2 · F3 |
| 출시 순서 prod 서버 먼저 → 정식 앱 · 되돌리기에 통역 되울림 · 새 경로 404(W-16) | ✓ Target Delta M-1 · A6 · predeploy · rollback · Review Surface | ✓ predeploy · F3 |
| 통역 TokenGate · 빈 final · `audio_stop` id 무시 · `playback_stopped` → `audio_end` · stop 큐 비움 · 시드 `.11` 검사 | ✓ M-8 · A5 · P1 · P5 | — |
| Firebase 준비됨 — 「사용자 대기」 조건 걷음 · `google-services.json` 한 벌 · 키 dev · prod 각 1 · 값은 레포 밖 | — | ✓ Target Delta · Review Surface · dependencies(사용자 Firebase 뺌) |
| Android 채널 「원장 호출」 · 「채팅」(OQ-A59 닫음) | — | ✓ |
| 착수 막는 OQ = 기본값으로 착수 가능(K18 · 77 · 78 이름 · A50 · A51) · 시안 게이트(A52 · A54) | ✓ Review Surface | ✓ |

새 digest: **없음** — 결속하지 못해 계산되지 않았다. 지금 Issue 는 v1 digest 그대로다(#262 plan `sha256:2f5930b3…` · #263 plan `sha256:85b22374…` — 옛 계약이므로 승인하면 안 됨).
