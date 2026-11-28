# [planner] 예약 현황판 고침 F1 ~ F6 + 문진 6개월 · KOS 문진 동기화 — SPEC 개정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec` (base `origin/main` `b9ac374e` · 너 혼자 쓴다)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` **§2 결정 표** ← 사용자 결정(2026-11-27 행 전부). **계약의 SoT. 다시 열지 마라. 위 행이 최신이고 아래 행을 덮는다(취소선 = 뒤집힘).** 여기 없는 정책은 발명하지 마라. §1 F1 ~ F6 은 피드백 원문.
- 근거 리포트(같은 폴더): `research-1-report.md`(F1 ~ F6 코드 원인 · 파일:줄 · 스펙 근거 R64 · R70 · spec-007 규칙) · `be-f6-debug-1-report.md`(F6 원인 확정 · 고칠 자리) · `be-kos-questionnaire-1-report.md`(KOS 문진 읽기 실물 · 경로 · 키 · 답 대조 표). **KOS 경로 · 키는 이 리포트 그대로**(지어내지 마라).
- 스크린샷(같은 폴더 · Read): `f1-kos-add-slot.png` · `f3-day-detail-modal.png` · `f3-kos-survey-menu.png` · `f5-day-device-card.png`
- 기존 SPEC(이 워크트리): `products/day/20-spec/spec-006-reservation-board.md`(R64 · R70 · R71 배치) · `spec-007-reservation-detail.md`(문진 QR · 여권 스캔 · 기기 팝오버 규칙 7 · 표시 요청 · 고침 이력) · `spec-003-mobile-app.md`(앱 표시 요청 · 태블릿) · `spec-002-procedure-board.md`(KOS 동기화 · 매핑 주인 확인) · `spec-000-data-model.md`(`questionnaire_history` · `external_ref`) · `20-spec.md` · `10-decision.md` · `log.md`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` (CENTURION_DAY `origin/dev` `65506f35` · `AGENTS.md` 먼저)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자가 dev 예약 현황판을 써 보고 피드백을 줬고, 조사 3건으로 원인과 결정을 닫았다(§2 결정 표). 이번에 SPEC 을 고치고 → 검수 → WORK · Delivery Issue → 코드까지 간다. 너는 **SPEC 개정**까지.

묶음(결정 표 요약 — 문장마다 결정 표 행을 근거로 인용):
1. **F1** 열 오른쪽 여백 = 카드 반 폭(70px) · 그 자리 호버 점선 [+] · 툴팁 「그룹 | 시작 ~ 끝」(끝 = 그 그룹 간격) · 누르면 그 그룹 · 시간 예약 등록
2. **F2** 카드 높이 = 예약 길이 비례(30분 = 1칸 · 60분 = 2칸 · 15분 = 반 칸 · 시간 칸 위에 시작 ~ 끝 위치) — **R70 뒤집음**. 시간이 겹치는 카드는 옆 자리(겹치는 동안만) — R64(5장 넘으면 아래 줄) · 행 높이 `lines` · R71(동행 같은 30분 행) · 동행 띠가 이 배치와 어떻게 맞는지 정리(결정에 없는 것은 OQ)
3. **F3 · F5** [문진 QR] = 팝오버 하나(위: 링크 복사하기 · 링크 열기 / 아래: 기기 줄) · [여권 스캔] = 팝오버 하나(기기 줄만) · 기기 줄 = `기기명 [점] 상태`(초록 연결 · 빨강 미연결 · 미연결도 보이고 누름) · 고르면 그때 요청 만들고 바로 보냄 · 웹 「이 화면 QR」 · 모달 안 기기 칸 없앰 · 링크 수명 10분 그대로. 링크 복사 · 열기의 요청 생성 시점(누를 때)과 기존 「같은 방문 열린 요청 취소」 규칙의 관계는 spec-007 규칙에서 정리(결정 없으면 OQ)
4. **F6 고침** 상세 다시 그리기(GET 상세 · 동행 저장 · 신분확인 · 앱 상세 JSON)가 공개 origin 을 넘김 — `be-f6-debug-1-report.md` §3. 시험 조건(GET 상세 실제 service 로 열린 문진 QR 이 그려지는지)
5. **F4** 문진 6개월 — 고객의 마지막 문진 제출일부터 · 재진에도 · 값 = env · 지나면 「초진 문진」 줄에 「6개월 경과」 · 판정 단위 = 고객(지금 방문 단위에서 바뀜 — 예약 상세 · 고객 차트 기준 통일)
6. **KOS 문진 동기화** — 10초 일정 동기화(`day.emr.sync_schedules_hospital`)에 같이 · 6개월 안 제출이 확인된 고객은 건너뜀 · 제출 없음 / 경과 고객만 매 회차 · KOS 공개 `get-questionnaire-submit` · 중복 = DAY 제출 응답의 KOS 제출 id 를 `external_ref` 에 저장해 가름 · `inputType` · `subText` = 양식 답 id 로 맞춤 · 400 = 제출 없음 · `source = read` 사용 여부 · `visit_id` 빈 행(고객 단위) 허용 — 리포트 「정할 것」 중 결정 표에 없는 것은 OQ 로

산출물: 관련 SPEC 개정(spec-006 · spec-007 · spec-000 · 동기화 주인 문서 — 어느 문서가 주인인지 기존 관례로 정함) · `20-spec.md` · `10-decision.md` · `log.md`. **30-work(WORK) · Delivery 는 이번에 쓰지 않는다** — SPEC 검수 통과 뒤 따로.

## 3. 계약

다른 워커와 합의된 계약 없음(문서 단계). 경로 · 칸 · 키 이름은 「이름 제안」. KOS 경로 · 응답 키 · 답 대조는 `be-kos-questionnaire-1-report.md` 그대로.

## 4. 먼저 읽을 핵심 파일

- 리포트 셋(§1) · spec-006 R64 · R70 · R71 근처 · spec-007 규칙 2 · 3 · 7 · 고침 6 · API 표
- 코드: `backend/day/policies/reservation_layout.py` · `policies/reservations.py:199-208` · `static/day.js`(research §3.1 · 3.2 줄) · `templates/partials/reservations_display*.html` · `services/displays.py` · `routers/reservation_detail.py:179 · 327 · 407` · `routers/api/reservations.py:104` · `services/questionnaire_reads.py` · `queries/customers.py:448-456` · `models/reception.py` · `enums/reception.py` · `emr/kos/identity.py` · `tasks/emr.py` · `emr/sync_schedules.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 결정 표 2026-11-27 행을 화면 요소 · 동작별로 묶고 SPEC 문장마다 근거(결정 표 행 요지 · 리포트 §)를 단다
2. spec-006 개정: F1 · F2(R70 뒤집기 이력 · 새 배치 규칙 · R64 · R71 과의 관계)
3. spec-007 개정: F3 · F5 팝오버 · 요청 생성 시점 · 이 화면 QR 없앰 · F6 origin 규칙 · F4 표시 · 판정 단위
4. 동기화 주인 문서 개정: KOS 문진 읽기(경로 · 키 매핑 표 · 건너뛰기 조건 · 중복 키 · 실패 처리) · spec-000 칸 변화(`external_ref` 종류 · `visit_id` null · `source`)
5. 앱(spec-003)에 닿는 것(F6 앱 상세 JSON origin · 여권 · 문진 흐름)은 웹과 같은 service 변경만 · 앱 화면 변경 없음이면 그렇게 적기
6. 케이스 매트릭스 · OQ · `20-spec.md` · `10-decision.md` · `log.md`
7. §8 검증

## 7. 범위 제약 — 하지 말 것

- **화면 문구를 지어 넣지 않는다.** 결정 표에 있는 문구만(「링크 복사하기」 「링크 열기」 「6개월 경과」 · 「연결」 「미연결」). 없으면 비우고 OQ
- 결정을 다시 열지 않는다. 결정끼리 어긋나 보이면 OQ 로 적고 코디에게 묻는다
- 범위 밖: 예약 · 접수 · 상담 · 시술 **모달 디자인 수정**(다음 단계) · 외국인 신분확인 · 기획안(`00-baseline/planning/`) · 다른 제품 폴더
- 스크린샷 · 리포트의 사람 이름 · 전화 · id 원문을 예시로 옮기지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 보고 본문에 결정 표 2026-11-27 행 중 SPEC 에 반영 안 된 것(있으면 이유)과 OQ 목록을 적어라.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
