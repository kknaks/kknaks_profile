# [pencil] 시술현황 화면 정의서 맵 — 디자인 화면 + 연결 화살표 + 정책 메모 (리드 + 서브에이전트)

너는 **cc-prototype `pencil` 워커(리드)**다. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil` · 코디와 같은 워크트리. **너는 앞 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. `pencil-correction-*.md` · `*.OLD-brief.md` · `*.HOLD.md` 는 폐기된 방향이니 읽지 마라.

## ⚠ 이번 판 실행 규칙 (앞 판에서 앱이 세 번 죽었다)

- **앱 모드 eval 금지. headless 만**: `bun ~/.bun/bin/openpencil eval /Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig -w --stdin < 스크립트`. 앱은 코디가 닫아 두었다 — 앱을 열지 마라.
- **eval 은 리드만, 한 번에 하나(직렬), 한 번에 작게**(섹션 하나 · 20초 안). 서브에이전트는 스크립트 작성과 정적 검토만 하고 **실행하지 않는다.**
- 실행 전 `medikit.fig` 를 `medikit.before-map.fig` 로 백업.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` ← **디자인 페이지(생김새 · 배치 정본).** 화면의 구성 · 배치 · 샘플 값은 이 시안대로.
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` ← 시안의 동작 결정(U1~U12 등) — 시안과 기획안이 다르면 이 결정이 앞선다.
- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` ← **화면 목록 · 정책 · 이동의 원천.** 메모 본문은 여기 원문 인용 + 줄.
- 앞 판 데이터(그대로 재사용 · 검증해서 고쳐 쓴다): `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/cc-procedure-map/screens.json`(56) · `edges.json`(66) · `notes.json`(173). 기존 `render.js` · `build.sh` 는 와이어판이라 버리고 새로 쓴다.
- 컴포넌트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` 「components」 페이지 26세트 · 120 variant · 변수 64. 만든 스크립트와 공통 함수: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/components/`(`_lib.js` 의 `inst()` 등) · 인벤토리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/pencil-components-report.md`
- 앞 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md`(화면별 UI 요소 · 정책 줄 범위)
- ⚠ 다른 레포의 기존 구현 코드(DAY · cc-prototype)는 열지 않는다.

## 2. 무엇을 만드나

`medikit.fig` 에 새 페이지 **「시술현황 맵」**:

```
┌ 1. 시술 현황 보기 ─────────────────────────────────────────┐
│ [디자인 화면] ──(버튼 이름)──▶ [디자인 화면]                 │
│  ①②③ 마커          [정책 · 기획 메모 카드: ① 원문 (L180) …]   │
└───────────────────────────────────────────────────────────┘
```

- **화면**: 「components」 세트의 **인스턴스로** 짓고, 시안 배치 · 샘플 값을 따른다(가짜 값 — 시안 샘플 그대로 쓰면 된다). 화면 프레임 이름 `screen/<screenId>`.
- **마커**: 화면 안 버튼 · 요소에 번호 ①②③(작은 원). 이름 `marker/<screenId>/<no>`.
- **연결**: 화면 → 화면 화살표 + 트리거(버튼 이름) 라벨. 이름 `edge/<from>→<to>`. 고아 0.
- **정책 · 기획 메모**: 화면 옆 카드, 마커 번호별 기획안 **원문 인용 + 줄**(요약 · 재작성 금지). 미정 항목(기획안 담당자 확인 필요: 변경 이력 위치 · 적용 확인 창 문구 · 담당자 목록 원천)은 빨간 테두리 `open-question`. 이름 `note/<id>`.
- 기획안 절(1~7)마다 섹션으로 묶고, CC 모바일 3화면은 가장자리 「CC 모바일(참고)」.
- 시안에 없는 화면(모달 · 토스트 · 상태 등)은 같은 컴포넌트 · 토큰으로 시안 스타일에 맞춰 짓는다. 문구는 기획안 그대로, 없으면 비운다(지어내지 않는다).

## 3. 계약

- 데이터 원본은 JSON(`screens` · `edges` · `notes`) + 새 `layout.json`(섹션 영역 · 화면 슬롯 · 메모 슬롯 좌표). 캔버스는 렌더 결과.
- 스크립트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/cc-procedure-map/sections/<절>.js`(섹션 하나 그리기) · `edges.js`(화살표, 마지막) · `run-map.sh`(백업 → 「시술현황 맵」 지우고 → 섹션 순서대로 → edges → 끝). 멱등.
- 「components」 · 「medikit」 · 「Page 1」 페이지와 변수 64개는 **읽기만.** 화면에 필요한데 세트에 없는 요소는 `custom/` 접두로 토큰만 써서 맵 안에 그리고 리포트에 목록으로.

## 4. 단계 — 쪼개서

**A. 리드 (작게, 먼저)**: 데이터 3종을 시안 · 기획안과 대조해 고친다(빠진 화면 · 엣지 · 잘못된 줄) → `layout.json` → 섹션을 서브에이전트 수만큼 나눈다(절 1~7 + 모바일).
**B. 서브에이전트(병렬 · 실행 금지)**: 각자 `sections/<절>.js` 작성. 받는 것: 이 브리프 · 자기 섹션 데이터 · layout 영역 · `_lib.js` · 컴포넌트 인벤토리 · tools.md.
**C. 리드(직렬 실행)**: 섹션 하나씩 headless 실행 → `info` 로 노드 수 확인 → 다음. 마지막 edges. `run-map.sh` 두 번 → 노드 수 같음. headless PNG(`export <파일> --page 시술현황 맵`)로 겹침 · 화살표 확인(글자 굵기 판정엔 쓰지 마라).
**린트**: `lint <파일>` 에서 color-contrast · min-text-size · touch-target-size 를 뺀 오류 · 경고 0(사용자가 이 셋은 껐다).

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` 의 「시술현황 맵」 페이지만(새로) · 백업 `medikit.before-map.fig`
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/cc-procedure-map/` (데이터 · layout · sections · 스크립트)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/pencil-map-report.md` (이것 하나)

## 6. 하지 말 것

- 기획안 · 시안에 없는 화면 · 버튼 · 문구 · 이동 발명 금지. 정책 재작성 금지.
- 앱 모드 eval · 병렬 eval · 서브에이전트의 eval 금지. 앱을 열지 마라.
- 다른 페이지 · 변수 · 컴포넌트 스크립트 수정 금지. 커밋 · push 금지.

## 7. 검증 (리포트에)

```
화면 수(56 대조표: 맵에 있음/없음) · 엣지 수(고아 0) · 메모 수(종류별, 전부 source 줄) · 인스턴스 / custom 요소 수 · run-map 두 번 노드 수 · 린트(3규칙 제외 오류 · 경고 0) · 시안과 기획안이 다른 곳과 어느 쪽을 따랐는지
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "pencil 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 \
  --text "[worker_done] pencil 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --text "[질문] pencil: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
