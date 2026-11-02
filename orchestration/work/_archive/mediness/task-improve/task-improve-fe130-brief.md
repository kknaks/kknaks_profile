
# [frontend] WP-130 — P5(상세 2단 셸+완료 모달) → P7(보드 v1) · P6(FE) · P8(FE)

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
base: `origin/dev` → PR `dev`. WP-129 커밋(5b98247a — 상세 메타 요청자 행 포함)이 이미 있다.
**BE 워커가 같은 워크트리 `back/`·`mcp/` 에서 병렬 작업 중 — 거기 금지.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-130-task-detail-unification.md` — **정본. 네 몫 = P5(상세 2단 셸 + 완료 모달) → P7(보드 v1 — 반드시 P5 뒤: 카드 드롭다운의 완료가 P5 모달을 연다) · P6 중 FE 항목(채팅 첨부 업로드 UI) · P8 중 FE**
- `../20-spec/spec-154-decision-workflow.md` §4.19(개정 노트 ㉘ — 2단 셸·본문 4블록·우측 레일 3카드·완료 모달·보드 v1·AC-33~41)
- **시안 원본(치수·문구·인터랙션의 시각 정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/reference/2026-09-01-mediness-task-improve/` — README 토큰·SPEC_screens·screens/task-board.dc.html·task-detail.dc.html (소스로 읽어라. **리포에 복제 금지**)
- 결정 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2

기대는 개념 — 해당 없음.

## 2. 핵심 계약 (어기면 검수 FAIL)

- **상세**: 본문 4블록(Todo·배경·목표·댓글/로그 탭) + 우측 레일 320px(일정·참고자료·제출자료). goal = 개행→불릿 렌더. 첨부 = 다운로드 카드 기본 + **이미지(png/jpg/gif/webp)만 인라인**(비이미지 인라인 금지). 링크 = 하이퍼링크. 출처 자동 행 = 참고자료 최상단 고정(삭제 X 없음). 제출자료 done 강조. 일정 카드 6행(서버 응답에 전부 실려 있음 — 파생 재계산 금지)
- **완료 모달**: 620px 3분할, **활성 조건 = 한 줄 요약 또는 제출자료 1건 이상**(«요약 무조건 필수» 아님 — 시안과 다른 확정). 미체크 경고 = 비차단. 중단/취소 사유 모달 480px 은 상세·보드 **공용 컴포넌트**
- **보드 v1**: 칸반 4열 불변·완료 컬럼만 월 필터(기준 `completed_at`, 프론트 파생 — API 파라미터 없음)·상태 칩 드롭다운 **항목 소스 = 서버 allowed_transitions**(시안의 5값 고정 나열 금지)·사유 필수 전이 2단계·마커 **5값 유지**(시안 2값 금지)·D-3 이하 마감 강조(프론트 파생)·«0차» 숨김·테이블 빈 그룹 미렌더·«내 할 일/내가 요청한 일» 분리 **만들지 마라(v2)**
- 화면이 자체 전이표·판정을 갖지 않는다 — 서버 projection(permissions·allowed_transitions·is_request 등)만 소비
- 권한 게이팅 v1 = 현행 유지 — 역할별·상태별 연필/버튼 분기 **만들지 마라(v2)**
- 체크리스트 드래그 재정렬 = 채택(서버 sort_order·전체 재배열 endpoint 실재 — WP P0 실측)

## 3. allowed_paths

- `front/` — ⛔ `back/`·`mcp/` 금지

## 4. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-app/task-improve/front && npx tsc --noEmit && npx prettier --check <네가 만진 파일만>
```
- 만진 파일 0 에러·전체 빌드 금지·검증 1회만. 기존 무관 실패는 stash 실측으로 «무관» 분리.
- BE 응답 필드(background·goal·references·완료 seam)가 아직 없으면 **스펙 계약 기준 fail-closed** 로 구현(WP-129 FE 선례) — shape 가 애매하면 [질문] 으로 물어라.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 금지.** 끝나면 두 명령 모두:

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "Phase 별 결과 / 변경 파일 / 검증(tsc·prettier) / 계약 준수 / 미결"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] frontend(WP-130) 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] frontend: <질문>" --enter`
