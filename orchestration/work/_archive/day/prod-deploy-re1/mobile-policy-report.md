# mobile-policy 결과 보고 — App Store 자료 · 스크린샷 기준 · /privacy · /support 문안 초안

## 상태: done (초안 · 공개 페이지는 아직 발행 불가)

## 수행 내용
- 새 문서 1개: mediness `products/day/60-release/app-store-preparation.md` (frontmatter `type: release` · `status: draft` · `sources:` 3개). 레포에 `60-release/` 선례는 없음(다른 제품에 `50-qa/` 1건만) — 브리프가 지정한 경로라 그대로 썼다. 다른 위치를 원하면 `git mv` 1회로 옮기면 된다.
- 문서 구성: §1 원천/산출물 경로 · 버전 묶음(0.1.0 (1) · 다음 build number 는 ASC 조회 후) / §2 iPhone 6.9"(1320×2868) · iPad 13"(2064×2752) 실제 시뮬레이터 캡처 기준 · 장면 5개 · 파일 이름 · manifest(hash · 버전 · commit) · 승인된 이미지만 업로드 / §3 fixture 허용 범위(출시 main 삽입 금지 · 더블 캡처 ≠ 서버 통합 증거 · 프리뷰/미출시 기능 광고 안 함) / §4 권한 문구 3개 원문(Info.plist:52-59 · 변경 없음) / §5 부제 · 키워드 · 설명 · 심사 메모 · Unlisted 사유 · 통역 5.1.2(i) 조건부 메모 / §6 /privacy · /support 공개 본문 초안 + 문장별 근거 표 / §7 확정할 값 17행(담당 사용자 · 서버 코디 · 앱 코디).

## 앞 분석에서 정정한 것
- "통역 음성에 개인정보가 포함된다"는 단정과 "동의 팝업 필수"를 뺐다. 통역 = 단순 실시간 통역(앱 → DAY 서버 → Soniox STT·번역·TTS)으로 설명했고, 5.1.2(i)은 개인정보 공유가 실제로 있을 때 확인할 조건으로만 적었다.
- "DAY 서버는 통역을 기록하지 않는다"(SPEC-003:660 · session.py:11)와 "Soniox 보관·학습은 공급자 정책·계약에 따름(미확인)"을 따로 적었다. 무보관 · 무학습 · 즉시 파기 · 안전 보장 문장은 쓰지 않았다.

## 검증
- 문안 근거를 파일:줄로 대조했다(§6-1 근거 표 · §6-2 근거 줄). Info.plist 3개 문구는 원문 그대로 옮겼다. 광고·분석 SDK 없음 = `pubspec.lock` firebase/sentry/crashlytics/analytics/amplitude/mixpanel 0건(재확인).
- `python3 scripts/lint-pipeline.py --strict` → **0 error**(전체 263 warning은 기존 · 새 문서 관련 0건).
- 기존 문서는 바꾸지 않았다. `git status` 에 보이는 `spec-002-procedure-board.md` · `log.md` 변경은 작업 시작 전부터 있던 다른 planner의 변경이다. 새 파일은 `?? products/day/60-release/` 하나뿐이다. 코드 레포 · 커밋 · push · PR · issue/Delivery 변경은 하지 않았다.
- Apple 링크는 공식 3개만 인용했다(screenshot-specifications · unlisted-app-distribution · review guidelines 5.1.2). 이번에 웹에서 다시 확인하지는 않았으므로, 규격은 촬영 직전 ASC와 대조하라고 문서에 적었다.

## 확정 / 미정
- 확정: URL 경로 `/privacy` · `/support`(서버 코디 소유), Unlisted, 이름·Bundle ID, 버전 0.1.0 (1), 권한 문구 3개, 통역·채팅·푸시·Keychain 처리 흐름(코드·SPEC 근거).
- 미정(§7): prod 배포(현재 502), 운영 주체, 지원 연락 방법, 개인정보 보호책임자, 보관 기간·파기(채팅은 DAY-ESC-001), 위탁·국외 이전, Soniox 보관·학습, 5.1.2(i) 해당 여부, 앱 안 개인정보 링크(현재 없음 · 5.1.1(i)), 예약현황 「곧 출시 예정」 처리, 시행일·법무 검토, ASC 남은 칸(URL 2개·연령·가격·지역·저작권·App Privacy·심사 정보), 서명(M-16)·build number, prod 데모 연결(D-1), 스크린샷(진행 중 — 아래 정합 수정), 설치 기기(M-1).

