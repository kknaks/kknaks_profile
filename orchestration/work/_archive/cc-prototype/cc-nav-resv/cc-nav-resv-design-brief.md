# [frontend · 시안] WP3 — 예약관리 데모 시안(요청 생성 · KOS 등록 · 변경 요청 · 수정 요청) + 폰 현황판 목록

너는 **cc-prototype `frontend` 워커**(시안 담당). claude design 작업(DesignSync). **코드 금지.**
먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 문서)

⚠ 같은 코드 워크트리(`/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv`)에서 다른 frontend 워커가 WP1(공통 헤더)을 코드로 작업 중이다. **너는 리포 파일을 하나도 건드리지 않는다.**

## SSOT

- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` — **D-05 · D-08 · D-10 ~ D-18 · OQ-401 ~ 403**
- 요청 원문 · 와이어 해석 · 데모 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/00-baseline/baseline-006-nav-reservation-demo.md`
- 와이어프레임(구조 참고만 — **그대로 옮기지 마라, 시안은 새로**): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/assets/cc-reservation-wireframe.png`
- 예약 흐름 배경(Linky → cc → KOS): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/00-baseline/baseline-004-reservation-idea.md`
- KOS 예약 카드 실물 캡처(스크린샷 자리에 들어갈 화면의 모양): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/reference/2026-10-12-cc-prototype/kos-screenshot/kos-reservation-card.png`
  - **실제 고객 정보다 — 이름 · 생년월일 · 연락처 · 차트번호 · 메모 원문을 시안에 옮기지 마라.** 모양(칸 구성 · 배치)만 참고하고 값은 가짜로
- 디자인 언어: claude design 프로젝트 `dda9a931-…` 의 기존 Ceramique 시안(현황판 v5 · 직원 화면) — 같은 medikit · Ceramique 테마

## 그릴 것

### A. 예약관리 (데스크톱 · 새 파일 「예약관리 v1」)

데모 흐름 하나로 이어지게 화면을 순서대로:

1. **빈 상태 + [링키 예약 요청 생성]** 데모 전용 버튼 — 데모용임이 화면에서 구분되게(D-10)
2. **예약 테이블** — 한 줄 = 예약 하나. 본사 요청 카드(요청 종류 · 받은 시각 · 고객 · 국적 · 첫 방문/재방문 · 예약 일시 · 시술 · 통역 언어) · 병원 상태 · 비고(버튼 · 사유). 상태 「예약 확인중」 줄의 버튼 = `KOS 등록하기 | 변경 요청하기`(D-16)
3. **KOS 등록 미리보기 모달** — 등록될 내용 확인 → [등록하기]
4. **확정 줄** — 상태 「예약 확정」 · [스크린샷 보기] · 스크린샷 보기 모달(KOS 예약 카드 모양 — 위 캡처 참고, 가짜 값)
5. **변경 요청하기 모달** — 사유 **텍스트 입력**(D-13) → 줄 상태 「변경 요청」 + 사유 표시
6. **수정 요청 이어 붙기** — 데모 버튼 [링키 수정 요청 생성](D-15) → 기존 예약 아래 수정 요청 줄(바뀐 값은 취소선 → 새 값, D-14) · 상태 「수정 확인중」 · `KOS 수정하기 | 변경 요청하기`
7. **수정 확정** — 기존 줄 「변경됨」(이전 스크린샷 보관) · 새 줄 「수정 확정」 · [스크린샷 보기]

상태 이름 · 카드 항목은 OQ-401 의 와이어 값으로 그리되, 더 나은 이름이 있으면 시안에 쓰고 리포트에 「바꾼 것」으로 적어라.
본사 쪽 화면(OQ-403)은 그리지 않는다 — 데모에선 예약관리 줄의 상태 · 사유로만 보인다.

### B. 폰 현황판 목록 (폰 폭 · 새 파일 「현황판 폰 v1」)

- 헤더는 햄버거(D-05) — 메뉴 열린 상태 1장(`현황판 | 예약관리 | 내 스케쥴`)
- 목록: 고객별 한 줄 `이름 · 지금 방 · 단계 · 담당`, 방별로 접어 보기(D-08). 읽기 전용(조작 없음)
- 샘플: 시나리오 고객 `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/cc-back-data/scenario/`(가짜 이름본) · 직원 `kos-staff.json`. `*.orig` · `staff-name-map.json` 은 실명 — 열지 마라(2026-10-14 정정)

## 범위

- claude design 에 새 파일 두 개(「예약관리 v1」 · 「현황판 폰 v1」). 기존 시안 파일 무수정
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/design-report.md`
- 코드 · 커밋 · KOS 호출 금지

## 검증 (리포트에 넣을 것)

- A 1~7 · B 항목별 반영 표(시안 화면 이름 ↔ 항목)
- 실제 고객 이름 · 생년월일 · 연락처 · 차트번호 0(캡처 값이 시안에 없는지)
- 와이어와 바꾼 것 목록 · 기존 시안 무수정

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_adf432d6-a97d-4457-a02d-041df0075fb7 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(시안) 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] frontend(시안) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] frontend(시안): <질문>" --enter`
