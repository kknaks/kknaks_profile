# 루프2 FE-4 검수 — 틀고정·오늘 기준·자동 스크롤이 계약대로인가

**read-only.** 코드·문서 수정 0건. 커밋 금지. **개발 서버 금지** — `localhost:5173`·`127.0.0.1:8100` 은
**사용자의 E2E 스택**이다.
**쓰는 파일 하나**: `orchestration/work/strong-hajin-projects/review-loop2-fe4-report.md`

## 읽을 것

- 역할: `.../roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- **계약**: `spec-005-projects.md` v0.2.0 §2.4 · §6 의 **L-36 · L-42~L-48**
- **계획**: `work-005-projects.md` **Phase FE-4**
- **조사**: `loop2-survey-report.md` **Q1**(고쳐야 할 넷) · `research-fe-structure.md` §4-3(공유 자산)
- **워커 리포트**: `loop2-fe4-report.md` ← **주장을 믿지 말고 실측하라**
- 1루프: `review-fe-report.md`(같은 지적이 재발했는지)

검수 대상: `git diff` 로 **`frontend/` 변경**. ⚠ 워크트리에 **1루프·Phase 0·BE-3 변경도 함께 쌓여 있다**
(커밋 0건). **이번 판이 만진 6파일만** 대상이다 — 리포트가 목록을 준다.
**`backend/` 는 다른 판이라 지적하지 마라.**

## 판정

**FAIL**(계약·시안과 다르다) / **WARN**(모호하다) / **PASS**. **각 지적에 `파일:줄` + 근거.**
**「조용히 통과하는 자리」** — 렌더는 되는데 계약이 깨진 곳 · 빈 단언 · 항상 참인 가드 · 목만 검사하는 테스트.

## 반드시 확인할 것

1. **틀고정의 다섯이 다 있나** — ① `sticky; left:0` ② `z-index` 양수 ③ `background`
   ④ **축(머리줄)의 200px 자리를 덮는 요소** ⑤ **`align-self: stretch`**.
   ⚠ ⑤는 **조사가 못 세고 워커가 찾은 것**이다 — 「행이 `align-items:center` 라 이름 칸 높이가
   글자 높이뿐이라 위아래로 격자가 샌다」. **그 주장이 사실인지 CSS 로 확인하라**
2. **좌표계가 안 움직였나** — `anchorIndex` · 바 기하 · 의존선 경로 · 행 `top` · 접힘.
   워커는 **0줄 이동**이라 주장한다. **1루프의 핵심(사라지는 선이 없다)이 그대로인가** —
   `L-48` 회귀가 실제로 그것을 재는지 보라
3. **첫 진입 스크롤이 계약대로인가** — 워커가 **계약에 없어 스스로 정한 것 넷**이 있다:
   「첫 진입 + 프로젝트 전환」 · **오늘 앞 여백 2일** · 「오늘이 축 밖이면 가장 가까운 끝」 ·
   「사람이 민 뒤에는 안 되감는다」. **SPEC 과 어긋나지 않는지** 확인하고, 어긋나면 FAIL,
   빈자리를 메운 것이면 **WARN 으로 올려라**(코디가 문서에 반영한다)
4. **자동 스크롤이 양방향이고 `nearest` 인가**(L-45·L-47) — **이미 보이는 것을 움직이면 FAIL**.
   워커는 「L-47 을 «행»에 맞췄다(바로 하면 가로가 튀어 L-45 와 싸운다)」고 한다. **그 판단이 맞나**
5. **완료 바 `opacity: .55`**(L-36) — 워커가 「눈 없이 고른 값」이라 적었다.
   **다른 바(accent·danger·not-started)와 톤이 어긋나지 않는지** 토큰 값으로 따져 보라
6. **공유 자산이 안 흔들렸나** — `components.css`·`shell.css`·`src/ds/`·DS 토큰 **0줄**이라는 주장 확인.
   `.scax-inbox-card`·`.scax-gutter-list` 규칙에 **이 화면 전용이 아닌 변경**이 섞였으면 FAIL
7. **테스트가 실제로 재는가** — 워커가 더한 단언들(`scrollLeft` 실수치 68 · 축 스페이서 폭 ·
   「어느 요소로 스크롤했는지」 · nearest 옵션)이 **뮤테이션에 반응하는가.**
   구현 한 줄을 무력화하면 빨강이 되는지 **최소 둘은 직접 확인하라**
8. ⚠ **워커가 고친 「테스트 순서 의존」이 옳은 수선인가** — `renderPage()` 가 `getTask` 를
   `mockClear` 하게 바꿨다. **단언을 약화시킨 것이 아닌지** 확인하라(1루프에서 빈 단언이 나온 적 있다)
9. **테스트 수치를 네가 다시 재라** — `make frontend-test` · `npx tsc --noEmit`.
   **기존 실패와 이번 판 실패를 분리**. 1루프에서 `MeetingMaterials`·`ActionCenter` 가 부하로 흔들렸다
10. **범위** — `backend/` 0줄 · **FE-5 몫을 미리 건드리지 않았나**(헤더 생성 버튼·모달 ·
    우 레일 업무 정보 블록 · 상태 드롭다운 · 좌 레일 헤더 한 줄) · 커밋 0건 · 개발 서버 0회

## 범위 밖 — 지적하지 마라

- BE-3 변경 · 1루프 · Phase 0 · FE-5 몫 · 루프3 이월 · SPEC 미결(OQ-604~607)

## 리포트

판정 한 줄 → 지적마다 `[FAIL-n] / 무엇이 / 파일:줄 / 어느 인수조건과 어긋나나 / 수정안 한 줄`
→ **10항목 결과** → **테스트 실측** → **§3 의 「워커가 정한 넷」 각각에 대한 판정**
→ **눈으로만 확인되는 것**(사용자 2차 E2E 가 볼 자리) 목록.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_9c8b5b13-bf3a-4c7b-a159-373cf1ed04b1 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 루프2 FE-4 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / 10항목 결과 / 워커가 정한 넷의 판정 / 테스트 실측 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — 루프2 FE-4 검수. 상세는 인박스." --enter
```