## 공개 페이지를 바로 발행할 수 있는가
- **아니다.** `/support` 는 라우트 배포(#1)와 연락 방법(#3)이 필요하다. `/privacy` 는 그 밖에 운영 주체 · 책임자 · 보관/파기 · 위탁 · Soniox 확인 · 시행일(#2·4·5·6·7·11)이 채워져야 한다. 502 상태라 ASC 제출 자료로도 아직 완료가 아니다.

## 미결·주의점
- `60-release/` 는 새 최상위 stage 디렉토리다(브리프 지정). 레포 규칙에 이 stage 정의가 없으니 코디네이터가 PR 때 위치를 확정할 것.
- 스크린샷 장면에서 예약현황 탭 본문은 뺐다. 다만 하단 메뉴 이름은 실제 UI라 그대로 보인다. #10 결정 뒤 장면을 다시 확인할 것.

## 2차 — 현재 상태 정합 수정 (task_6f5f394d60b0 · 2026-11-11)

수정 파일: `products/day/60-release/app-store-preparation.md` · 이 리포트. 그 밖 파일 변경 0.

- **ASC record**: "미확인"을 "있음"으로 고쳤다. bundle `day.medisolveai` 정확 일치, 편집 버전 `1.0`→`0.1.0` 재사용, `MANUAL`, ko 설명·키워드·부제, `BUSINESS` 등록·GET 확인(정본 `mobile-asc-report.md`). §1-2 · §5-1 · §7 #12 · #14 반영. URL 2개·심사 정보·연령 등 남은 칸은 미입력으로 표시.
- **설명 문안 차이**: ASC 등록본은 이전 제출 초안 본문(207자)이다. 문서 §5-2 후보 문안과 다르다는 점과, 바꿀지는 사용자 판단이라는 점을 적었다(등록본이 현재 값).
- **스크린샷**: "폴더 없음 · 미작성"을 "진행 중"으로 고쳤다. `app/store/0.1.0/screenshots/iphone/` 에 01-board·02-room·03-chat·04-notifications·05-interpret(1320×2868) 생성 중, ipad 비어 있음, manifest·승인·업로드 전(ASC 세트 0). 촬영 진입점 `app/tool/store_capture/main.dart`(lib 밖·가짜 back·서버 통합 증거 아님)를 §2·§3에 넣었고, 파일 이름 규칙을 실제(`screenshots/{iphone|ipad}/NN-장면.png`)에 맞췄다. 완료로 적지 않았다.
- **확인 필요(새 정책 아님)**: 지금 PNG 5장이 모두 RGBA(알파 채널)다 — Apple 규격(알파 없음)에 맞추려면 업로드 전 변환이 필요하다. 촬영 빌드가 별도 target debug 빌드라 디버그 표시 유무를 승인 때 보도록 적었다. `app/store/` · `app/tool/store_capture/` 는 CENTURION_DAY 작업 트리에 untracked 상태다.
- **60-release 경로 결론: 유지.** AGENTS.md(디렉터리 역할 표)·rules/document-pipeline.md(권장 폴더 구조)·archive/README.md(사용하지 않는 경로)·lint 어디에도 금지 규정이 없다. 표준 목록 밖 번호 경로 선례도 있다(`05-roadmap.md`·`25-ui-rules.md`·`31-issue.md`·`50-qa/`). lint `--strict` 0 error(새 문서 관련 경고 0). 다만 권장 구조 표에 `60-release/` 가 정의돼 있지는 않으니, 규칙에 올릴지는 코디/사용자 판단.
- 새 정책·개인정보 공유 단정·동의 팝업 요구는 추가하지 않았다. 커밋·push·PR 없음.

## 3차 — 실행 현황 · 설명 원천 · Soniox 공개 정책 반영 (task_b03a9e87179c · 2026-11-11)

수정 파일: `products/day/60-release/app-store-preparation.md` · 이 리포트. 그 밖 파일 · 코드 · ASC 원격 변경 0.

1. **실행 현황**: §1-3 표 한 곳에 요약하고 정본 보고서(`mobile-asc-report.md` · `mobile-screenshot-report.md`)를 가리키게 했다. ASC record · 0.1.0 MANUAL · ko 메타데이터 · BUSINESS · URL 2개 등록(페이지는 502 — 등록 ≠ 동작), 스크린샷 iPhone 1320×2868×5 · iPad 2064×2752×5 · RGB · manifest · 코디 시각 승인 · SHA allowlist · 10장 COMPLETE. 바이너리(서명 · 업로드 · 빌드 연결)는 **진행 중**으로 적었다. 출시 main = `lib/main.dart`, 촬영 = `tool/store_capture/main.dart`. 다른 절의 중복 상태 문구는 §1-3 참조로 줄였고, §2-4 기록 방식 · §3 fixture 위치를 실제(manifest.sha256.txt · README · test/support)에 맞췄다. §7 #13 진행 중 · #16 끝남.
2. **§5-2 설명**: 후보 문안을 지우고 ASC 등록본을 그대로 넣었다(207자 · sha256 앞 8자 `0af2b167` — 블록을 다시 계산해 보고서 GET 값과 일치). 사용자에게 새 선택을 묻지 않는다. 원격 변경 없음.
3. **Soniox**: 공식 Privacy Policy(Last updated 2026-06-29) §1 · §4 · §5와 Security and privacy 문서를 직접 확인했다. 실시간 API는 일시 처리 · 미저장(§5), Customer Content 학습 · 평가 · 개선 미사용(§4 · TTS 입력/생성 음성 포함), 콘텐츠 없는 운영 메타데이터 · 사용량 · 보안 · 청구 기록은 별도 보관(기간 미명시), 서명 계약 우선(§1). 이걸 DAY 코드(실시간 STT/TTS WS만 · `soniox.py:26-27` · Async 호출 grep 0)와 대조해 §5-5 · `/privacy` 5항 · 근거 표에 반영했다. 개별 계약 · DPA · Console 설정은 **미확인**으로 남겼다(§7 #7 문구를 "실물 미확인"에서 "공개 정책 확인 · 개별 설정 미확인"으로 고침). 일시 처리 문장이 TTS를 따로 이름 짓지 않는다는 점도 적었다. 개인정보 포함 단정 · 동의 팝업 필수 · "실시간 전송 = 항상 수집" 단정은 넣지 않았다. 계정 · 푸시 · 채팅 서버 저장 항목은 그대로 두었다.

검증: lint `--strict` 0 error(60-release 관련 0건). 미정 그대로 — 운영 주체 · 지원 연락처 · 책임자 · 서버 보관/파기 · 위탁 · 시행일(사용자 미응답). **공개 페이지는 여전히 바로 발행할 수 없다**(라우트 502 · 위 값 미정).
