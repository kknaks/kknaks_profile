# 재개점 — 2026-11-12 확인 · 사용자 지시로 대기

**현재: 대기.** 사용자 마지막 지시 = 실제 환경과 데모 환경 로그인을 모두 확인해야 하니 일단 대기. 상태 확인/기록만 했고 배포·테스트를 재개하지 않았다.

## 완료(2026-11-11 확인 결과)

- 정식 DAY `day.medisolveai` / `0.1.0 (1)` 바이너리 ASC 업로드·VALID·버전 연결 완료. 스토어 공개 상태가 아님.
- iPhone5+iPad5 스크린샷10장 COMPLETE. App Store/TestFlight 한국어 설명283자·연락처·테스트 안내 반영.
- 정책/지원 문안은 mediness `products/day/60-release/app-store-preparation.md`에 작성·검수 보완. 원천과 API 반영 결과는 `mobile-paperwork-registration.md`.
- TestFlight 테스터 배포·App Store 심사 제출·공개 출시·Unlisted 신청은 미실행. 데모 자격은 사용자 직접 입력하도록 빈칸 유지.

## 사용자가 재개를 지시하면 먼저 할 것

1. 현재 prod/dev 서버 배포·헬스·앱 등록 상태를 다시 확인(이전 기록의 502 등을 현재 상태로 단정하지 않음).
2. 사용자 준비 관리자 계정으로 **정식 앱 → 실제 환경(prod)** 로그인·병원/권한 확인.
3. 사용자 준비 데모 계정으로 **같은 정식 앱 → 데모 환경(dev)** 로그인 넘김 확인. environment/api_base_url/세션이 기대한 환경에 묶이는지 확인.
4. 두 로그인 결과를 각각 기록한 뒤 조회·상태 변경·채팅·첨부·푸시·통역 테스트로 이어감. 업무 쓰기는 지정 테스트 대상·사용자 승인 범위에서만.
5. 앱 코드가 바뀌지 않았다면 기존 정식 빌드(1)을 사용. 새 앱 변경이 있으면 빌드2 이상으로 재빌드·업로드 여부 판단.

## 남은 일·결과 문서

- 사용자: 관리자 계정 준비, 심사 데모 자격 직접 입력.
- 서버/페이지: prod 배포 및 `/privacy`·`/support` 공개 접근, 정책 문안과 실제 보관·파기·로그·백업 설정 대조.
- 심사 전: 앱 내부 개인정보 링크·예약 placeholder·App Privacy/연령/가격·지역/저작권 등 기존 미완 항목.
- 결과 요약: `mobile-paperwork-registration.md`(최신 서류/연락처), `mobile-registration-report.md`(최초 등록), `mobile-prod-upload-report.md`, `mobile-asc-report.md`, `mobile-screenshot-report.md`.
- 개인 심사 연락처·키·계정 자격은 이 문서에 복사하지 않음. 활성 발주 없음.

---

아래는 당시 진행 기록이다. 재개 기준은 위 최신 상태와 결과 문서다.

# 최신 상태 — 2026-11-11 서류 준비 종료

mobile-paperwork-registration.md가 이번 후속 작업 결과 요약이다. 연락처·최종 설명·심사 메모A·TestFlight 안내 반영/GET 확인, 데모자격 빈칸 유지. 권장 개인정보/지원 문안 작성·검수 보완 완료. 모든 발주 결과 수신·검증·release 요청 완료, 활성 발주 없음.

내일 2026-11-12 사용자 관리자계정 생성 후 prod TestFlight 실기기 확인. 기존 정식0.1.0(1) VALID·버전연결·이미지10 COMPLETE 유지. 오늘 후속 작업에서 추가빌드·업로드·테스터배포·심사제출 없음. 페이지 공개·서버 기술설정 대조와 App Store 심사 전 남은 항목은 결과 보고서에 유지. 개인 심사연락처를 공개 문서에 복사하지 않는다.

---

# 현재: 서류·심사 연락처·TestFlight 안내 준비 완료

최신 결과: mobile-paperwork-registration.md. 제품설명은 기존 EMR 조회/상태변경 + 직원채팅으로 283자/85ed67f7, App Store/TestFlight 양쪽 반영·GET 확인. App Review/Beta Review 연락처·블록A notes, TestFlight 피드백메일·한국어 테스트안내 반영. 데모자격은 사용자직접입력(빈칸 유지). 개인정보/지원 문안은 권장안으로 작성·검수 보완 완료, 공개 전 기술사실 대조와 페이지 배포는 남음.

