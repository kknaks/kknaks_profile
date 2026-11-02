# [frontend] WORK-001 WP8 — SPEC 0.2.1 화면: 현황판 v4 · 직원 배정형/순회형 5직군 · 접수 · 결제 완료

너는 **cc-prototype `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더).
워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` — **`cc/front/` 만.** back 은 끝났다(읽기 · 실행만).

## 1. SSOT

- **시안(화면 정본)** — claude design `dda9a931-097f-4780-9301-972d5ac1fc23` 를 **DesignSync 로 받아라**: `Ceramique 현황판 v4` · `직원 - 의사` · `- 상담사` · `- 피부관리사` · `- 코디` · `- 간호사` · `- 로그인` · `- 통역 모달 상태`. 시안 설명: `design-r4-report.md` · `design-r4b-report.md`(이 폴더)
- **SPEC-001 0.2.1**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` — §0-a · §3 · §5.2 · §5.3 · §7
- **API 계약**: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/README.md` 의 요청 · 응답 예시(WP7 · WP7b) — `lib/types.ts` 를 이것에 맞춰 다시 쓴다. 모양이 이상하면 바꾸지 말고 `[질문]`
- 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md`
- 앞 판: `wp3-fe-report.md` · `wp4-fe-report.md` · `contract-check-fe-report.md`

## 2. 할 것

1. `lib/types.ts` · `lib/api.ts` — 0.2.x 계약(단계 모델 · `/api/desk/*` · home 두 틀 · `unpaidAmount` · `paymentRequired` · `procedure-candidates` · `payment-complete`). 0.1.0 조작 경로 삭제
2. **/desk = 현황판 v4 시안대로**: 범례 6색 · 접수대기실 · 수면시술실 · 예약 탭 첫 방문 배지 · 접수 모달(단계 고르기) · **고객 중심 방 패널**(단계 목록 · 단계별 배정/해제 · 시술 추가 · 순서 ↑↓ · 수면시술실/원래 방 · 귀가 확인 · 상담 결과 줄 · 수납필요 칩 · 미결제 줄 [결제 완료]) · [초기화] · 되돌리기 토스트
3. **/staff**: 배정형(의사 · 상담사 · 피부관리사 — 지금/다음/완료, 예정 없음, 단계 종류별 시작/종료) · 순회형(코디 · 간호사 — 오늘 시술 · 손 필요 배지)
4. **환자 상세**: 메모 공개 시점(상담 후 공개 자리표시) · 작성자 없음 · `**` 굵게 · 빈 양식 줄 숨김 · 수납필요 칩 · 통역 모달(WP4 그대로)
5. **로그인**: 시연 카드 5장 · 계정 목록 = back `staffIds`

## 3. 범위

- `cc/front/` 만 · 커밋 금지 · KOS 호출 금지
- 확인은 임시 포트(back · front 둘 다 임시, back 은 **별도 DB**). 사용자 포트 3600 · 8600 · `data/cc.db` · `seed.json` 금지

## 4. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없음. 사용자 포트·프로세스 안 건드림
```
- 이번 WP 항목만: 실제 back(임시)으로 headless 크롬 — S1 흐름(접수 → 방 → 상담사 배정 → 상담사 로그인 시작 · 종료 → 수납필요 · 미결제 → [결제 완료] → 시술 의사 배정 → 의사 시작 · 종료 → 귀가) 화면 캡처 몇 장 · 콘솔 오류 0 · 시안 대조표
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp8-fe-report.md`

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_1bd4c892-2253-4670-9a5f-c6412cf15a9d \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
