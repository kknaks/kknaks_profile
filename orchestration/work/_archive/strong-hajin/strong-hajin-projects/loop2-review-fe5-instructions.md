# 루프2 FE-5 검수 — 마지막 구현 판

**read-only.** 코드·문서 수정 0건. 커밋 금지. **개발 서버 금지** — `5173`·`8100` 은 **사용자 E2E 스택**이다.
**쓰는 파일 하나**: `orchestration/work/strong-hajin-projects/review-loop2-fe5-report.md`

## 읽을 것

- 역할: `.../roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- **계약**: `spec-005-projects.md` v0.2.0 — §2.1·2.2·**2.6**·2.7·**2.10** · §5 · §6 의 **FE-5 몫**
- **계획**: `work-005-projects.md` **Phase FE-5**
- **백엔드 실물**: `loop2-be-report.md` **§3-6 의 열두 자리** ← **FE 가 틀리기 쉬운 자리 목록이다**
- **워커 리포트**: `loop2-fe5-report.md` ← **주장을 믿지 말고 실측하라.**
  특히 **§6「테스트가 못 무는 자리」**와 **§4「계약에 없어 내가 정한 것 셋」**
- 앞 판: `loop2-fe4-report.md` · `review-loop2-fe4-report.md`(같은 지적이 재발했는지)

검수 대상: `git diff` 로 **`frontend/` 변경**. ⚠ 워크트리에 **1루프·Phase 0·BE-3·FE-4 도 쌓여 있다**
(커밋 0건). **FE-5 가 만진 9파일만** 대상 — 리포트가 목록을 준다. **`backend/` 는 지적하지 마라.**

## 판정

**FAIL** / **WARN** / **PASS**. **각 지적에 `파일:줄` + 근거.**
**「조용히 통과하는 자리」** — 렌더는 되는데 계약이 깨진 곳 · **빈 단언** · **자기참조 단언**
(앞 판에서 실제로 나왔다) · **`waitFor` 없이 비동기 값 읽기**(앞 판의 FAIL) · 목만 검사하는 테스트.

## 반드시 확인할 것

1. **백엔드 열두 자리를 바르게 처리했나** — `loop2-be-report.md` §3-6 을 **하나씩 대조**하라. 특히:
   **① `access` 로 체크리스트를 감추지 않는가**(`read_only` 인데 `checklist` 가 온다) ·
   **② 키의 «유무»로 가르는가**(`body.checklist?.length` — `.length` 직접 접근은 터진다) ·
   **③ 미터 재료가 프로젝트 상세의 `checklist_progress` 인가**(상세 응답으로 그리면 빈다) ·
   **⑤ 리드라고 쓰기를 열지 않는가** · **⑥ 체크박스가 읽기 전용인가**(담당 아니면 404) ·
   **⑩ 초대돼도 `may_manage` 는 false — 관리 손잡이가 서면 안 된다** ·
   **⑪ 거절 뒤 목록을 다시 읽는가**
2. **상태 관문 열 개가 실제로 도는가** — 워커는 **전부 구현**이라 주장한다. SPEC §2.6 의 표와
   코드를 **하나씩 대조**하라. 특히 **막힘 → 사유 프롬프트** · **요청 업무 완료 → 완료 보고 모달** ·
   **게이트 둘**(`task.self_manage` + 수락 대기 아님) · **`version` 동봉**(업무 상세로 읽은 회차) ·
   **성공 뒤 다시 읽기**(업무 상세 + 프로젝트 상세) · **갈 곳 없으면 읽기 배지**
3. **생성 버튼 게이트가 `project.manage` capability 인가** — 「관리」의 `may_manage` 와 **섞이지 않았나.**
   **빈 상태(프로젝트 0개)에서도 버튼이 서는가**(L-15·L-16). 그 갈래를 코드로 따라가라
4. **생성 모달이 네 칸인가** — `external_key` 가 화면에 **없어야** 한다. 거절 네 갈래를 말하는가
5. **관리 모달의 기존 생성 폼이 «그대로» 있는가** — 루프3 몫이라 **지우면 FAIL**
6. **좌 레일 헤더 한 줄 + 건수 배지** — 기존 `Badge variant="count"` 를 쓰는가.
   ⚠ **FE-4 가 `.scax-gutter-list__body` 에 단 `ref` 와 카드의 `data-task-id` 가 살아 있는가**
   (지우면 자동 스크롤 L-46 이 죽는다)
7. **우 레일 블록 순서** — 메타 → **업무 정보(설명+체크리스트)** → 관계 → 하위 업무
8. **메타 표 셋** — 값 좌측 정렬선 하나 · 행 높이 통일 · **버튼 시인성(두 자리 모두)**
9. **공유 자산 0줄** — `src/ds/`·`components.css`·`shell.css`·`MyWorkPage.tsx`·`WorkModals.tsx`.
   워커는 **diff 빈 출력**이라 주장한다. **네가 직접 확인하라**
10. **테스트가 실제로 무는가** — **뮤테이션으로 최소 넷** 확인하라. 그리고 워커가 §6 에 적은
    **「못 무는 자리」가 사실인지** — 정직한 고백인지, 아니면 **더 물 수 있는데 안 문 것**인지
11. **앞 판 FAIL 이 재발했나** — `waitFor` 없는 비동기 읽기 · 자기참조 단언
12. **범위** — `backend/` 0줄 · 루프3 몫 0줄 · 커밋 0건 · 개발 서버 0회
13. **테스트 수치를 네가 다시 재라** — `make frontend-test` · `npx tsc --noEmit`.
    ⚠ **기존 흔들림**(이 판 밖): `task checklist`(2) · `task checklist span/null` ·
    `adjustment and resubmission` · `product surfaces`. **분리해 보고하라**

## 범위 밖 — 지적하지 마라

- BE-3 · FE-4 · 1루프 · Phase 0 · 루프3 이월(관리 모달 정리 · 리드 권한 화면) · SPEC 미결

## 리포트

판정 한 줄 → 지적마다 `[FAIL-n] / 무엇이 / 파일:줄 / 어느 인수조건과 어긋나나 / 수정안 한 줄`
→ **13항목 결과** → **백엔드 열두 자리 대조표** → **상태 관문 열 개 대조표**
→ **테스트 실측** → **눈으로만 확인되는 것**(사용자 2차 E2E 가 볼 자리).

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_816c39e4-e2c0-4a25-bf27-ad371d140007 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 루프2 FE-5 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / 13항목 결과 / 열두 자리·관문 열 개 대조 / 테스트 실측 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — 루프2 FE-5 검수. 상세는 인박스." --enter
```
