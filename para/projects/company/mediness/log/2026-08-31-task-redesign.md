
# 작업 요약 — task-redesign (mediness)

기간: `2026-08-31` ~ `2026-08-31`
결과: dev 머지·배포 완료(mediness-dev 실검증 통과). main 릴리스 PR 2건(mediness#667·mediness-app#138) 오픈 상태로 종료.

## 1. 무엇을 했나

mediness 의 업무 태스크가 세 원장(`tasks` 정본 / `version_wbs_task` 미러 / `decision_execution_task` 레거시)으로 갈라져 상태 어휘가 4벌이었고, incident 워크플로(SPEC-152)는 개정 8회 누적으로 죽은 계약 27건이 잔존한 채 코드와 어긋나 있었다. 사전 조사(문서·코드 2벌 × 2라운드) → 사용자와 쟁점을 하나씩 확정 → 스펙(도메인 SoT 2건 신설·ERD 재작성·SPEC 10건 개정) → 코드(WP-126: 5값 cutover·거절 폐기·착수 명시화 / WP-127: incident 라운드 판정 1벌·run 감사·Slack fail-loud) → 사용자 실물 샘플 기반 **슬랙 에러 채널 어댑터**(#900 전건 자동 승격, IB-1~9)까지 한 작업 단위로 착지시켰다. 검수(스펙 2R + 코드 3R) 전 라운드 FAIL 해소, dev 실배포로 마이그레이션·enum·파드 검증까지 완료.

## 2. 적용한 기술·개념

- **PG enum 동시 cutover + 사전 가드 마이그레이션 (0136)** → [[database-migration]] 보강 — 값이 동형 계약인 enum 2개(`runtime_task_status`·`version_wbs_task_status`)를 한 migration 에서 5값으로 접고 `accepted_at` 을 drop
  - 왜 이걸 골랐나: PG 는 enum 값 제거 문법이 없어 rename→새 타입→USING 캐스트→drop 4단(0108 선례)이 유일한 길. 두 enum 을 따로 바꾸면 「6=6」 동형 계약이 순간적으로 깨진다
  - 무엇이 어려웠나: 운영 DB 실측 불가(P0) → 검증을 **migration 안 RAISE 가드**로 옮겼고, 로컬 기동에서 가드가 실제 발화(고아 60건 — 전부 레거시 decision 이관분)해 backfill(이벤트 소급 후 drop) 설계로 확정. "가드가 배포를 멈춘다"를 리스크가 아니라 실측 수단으로 쓴 사례
  - 근거: `back/alembic/versions/0136_task_status_five_value_cutover.py` · mediness-app#136 · dev 실배포 alembic head 확인
- **상태머신 축소가 실버그를 지우는 설계** — `accept_pending`·거절 폐기(5값)로 「거절한 태스크 1건이 run 을 영구 정지시키는」 구조 결함이 **상태 하나 지우는 것으로 자동 해소**
  - 왜 이걸 골랐나: 거절은 상태를 안 바꿔 비terminal 로 영구 잔존했고, 게이트는 이미 반쯤 무력화(WBS 400·phase 도달 불가·incident round0 우회). 「내가 못 한다」는 재배정 요청(todo 리셋)으로 흡수 — 원장이 멈추지 않는 표현으로 대체
  - 근거: research-task-status.md §B-S6·C8 · `machine.py` · `_RESUME.md` §2
- **라운드 종결 판정 수렴 (4벌→1벌)** — 같은 판정이 4곳에 다른 모수로 구현돼 「이전 라운드 비terminal 1건 = 루프 영구 정지」. `round_rule.active_round_complete` 정본 1벌 + 전이 seam 안쪽 호출로 완료 표면 4개가 전부 워크플로를 깨우게
  - 무엇이 어려웠나: 판정 트리거에 CANCELED 누락(마지막 태스크를 취소로 닫으면 라운드 미종결)이라는 잠복 실버그를 P0 실측이 발견 — 스펙의 「취소도 terminal」 계약 착지로 함께 수리
  - 근거: `back/app/services/action_runtime/tasks/round_rule.py` · reviewer 리포트(review-code-wp126-report.md)
- **fail-loud 원칙 (조용한 no-op 폐기)** → [[fail-fast]] 신설 — Slack 토큰 미설정 시 채널 생성을 건너뛰고 성공 처리하던 것을 503 실패로 전환. 커널에 `ExecutionUnavailable` seam(실패 원장 커밋 후 재-raise)
  - 왜 이걸 골랐나: `responding` 의 유일한 출구가 그 채널이라 조용한 no-op = run 영구 매장. 웹 완료 버튼 대안은 사용자가 기각(대응 대화가 회고의 유일한 입력)
  - 근거: spec-152 §U-2 · `engine/runtime.py` · test_wp126_fail_loud.py
- **슬랙 에러 채널 어댑터 — 실물 우선 계약** — 형식 문서가 없는 인바운드를 사용자 제공 샘플 2종(HTTP/TASKIQ)으로 계약화(IB-1~9). 파서는 예외 불투과·파싱 실패여도 raw 로 raise(유실 금지), 제품명→슬러그 검색 해소(부분 일치 거부)
  - 무엇이 어려웠나: 검수가 파서 헬퍼의 예외 누출(불가능 시각 '24:00' → 500 → Slack 재전송이 duplicate 로 접혀 **알림 유실**)을 격리 재현으로 잡음 — 유실 금지 계약의 정면 구멍이라 R2 정정
  - 근거: `incident/slack_error_adapter.py` · spec-152 §인바운드 트리거 · review-adapter-report.md
- **squash-merge 후 브랜치 위생** — squash 된 브랜치는 `git log` 로 미머지처럼 보인다(런북 기지). 아카이브 안전검사가 이를 잡았을 때 tree-diff 로 내용 동일성을 증명하고 origin 으로 reset 해 원인 제거(검사 우회 금지 규율)
- **셀프호스트 러너 긴급 CD 우회** → [[ci-cd]] 보강 — GitHub 결제 장애로 호스팅 러너 전면 차단 → build 를 `medisolve-arm64`(사내 ARC)로 전환해 배포 완주. az CLI 부재는 설치가 아니라 **`az acr login` = docker login 치환**으로 해소(ephemeral pod 라 설치 무의미)
  - 근거: mediness-app `e0748f66` · CHARTY stg run 33389477922 전 잡 성공 · k8s_infra_mac docs/self-hosted-ci.md 갱신분

## 3. 막혔던 것 / 사고

- **upstream 번호 선점 2회** — 작업 중 base 에 #659(WP-124)·#665/#137(WP-125·migration 0135)이 머지돼 우리 번호와 충돌 → rebase 충돌 해소 + 재번호(WP 2건·DOC 2건·migration 1건·코드 90/스펙 18파일). upstream 이 추가한 줄을 line-exact 보존 목록으로 지키는 방식으로 의미 오염 0. **교훈: 활동 많은 base 에서 번호 자원(WP·DOC·migration)은 늦게 붙일수록 안전하고, 치환은 문맥 앵커가 필수**
- **로컬 DB 고아 alembic 리비전** — 폐기된 실험 브랜치가 DB 버전만 남기고 사라져 upgrade 불가 → 스키마 실측(프로브)으로 0124 동등성 증명 후 버전 포인터만 정정. **reset 대신 실측 먼저** 규율이 데이터(task 656·회의 87) 지킴
- **GitHub Actions 결제 차단** — 「잡이 5초 만에 스텝 0개로 실패」가 코드 문제처럼 보였으나 어노테이션 확인으로 결제 원인 판명. 셀프호스트 우회로 당일 배포 완주(위 §2)
- **검수 지적의 사후 낙과 1건** — 코디가 나중에 넣은 0135 backfill 수정이 기존 orphan 테스트(구 계약 어서션)를 깨뜨린 걸 재번호 라운드에서야 발견. **마이그레이션을 고치면 그 마이그레이션의 테스트를 즉시 재실행**해야 했다
- **워커 API 사망 2회·보고 명령 hang 1회** — 런북 표대로 재개 주입·ctrl+b 백그라운드 전환으로 회수. 재부팅으로 코디 핸들 교체 1회(브리프 갱신 + 인박스 폴링 병행)

## 4. 결정

`_RESUME.md` §2 결정 표가 정본(19건). 핵심만:

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-08-31 | `accept_pending`·수락·거절 폐기 → 5값 | 게이트 반쯤 무력 + 거절이 run 영구 정지 유발. 거절 = 재배정 요청으로 흡수 |
| 2026-08-31 | 착수 = 명시 시작만 (시스템 생성도 todo → 시작 전이) | 자동 착수 3벌이 실제 착수와 원장을 갈라놓음 |
| 2026-08-31 | 원장 전면 통합 + incident 재정비 = 한 작업 | 사용자 「전체 재정비」 확정 |
| 2026-08-31 | run 감사 payload 요구 폐기 — 기존 원장 + 역조회 | `workflow_run_events` 의 「payload 의도적 부재」 계약 존중 (검수 실측) |
| 2026-08-31 | accepted_at 고아 = backfill 후 drop | 로컬 RAISE 실증 — 60건 전부 레거시 이관분, 이력은 이벤트 원장으로 |
| 2026-08-31 | 슬랙 어댑터 = #900 전건 자동 승격, 게이트가 사람 필터 | 사용자: 「메시지 쌓이면 바로 승인 게이트」 — 사전 필터 없음 |
| 2026-08-31 | 추적 Task cc = AI 초대 후보 유지 | 「버전 참여자」 축이 시스템에 부재(실측) — 발명 금지, OQ-13 재정의 대기 |
| 2026-08-31 | ~~요청 테스크 같은 작업 단위~~ → 별도 신규 작업 분리 | 기존 작업 확실히 마무리 우선 (설계 결정 7건은 확정 상태로 이월) |
| 2026-08-31 | 알림/DM·게이트 에스컬레이션 = 후속 고도화 | 범위 통제 |

## 5. 날짜별 로그

- `2026-08-31` 사전 조사 2벌(task·incident) → 쟁점 확정 → 스펙 라운드(검수 2R) → spec PR #661
- `2026-08-31` WP-126 코드(BE/FE, 검수 R2) + WP-127 문서·코드(검수 R2) + 슬랙 어댑터(스펙 IB-1~9 + 코드, 검수 R2) → code PR #136
- `2026-08-31` 로컬 스택 기동 검증(0136 가드 실증→backfill)·upstream 2차 동기(재번호)·#661/#136 squash 머지·main 릴리스 PR #667/#138
- `2026-08-31` GitHub 결제 장애 → 셀프호스트 러너 우회로 mediness dev 배포 완주(실검증) + CHARTY stg 배포 지원 + 러너 가이드 갱신

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/661 (MERGED) → main 릴리스 https://github.com/MediSolveAIDev/mediness/pull/667 (OPEN)
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/136 (MERGED) → main 릴리스 https://github.com/MediSolveAIDev/mediness-app/pull/138 (OPEN)
- 리포트: `review-spec-report.md`(R1+R2) · `review-wp126-report.md` · `review-code-report.md` · `review-code-wp126-report.md` · `review-adapter-report.md`
- 조사: `research-task-status.md` · `research-incident.md` · `research-slack-error-adapter.md`
- 부수: CHARTY stg 셀프호스트 배포(#46 + stg ACR fix) · k8s_infra_mac `docs/self-hosted-ci.md` 긴급 우회 절(lusca 워크트리, 미커밋)

## 7. 잔여

- **main 릴리스 PR 2건 머지 대기** — mediness#667 · mediness-app#138 (배포 주의 5건 본문 기재: 0136 가드·Slack 토큰/scope·어댑터 활성화 사람 작업 3개·좌초 run 처분·prod 첫 풀 ~10분)
- **prod 배포 사전조건**: `slack_decision_bot_token`+scope 4종 / 봇 #900 초대·`message.channels` 구독·env 2개(`SLACK_ERROR_ALERT_CHANNEL_ID`·`SLACK_ERROR_ALERT_BOT_IDS`)
- **다음 작업(신규 슬러그)**: 업무요청 테스크 — 결정 7건 확정 상태(게이트 없음·파생 구분·member 축·due/expected 분담·슬랙 DM 전달·진입점 2곳·페이지 리디자인은 사용자 주도)
- 후속 판단: 결제 복구 후 CHARTY CD runs-on 원복 여부 · mediness build 셀프호스트 유지(arm64 네이티브라 유리) · 러너 이미지에 az 굽기 · self-hosted-ci.md 갱신분 커밋 경로
- 이월 OQ: 알림/DM·게이트 에스컬레이션(OQ-2) · 좌초 responding run 소급 처분 · SPEC-153 콘솔 본체 · WP-114 소유 조정(OI-1) · 회의록 어휘 코드 반영은 WP-126 P6 완료로 닫힘
