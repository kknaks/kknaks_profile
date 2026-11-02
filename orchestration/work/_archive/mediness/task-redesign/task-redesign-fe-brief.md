
# [frontend] WP-125 태스크 원장 단일화 — FE 표면 (P5 front + P9 front 테스트)

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **BE 워커가 같은 워크트리 `back/`·`mcp/` 에서 병렬 작업 중** — 그쪽을 건드리지 마라. 너는 `front/` 만.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/30-work/work-125-task-ledger-unification.md` §Phase 5 ← **빌드 계획의 SoT.** 여기 없는 건 발명하지 마라
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/runtime_task.md` — 상태 5값·전이표·terminal 집합 정본
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/20-spec/spec-154-decision-workflow.md` §4.19 — 상태 배지·한글 라벨 정본
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/20-spec/spec-230-landing-agent-chat.md` §U-7 — 랜딩 칩 정정(«수락 대기»→«대기», 다섯 상태)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

태스크 상태의 한글 라벨이 FE 안에 3~4벌(`lib/incident.ts`·`lib/wbs.ts`·`lib/decisions.ts`·백엔드 채팅 라벨)로 갈라져 같은 값이 화면마다 다른 한국어(대기/예정/할 일)로 보였다. 스펙 라운드에서 `accept_pending`·수락·거절이 폐기되고 상태가 5값으로 확정됐다(spec PR #661). 이 발주는 FE 표면을 그 계약에 맞추는 것이다: **라벨 사전 1벌 · 칸반 4열 · 수락/거절 UI 제거 · declined 파생 제거 · decline BFF 3건 삭제**.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

BE 워커와 합의된 계약 (이대로 소비하라):

- 상태 어휘 = **5값** `todo|in_progress|blocked|done|canceled` — 타입·terminal 집합을 이 값으로
- 전이 버튼은 서버 `allowed_transitions` 만 소비(현행 유지). `TRANSITION_LABEL` 하드코딩에서 «수락» 제거, 새 edge 폴백이 상태명으로 새지 않게 라벨 사전과 정합
- `MyTask.declined`·`decline_reason`·`declined_at` 파생 필드가 응답에서 사라진다 — 렌더·타입 제거
- decline REST 가 서버에서 사라진다 — BFF `front/app/api/ax/**/decline/route.ts` 3건 삭제
- 재배정은 담당자 본인도 요청 가능 — 거절 UI 의 대체 동선은 재배정

## 4. 먼저 읽을 핵심 파일

- WP-125 §Code Surface 표의 front/ 행 — 만질 파일 후보 전체
- `front/lib/tasks/canonical-task.ts` — 상태 타입·terminal 집합. 라벨 사전 1벌이 앉을 자리 후보
- `front/lib/incident.ts` · `lib/wbs.ts` · `lib/decisions.ts` — 라벨 3벌 + declined 파생. 사전 1벌로 수렴 대상
- `front/app/(authenticated)/ax/tasks/task-kanban.tsx` — 5열→4열·`accept_pending` 필터/칩 제거
- `front/components/tasks/detail/TaskHeaderActions.tsx` — TRANSITION_LABEL·수락/거절 CTA
- `front/app/(authenticated)/ax/incidents/[run_id]/incident-detail.tsx` — 수락 버튼·거절 모달·거부 배지

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. WP-125 §P5 의 front 작업 항목을 정독하고 파일 후보를 실물과 대조한다
2. 라벨 사전 1벌을 만들고(정본 = SPEC-154 §4.19) 3~4벌 소비처를 전부 그 사전으로 수렴
3. 칸반 4열·수락/거절 CTA·거부 배지·`declined` 파생·decline BFF 3건 제거. 랜딩 칩(SPEC-230 §U-7) 정정
4. WbsTaskModal·meeting-v2 라벨/선택지 정합 (WBS 상태 칩 선택지는 5값 중 지정 가능값만 — 도메인 문서 참조)
5. ⚠ **WP-114(태스크 보드 개선, in_dev)와 파일이 겹친다** — WP-114 가 이미 착지시킨 변경을 회귀시키지 마라. 충돌·애매한 지점은 고치지 말고 완료 보고에 목록으로 남겨라 (소유 조정은 코디 몫, OI-1)
6. P9: 만진 표면의 기존 테스트 갱신 + §8 검증

## 7. 범위 제약 — 하지 말 것

- `back/`·`mcp/` 수정 금지 (BE 워커 병렬 작업 중) · 문서 레포 수정 금지
- 새 화면·새 UX 발명 금지 — 이번 라운드는 어휘·표면 정합이다. 드래그앤드롭 등 칸반 심화는 범위 밖(SPEC-152 OQ-8)
- WP-114 착지분 되돌리기 금지 — 충돌은 보고로
- 구현 중 계약과 어긋나는 사실이 나오면 코드를 고치지 말고 §9 질문 채널로

## 8. 검증

```
cd front && npx tsc --noEmit (네가 만진 파일 0 에러) + prettier --check <네가 만진 파일만>. 전체 빌드·전체 포맷 검사 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_3d56bec5-4301-42ae-9832-d7a07096ac9e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
