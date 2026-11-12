# [researcher] E3 · E4 — 방 카드 오더 메모 위 「담당 상담사」 표시 원천 조사 (read-only)

너는 **day `researcher` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 rules · skills · tools · workflow).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web` (코디 워크트리 — 리포트 1개 외 수정 · 생성 금지)

## 1. SSOT

- 사용자 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` 「E2E 피드백」 E1 ~ E4 + 보충. 요지: 방 카드 오더 메모에 제목 줄 「오더 메모 [상담사 이름 배지 …]」 + 오른쪽 끝 파란 「접기/펼치기」 · 구분선 없음 · **상담사 여러 명이면 여러 명 다**(사용자 결정).
- 사용자 HAR(값 출력 금지): `/Users/kknaks/Downloads/상담사 조회 .har` — 코디 확인: entry 80 `POST …/consultation/v1/queries/get-consultations-by-visitor-id` 응답 `data[].counselors[]`(id · name) 에 담당 상담사가 있음. entry 24 `schedule/v2/queries/get-schedules-for-reservation` 의 tasks[].doctors[] 에도 같은 이름이 나옴(상담 작업의 담당자일 수 있음 — 확인).
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web` (dev + fix-web 미커밋 변경 — **frontend/backend 워커 작업물, 수정 금지**). 단서: `backend/day/emr/kos/mapper.py:535` `counselor_external_id=single(row.get("counselors"))` · `:600` `requested_counselor_external_id` · `backend/day/emr/sync.py:941` `requested_counselor_id` · `:1646-1672` 상담 `counselor_id`.
- 스펙(읽기만): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec/products/day/20-spec/spec-000-data-model.md` · `spec-002-procedure-board.md`(U-1 카드 메모 · E39 · 스냅샷 cards[]).

## 2. 질문

1. DAY 가 지금 저장하는 상담사 값 전부: 테이블 · 칸 · 원천(KOS 어느 응답 · 어느 필드) · 동기화 주기. `single(...)` 이 여러 명 중 하나만 고르는지(버리는 규칙).
2. 판 카드(방문 1건)에서 「담당 상담사」로 쓸 후보: (a) 그 방문의 상담 기록 `counselor_id` (b) 방문 예약 `requested_counselor_id` (c) 상담 작업(task)의 담당자 (d) 기타. 각 후보가 HAR 의 「(HAR 의 상담사)」과 같은 값인지, 지금 로컬 DB(읽기만 · `day-local` postgres 컨테이너 `docker exec day-local-postgres-1 psql …` SELECT 만 · 값은 건수 · 있음/없음만 출력)로 판 카드에 붙일 수 있는지.
3. **여러 명**: KOS 가 상담사를 여러 명 주는 자리(`counselors[]` 배열)를 DAY 가 담을 칸이 있나. 없으면 바꿀 후보(배열 칸 · 연결 테이블 · …)와 migration 필요 여부 · 데이터 규칙(spec-000 · `config/projects/day.json` data_rules) 충돌.
4. 오더 메모(판 카드 메모)의 원천 · 그 메모와 상담의 연결(같은 상담 행인가) — 「오더 메모 위 상담사」가 그 메모를 쓴 상담의 상담사가 되도록 묶을 수 있나.
5. 스냅샷 `cards[]` 에 상담사 이름을 싣는 자리 후보 · 앱(`app/lib/model/board.dart`)이 새 칸을 무시하는지(깔린 앱 무영향 확인).
6. 손댈 파일 목록(백엔드 · 템플릿 · CSS · 테스트 · 스펙 절) — grep 전수.

## 3. 범위 제약

- 파일 수정 · 커밋 금지. KOS 호출 금지(HAR · 코드 · 로컬 DB 읽기만). DB 쓰기 금지. 11040 화면 조작 금지.
- 고객 · 직원 실명 · 키 · 토큰 리포트 출력 금지(「HAR 의 상담사」처럼 가린다).

## 4. 검증 · 리포트

질문마다 답 + 근거(파일:줄 · HAR entry 번호 · SQL 건수). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 고칠 방향 후보 · 「정할 것」.

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/research-2-report.md`

## 5. 완료 보고 — 문구 변경 금지

- 커밋 · push · PR 하지 마라. 끝나면 두 명령 모두:

```bash
orca orchestration send --to term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: <한 줄>" --body "요약 / 정할 것"
orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
