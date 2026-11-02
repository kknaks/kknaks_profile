
# 작업 요약 — task-improve (mediness)

기간: `2026-09-01` ~ `2026-09-01`
결과: 머지·배포까지 완주 — dev(5df3ecea)·prod(494d6fec) 롤아웃, alembic 0138, k8s hostPath 볼륨까지 반영. 문서 마감(WP status·WP-131 환류)만 잔여.

## 1. 무엇을 했나

mediness 에서 남에게 일을 시키는 통로가 샤라웃(의사결정 등록)의 지시 유형뿐이라 태스크 하나에 결재 원장이 따라붙었고, 태스크 상세는 출처마다 담는 내용이 달랐으며, 완료에는 근거가 남지 않았다. **업무 요청을 파생 개념**(비워크플로 ∧ created_by≠assignee)으로 열고, 상세를 5부(배경·목표·Todo·참고자료·산출물·로그)로 통일했으며, 완료에 근거(산출자료 또는 완료기록)를 강제했다. 사용자 시안으로 보드·상세·승인 카드를 v1 확정하고, 샤라웃 지시 입구를 재활성 가능한 주석으로 닫았다. 스펙 3커밋(#675→#667 main)·코드 8커밋(#140→#138 main)·k8s_infra#2 로 착지.

## 2. 적용한 기술·개념

- **파생 판정으로 개념 열기 (요청 = created_by≠assignee)** — 새 엔티티 없이 업무 요청 축을 열었다 → [[derived-predicate]]
  - 왜 이걸 골랐나: 요청 테이블/타입을 만들면 태스크와 요청이 두 원장이 되고 워크플로 fanout 이 오염된다. 판정 술어를 한 곳(repositories/task_request)에 두고 grep 테스트로 중복 정의를 막았다
  - 무엇이 어려웠나: 검수가 계층 역전(repo→service import)을 잡았다 — 술어가 SQL WHERE 를 조립하므로 repositories 층이 소유하는 게 맞았다
  - 근거: `back/app/repositories/action_runtime/task_request.py` · review-code-report.md W1 · PR #140

- **«요청자=담당자» 가정이 깨질 때 죽는 소비처 전수조사 실패** — 이 작업의 가장 비싼 교훈 → [[contract-surface-enumeration]]
  - 판단이 갈린 지점: 담당자 해소(«태우님께…»)를 열자 그 가정을 깔던 자리들이 연쇄로 터졌다 — MCP 툴 설명(«본인 고정»)·초안 카드 결재자 축(수신자가 결재자가 되어 요청자 pending 에서 카드 소실)·WBS 승인 버튼 화이트리스트
  - 무엇이 어려웠나: 스펙·검수 모두 「스펙과 일치하나」만 봐서 스펙 밖 표면(입구·툴 문구·카드 축)은 못 잡았다. 실기동 반려가 유일한 검출기였다
  - 근거: 커밋 `9aad87f9`·`6f7f65b2`·`b5c0b07e` · memory feedback_enumerate_all_surfaces

- **첨부 스테이징의 소유자·방·1회성 3겹 바인딩** — 채팅 업로드가 30분 안에 남의 태스크에 붙는 결함을 닫음
  - 왜 이걸 골랐나: draft_id 를 서버가 발급·재사용하고 소비를 생성 발화 흐름에 한정 + 즉시 삭제. 수정 카드 첨부는 대상 검증 설계가 한 겹 더 필요해 v1 봉인(반쪽 구현 잔재 제거)
  - 무엇이 어려웠나: FE 가 turn body 에 attachments 배열을 가정했는데 extra=forbid 라 422 로 전멸할 자리였다 — FE 워커의 계약 실측이 배포 전에 잡았다
  - 근거: `back/app/services/action_runtime/workflow/task_draft/attachment_binding.py` · review-code130-report.md 위반③

- **완료 근거 422 의 검사 순서와 면제 축** — 사람 4경로 강제 · 시스템 2경로·체크리스트 파생 면제
  - 판단이 갈린 지점: 파생 완료(체크 다 켬)에 근거를 요구하면 「체크 다 했는데 완료가 안 됨」, 면제하면 근거 없는 완료의 뒷문 — 파생 면제로 확정(OI-2)
  - 무엇이 어려웠나: 자격·합법성 precheck → 근거 → 상태기계 순서를 지켜 부분 부수효과 0 을 만들어야 했다. WBS 상태 칩 완료가 모달 없이 422 로 막히는 파급도 실기동에서 발견 — 공용 완료 모달 경유로 연결
  - 근거: `back/app/services/action_runtime/tasks/lifecycle.py` · WP-130 P3

- **스쿼시 머지·역머지 경합 처리** — main 직행 커밋과 브랜치 릴리스의 충돌 → [[database-migration]] 결의 운영 개념
  - 무엇이 어려웠나: 릴리스 PR #667 이 DIRTY — main 에 SPEC-240 이 직행해 있었고 doc_no(DOC-245)가 우리 WP-125 와 경합(파일명이 달라 git 이 못 잡는 종류). 신규인 SPEC-240 을 251 로 재발번하고 «최종 수정» 체인은 main 머리 + 우리 체인으로 재직조
  - 근거: mediness 커밋 `e2e1f304` · 아카이브 task-redesign 의 같은 경합 선례

- **hostPath 볼륨 관례 재사용 (첨부 영속)** — env root + `/mnt/mac/<이름>`(-dev 분리) + DirectoryOrCreate
  - 왜 이걸 골랐나: 부서공간·오디오가 이미 이 관례다. path-guard 도 부서공간 것을 공용 storage_guard 로 들어내 재사용(신규 구현 0)
  - 근거: k8s_infra_mac#2 · `back/app/services/storage_guard.py`

## 3. 막혔던 것 / 사고

- **확인 없이 스펙 발주 → 전면 롤백** — 세팅 직후 확정 결정이 이월돼 있다는 이유로 planner 발주~검수 2라운드를 자동 진행 → 사용자 반려로 워커 중지·스펙 워크트리 전체 롤백. 이후 「발주 전 범위·문서·산출물 계획을 보여주고 승인」으로 전환 → memory feedback_orchestration_approval_gate
- **실기동 반려 연쇄 (5건)** — 승인 버튼 소실(선재 화이트리스트 누락)→카드 내용 부실→툴 설명 낡음→모달 첨부 부재→결재자 축 오배정. 원인은 하나: 계약이 닿는 표면(입구·툴·카드) 전수조사 없이 결정된 2개 입구만 구현. 첫 반려에서 멈춰 전수조사로 갔어야 했다 → memory feedback_enumerate_all_surfaces
- **코디 판정 2건이 사용자에게 뒤집힘** — ①자료 추가 «인라인 통일»(시안에 모달 디자인이 있었다 — 오독) ②빈 메타 축 행 제거(«미지정 항목 일단 다 보여주라»). 시안·사용자 의도가 정본이고 코디 미학 판정은 뒤집기 가능으로만
- **워커 사고 2건** — BE 가 공유 워크트리에서 `git stash -u`(FE 작업물 100초 노출, 무피해 복원)·BE 가 전체 스위트 실행 시도(방침 위반, 코디 중단). 브리프에 금지를 써도 실행 중 감시가 필요하다
- **로컬 DB 스탬프 고아** — upstream 재번호로 alembic_version 이 소멸한 리비전 id 를 물고 있었다. 내용 적용 실측(enum 5값) 후 스탬프만 UPDATE

## 4. 결정

정본은 `_RESUME.md` §2 (19건). 핵심만:

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-01 | 요청 = 파생 판정, 자동 cc 없음 | 원장 이원화 방지 · created_by 가 이미 접근 자격 |
| 2026-09-01 | 상세 5부 통일 — background/goal 컬럼·원장 렌더 폐지·출처는 링크 | 출처별 상세 분열의 원인 제거 (실측: 라이브 렌더 조립 코드는 서버에 없었다 — 스냅샷 신설이 실물) |
| 2026-09-01 | 완료 = 근거 최소 1(서버 422)·시스템/파생 면제 | 근거 없는 완료가 요청 추적을 무의미하게 함 |
| 2026-09-01 | 샤라웃 지시 전면 배제(슬랙·채팅) — 입구만 주석, 재활성 가능 | 일 시키기는 태스크 생성으로 · 결재/승인 축은 유지 |
| 2026-09-01 | 승인 카드 = 생성 모달 컬럼 세트 정합 + 빈 축 «미지정» 상시 표시 | 어느 입구든 같은 컬럼 · ~~빈 축 미적재~~ 사용자 재정정 |
| 2026-09-01 | «내가 요청한 일» 화면·권한/상태별 게이팅·@멘션 = v2 | 복잡도 절단 — v1 은 «볼 수 있으면 고칠 수 있다» 유지 |

## 5. 날짜별 로그

- `2026-09-01` 세팅→롤백 사건→결정 재확정(19건)→스펙 3라운드(검수 FAIL→R2 PASS)→WP 2건 분할→코드 2 WP 병렬(검수 R2 PASS)→실기동 수리 5건→dev·main·prod 릴리스+hostPath 볼륨 완주

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/675 (→ main #667 `bacb9374f`)
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/140 (→ main #138 `494d6fec`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/2 (`4f1b7d6dc`)

- `kknaksss/task-improve` → `dev`
  - `9d790f5f` fix(card): 정본 컬럼 세트 상시 표시 — 빈 축도 «미지정/미기재» 행으로 (사용자 확정)
  - `9aad87f9` fix(task-draft): 초안 카드 결재자·요청자 = 요청자 본인 — 담당자 해소 뒤 축 분리 반영
  - `bf8f1bba` feat(task): 승인 카드 본문 = 생성 모달 컬럼 세트 정합 + 생성 모달 첨부 (실기동 반려 수리)
  - `6f7f65b2` fix(mcp): task_draft_request 툴 설명을 WP-129 계약으로 정정 — 담당자 = 발화 해소
  - `b5c0b07e` fix(action-runtime): wbs_task 2종을 command 화이트리스트에 등재 — 승인 버튼 소실 선재 버그
  - `3573ecf4` fix(task): 자료 추가 = 레일 발 중앙 모달(시안 정본) — 완료 모달 안은 인라인 유지
  - `db4bcfab` feat(task): 상세 5부 통일 + 완료 근거 + 참고자료·산출물 원장 (WP-130)
  - `5b98247a` feat(task): 업무 요청 축 도입 + 샤라웃 지시 입구 차단 (WP-129)
- 리포트: `review-spec-report.md` · `review-design-report.md` · `review-code-report.md` · `review-code130-report.md` · `backend-130-fix-report.md` · `REPORT-wp131-card-body-be.md` · `design-analysis.md`

## 7. 잔여

- **문서 마감**: WP-129/130 frontmatter status done 승격(P0 prod 실측·P8 CI 는 이번 릴리스로 실증됨) + 실기동 수리분 WP-131 등재 — 스펙 레포 후속 커밋 1건
- **공지 2건**: slack 미매핑 5명은 요청 DM 미수신(태스크는 생성) · 기존 decision/incident 태스크 배경·목표 빈 값(description fallback)
- **v2 이월 5건**: «내가 요청한 일» 화면(OQ-22) · 역할/상태별 수정 게이팅(OQ-23) · @멘션(OQ-24) · 기존 초안에 첨부 추가(수정 경로 바인딩 설계) · task.draft 참조자/완료예정 축(초안 LLM 스키마)
