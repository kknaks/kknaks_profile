# [reviewer] FE-1~FE-3 검수 — 화면이 시안대로이고 계약대로 읽는가

너는 **strong-hajin `reviewer` 워커**다. **맥락이 하나도 없다.** 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md` 전부) · 코드 레포 `AGENTS.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` ← 계약 (인수조건 §6) · `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` ← FE-1~3
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/fe-impl-report.md` ← **FE 워커 리포트. 주장을 믿지 말고 실측하라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md` **§6** ← **백엔드가 실제로 내려주는 응답**(실물 JSON)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← 시안의 틀·부품·색·기하
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md` **§4-3** ← **공유 자산 지도**(건드리면 흔들리는 화면들)

검수 대상: **`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`** — `git diff` 로 `frontend/` 변경 전부를 본다.
⚠ `backend/` 변경은 **다른 워커 몫이라 이번 검수 범위 밖**이다.

## 1. 판정

**FAIL**(계약·시안과 다른 것이 돈다) / **WARN**(모호하다) / **PASS**. **각 지적에 `파일:줄` + 근거.**
**「조용히 통과하는 자리」** — 렌더는 되는데 계약이 깨진 곳, 빈 단언, 목만 검사하는 테스트.

## 2. 반드시 확인할 것

1. **사라지는 의존선이 없는가** ← **이 판의 핵심**. 시안 `DepLines` 의
   `if (!a || !b) return` 을 그대로 베꼈으면 **FAIL**. 접힌 가지에 걸린 선이
   **접힌 부모 바에 붙는지** 코드로 확인하라. 테스트가 그것을 겨누는가
2. **간트가 깊이 제한 없는 재귀인가** — 2단계에서 끊기면 FAIL. 손자·증손자 행이 서는가
3. **들여쓰기 예산** — 깊이당 12px · 최대 5단 (D-18). 나머지 기하(행 40 · 하루 34 · 라벨 200 ·
   바 22/14/18 · 레일 380/342)가 시안과 같은가
4. **진행률 넷** — ① 체크리스트 기반 ② **`total==0` 이면 % 도 fill 도 안 그린다**(0% 금지)
   ③ 상위 바는 % 없음 ④ `cancelled` 는 fill 없음·취소선
5. **BE 응답을 바르게 읽는가** (`be-impl-report.md` §6):
   **`assignee: null` 을 「미정」으로 지어내지 않는가** · **간트가 `span_*` 을 쓰는가**(원값 아님) ·
   **`overdue_days` 가 없는 업무를 「지연」으로 세지 않는가** · **`blocked` 값을 떨어뜨리지 않는가**
6. **요약 스트립 모수** — 「전체 업무」와 진행률 분모가 **둘 다 취소를 뺀 수**인가
7. **공유 자산** — `.scax-inbox-card` 선택 CSS 가 **`[role="button"]` 으로 좁혀졌는가**(안 그러면
   수신함·캘린더 카드에 얹힌다) · `Empty`(29곳) · `AppHeader titleEnd`(5화면) ·
   `.screens-b-lead`(조직·관계탐색·보고 + `OrgPage.test.tsx:249`) 를 **건드렸는가**
8. **후행은 클라이언트 역산인가** — 서버에 없는 경로를 부르고 있지 않은가
9. **`api.ts` 밖 fetch 0건** · 관리 모달이 **기존 기능을 옮긴 것**인지(새 발명 아님)
10. **범위** — `backend/` 0줄 · 커밋 0건 · 개발 서버 기동 0건

## 3. 테스트 — 직접 돌려라

- `make frontend-test` · `frontend` 에서 `npx tsc --noEmit`. **수치를 네가 재라**
- **기존 실패와 이번 판의 실패를 분리**해 보고
- **개발 서버를 띄우지 마라**(브라우저 E2E 는 사용자 몫)

## 4. allowed_paths

- **read-only.** 수정·커밋·push 금지. **쓰는 파일 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-fe-report.md`

## 5. 리포트

판정 한 줄 → 지적마다 `[FAIL-n] / 무엇이 / 파일:줄 / 어느 계약·인수조건과 어긋나나 / 수정안 한 줄`
→ **§2 의 10개 항목 결과** → **테스트 실측** → **시안 대비 눈에 띄는 차이**(있으면).

## 6. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_dd893990-2501-4dc6-843a-712588a9aaf6 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: FE-1~FE-3 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / §2 10개 항목 결과 / 테스트 실측 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — FE 검수. 상세는 인박스." --enter
```
