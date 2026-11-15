# 작업 요약 — llm-codex-hotfix (mediness)

기간: `2026-11-13` ~ `2026-11-15`
결과: spec #942·code #153 머지(main `6f175d80`)·dev 반영 #154 — 11-13 15:14 KST 운영 배포, 실물 codex 호출 D(주간보고)·B(결정 게이트) 성공, C(브리프)는 백필 없이 정기 실행으로 11-14·11-15 PUBLISHED(11-10~13 FAILED 이후 첫 성공)

## 1. 무엇을 했나

2026-11-10 조직이 Claude Code 구독 접근을 막아, 서버가 worker 경유로 부르는 claude 호출이 전부
`Your organization has disabled Claude subscription access for Claude Code` 로 실패하고 있었다(데일리 브리프
11-10~13 매일 FAILED, 주간보고 AI 요약 11-13 4콜 실패). 운영 배포 env 를 실측해 claude 를 실제로 쓰는 경로를
가려내고(A·B·C·D, E·F 는 이미 codex), worker 를 타는 B(결정 게이트)·C(데일리 브리프)·D(주간보고)를 회의록 v2
선례 모양의 codex 제출로 바꾸는 main 핫픽스를 냈다. back 이 직접 spawn 하는 A(AX 비서)는 인프라 작업이 필요해 후속으로 뺐다.

## 2. 적용한 기술·개념

- **코드 기본값이 아니라 배포된 파드의 env 로 판정** — 「어디서 claude 를 쓰나」 조사
  - 왜 이걸 골랐나: 코드 grep 만으로는 후보 6개였고 회의록이 codex 인지도 기본값으로만 말할 수 있었다. 사용자가 「서버 배포 기준」을 요구했고, 실측해 보니 `ACTION_RUNTIME_LLM_DRIVER` 는 차트가 아니라 클러스터 secret 에 있었고, 브리프(C)는 `LLM_VENDOR=mock` 인 dev 에서도 claude 로 나가 같은 에러로 죽는 등 코드만으로는 안 보이는 사실이 나왔다.
  - 무엇이 어려웠나: provider 가 worker 로그에 안 찍혀 「큐 → 코드의 provider 값 + 성공/실패 패턴」 으로 판정했다. back 로그는 APScheduler 스팸으로 ~6h 만 남아 A 의 실패는 추정으로 남았다.
  - 근거: `survey-prod-claude-usage.md` · [[externalized-configuration]]
- **CLI provider 전환 = 변수 교체가 아니라 제출 스펙 교체** — claude ↔ codex
  - 왜 이걸 골랐나: codex 어댑터는 claude 전용 키(`system_prompt`·`max_turns`·`mcp_config`·`allowed_tools`·`disallowed_tools`·`effort`)를 받으면 제출 자체를 거부한다. 그래서 provider 문자열만 바꾸는 대신 system 은 본문 앞 합성, turn 상한은 시간 상한으로, 허용 도구는 `-c mcp_servers.<key>.enabled_tools`(접두어 없는 이름)+툴별 approve 로 옮겼다. 접두어를 붙인 채 넘기면 조용히 「툴 0개」 가 된다.
  - 무엇이 어려웠나: 새로 설계하면 검증이 길어진다 → 운영에서 이미 도는 회의록 v2 의 조립(`meeting_v2_submission`)을 글자 단위로 따르고 `compose_prompt`·`redact_config_overrides` 를 재사용해 리뷰를 「선례와 같은가」 대조로 줄였다.
  - 근거: mediness-app #153 `back/app/services/server_llm_submission.py` · WP-133 대응표 · [[tool-allowlist-by-phase]]
- **argv 단일 문자열 한계(`MAX_ARG_STRLEN` 128KiB)** — codex 는 프롬프트를 argv 하나로 넘긴다
  - 왜 이걸 골랐나: 회의록 v2 가 147KB 에서 `E2BIG` 로 터진 전례가 있고, 브리프는 본문만 ~100KB 를 목표로 한다. cap 을 줄이는 건 SPEC 계약 변경이라 핫픽스에서 하지 않고, system+본문 합본 바이트 로그를 넣어 첫 실호출로 여유를 재기로 했다.
  - 근거: `review-code-report.md` 실물 체크포인트 2 · [[argv-length-limit]]

## 3. 막혔던 것 / 사고

