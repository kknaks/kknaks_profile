# [frontend · 시안 읽기] 간호사 모바일 · 시술실 태블릿 시안 받아 정리 (read-only)

너는 **cc-prototype `frontend` 워커**. claude design(DesignSync). **시안 수정 · 업로드 금지 · 코드 수정 금지.**
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 산출물 경로 말고 건드리지 마라.

## 1. 배경

시술 현황판(웹 · 간호 스테이션)은 구현 · 로컬 E2E 중이다. 사용자가 **디자인 2단계 — 시술실 태블릿 · 간호사 모바일** 시안을 claude design `dda9a931` 에 만들었다. 이걸 보고 코디 · 사용자가 다음 범위(결정 · 스펙)를 정한다.

- 시안: `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23` — **`Ceramique 간호사 모바일.dc.html`** + 태블릿 시안(이름 모름 — 목록에서 찾아라: 「태블릿」 · 「시술실」 · 「모바일」 · 최근 새 파일). 함께 읽을 것: `_ds/medikit-aea7ac33-…/_ds_bundle.css` · `_ds_bundle.js` · `fonts/fonts.css` · `styles.css` · `ceramique-theme.css` · `medikit-patches.css` · `support.js`
- 지금까지 정한 것: `para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`(D-29 「원칙은 시술실 태블릿 · 모바일, 지금은 간호 스테이션」 · D-34 범위 밖) · `20-spec/spec-003-procedure-board.md`(0.2.0 · 상태 · 버튼 활성표 · API) · 결정 이력 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 · E2E 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/e2e-feedback-batch-1.md`
- 웹 현황판 확정 시안: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-user-r4/Ceramique 시술현황판 v2.dc.html`

## 2. 할 일

1. `list_files` — 47개(r4 읽기 때)와 비교해 새 파일 전부. 모바일 · 태블릿 후보를 **전부** 받는다 → `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile/`(원래 이름 · truncated 확인)
2. 파일마다: 기기 폭 · 화면/장면 목록(scene props 값) · 화면마다 요소(목록 · 카드 · 버튼 · 상태 이름 · 모달 · 로그인 · 탭) · **누가 쓰는가**(간호사 · 피부 · 원장 · 시술실 공용)
3. **흐름** — 로그인 → 고객 고르기 → 마취 · 의사 호출 · 수락 · [시작]/[종료] · 귀가 대기 중 무엇을 어디서 하는지. 웹 현황판과 같은 조작 / 새 조작 / 빠진 조작
4. **SPEC-003 과 대조** — 이미 back 이 주는 스냅샷 · 조작 API 로 그릴 수 있는 것 / 새 필드 · 새 API 가 필요한 것(사실만)
5. **DEC-005 · E2E 결정과 다른 점**(예: 개인 계정 로그인 · 전체 고객 · 수락 위치 · 마취 · 방 배정 줄 등) — 판단 말고 사실 한 줄씩
6. **정책 후보** — 시안이 정한 것처럼 보이는 규칙 · 「정할 것」
7. 배포 웹 코드(`/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2/procedure/front`) 컴포넌트를 재사용할 수 있는 곳 · 테마 어긋남

## 3. 산출물 — 이것만

- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile/` (받은 파일)
- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-mobile-read-report.md` — 맨 위 「찾은 파일」 → 화면 · 흐름 → SPEC 대조(재사용 / 새로 필요) → DEC · E2E 차이 → 정책 후보 · 정할 것

## 4. 하지 말 것

- DesignSync 쓰기 0 · 코드 · 리포 수정 0 · 커밋 금지 · 결정하지 마라
- 실제 사람 이름 · 연락처는 리포트에 옮기지 마라(public)

## 5. 검증

- 목록 수 · 받은 파일 truncated:false · 리포트 사람 이름 · 연락처 0(grep)

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 모바일 · 태블릿 시안 읽기" \
  --body "찾은 파일 / 바뀐 것 수 / 정책 후보 수 / 코드 어긋남 수 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 모바일 · 태블릿 시안 읽기 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
