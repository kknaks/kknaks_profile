# [mobile] 정식 DAY 시뮬레이터 스크린샷 제작

너는 역할 문서 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/mobile/{role,rules,skills,tools,workflow}.md 를 읽는다. 작업 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1. 다른 워커가 backend/ 수정 중. 네 소유는 app/와 아래 리포트뿐이다. 앞 세션 맥락은 파일로만 읽는다.

## 1. SSOT
- 코드 AGENTS.md 및 app/README.md
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-submission-draft.md, mobile-build-report.md
- /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-003-mobile-app.md
- app/test/capture/visual_capture_test.dart 및 chat_capture_test.dart (실제 UI에 넣는 가짜 데이터 예시)
기대는 개념 없음.

## 2. 사용자 요청(이번 명시 승인)
“시뮬레이터로 다시 빌드해서 앱 이미지 찍고, 지금 다 준비하고 App Store Connect API에 등록”. 시뮬레이터 부팅·새 앱 빌드·설치·조작·촬영 승인됨. 운영 데이터 변경 금지. ASC 작업은 코디가 별도 담당한다.

## 3. 계약
정식 ID day.medisolveai, 이름 DAY. 출시 앱과 동일한 실제 Flutter UI를 촬영. 한국어. iPhone 17 Pro Max 1320x2868, iPad Pro 13-inch M5 2064x2752(시뮬레이터 실제 크기 확인). status bar 9:41, 배터리 정상. 카메라/음성 권한 문구 변경하지 않는다.

## 4. 목표
각 기기 4~5장: 시술 현황, 룸 상세, 채팅, 알림(실제 보이는 기능), 가능하면 통역(실제 UI만). 로그인·빈화면·준비중 예약탭은 제출 이미지에서 제외. 실존 직원·환자·이메일·전화번호·민감정보 금지. 이미지 합성이나 존재하지 않는 기능을 그리지 않는다.

## 5. allowed_paths
- app/store/0.1.0/screenshots/iphone/ 및 ipad/ PNG: 제출 원본
- app/store/0.1.0/README.md: 데이터·촬영 기준, 장면별 출처, 크기·버전·파일명·재현 방법
- app/tool/store_capture/ 또는 app/test/의 촬영 전용 진입점·fixture(필요할 때만)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-screenshot-report.md 리포트 1개
- 빌드 생성물 app/build/ 및 기존 무시 파일. 앱 일반 진입점/lib/·프로덕션 동작·backend/·deploy/·기존 _RESUME 수정 금지.

## 6. 실행
1. branch/status 확인, 이전 빌드 보고서 읽기. 현재 실제 UI와 capture fixtures 구조 확인.
2. 데모 API가 가짜 데이터만 주는지 확실한 경우만 사용. 로컬 simulator-login 토큰은 ~/.config/day/apple/simulator-login.local.json(비밀·계정 출력 금지). 실명 데이터이거나 인증 안 되면 우회 권한을 만들지 않는다.
3. 실제 앱 UI를 deterministic fixture로 실행하는 촬영 전용 Flutter main을 app/tool/store_capture/에 추가해 시뮬레이터 앱으로 빌드하는 방법을 우선 검토. 기존 위젯·컨트롤러·테스트 더블을 재사용하고 새 화면을 가짜로 그리지 않는다. 출시 main에는 진입점/fixture 포함 금지. 문서에 명확히 '실제 UI+가짜 fixture 데이터·촬영용 진입점'으로 기록. 서버 통합 증거로 쓰지 않는다.
4. fvm flutter build ios --simulator --debug --target=촬영진입점 (+ identity local 파일이 없으면 한시 생성후 제거) → simctl install/launch. 시뮬레이터에는 release 모드 제약이 있으니 debug 배너를 앱 화면에서 숨기고 실제 런타임 빌드 모드는 문서에 기록.
5. 조작은 orca skills get orca-emulator 가이드 먼저 읽고 orca emulator attach/ax/tap. 스크린샷은 xcrun simctl io UDID screenshot 경로. simctl CLI는 부팅/설치/launch/statusbar/촬영만. GUI 조작을 임의 스크립트로 하지 않는다.
6. 각 PNG 원본 해상도·알파·장면 확인, 미디어 정보 노출 확인. 알파 있으면 손실 없는 RGB 변환만 허용. 사진을 새로 합성·수정하지 않는다. screenshots 메타데이터 manifest에 sha256 기록.
7. 앱 동작 바꾸지 않았으므로 전체 기존 테스트 반복 금지. 새 capture harness는 analyze(관련 파일)와 simulator build로 확인. 기기별 screenshot을 이미지로 직접 확인하고 리포트 작성.

## 7. 제약
커밋·push·PR·서명·ASC 변경/업로드 금지(코디 별도). 기존 권한·통역 동의·예약탭 동작을 임의 변경하지 않는다. 사진·시드 가짜 데이터만. backend 업무 쓰기·운영 로그인·실제 고객 API 금지. 기기 기존 앱 데이터 삭제/초기화 금지. 시작시 부팅된 기기는 건드리지 않고 작업용 기기를 선택. 끝에 emulator helper kill, 사용자 원래 기기 종료 금지. 키·토큰·계정 로그/리포트 금지.

## 8. 수용
iPhone/iPad 제출 규격 실물 PNG, 장면과 재현법, 가짜 데이터 출처·release와 차이, 앱 일반 소스 변화 없음 증거. 못 만드는 장면은 이유 기록. 이미지 출력에 개인정보 없음을 확인. 모든 답 한국어.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2b709186-d9f1-4811-8538-95544d6d21b8 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