- 사용자 의도를 두 번 잘못 읽었다 — 「핫픽스라는 게 클로드로 생성한다는 거야?」 에 서버 쪽과 워커 쪽을 섞어 답했고, 「재개해 줘」 「코드 수정부터 하라니까」 에서 머지 확인을 한 번 더 물어 흐름을 끊었다. → 이미 「codex 로 살린다」·「테스트 안 돌려도 된다」 로 방향이 정해졌으면 남은 단계(머지)는 진행하고 보고한다.
- 「변수만 바꾸는 거니까 테스트 안 돌려도 된다」 — 실제로는 제출 스펙 전체가 바뀌는 변경이었다. 테스트 생략은 받아들이되(CI 가 테스트를 안 돌림을 확인) 완료 조건을 운영 실물 호출로 남겼다. 기존 claude 단정 테스트 3파일은 깨진 채로 남는다.
- 프로젝트 config 에 main 기준 backend·reviewer 워커가 없었다 → `backend_hotfix`·`reviewer_code_hotfix`(repo `app_main`)를 추가했다. 첫 시도는 JSON 재직렬화로 diff 68줄이 났고, 되돌려 블록만 끼워 넣었다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-13 | 판단 기준은 코드 기본값이 아니라 운영 배포 env | 사용자 지시 |
| 2026-11-13 | 사용자 PC 데몬 `agent/` 는 범위 밖 | 사용자 — 개인 로컬, 서버 토큰과 무관 |
| 2026-11-13 | codex 로 살린다 — 이번 범위 B·C·D(코드만), A 는 인프라 후속 | 사용자 · worker 에만 codex·인증이 있다는 실측 |
| 2026-11-13 | main 기준 핫픽스 → main→dev 반영 | 운영 = main |
| 2026-11-13 | 설정 키는 공용 한 벌 `SERVER_LLM_PROVIDER`·`SERVER_CODEX_MODEL` | 같은 큐를 쓰는 세 콜 — WP 권장안 |
| 2026-11-13 | 테스트 작성·실행 생략, 수용은 운영 실물 호출 | 사용자 · CI 가 테스트를 돌리지 않음 확인 |
| 2026-11-13 | 브리프(C) 백필·W47 주간보고 재채움 안 함 | 사용자 — 사람이 직접 채움 |

## 5. 날짜별 로그

- `2026-11-13` 운영 실측으로 서버 claude 경로가 11-10 부터 이미 실패 중임을 확인 → SPEC 4건·WP-133(#942) → B·C·D codex 전환 핫픽스(#153) main 머지
- `2026-11-13` CI 가 ARC 러너 403 으로 대기 → 인프라가 GitHub App 인증으로 교체, 낡은 listener 삭제·재실행 → 15:14 KST 배포 완료(back 이미지 받기로 API 약 18분 중단) · 운영 실호출 D·B 성공
- `2026-11-14` main → dev 반영(#154 cherry-pick, 충돌 없음)
- `2026-11-15` 브리프 정기 실행 11-14·11-15 codex 로 PUBLISHED 확인 → 마감

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.
아래에는 판단의 근거가 된 리포트·PR·커밋을 구체적으로 남긴다.

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/942
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/153
- dev 반영 PR: https://github.com/MediSolveAIDev/mediness-app/pull/154 (cherry-pick, 스쿼시 `628f7d8e`)

- `kknaksss/llm-codex-hotfix-spec` → `mediness`
  - `3f63221c` spec(mediness): 서버 LLM codex 전환 핫픽스 — SPEC-111/070/130/116 개정 + WP-133
- `kknaksss/llm-codex-hotfix-hotfix` → `main`
  - `ebbb2e42` fix(back): 서버 LLM 콜 claude → codex 전환 핫픽스 — 결정 게이트·데일리 브리프·주간보고 (WP-133)
- 리포트: `survey-prod-claude-usage.md` · `review-spec-report.md` · `be-hotfix-report.md` · `review-code-report.md`

## 7. 잔여

- A(AX 비서 — back 이 `claude -p` 직접 spawn): back 파드에 codex 실행 파일·인증이 없다. GitOps 차트(`/opt/codex` 마운트 + PATH + back 용 codex 인증 — worker `CODEX_HOME` 공유 금지) 후 secret `ACTION_RUNTIME_LLM_DRIVER=codex-unsafe-tools`. 보안 대가(임의 파일 읽기) 사용자 판단 필요.
- `DEPLOY.md §4-4` 가 docker-compose 시절 절차 — k8s(secret `mediness-secret`) 기준으로 개정.
- 기존 테스트 `test_brief_synthesizer`·`test_decision_gate_ai`·`test_decision_gate_redesign` 의 claude 단정 — codex 기본값으로 깨진 채.
- WP-133 Open ②~⑤: 브리프 argv 여유(첫 실호출 bytes) · 브리프 본문 펜스 · B 계측 `collect_stream_stats` codex 호환 · SPEC-111 속도 재측정.
- 브리프 argv 여유(Open ②)는 아직 못 쟀다 — 11-14·15 성공분의 `server_llm final_prompt` 로그가 back 로그 순환(~6h)으로 사라짐. 재려면 실행 직후 로그를 떠야 한다.
- back Deployment 가 Recreate 라 이미지 교체 동안 API 가 내려간다(이번 18분) — 롤링 전환·이미지 선반입 검토.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/mediness/llm-codex-hotfix/README|llm-codex-hotfix]]
<!-- work-links:end -->
