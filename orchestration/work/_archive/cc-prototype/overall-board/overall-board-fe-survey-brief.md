# [frontend] 현재 시술 현황판(procedure) 인벤토리 — 전체현황판 비교 준비 (read-only 조사)

너는 **cc-prototype `frontend` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/README.md` · 레포 루트 `.claude/` 안내가 있으면 그것도

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (branch `kknaksss/overall-board`, base `origin/main` = `eaa9169`)

⚠ 이번 판은 **read-only 조사**다. 코드를 고치지 마라. 병렬로 researcher 워커가 새 디자인(「Ceramique 전체현황판」)을 분석 중이다 — 너는 **현재 코드 쪽만** 본다. 디자인과의 차이 비교는 다음 판.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` ← 현재 현황판 계약
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-003-procedure-board.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/log/2026-10-22-myeongdong-poc-v2.md` §7 잔여 (OQ-517~519 · 시안 정책 후보 P-1~5)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 하나

명동 PoC v2 의 「시술 현황판」(`procedure/front` + `procedure/back`)을 사용자가 새로 디자인한 「Ceramique 전체현황판」으로 업그레이드한다. 대상은 **현황 탭 하나**다(다른 탭은 안 만든다).
이번 판은 **지금 현황판이 실제로 무엇을 보여주고 어떻게 동작하는지**를 디자인과 같은 축으로 정리해 두는 것이다. 다음 판에서 이 리포트와 디자인 분석 리포트를 맞대어 차이를 뽑는다.

## 3. 계약

해당 없음 (조사).

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/app/(main)/procedures/page.tsx` · `procedures/live/page.tsx` · `app/(main)/layout.tsx`
- `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/components/procedures/` (`OrderCard.tsx` · `Aside.tsx` · `CallPopover.tsx`) · `components/common/AppHeader.tsx` · `lib/`
- `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back/` — 현황판이 부르는 API 라우터 · 응답 스키마 · KOS 호출부
- `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/tailwind.config.ts` · 전역 css — 테마/토큰

## 5. allowed_paths — 이 밖은 건드리지 마라

- 코드 레포: **수정 금지(read-only)**. 빌드 · 서버 실행 · 포트 사용도 하지 마라(사용자 포트·프로세스 금지).
- 산출물은 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/current-board-report.md`

## 6. 할 일

아래 축으로 **현재 현황판**을 적는다. 각 항목에 근거 `파일:줄`.

1. 라우트 · 화면 구성: `/procedures` 와 `/procedures/live` 가 각각 무엇인지, 공통 헤더 · 로그인 · 역할(관리자/원장/간호) 진입
2. (a) 레이아웃 영역: 헤더 · 필터/툴바 · 본문(칼럼·그리드) · Aside · 하단
3. (b) 상태/칼럼 체계: 단계(칸) 목록 · 순서 · 라벨 원문 · 개수 표시 · 단계 판정 로직(어떤 데이터로 어느 칸에 들어가나)
4. (c) 카드 해부: OrderCard 표시 필드 · 칩/뱃지 · 색 규칙 · 조건부 표시(예: 「방 배정 · 준비중」 줄, `canCall`)
5. (d) 상호작용: 호출(CallPopover) · 토스트 · 폴링/SSE 주기 · 클릭 동작 · 앱(시술실 앱)과 주고받는 것
6. (e) 데이터 필드 표: 화면 필드 → front 타입 → back 응답 필드 → **KOS 원천**(어느 KOS API · 필드인지, 내부 API 인지 공개 API 인지). 원천을 못 찾으면 「못 찾음」
7. (f) 테마: tailwind 토큰 · 폰트 · 로고 · medikit/디자인 시스템 사용 여부
8. (g) 상태 변형: 빈 상태 · 로딩 · 에러 · 반응형
9. 스펙과 코드가 어긋난 자리(예: OQ-517 「방 배정」 줄, P-1 토스트 위치)를 따로 표로.

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서 수정 금지. 커밋 금지. 서버 · 빌드 · npm install 금지(파일 읽기로 충분하다).
- 디자인 파일을 찾아 비교하지 마라(다음 판).
- 실명 · KOS id · 키 값을 리포트에 옮기지 마라(public 레포). 필드명과 형식만.

## 8. 검증

```
각 항목 근거 파일:줄. 코드에서 확인 못 한 것은 「확인 못 함」으로. 추정으로 채우지 않는다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_e934c05f-d4a8-43f6-925d-4e8fe3c873f5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
