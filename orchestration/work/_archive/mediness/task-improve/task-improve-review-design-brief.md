
# [reviewer_spec] 시안 v1 스펙 개정 검수 (targeted)

너는 **mediness `reviewer_spec` 워커**다. planner 의 시안 v1 확정 라운드(미커밋 6파일: spec-154·155·30-work.md·work-129·work-130·log.md)를 **read-only 검수**한다. 직전 커밋 522f485ac(업무 요청 축)은 이미 검수 통과분 — **이번 미커밋 diff 만** 본다(`git -C <워크트리> diff`).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec`
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/reviewer/role.md`

## 판정 기준 (SSOT)

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/design-analysis.md` — 시안 분석 + 사용자 판정 6건 + 규율 교정 + 코디 기본값. **이 문서와 어긋나면 FAIL**
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2 — 결정 표
- 시안 원본: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/reference/2026-09-01-mediness-task-improve/` — 치수·문구 대조용
- 발주 브리프: 같은 폴더 `task-improve-spec-design-brief.md` (A~D 범위)

## 체크리스트

1. **사용자 판정 6건 정확 반영** — ①상세 2단 배치(5부 = 구성 목록, 순서 계약 아님) ②완료 모달 활성 = 요약 **또는** 제출자료 1(«요약 필수» 흔적 잔존 시 FAIL) ③마커 5값 ④D-3 강조(프론트 파생 — 서버 축 신설 서술 있으면 FAIL) ⑤「내가 요청한 일」= v2 OQ(v1 확정 서술 잔존 시 FAIL) ⑥권한·상태별 수정 = v2(삭제 3원칙이 v1 계약으로 남아 있으면 FAIL)
2. **규율 교정** — 드롭다운 항목 소스 = allowed_transitions 명시·태그→배지 5슬롯 매핑·0차 숨김·빈 그룹 미렌더 불변
3. **구 서술 스윕 재검** — «6블록»·«요약 필수»·«시안 대기»(활성 문맥)·«올린 본인+담당+요청자»(v1 문맥)·«지남 강조 없음» grep — 활성 잔존 FAIL
4. **gap 실측 3건 재검증** — 코드(read-only, `/Users/kknaks/orca/workspaces/mediness-app/task-improve`)로: 상세 응답 일정 6행 실재 / 목록 행 completed_at + 전량 로드 / task_check_items.sort_order + 재배열 endpoint. planner 의 «신규 서버 작업 0» 판단이 실물과 맞나
5. **WP-130 정합** — BLOCKED 0·P5↔P7 선후행·P4 자격 단순화·OI-6/7 닫힘·OI-8 신설·Pre-deploy 공지 2건. WP-129 6번째 입구 등재(P0·P5·P6)·SPEC-155 assignee_name 정정 3자리
6. planner 기본값 4건의 «사용자 뒤집기 가능» 표기 실재
7. lint `--strict` mediness ERROR 0 · 인덱스 3표 동기

## 산출물

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-design-report.md` — 판정(PASS/WARN/FAIL) + 근거(파일:줄). 리포 파일 수정 금지. «v2 OQ»·«planner 기본값» 을 미완성이라 FAIL 하지 마라 — 발주 계약이다.

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_spec(시안) 완료: <판정>" \
  --body "판정 / 위반 목록(파일:줄) / 리포트 경로"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] reviewer_spec(시안) — <판정 한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] reviewer_spec: <질문>" --enter`
