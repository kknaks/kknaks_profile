
# [planner] WP-129 를 역할별 2건으로 분할 (사용자 지시)

너는 **mediness `planner` 워커**다. 직전 라운드 산출물(스펙 9건 개정 + WP-129 단일 문서)이 이 워크트리에 미커밋으로 있다. **스펙 개정은 그대로 두고, WP 문서만 2건으로 분할**한다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness`

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2 — 결정 표 (불변)
- 직전 브리프: 같은 폴더 `task-improve-spec-brief.md` — 계약·제약 전부 유효
- 현재 산출물: `products/mediness/30-work/work-129-task-request-and-detail-unification.md` (11 phase — 분할 원본)

## 2. 분할 계약 (사용자 확정 2026-09-01 "역할별로 2개")

**WP-129 — 업무 요청 축 + 샤라웃 지시 입구 차단** (시안 무관 — 먼저 코드 발주 가능)

- 생성 표면 담당자 개방(모달·채팅 담당자 지정·발화 패턴)
- «내가 요청한 일» 조회(scope=requested) + `created_by` 인덱스
- DM 훅(spec-119 재사용·graceful) · 요청자 권한(수정·취소)
- 샤라웃 지시(실행 요청) 유형 입구 주석 비활성(슬랙·채팅) + 개인 대시보드 3자리·배정 부트스트랩
- migration: **인덱스 1건**

**WP-130 — 상세 5부 통일 + 완료 근거** (시안 맞물림 — P8 시안 대기 BLOCKED 이쪽에 귀속)

- `background`·`goal` 컬럼 + 원장 렌더 폐지(스냅샷) + description fallback
- `task_references` 테이블 + 파일 스토리지(path-guard·env root·25MB·denylist) + 표시(하이퍼링크·이미지 인라인·다운로드 카드)
- 완료 등록 모달(서버 강제·시스템 예외)
- 채팅 초안 필수 채움(배경·목표·체크리스트) + 채팅 첨부 스테이징
- migration: **컬럼 2 + 테이블 1** · 배포 사전조건(k8s_infra_mac hostPath) 이쪽에 명시

분할 판단이 애매한 항목은 「그 항목이 background/goal·task_references 를 필요로 하는가」로 가른다 — 필요하면 130, 아니면 129.

## 3. 해야 할 일

1. `work-129-…md` 를 위 계약대로 **WP-129 / WP-130 두 문서로 재구성** (파일명·doc_no·covers·depends 정리. 129↔130 의존은 실제 의존만 — 억지로 직렬화하지 마라)
2. 스펙 쪽 WP 참조(«구현 WP = …») 를 두 WP 로 정확히 재배선
3. `30-work.md` Board/WP List/Spec Coverage · `log.md` 동기
4. 검증: `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0

**하지 말 것**: 스펙 계약 내용 변경 금지(분할·재배선만) · phase 내용 재설계 금지 · migration 총계 변경 금지(분배만).

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 아래가 다르면 preamble 이 맞다.

- **커밋·push·PR 금지.**
- 끝나면 아래 두 명령 모두 실행:

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner WP분할 완료: <한 줄>" \
  --body "분할 결과(WP별 phase·migration 분배) / 재배선 목록 / lint 결과"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] planner WP분할 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] planner: <질문>" --enter`
