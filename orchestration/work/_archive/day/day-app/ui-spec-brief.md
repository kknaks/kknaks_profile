# [planner] DAY 직원 앱 UI 교정 — 스펙만 반영

너는 DAY planner 워커다. 앞 맥락은 없다고 보고 이 브리프 한 장을 따른다. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/의 role.md·rules.md·skills.md·tools.md·workflow.md와 스펙 레포 AGENTS.md 및 그 문서 라우팅을 읽는다.
작업 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec, branch kknaksss/day-app-spec, 기존 SPEC PR #921 미머지. 현 HEAD78f3ee59c8a10e0abb1bde8896302873a46d0732. base origin/main. 새 브랜치/워크트리 금지.

## 1. SSOT — 먼저 읽을 것
- 위 스펙 트리 products/day/README.md, 20-spec.md, 30-work.md, 20-spec/spec-003-mobile-app.md, spec-002-procedure-board.md, 40-architecture/mobile-deployment.md.
- 사용자 확정 UI 교정 원천: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/_RESUME.md §2 사용자 지시(2026-11-10). 이전 11/09 결정과 충돌 시 최신 지시 우선.
- 같은 폴더 research-prototype-toasts.md, research-prototype-board.md.
- 프로토 read-only /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app. DAY 코드 read-only /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 및 /Users/kknaks/git/CENTURION_DAY. 옆 세션 orchestration/work/day-procedure-board-2/_RESUME.md read-only.
- 개념: 해당 없음, 사용자 확정과 현 DAY 업무 계약을 따른다.

## 2. 배경·목표
사용자가 시뮬레이터에서 원래 앱과 다른 디자인을 발견했다. 원래 디자인을 유지하고 DAY 컬러/브랜드·서버값·권한에 맞추는 것이 계약. 아래 교정은 사용자와 합의 완료. 최신 지시 「지금 백엔드/웹프론트 작업 하고 있어서 일단 스펙까지만 작성」. 스펙+리뷰까지만, WP/이슈/코드 변경 금지. 이후 승인 단계 새로 만들지 말고 현재 범위만 완결.

