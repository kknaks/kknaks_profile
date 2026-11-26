# [researcher] 앱 시술현황 차트 — 웹 차트와 같은 기능으로 올리기 위한 현황 조사

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app` (코디 워크트리 — 리포트 1개 말고는 아무것도 쓰지 마라)

**read-only 조사다.** 코드 · 스펙 레포는 전부 읽기만 한다.

## 1. SSOT — 먼저 읽을 것

코드 = `MediSolveAIDev/CENTURION_DAY` **`origin/dev` = `55e60aa4`** 기준.
canonical `/Users/kknaks/git/CENTURION_DAY` 는 사용자 체크아웃이라 **checkout · pull 금지**. 읽기는 `git -C /Users/kknaks/git/CENTURION_DAY show 55e60aa4:<path>` · `git grep … 55e60aa4` 로만.

스펙 = `MediSolveAIDev/mediness` `origin/main`, canonical `/Users/kknaks/git/harness_works/mediness-mediness`(같은 규칙 — `git show origin/main:<path>`).

- `products/day/20-spec/spec-002-procedure-board.md` — 시술 현황 · 차트(웹) 계약
- `products/day/20-spec/spec-003-mobile-app.md` — 앱 계약
- `products/day/20-spec/spec-000-data-model.md` — `visit_photo` 등
- 웹 차트 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/_archive/day/day-chart-photo/` (`_RESUME.md` · `SUMMARY.md`) 와 그 안에서 가리키는 `reference/2026-11-24-day-picture/chart-photo-decisions.md`(C1 ~ C36 — profile 레포 main 에 있으면 그것)
- 사용자 스크린샷(현재 앱 차트): `/Users/kknaks/.config/day/reference/app-chart-2026-11-25.png` — **공개 레포에 복사 금지**

기대는 개념: 해당 없음(조사).

## 2. 배경 / 무엇을 바꾸나

직원 앱 시술현황에서 시술을 누르면 차트 시트가 뜨는데 **읽기만 되고 디자인이 이상하다.** 사용자가 짚은 것:

- 탭(간호 관리 차트 · 의사 차트) 아래 **까만 가로줄**
- (코디 관찰) 시트가 **하단 탭바 밑에 깔려** 마지막 칸이 잘린다

웹 차트는 11-24 day-chart-photo 로 끝났다 — 탭 3(간호관리 · 의사 · 시술전후사진) · 탭별 명시적 저장(저장 전 KOS 확인 · 다르면 전부 거절 · KOS 글 + 내 글 이어 붙임) · 사진 여러 장(DAY 저장소 `beforeAfter/` + `visit_photo` + KOS 등록) · 사진 탭 열린 동안 10초 KOS 가져오기.

목표: **앱 차트를 웹과 같은 기능으로.** 이 조사는 스펙 · WP 를 쓰기 전 「무엇이 있고 무엇이 빠졌나」를 세는 것이다. 뒤에 예약 탭(WORK-002)이 이 차트의 사진 흐름을 다시 쓸 예정이니, 사진 업로드 경로는 예약 탭에서도 부를 수 있는지 관점으로도 본다.

## 3. 계약

해당 없음(조사).

## 4. 먼저 읽을 핵심 파일 (55e60aa4)

- `app/lib/ui/chart_sheet.dart` — 지금 앱 차트
- `app/lib/ui/board_screen.dart` · `app/lib/ui/shell.dart` · `app/lib/ui/theme.dart` — 여는 흐름 · 시트가 어디에 붙나 · 앱 DS
- `app/lib/data/` · `app/lib/model/board.dart` · `app/lib/state/board_controller.dart` — 앱이 부르는 API
- 웹/백: `backend/day/services/board_charts.py` · `board_chart_writes.py` · `backend/day/policies/board_chart_rules.py` · `board_chart_tabs.py` · `backend/day/dtos/board_charts.py` · `backend/day/presentation/board_chart_reads.py` · `backend/day/templates/partials/board_chart*.html` · 관련 static js · 사진 업로드 라우터
- `.agents/skills/verify-day-chart/` — 차트 저장 규칙 명세(있는 그대로 참고)

**위 목록은 출발점이다.** 차트 · 사진 · 저장에 닿는 곳은 `git grep` 으로 **전부** 세라(라우터 · api/ · 앱 쪽 호출 · 인증 방식 — 앱 토큰으로 웹 차트 API 를 부를 수 있나).

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-1-report.md`

## 6. 조사 단계

1. **앱 현재 상태**: 차트 시트를 어떻게 여나 · 무엇을 보여 주나 · 어떤 API 를 부르나 · 편집 가능한 곳이 있나. 까만 줄의 원인(위젯 · 줄) · 시트가 탭바 밑에 깔리는 원인(어느 Navigator/Scaffold 에 띄우나).
2. **웹 차트 기능 전수표**: 기능 하나당 행 — 탭 · 칸 구성 · 저장 단위 · KOS 확인/거절 · 이어 붙이기 · 사진 업로드/여러 장/삭제/보기 · 10초 가져오기 · 권한(직군) · 오류 문구. 각 행에 「웹 코드 위치 · 백엔드 API(메서드 · 경로 · 인증) · 앱에 지금 있나(있음/일부/없음)」.
3. **API 재사용성**: 앱이 웹 차트 API 를 그대로 부를 수 있나(세션 쿠키 vs 앱 토큰 · HTML partial 응답 vs JSON). 앱 전용 JSON API 가 따로 있나. 없으면 무엇이 빠졌나(목록만 — 설계하지 마라).
4. **앱 네이티브 · 패키지**: 카메라 · 앨범 · 파일 선택 · 이미지 업로드에 쓸 수 있는 것이 이미 있나(채팅 첨부 `chat_attach_sheet.dart` 등 재사용 후보) · iOS Info.plist / Android 권한 상태.
5. **스펙 대조**: SPEC-002 · SPEC-003 에 앱 차트가 어떻게 적혀 있나(읽기 전용이라고 정했나 등) — 바꾸려면 어느 절을 고쳐야 하나.
6. **정할 것 목록**: 사용자가 정해야 할 질문만 모은다(추천이 있으면 한 줄 추천 + 근거). 예: 사진 탭을 앱에도 둘지 · 저장 버튼 위치 · 시트 vs 전체 화면.

## 7. 범위 제약 — 하지 말 것

- 코드 · 스펙 · 디자인 수정 금지. 설계안 · WP 쓰지 마라 — 사실과 질문만
- 예약 탭 · 여권 스캐너 · 문진 QR 조사 금지(다음 단계)
- 앱을 빌드 · 실행하지 마라 · 사용자 포트/프로세스 건드리지 마라
- 서버 · DB 접속 금지

## 8. 검증

```
질문마다 답 + 근거(파일:줄 @55e60aa4 · git ref · 문서 경로). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 리포트 맨 위에 한 화면짜리 요약(앱에 있음 · 빠짐 · 백엔드 추가 필요 여부 · 정할 것 수).

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
