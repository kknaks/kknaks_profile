# [frontend] WP-FE — front/ 전부 (월별 매출 리스트 화면 · cc-prototype 디자인 복사)

너는 **agency-settlement `frontend` 워커**다. **맥락이 하나도 없다고 가정하고** 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리 `back/` 에서 병렬 작업 중 — `back/` · 레포 루트 `README.md` 를 건드리지 마라.** 붙이기는 SPEC §4.2 계약으로 — back 이 아직 없으니 가짜 응답으로 화면을 먼저 만든다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` (**0.2.1**) ← 계약의 SoT. **여기 없는 건 발명하지 마라.** 막히면 §9 로 물어라
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` — 네 WP 행(완료 조건 · 검증 명령)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` — 결정
- KOS 공식 스펙 `https://developers.kos-solution.com/openapi.yaml` — 필드 확인용

기대는 개념:
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/areas/concept/cs/no-inference-from-free-text.md` — 자유 텍스트(메모 · `…FunnelDetail`)를 읽어 무엇을 추정하지 마라

## 2. 배경 / 무엇을 바꾸나

빈 레포에 `front/`(Next.js)를 세운다. 월 선택 `[‹] [›]` · 다시 불러오기 · 수납 묶음 머리 + 품목 줄 · payment 줄 · 음수 줄 · 경고 배지 · 상태 화면 5종(SPEC §3). 디자인은 **cc-prototype `procedure/front` 의 토큰 · 컴포넌트를 복사**한다(SPEC §8 목록 · import 금지 · 파일 머리 「원본:」 주석). medikit 은 npm `@medisolve-ai/medikit@1.4.0`(사용자 `~/.npmrc` 로 설치됨).

## 3. 계약

SPEC-001 §4.2(응답 shape) · §4.3(오류) 그대로. BE · FE 가 이 둘을 공유한다 — 필드명 하나라도 다르게 만들지 마라. 계약을 바꿔야 할 것 같으면 바꾸지 말고 §9 로 물어라.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/front/tailwind.config.ts` · `postcss.config.mjs` · `app/globals.css` · `app/styles/` · `app/layout.tsx` · `components/common/` · `lib/time.ts` · `lib/api.ts` — SPEC §8 복사 목록의 원본
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/front/package.json` — 판 맞춤(medikit 1.4.0 · Next 판)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. SPEC §3 · §4.2 · §6.3 · §8 과 WORK WP-FE 행을 읽는다
2. §8 목록대로 복사 → `lib/types.ts`(§4.2 그대로) · `lib/labels.ts` → `app/page.tsx`(`?month=` · 기본 이번 달 KST) · `components/monthly/*`
3. 가짜 응답(가짜 이름 `홍**` · 가짜 금액)으로 상태 5종 · 묶음 · payment 줄 · 음수 줄 · 배지 2종 스크린샷을 scratchpad 에 찍고 경로를 보고한다
4. §8 검증

## 7. 범위 제약 — 하지 말 것

- 실제 고객 이름 · 금액을 가짜 데이터 · 스크린샷에 쓰지 마라
- `localStorage` · `sessionStorage` 금지 · cc-prototype import 금지(`grep -rn "procedure/" front` = 「원본:」 주석만)
- 커밋 · push · PR 금지. 사용자 포트 · 프로세스를 건드리지 않는다(띄워 볼 때는 다른 포트 · 끝나면 내린다)

## 8. 검증

```
cd front && npm install && npx tsc --noEmit && npm run lint && npm run build
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고에 WORK-001 네 WP 완료 조건을 한 줄씩 「충족 / 미충족(사유)」으로 적는다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3605662c-607d-4c3e-8480-a4fdce8f45af --from term_eb595f4c-ebea-448b-b27d-7137f208d9e5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3605662c-607d-4c3e-8480-a4fdce8f45af \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3605662c-607d-4c3e-8480-a4fdce8f45af --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
