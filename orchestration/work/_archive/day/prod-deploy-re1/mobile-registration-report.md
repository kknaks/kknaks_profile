# DAY 정식 앱 ASC 등록 결과 — 2026-11-11

## 완료한 등록

- 정식 record DAY / day.medisolveai / ASC 6833456680. DAY Dev 변경 없음.
- iOS 0.1.0 편집 버전(기존 1.0을 수정해 재사용), MANUAL. 한국어 설명 207자·부제·키워드·BUSINESS 반영.
- 개인정보 URL https://day.medisolveai.com/privacy, 지원 URL https://day.medisolveai.com/support를 draft에 저장. 현재 페이지는 502이고 서버 코디가 배포 소유.
- iPhone 1320×2868 5장 / iPad 2064×2752 5장, 실제 simulator screenshot. 실제 DayApp UI + 가짜 fixture, 출시 main과 별도. RGB·알파 없음·원본 규격·SHA allowlist·코디10장 직접시각검토.
- API 업로드 10/10 COMPLETE, 원본 MD5 일치, 세트별 01→05 순서. 코디가 독립 GET으로 동일 결과 확인.
- 정식 배포 IPA 0.1.0(1) 생성·validate/upload 성공. Apple 처리 VALID, 암호화 면제 false, expired false.
- 빌드 9c4cd151-eee6-4f50-bcdf-7207d38a50ba가 0.1.0 버전 e0ae563c-4586-41a3-899e-f4fc1b89deea에 연결됨. 코디 최종 API GET으로 확인. 앱 상태 PREPARE_FOR_SUBMISSION.
- 실제 서명 IPA target lib/main.dart 확인. fixture/촬영 target 문자열 혼입 없음. 프로파일 aps production, prod 앱 일치, get-task-allow false. IPA sha256 dc96e1f74779e686311b3606fc4c3ed28533d93448babfb7539e47f203ca75d1.
- 심사 제출·출시·Unlisted 신청·테스터·가격·계약 변경 없음.

## 원천과 산출물

- 정책·문안 원천: mediness spec 워크트리 products/day/60-release/app-store-preparation.md(새 draft).
- 이미지·촬영 fixture: CENTURION_DAY app/store/0.1.0/ · app/tool/store_capture/main.dart(새 파일, 아직 미커밋).
- 이미지 목록·재현법: app/store/0.1.0/README.md 및 screenshots/manifest.sha256.txt.
- IPA: CENTURION_DAY app/build/store-prod/ipa/DAY.ipa(무시 경로, 커밋 금지).
- 세부 근거: mobile-screenshot-report.md · mobile-prod-upload-report.md · mobile-asc-report.md · mobile-policy-report.md.

## 아직 미완 — 심사 제출 전

1. prod 서버 배포 및 /privacy·/support 공개 본문 확정·로그인 없이200확인. 정책의 운영주체·지원연락처·책임자·서버보관/파기·위탁·시행일은 사용자 미응답으로 추정하지 않음.
2. 앱 내부 개인정보 링크 추가, 예약현황 ‘곧 출시 예정’ 처리 결정. 현재 binary는 기존 실제 앱 소스 그대로다.
3. 심사 연락처·데모 로그인 자격·심사 메모, copyright, 연령등급, App Privacy, 가격·판매지역, 콘텐츠권리 선언. 입력 미정값은 넣지 않음.
4. 정식 앱의 prod 로그인·데모 dev 넘김·푸시/M-20·채팅/통역 실물 확인.
5. 정식 준비가 끝난 뒤 심사 제출과 Unlisted 별도 신청. 현재 등록 완료는 심사 준비 전체 완료가 아님.

## 개인정보 질문에 관한 정리

직원 계정 식별정보와 푸시 기기 등록 정보, 채팅/첨부는 서버에 저장된다. 화면에서 조회만 하는 고객 데이터, 기기 Keychain 세션, 실시간 통역을 모두 같은 수집 항목으로 묶지 않는다. 단순 통역만으로 개인정보가 포함되거나 별도 동의 팝업이 필수라고 단정한 앞 판단은 정정했다.

DAY는 통역 대화를 기록하지 않는 코드/SPEC이고, Soniox 공개정책은 실시간 API 내용을 일시 처리·미저장, 모델 학습/평가/개선 미사용으로 설명한다. 콘텐츠 없는 운영 메타데이터는 별도 보관된다. 개별 계약/프로젝트 설정을 검증했다고 주장하지 않는다. 근거: https://soniox.com/policies/privacy-policy · https://docs.soniox.com/security-and-privacy .

## 경계와 후속

앱 일반 lib/·ios/·권한문구·서버/웹/env·기존 _RESUME 수정 없음. 추적 app 파일 diff 없음. 회사 레포 commit/push/PR 없음. 서버 코디가 같은 브랜치의 다른 변경을 소유하므로 새 app/store와 tool/store_capture를 보존해 함께 검토해야 한다. 모든 발주 결과 수신·검증·release 요청 완료(external terminal은 retained/no process action). 활성 발주 없음.