내일 2026-11-12 사용자 관리자계정 생성 후 prod TestFlight 실기기 확인. 이번 후속 작업의 추가업로드/테스터배포/심사제출0. 기존 정식0.1.0(1) VALID·연결 및 이미지10 COMPLETE 유지. 활성 발주 종료 정리 중.

---

# 현재: 내일 prod TestFlight 테스트를 위한 서류 마감 중

사용자 2026-11-11: 지원·심사 연락처 제공, 데모 계정은 사용자 직접 입력, 운영주체/보관삭제 기준은 권장안대로 서류 준비. 내일(2026-11-12) 관리자 계정 생성 후 prod TestFlight 테스트 예정. 오늘 추가 빌드/업로드/테스터 배포/심사제출/출시 없음.

제품정체성 확정: 기존 병원 EMR을 조회하고 상태변경하는 직원용 앱, 신규 업무 콘텐츠는 채팅·첨부. EMR 원본·DAY 동기사본·채팅·기술정보를 구분.

- 심사 연락처는 ~/.config/day/apple/store-contact.local.json(600)에 보관, App Review와 Beta Review에 API 반영·GET 확인. 공개 레포/페이지에 개인심사 연락처 복사 금지. 공개 지원메일만 문안에 사용.
- 데모 계정/암호 빈칸 유지, 사용자 입력 대기.
- TestFlight ko 앱 설명·피드백메일·build(1) 한국어테스트안내 API 반영·GET 확인. 테스터/그룹 변경 없음.
- 서류 worker task_f661ffb9876c / ctx_8193eda517d3 / term_8dce4f8c-3493-4d48-ad43-c71f41a9d03d. source products/day/60-release/app-store-preparation.md + mobile-paperwork-report.md + mobile-description-final.txt.

---

# 현재: 정식 DAY App Store Connect 등록 완료(심사 제출 전)

최종 정본 요약: mobile-registration-report.md. 0.1.0(1) VALID·버전 연결 완료, screenshot10 COMPLETE, ko metadata·URL 등록·GET 확인. MANUAL, PREPARE_FOR_SUBMISSION. 심사 제출·출시·Unlisted 신청은 안 함. 정책 페이지/연락처/설문/서버 실물 등 미완 항목은 최종 보고에 명시. 활성 발주 없음. 앱/정책 문서 새 파일은 회사 워크트리에 미커밋으로 보존.

---

# 현재 실행 — 시뮬레이터 촬영 및 ASC 등록(사용자 추가 승인)

사용자 최신 지시: 시뮬레이터에서 재빌드·스크린샷 촬영하고 지금 준비해 App Store Connect API 등록까지 수행. 앞의 준비전용/업로드대기 제한은 이번 지시 범위에서 해제. 실제 심사 제출·공개 출시는 아직 실행하지 않는다.

- ASC 정식 DAY record 기존 존재: 6833456680 / day.medisolveai(정확 비교). 한국어 설명·부제·keywords, BUSINESS, 편집버전 0.1.0 및 MANUAL 반영·GET 확인 완료.
- 스크린샷 제작 완료(10장 RGB·원본 해상도·코디 직접 시각 검토·SHA allowlist 승인): task_fc81ec4b8332 / ctx_a53fc1ae0412 / term_cae7a641-7ee7-45cb-88a8-f194b5ce6f27. 실제 UI+가짜 fixture를 촬영용 별도 진입점으로 시뮬레이터 실행. 출시 main 변경 금지. 이미지 app/store/0.1.0/screenshots/.
- ASC 등록: task_45cdbd3fffa8 / ctx_68a31f8e637e / term_8c96f2f3-b712-4d47-8e88-68ab9614b819. 메타데이터 등록 끝, 이미지 시각 검토 뒤 업로드 대기. 클라이언트 ~/.config/day/apple/asc_day.py, asc_upload_shots.py(600). URL 두 개 draft 등록·GET 확인. 이미지10장 API COMPLETE·원본MD5일치·01→05순서, 코디 GET독립확인 완료.
- 정책·자료 원천 초안 완료(현재 미정값으로 공개 발행 불가): task_912affdd5189 / ctx_a09b104b415a / term_8dce4f8c-3493-4d48-ad43-c71f41a9d03d. mediness products/day/60-release/app-store-preparation.md 신규 1개만 작성 중.
- 링크 확정(서버 코디 답): https://day.medisolveai.com/privacy · /support. prod 자체 미배포라 현재 502. 페이지 본문·연락처 확정 뒤 서버 코디가 공개 GET 라우트 생성·배포 소유.
- 정식 binary task: task_90f478bfdf6c / ctx_69fa2de41ed4 / term_cae7a641-7ee7-45cb-88a8-f194b5ce6f27. 0.1.0(1) 정식IPA 생성·validate/upload 성공. Apple 처리 및 version 연결 대기. Generated target lib/main.dart, IPA fixture문자열0, profile aps production·prod appid 일치·get-task-allow false 코디확인.
- 지원 이메일·심사 연락처 사용자 질문 대기. placeholder나 가짜 연락처 등록 금지.
- 앞의 음성 개인정보 포함 단정 및 무조건 별도 동의 필요 판정은 사용자 지적에 따라 정정. 단순 통역 기능으로 사실 기술, 실제 개인정보 공유가 있을 때 Apple 조건 확인. 팝업 임의 추가 안 함. 기존 마이크/갤러리 한국어 문구 유지.

