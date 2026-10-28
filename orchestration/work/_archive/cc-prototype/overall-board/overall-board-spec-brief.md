# [planner] 시술 현황 → 전체현황판 시안 반영 — SPEC-003 0.4.0 패치 + WORK-005

너는 **cc-prototype `planner` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 코디와 공유. allowed_paths 밖은 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

- **결정 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 결정 표 (2026-10-23 줄 전부).** 이번 판의 정책은 여기 있는 것뿐이다. 취소선 줄은 뒤집힌 것이다 — 지금 것만 반영.
- **시안(정본)** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 의 **「시술 현황」 하위 화면**(`M:777-1098` + 팝오버 `M:1101-1153`) 과 헤더(`M:63-92`)
  - 분석 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md` §1 · §2 · §4 · §6(시술 행) · §8 · §10 · §11
- 현재 코드 인벤토리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/current-board-report.md` (전 항목 `파일:줄`)
- 고칠 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` (0.3.0) · 형식 참고 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-003-procedure-board.md`
- 결정 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자가 시술 현황판을 Claude Design 에서 「Ceramique 전체현황판」으로 다시 그렸다. 이 시안의 「현황」 메뉴 안에는 예약 현황 · 원내 현황 · 시술 현황 세 하위 화면이 있는데, **이번 판은 시술 현황만** 한다(예약 현황은 KOS API 조사가 먼저라 다음 판 · 원내 현황은 범위 밖). **시안이 정본**이다.

`_RESUME.md` §2 의 2026-10-23 결정을 요약하면(원문은 거기서 읽어라):
1. 헤더 상단 메뉴는 **「현황」 하나만**. 시안 헤더(로고 · 메뉴 · 시계 · 지점 · 계정 · 로그아웃 · 사이드바 없음)를 따른다. 호버 드롭다운 하위 항목은 **「시술 현황」 하나만**(예약 · 원내 현황은 아직 없으니 그리지 않는다 — 코디 기본값, §10 에 열린 것으로)
2. 시술 카드 **「방 배정」 줄만 뺀다** — KOS ETCETERA 중 room 이 있는 작업(코드 `procedure/back/app/kos/sync.py:39-40` 판정 규칙). **다른 ETCETERA(마취 · 시트팩 · 관리 마무리 등)는 남긴다** — 지금처럼 읽기 전용 줄(제목 + KOS 상태). 시안엔 이 줄이 없지만 사용자 결정이 이긴다 → §6.7 표에 적는다. OQ-517 을 닫는다
3. **[입실순 | 배치순] 버튼 뺀다.** 정렬 = 드래그 순서
4. **「KOS 반영 중 / 실패」 카드 표시 뺀다**(시안대로). 실패는 토스트로만(지금 코드의 오류 토스트)
5. **카드 드래그 순서 = back DB 저장**(ccc 만 · KOS 반영 없음). 기본값: 모든 화면 공유(SSE 스냅샷에 실음) · 그날 단위 · 순서 없는 새 카드는 맨 뒤(그들끼리 입실순) · 귀가 대기 카드는 드래그 제외 · 맨 뒤 귀가 대기 시각 순(시안 `M:1425-1430`)
6. 그 밖의 화면 차이는 **시안대로**(리포트 §4 와 current 리포트를 맞대어 찾아라 — 예: 카드 불투명도 · 드래그 중 표시 · 범례 · 제목 줄 · 패널). 코드가 시안과 다른데 결정 표에 없는 것은 **시안을 따르고** 목록으로 남긴다. 판단이 안 서면 열린 것(OQ)으로.

## 3. 계약

이번에 네가 **만든다** — back ↔ front 계약(드래그 순서):
- 테이블(§3.2) · API(§7.3 조작에 추가, 예: `PUT /api/board/order` body = 카드(visit) id 목록 — 모양은 네가 정하되 기존 §7 관례(오류 `{error:{code,message}}` · Bearer) 를 따른다) · 스냅샷(§7.2)에 순서 반영 방식(카드 배열을 이미 정렬해서 줄지, `order` 필드를 줄지 — 하나로 정하고 근거)
- 동시에 두 사람이 바꿀 때 규칙(마지막 쓰기가 이긴다 등) · 순서 목록에 없는/이미 없어진 카드 처리

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` §3.2 · §5.9 · §6.2 · §6.3 · §6.7 · §7.2 · §7.3 · §10
- 코드는 읽기만: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back/app/` · `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/components/procedures/` · `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/components/common/AppHeader.tsx` · `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/app/(main)/procedures/live/page.tsx`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` (0.3.0 → **0.4.0** · updated_at 2026-10-23)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-005-overall-board-procedure.md` (새로) · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/README.md` 인덱스 · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/README.md` 인덱스(버전 표기가 있으면)
- `reference/2026-10-12-cc-prototype/workflow-v2.md` 는 **이번 판에서 건드리지 마라**(다음 판)

## 6. 할 일

1. **SPEC-003 0.4.0** — 바뀌는 절만 고친다. 뒤집힌 줄은 지우지 말고 ~~취소선~~ + 「(0.4.0 바뀜)」, 그 아래 지금 것. 근거 칸은 `_RESUME 10-23` · 시안 `M:줄` · 리포트 절로.
   - §6 머리 표: 화면 정본에 전체현황판 시안 파일 추가
   - §6.2 헤더 · 제목 줄 · §6.3 카드(방 배정 줄 · KOS 반영 표시 · 정렬 · 드래그) · §5.9 표시 순서 · §6.7 시안 차이 표 갱신(#5 · #8 등)
   - §3.2 순서 테이블 · §7.2 스냅샷 · §7.3 순서 API · §9 E2E 검증 항목 추가
   - §10 열린 것: OQ-517 닫음 + 새 OQ(드롭다운 하위 항목 등)
   - 부록에 「0.4.0 반영표」(결정 줄 → 절) 하나
2. **WORK-005** — WORK-003 형식. WP 를 BE · FE 로 나누고 각 WP 에 대상 파일 · 완료 조건 · 검증 명령. 예상:
   - WP-BE: 순서 테이블 · 마이그레이션/생성 · 저장 API · 스냅샷 반영 · 「방 배정」 작업을 카드 작업 목록에서 제외(back 에서 뺄지 front 에서 뺄지 하나로 정해라 — back 이 낫다면 근거) · 테스트
   - WP-FE: 헤더 · 카드(방 배정 줄 · KOS 반영 표시 · 정렬 버튼 제거) · 드래그(시안 동작) · 시안 차이 반영
   - BE ↔ FE 병렬 가능 여부와 계약 고정점
   - 마지막 WP: 리뷰 + 코디 E2E(데모 지점)
3. 링크 · 인덱스 갱신.

## 7. 범위 제약 — 하지 말 것

- 코드 수정 금지. 결정을 새로 만들지 마라 — 결정 표에 없는 정책은 시안 또는 OQ.
- 예약 현황 · 원내 현황 · 다른 메뉴를 SPEC 에 넣지 마라(Out 에 한 줄만).
- public 레포 — 실명 · KOS id · 키 0(시안 공지 예시에 실명이 있다, 옮기지 마라).

## 8. 검증

```
SPEC 의 모든 절이 DEC · workflow · 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 실명 0(grep)
```

- 이번 판은 「DEC」 자리에 `_RESUME 10-23 결정 줄`을 근거로 쓴다.
- 결정 표 2026-10-23 줄 각각이 SPEC 어느 절에 들어갔는지 부록 반영표로 전수 대조.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_80bdf881-7dba-45c3-ab8c-2130e14e3760 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
