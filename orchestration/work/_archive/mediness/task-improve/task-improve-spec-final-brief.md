
# [planner] 최종 문서 환류 — 코드 검수·구현 실측의 스펙 반영 (소라운드)

너는 **mediness `planner` 워커**다. WP-129·130 코드가 검수 PASS 로 착지했다(code PR #140). 구현·검수에서 확정된 사실을 문서에 환류한다 — 이 라운드로 스펙이 최종 닫힌다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec` (커밋 ae53ad84f 위, clean)

## SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code130-report.md` — 미결 ⓐⓑ 판정·WARN 목록(W-2·5·6·7)·R2 절
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/backend-130-fix-report.md` — 바인딩 3겹·수정카드 v1 봉인 실물
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2 — 인라인 폼 통일 등 실기동 확정

## 해야 할 일 (전부 문서만 — 코드 무접촉)

1. **ⓐ SPEC-155 §6.1 정정** — «그 턴에 카드를 세우지 않는다» 가 실물(네 경로 전부 카드를 세움·버전 되묻기 동형 — 본문 필수 되묻기도 카드에 문구)과 어긋난다. 검수 판정 «코드가 옳다» — 문장을 구현 쪽으로 정정 + 개정 노트 근거
2. **ⓑ domains/runtime_task.md task_references 표에 size_bytes 행 추가** (0138 docstring 근거)
3. **채팅 첨부 계약 반영** — SPEC-155 §6.12 를 착지 실물로 구체화: POST /action-runtime/task-draft-attachments(draft_id 서버 발급)·POST /turns draft_id additive·바인딩 3겹(소유자 fail-closed·room+발화 교체·생성 흐름 1회성 consume)·수정 카드 첨부 = v1 미지원 명시
4. **W-2 배포 공지** — WP-130 Pre-deploy 에 «기존 decision·incident 태스크의 배경·목표는 빈다(스냅샷은 신규 생성분부터·description fallback 표시)» 추가
5. **자료 추가 인라인 폼** — §4.19 해당 절에 확정 모양([링크|파일] 토글·표시 이름·취소/추가, 레일·완료 모달 공용 한 벌) 반영. 배지 한 줄은 ㉘/시안 :58 정본과 구현이 일치하는지 확인만
6. **W-5·6·7** — 리포트 처분대로 문서 환류 (코드 수정 항목이면 «후속» 표기만)
7. **WP-129·130 Status 갱신** — 전 phase 구현 완료·검수 PASS 를 완료 증거로 기재(frontmatter status 는 in_dev — 머지·배포 전이므로 done 으로 올리지 마라). 30-work.md 3표 동기

검증: `python3 scripts/lint-pipeline.py --strict` — mediness ERROR 0.
**하지 말 것**: 계약 재설계 금지·코드 레포 수정 금지·위 항목 밖 신규 개정 금지.

## 완료 보고 — 문구 변경 금지
> ⚠ 핸들은 dispatch preamble 값을 믿어라.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "planner 최종 환류 완료: <한 줄>" --body "항목별 좌표/lint"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] planner 최종 환류 — <한 줄>. 상세는 인박스." --enter
```
