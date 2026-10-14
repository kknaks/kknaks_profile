# [frontend · 시안 r4] WORK-001 WP6 — 현황판 고객 중심 방 패널 · 접수 모달 · 순회형 손 필요 표시 · 5직군

너는 **cc-prototype `frontend` 워커**다. 이번 판은 **claude design 시안 작업**(DesignSync). 코드는 쓰지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더). 맥락이 없으면 아래 파일부터.

## 1. SSOT

- **업무 흐름(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` — 전부 읽어라
- **SPEC-001 0.2.0**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` — §0 바뀐 것 · §2 원칙 · **§3 화면**(3.1 접수 모달 · 3.2 방 패널 · 3.3 직원 첫 화면 · 3.4 환자 상세) · §5.1 방 상태
- E2E 피드백: `e2e-feedback-batch-1.md`(이 폴더) — #11 #13 #14 #17 #19 #20 #21
- 앞 판: `design-staff-report.md` · `design-staff-r2-report.md` · `design-staff-r3-report.md`
- 시안: claude design `dda9a931-097f-4780-9301-972d5ac1fc23` — `Ceramique 현황판 v3` · `Ceramique 직원 - 의사` · `- 코디` · `- 로그인` · `- 통역 모달 상태`

## 2. 그릴 것

1. **현황판(새 파일 `Ceramique 현황판 v4` — v3 는 복제해서 바꾸고 v3 원본은 수정 금지)**
   - 범례 5직군(의사 · 상담사 · 피부관리사 · 간호사 · 코디) 색 점 — 2개 추가
   - 이름: 「라운지」→**접수대기실** · 「수면실」→**수면시술실**
   - 예약 탭: **첫 방문 배지** · 시술 · 원장 칸은 값 없으면 「-」
   - **접수 모달(§3.1)**: 동선 단계를 데스크가 고른다(상담 · 원장 상담 · 시술 후보 체크). 첫 방문 기본 = 상담 / 재내원 기본 = 보유 시술권. 「원장 진료 · 진정 관리는 자동으로 들어가요」 문구와 그 자동 단계 **삭제**
   - **방 패널(§3.2) — 고객 중심**: 머리(방 · 고객 · 상태 · 경과) → 동선 단계 목록(한 줄 = 단계 하나, 시술은 1장 = 1줄) · 단계마다 [배정](그 단계 직군 직원 목록 + 각자 지금 일)/[해제] · 상태 배지 5종(예정 · 대기 · 진행 중 · 완료 · 진행 안 함) → [시술 추가](후보 목록 시트) · **순서 바꾸기**(진행 중 단계 없을 때만, 위/아래) · [수면시술실로 이동]/[원래 방으로] · [귀가](확인: 남은 단계는 「진행 안 함」)
   - 방 칸 상태 문구(§5.1): 「○○ 대기」 · 「다음 단계 대기」 · 「원장 대기 · 세팅 준비」 · 「귀가 대기」
   - 직원 중심 영역(「현재 방에 있는 직원 · 직원 배정하기 · 큐」)은 **없앤다**
2. **직원 화면**
   - `직원 - 의사` → **배정형** 틀로 이름만 일반화(의사 · 상담사 · 피부관리사 공용): 지금 진행 중 · 다음 · 완료(**예정 없음**). 환자 상세 버튼 = 단계 종류별 [상담 시작/종료] · [시술 시작/종료]. 상담사 · 피부관리사 예시 화면 1장씩 추가
   - `직원 - 코디` → **순회형** 틀(코디 · 간호사 공용): 내원 목록에 **오늘 시술 목록** · **손 필요 배지**(「다음 단계 대기」 · 「귀가 대기」). 간호사 예시 1장 추가
   - 환자 상세: 작성자 이름 없음(출처는 칸 이름만) · `**` 는 굵게 · 빈 양식 줄 숨김 · 상담/오더 메모는 상담 완료 전엔 「상담 후 공개」 자리표시
3. 로그인: 시연 카드 = 데스크 · 의사 · 상담사 · 피부관리사 · 간호사

샘플 값: 10-09 실데이터(고객 · 동행인 이름만 가짜 — r2/r3 규칙). 직원 이름 · 직군은 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/kos-staff-api-report.md` §4 표(실제 KOS 직군)

## 3. allowed_paths

- claude design 에 **새 파일 추가** + 네가 만든 `Ceramique 직원 - …` 파일 수정. `현황판 v3` · `의사 모바일` 원본 수정 · 삭제 금지
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-r4-report.md`
- 그 외 로컬 파일 · 코드 수정 금지. 커밋 금지. KOS 호출 금지

## 4. 산출물 · 검증

리포트: 상태 · 만든/고친 파일 링크 · SPEC §3 항목별 반영 표 · 내가 정한 것 · 이슈.
검증: §2 의 1~3 전부 시안에 있음 · 자동 단계 문구 0 · 직원 중심 배정 영역 0 · 실제 고객 이름 0(10-09 visitor.name 대조) · v3 원본 무수정

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_a1daffd6-7d91-48d1-87fe-bac9ebe6a012 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(시안 r4) 완료: <한 줄>" \
  --body "만든/고친 파일·링크 / 요약 / 검증 결과 / 내가 정한 것 / 미결"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend(시안 r4) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
