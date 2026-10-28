# [researcher] Ceramique 시안 다시 받기 · 바뀐 곳 보고 (read-only 조사)

너는 **cc-prototype `researcher` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 코디와 공유. 지정한 경로 밖은 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

- **Claude Design 프로젝트**(원천): `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23`
  - 웹 주 파일: `Ceramique 전체현황판.dc.html` (+ import 전부 — `_ds/medikit-…/` 번들 · 폰트 · `ceramique-theme.css` · `medikit-patches.css` · `support.js` · `assets/`)
  - **앱 시안**: 사용자가 「우리 앱 디자인도 어느 정도 나왔다」고 했다. 파일 이름은 모른다 — 프로젝트 파일 목록에서 찾아라(「앱」 · 「모바일」 · 「태블릿」 · 「의료진」 · 「간호사」 · 「코디」 · 「상담」 · 「문진」 · 「QR」 · 「스캔」 · 최근 수정 파일). 앞 판 앱 시안 = `Ceramique 의료진 앱 (구현 v3)` · `간호사 모바일 (구현 v3)` · `시술실 태블릿 (구현 v3)` — 이것보다 **새로 생기거나 바뀐 앱 파일**이 대상
  - 접근: `DesignSync` 도구. 인증이 안 되면 **혼자 우회하지 말고** §9 질문 채널로 「/design-login 필요」라고 물어라
- 지금 레포에 있는 이전 판(비교 기준): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/`
- 이전 판 분석(비교 축 참고): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 하나

cc-prototype 「Ceramique 전체현황판」 1차(시술 현황 · 예약 현황 웹)가 배포됐다. 다음 판은 세 갈래 — ① 앱(Flutter) ② 시술 현황(시술 차트 · 상태 2계층) ③ 예약 현황 잔여. 사용자가 시안을 고쳤고 앱 시안도 새로 만들었다. 범위를 정하기 전에 **새 시안을 받고, 이전 판과 무엇이 달라졌는지**를 알아야 한다.

## 3. 계약

해당 없음 (조사).

## 4. 먼저 읽을 핵심 파일

§1 프로젝트 파일 목록 전체 → 웹 주 파일 · 앱 시안 파일과 그 import.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design-prev/` — **먼저** 지금 `design/` 을 통째로 여기로 옮긴다(이전 판 보관 · 비교용)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/` — 새 판 **원본 그대로**(프로젝트 안 경로 구조 유지). 웹 주 파일 + 앱 시안 파일 + 둘의 import 전부
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-refresh-report.md` — 리포트 1개

두 폴더는 `.gitignore` 에 이미 들어 있다(실명 예시값 — 로컬만).

## 6. 할 일

1. `design/` → `design-prev/` 로 옮기고, 새 판을 `design/` 에 받는다. 리포트 머리에 **프로젝트 파일 목록 전체**(이름 · 수정 시각 있으면) + 받은 파일 목록 · 크기 + import 대조 결과.
2. **웹 주 파일 — 이전 판과 비교**(`diff` 로 직접). 바뀐 곳마다 표 한 줄: 화면 · 영역 | 추가 / 변경 / 삭제 | 무엇이 | 근거(새 `파일:줄` ↔ 이전 `파일:줄`) | 닿는 갈래(② 시술 현황 / ③ 예약 현황 / 공통). 특히 아래는 빠뜨리지 말고 따로 적는다:
   - (a) **시술 차트** — 간호관리차트 · 의사차트 · 시술 메모를 보고 쓰는 화면 · 칸 · 버튼이 생겼는지
   - (b) **시술 현황 상태 표시** — 주 상태 + 부상태(대기 · 진행 · 완료) 색 · 뱃지가 바뀌었는지
   - (c) **예약 카드 드래그** — 시안의 드래그 코드(이벤트 · `draggable` · 잡는 영역 · 놓는 자리)가 어디 있는지 `파일:줄`. 바뀌지 않았어도 위치를 적는다(지금 구현은 예약 카드가 안 잡혀서 다음 판 수정 때 대조한다)
   - (d) **공지 [수정하기]** · 상담사 목록 · 그 밖 예약 현황 변경
3. **앱 시안** — 파일마다: 대상 사용자 · 기기(폰 · 태블릿) · 화면 목록 · 화면별 영역 · 표시 필드 · 버튼 · 상호작용(`파일:줄`). 앞 판 앱 시안(구현 v3)이 있으면 그것과 비교. 아래 주제가 시안에 있는지 있음 / 없음으로 표 하나: 코디 계정 · 상담사(실장) 계정 · 상담사 배정 푸시 · 고객 QR 문진 입력 · 신분증 스캐너(국적 · 여권번호 · 이미지) · 시술 현황 되돌리기 · 시술 차트.
4. 시안 안 메모 · 주석 · TODO 원문 중 **새로 생긴 것**만 모은다.
5. 「정할 것」: 시안만으로 동작이 정해지지 않는 자리. **결정하지 마라.**

## 7. 범위 제약 — 하지 말 것

- Claude Design 에 **쓰지 마라** — 읽기만.
- 코드 레포 · `para/` 문서 수정 금지. KOS 호출 금지(이번 판은 시안만).
- 디자인 파일을 리포트에 통째로 붙이지 마라 — 요약 + `파일:줄`.
- 실명 · 연락처가 시안 예시값에 있으면 리포트에 옮기지 말고 「실명 있음(n건)」으로만 적는다(public 레포).

## 8. 검증

```
바뀐 곳마다 근거(새 파일:줄 ↔ 이전 파일:줄). 시안에 없는 것은 「시안에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 받은 파일 수가 import 목록과 맞는지 리포트에 대조 결과를 적는다.
- 리포트에 실명 · KOS id · 토큰이 없는지 grep 결과(0건)를 적는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_5351b98b-492b-4abb-9111-f79009768111 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] researcher: <질문>" --enter`