---

# DAY 정식 앱 준비 — 앱 세션 상태

2026-11-11 · 서버/웹 코디의 `_RESUME.md`와 별도 기록.

- 요청: 정식 DAY 앱의 prod 기준 App Store 준비. 업로드·심사 제출은 결과 보고 뒤 사용자 판단.
- 범위: 같은 코드 워크트리의 app/만. backend/ · deploy/ · 환경 설정 · 기존 `_RESUME.md` 무수정. 커밋·push·PR 미실행.
- 사용자 확인: 개인정보처리방침 URL·지원 URL 둘 다 미정.
- 정식 앱 record 생성·서명 방법 M-16·설치 기기 M-1은 사용자 판단. M-20은 서버 코디 몫.
- 입력 초안: `mobile-submission-draft.md`.
- 빌드 검증: `mobile-build-brief.md` → `mobile-build-report.md`(워커 작성).
- Run `run_2e6d9d6eeb00`, task `task_449ec6695e0b`, dispatch `ctx_2c5633ca3d10`, 워커 `term_cae7a641-7ee7-45cb-88a8-f194b5ce6f27`.
- 코디 `term_2b709186-d9f1-4811-8538-95544d6d21b8`. 서버/웹 작업은 다른 코디가 계속 소유한다.

빌드 검증 완료: analyze 0 issues · 테스트 343 passed/73 capture skip/0 failed · 서명 없는 prod release 성공(70초 · 20.7MB). Bundle ID day.medisolveai, 이름 DAY, 0.1.0 (1). 앱 소스 변화 0.

빌드 산출물: /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1/app/build/ios/iphoneos/Runner.app. 배포 서명·IPA·업로드 없음.

독립 검수: task task_e41679088c56 / dispatch ctx_8c90bd5b2bdd / worker term_8c96f2f3-b712-4d47-8e88-68ab9614b819 → mobile-review-report.md.

우선 보완: 앱 내 개인정보 링크, 통역 음성 제3자 전달 고지·허가, 예약 탭 ‘곧 출시 예정’ 처리. 그 뒤 정식 record·서명·실기기·스크린샷·App Privacy 확정.

코디 검증: 산출물 Info.plist·아이콘·iPhone/iPad family·privacy manifests 7개를 직접 확인했고 app/ diff 빈 결과 확인. 빌드 리포트의 Unlisted 신청 시점·ASC record 존재 미조회·공급자 보관 미확인 문구는 코디가 정정했다.

독립 검수 완료: WARN(FAIL 0 · WARN 8). 빌드 사실은 산출물과 일치. 문서 표현·분류 경고는 코디가 후속 반영했고 미확인 항목은 유지. 준비 점검과 초안 작성 완료, 정식 제출 미준비. URL·앱 내 정책 링크·외부 음성 전달 고지 및 허가·실기기 통합이 미확인인 상태를 제출 가능으로 표시하지 않는다.

모든 발주 결과 수신·검증 완료. 빌드 워커와 리뷰 워커에 release 요청(external terminal은 retained/no process action 반환). 새 발주 없음.
