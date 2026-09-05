
# [designer] 디자인 패키지 프론트 구조 분석 — 페이지 구성 · Next.js 구조 · shadcn 컴포넌트 · 공용 컴포넌트 · 소요

너는 **task-management `designer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/designer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**⚠ 이 워크트리는 코디네이터와 공유한다.** 너는 read-only 분석자다 — 아래 §5 의 리포트 파일 1개 외에는 **어떤 파일도 만들거나 고치지 마라.** git 명령은 읽기(log/diff/show)만.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/00-README.md` ← 디자인 핸드오프 패키지 인덱스. **여기 없는 건 발명하지 마라.** README 의 「읽는 순서」대로 md 00~15 전부 + dc.html 원본을 읽는다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/README.md` ← 제품 지도 — 스택(Tauri + Next.js 프론트 + FastAPI 백엔드)·타겟(macOS·Windows 데스크톱, macOS 웹뷰는 WKWebView 라 Safari 호환 고려)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

task-management 앱의 문서 파이프라인(디자인 → 기획서 baseline → 정책서 decision → 기능정의서 spec → work)을 시작한다. 이 분석 리포트가 **파이프라인 전체의 입력**이 된다 — 이후 기획서는 기능(영역) 단위로 「왜 + 인/아웃바운드 + 기능명세」를, 정책서는 「CRUD 기준 규약」을, 기능정의서는 스펙을 이 리포트를 근거로 쓴다.

이번 발주는 그 첫 단계로, 완성 디자인 패키지(`00-design/` — dc.html 9종 + md 00~15)를 **프론트엔드 구현 관점**에서 구조화한다. 분석 관점 4 + 소요 1:

1. **페이지 구성 파악** — 화면/페이지 인벤토리. 페이지 · 드로어 · 팝오버 · 모달을 구분하고, 영역(내 업무·auth·회의록·캘린더·문서함·메시지함·홈 등)별 네비게이션 구조를 표로.
2. **Next.js 프론트 구조** — App Router 기준 라우트 트리와 레이아웃 계층 **제안**. 사실(디자인이 요구하는 화면 관계)과 제안(라우트 설계)을 절로 분리하고, 갈리는 지점은 결정하지 말고 질문으로 남긴다.
3. **shadcn/ui 사용 컴포넌트 파악** — 디자인 시스템·화면 정의서의 UI 패턴을 shadcn/ui 컴포넌트로 매핑(예: Dialog/Sheet/Popover/Command/Table/Badge/Calendar…). shadcn 으로 안 되고 커스텀이 필요한 것을 따로 표기하고 근거를 단다.
4. **공용 컴포넌트 도출** — 여러 영역에서 반복되는 패턴(드로어 프레임, 상태 배지, 필터/정렬 바, 카드, 검색 팝오버, 에디터 등)을 후보로 뽑고, 어느 화면들이 공유하는지 매핑.
5. **작업 소요 파악** — 영역별 구현 규모 추정(페이지 수 · 신규/공용 컴포넌트 수 · 복잡도 상대 평가)과, 어느 영역부터 문서화·구현하는 게 의존성이 적은지 순서 제안.

모든 발견 항목에 안정 ID 를 부여한다 (페이지 `P-xx` · 컴포넌트 `C-xx` · 공용 컴포넌트 `S-xx` · 미결 질문 `Q-xx`) — 이후 baseline/decision 이 이 번호로 인용한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 첫 발주. 코드 레포는 아직 스캐폴딩 전이다.

## 4. 먼저 읽을 핵심 파일

- `00-design/00-README.md` — 패키지 구성과 읽는 순서·전제(개인용 단일 사용자, 데스크톱 전용 1280 미만 미지원, 1920×1080 실측 좌표)
- `00-design/01-screens.md` — 화면 목록·보드 매핑 (관점 1 의 뼈대)
- `00-design/09-design-tokens.md` + `00-design/디자인 시스템.dc.html` — 토큰·컴포넌트 패턴 (관점 3·4 의 뼈대)
- `00-design/10-open-questions.md` — 미해결 항목. **임의로 답을 채우지 마라** — 리포트 Q-xx 로 옮긴다
- 나머지 md(02~08 · 11~15)와 dc.html 원본 전부 — 커버리지 표에 파일별 반영 위치를 남긴다

## 5. allowed_paths — 이 밖은 건드리지 마라

- 산출물은 이 파일 **1개뿐**: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/docs-v1-design-report.md` (완료 후 slug 통합으로 경로 변경 — 원 발주 시점 경로는 design-frontend-structure/)
- 그 외 리포 파일 수정·생성 일체 금지 (read-only). 커밋·push 금지.

## 6. 구현 단계

1. 역할 문서(role.md)를 읽는다.
2. §1·§4 순서대로 디자인 패키지 전체를 읽는다 (md 00~15 + dc.html 9종 — dc.html 은 구조·컴포넌트 확인 수준으로).
3. 관점 1 — 페이지/드로어/팝오버 인벤토리 표 (P-xx).
4. 관점 2 — Next.js App Router 라우트 트리·레이아웃 계층 제안 (사실/제안 분리).
5. 관점 3·4 — shadcn 매핑 (C-xx) + 공용 컴포넌트 후보 (S-xx, 공유 화면 매핑).
6. 관점 5 — 영역별 소요 추정과 진행 순서 제안.
7. 입력 파일 전체 커버리지 표 + `10-open-questions.md` 대조(누락 없이 Q-xx 로 이관) 확인.
8. 리포트 작성 → §8 검증 → §9 완료 보고.

## 7. 범위 제약 — 하지 말 것

- 코드를 만들지 않는다 (스캐폴딩·컴포넌트 코드·설정 파일 일체).
- 디자인 원본(`00-design/`)을 고치지 않는다.
- baseline/decision/spec 문서를 쓰지 않는다 — 그건 다음 단계 워커 소관.
- open question 에 임의로 답하지 않는다. 판단이 필요한 것은 전부 Q-xx 질문으로.
- 모든 주장에 근거 파일(파일명 + 절/줄)을 단다. 근거 없는 항목은 싣지 않는다.
- 메시지함·홈 등 범위 판단(v1/v2)은 하지 않는다 — 패키지 전체를 분석하고, 범위는 사용자가 정한다.

## 8. 검증

```
분석은 read-only — 코드를 만들지 않고 디자인 원본을 고치지 않는다. 리포트에 입력 파일 전체 커버리지 표(파일별 반영 위치)를 남기고, 미결 질문은 원본 open questions 와 대조해 누락 없이 옮겼는지 확인한다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "designer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2 \
  --text "[worker_done] designer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e6d07c2f-a88d-46b4-9d0c-3ed44e6c90a2 --text "[질문] designer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