## 3. 확정 교정 계약
1. 하단 메뉴 예약현황/시술현황/채팅/설정 4개, 프로토 phone/tablet 구조 유지. 예약현황은 사용자 문구 「곧 출시 예정」. 채팅·설정 상세 기능은 후속, 내원현황 5번째 탭 추가 금지. 기존 호출/시술완료 인박스는 하단 메뉴와 혼동 없이 유지.
2. 각 메뉴 탭 공통 헤더: DAY 브랜드, 현재 탭 제목, 우측 종 아이콘+실제 미읽음 수 배지. 계정/로그아웃은 설정으로 이동. 알림 상세 API/목록 계약이 없으면 없음을 별도 의존으로 명시하되 가짜 고정 배지/API 경로/새 백엔드 구현을 발명하지 않는다. 설정 이동은 계정 기능을 보존하고 설정의 다른 신규 상세를 만들지 않는다.
3. 목록 필터 4개 전체/확인 필요/시작 가능/시술 대기 유지, 서버 inbox.section만 사용. 프로토 8개로 바꾸지 않음.
4. 카드: 1행 방(좌)/수납 필요(우·서버조건), 2행 고객명/한글발음, 3행 나이|국적|현재 서버제공 기타정보, 4행 상태박스 「시술 대기 / 담당의 미정」. 확정한 4행 구조에 임의 0/2 줄 추가 금지. 데이터없는 칸 발명 금지.
5. 마취중 한 줄(상태/시작시각/기준/경과), 연보라·20분 초과 빨강. 기존 anesthesia.long/서버 임계값 계약 소비, 앱 업무재계산 금지. 마취완료는 「시술 대기 - 마취 완료 {N}분 / 담당의 미정(또는 실제 담당의)」. 서버 시간 표시재료가 부족하면 기존 필드 기준 부족을 표시하고 필드/API 추가를 발명하지 않는다.
6. 호출 후 목록카드에도 호출 대상/수락대기, 호출시술명, 경과시간, 건수와 수락버튼. 상세로 들어가지 않아도 수락. 상세 호출 강조박스도 원본처럼 대상/호출시각/건수/기준/큰 경과시간/큰 수락버튼.
7. 개인 로그인 직무 분기: 원장 「수락 · N건」→로그인 staff.id 본인 즉시수락, 원장선택창 없음. 간호사 「원장 골라 수락 · N건」→원장선택 드로어→대리수락. 목록/상세/호출탭 공통. board.accept/can* 기존 서버권한 유지. 관리자 등 기존 다른 허용직무 권한 축소/새정책 발명 금지.
8. 상세 헤더 「< 시술현황     {방}」. 오더 메모 상단 과다여백 축소. 시술 줄은 프로토 카드형(시술/담당의/상태/시작). 진행중 연한 DAY 배경·테두리·시간강조, 완료 아래 회색톤. 종료/시작 버튼 DAY색 일관. 더보기 세로 ⋮, 기존 canUndoStart/Finish에 따른 「시작 취소」「완료 취소」 확인없이 바로, KOS는 서버 세션몫.
9. 상세에서 상시 체크박스·전체선택 없애고 [의사 호출]→시트 안 시술 체크/전체선택+대상원장선택→호출. 이게 2단계(상세→시트)이며 임의 Next 마법사 두장 금지. pickable/canCall 그대로. 재호출 노출조건 기존 A22 유지.
10. 전부완료 후 강조박스 「시술 모두 완료」/「마지막 종료 {시각}」/[귀가 대기], 헤더 「시술 모두 완료 · 귀가 대기 전」. canHome/카드이탈·doneTab 등 DAY 서버계약은 유지. 상태 헤더의 UI글자와 서버 업무상태를 혼동하지 않음.
11. 통역 드로어 원형복원: 핸들, 통역·선택언어 드롭다운/방·경과/종료, 중앙자막, 하단 둥근 빠른말하기 칩/큰 원형마이크/듣기·멈춤 안내. 하단 4메뉴. 빠른말하기 스피커아이콘·라운드·가로스크롤+통역하기 버튼. 기존 문구·번역만.
12. 고객 언어 자동매핑: TW 초기 중국어(번체) zh-Hant 확정. 빠른말하기/WS언어 동일, 이전 고객/전역 마지막언어가 TW를 en으로 덮지 않음. 수동변경 가능. 다른 국적은 원천의 7언어 대응/확정범위만 근거와 함께 적고 미확정은 남김, 번역발명 금지. TW 결정을 OQ-A9 미정에 묻지 말 것. vi/yue 빠른문구 없음은 유지. zh-Hant 화면라벨 사용자확정 「중국어(번체)」를 적용하고 기존 대만어 글자와 중복모순 정리.
13. 토스트: 성공 토스트는 프로토 원문(조사보고서 §4)으로 원래 어두운 둥근 상단 토스트·일반2.6초·새 메시지 덮어쓰기. **토스트 안 되돌리기 버튼 추가 안함**(최신 브리핑에 사용자 「응」). 취소는 DAY 더보기 방식 유지. 오류는 DAY 코드 문구 우선, 세션/중복탭/오래된응답 격리 보존. SSE로 남의 모든 상태변경을 임의로 성공토스트 하지말고 본인 조작성공 기준을 명시.

## 4. 정합 대상
SPEC 본문/U계약/시나리오/프로토와차이표/인수조건/OQ/화면목록/범위제외를 함께 고쳐 모순0. 사용자변경 출처날짜와 기존계약 대체를 기록. 전체 기존 1차 기능을 임의 축소하지 않음. 스펙 stable 메타는 규약에 따라 유지하되 코드 미반영·리뷰기준선 달라짐 명시. 승인/머지됐다고 쓰지 않음.

## 5. allowed_paths
products/day/20-spec/spec-003-mobile-app.md, products/day/20-spec.md의 SPEC003 설명/날짜/버전 등 정합 최소행만. 그 밖은 수정금지. 특히 30-work.md 및 Delivery Issue #235·로컬WP·SPEC002·SPEC001·배포문서·옆세션·코드·백엔드 수정금지. 필요한 타문서 후속은 보고서에만. 보고서 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/planner-ui-spec-report.md 한개.

## 6. 순서
읽기→SPEC교정→본문/인수조건/OQ 정합→lint→보고. git diff --check와 lint --strict를 수행, products/day ERROR0. 새 SPEC ID/문서생성 안함.

## 7. 하지말것
하위워커/내부서브에이전트 금지. 커밋/push/PR/merge/서버/시뮬레이터/코드변경 금지. WP는 아직 갱신하지 않음. 문구/번역/신규API 발명금지. 다른 세션작업은 read-only. 미해결 서버의존은 UI와 구분해 보존.

## 8. 완료
변경파일/확정사항반영표/남은의존과OQ/검증명령과수치/기존계약보존을 한국어로 보고. live preamble ID/핸들/outcome이 아래 예시보다 우선. reviewer_doc가 다음에 독립검수함.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
