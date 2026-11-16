# mobile-deployment 결과 보고

## 상태: done

## 수행 내용
- 신설 `products/day/40-architecture/mobile-deployment.md` (type architecture · status draft · owner TBD). 위치 근거: document-pipeline 「40-architecture = 여러 SPEC/WP 공유 장기 구조 요약」, 기존 system.md · code-structure.md 와 같은 자리. 새 최상위 디렉토리 없음.
  - 표시 4종 [확정]/[제안]/[미결]/[설정 완료(현재 없음)] 구분.
  - 공통 Flutter 1벌 → iOS/Android × dev/prod 4개, 앱 → HTTPS → DAY 서버(APP_ENV) → day_dev/day_prod · KOS 데모(is_demo)/실제 연결. 앱에 KOS · 서명 · 푸시 키 없음. 기존 Bearer `/api/auth/*` · 같은 service 유지. staging 미도입 제안.
  - 앱명 DAY Dev / DAY, `com.medisolveai.day(.dev)` = 두 플랫폼 후보(미등록·도메인 미확인), 동시 설치, flavor vs debug/release 축 구분, 로컬 API 덮어쓰기 dev 만.
  - iOS: Team/App ID/Bundle ID/App Store Connect 레코드, scheme·configuration, 인증서·provisioning 쉬운 설명, iPhone+iPad·최소 OS 미결, Keychain, 기능별 최소 권한, 자동 서명 시작·CI 서명 향후, TestFlight = 시험 수단.
  - iOS 비공개 4안 비교(Custom/Unlisted/Enterprise/Ad Hoc), 비공개≠심사 생략, Enterprise 를 고객 병원 대안으로 확정하지 않음, Ad Hoc 100대/제품군/년.
  - Android: 계정 미결, Application ID, flavors, 서명 keystore 보관·백업(Android Keystore 시스템과 구분), APK 직접 배포(Play 필수 아님·알 수 없는 앱 허용·업데이트 책임) / managed Google Play 비공개 후보, 개발자 인증(공식 문서 문구만 — 2026-09-30 4개국, 2027 이후 전 세계, 한국 시점 미명시 → 미결).
  - 푸시: APNs 직접 유지, FCM 후보·미결, sandbox/production = provisioning entitlement 기준(TestFlight=production), 기기 토큰 구분(계정·설치·플랫폼·앱ID·푸시 환경) = 향후 계약·테이블 변경 아님, SSE(foreground) vs 푸시(background).
  - 환경별 구성표, Mermaid 1장, 버전/build, 로그·crash 환자정보 금지, release 확인 항목, iOS 순서 7단계(시작 안 함 명시), 미결 M-1~M-15, 공식 링크 12개 + 확인일 2026-11-08.
- `README.md`: 진입 목록에 링크 1줄 + last_updated 2026-11-08.
- `system.md`: 「환경」 절에 링크 1줄 + last_updated 2026-11-08.

## 검증
- `python3 scripts/lint-pipeline.py --strict`: exit 0 · **0 error** · 263 warning, products/day 범위 warning 0 (warning 은 모두 다른 제품 기존분 — 무관).
- `git diff --check`: 통과. 신규 파일 줄끝 공백 없음.
- 상대 링크 실재 검사(3 파일): 깨진 링크 0.
- 공식 문서: Flutter 3 · Apple Unlisted/배포 방식/Enterprise/Devices · Android 대체 배포/개발자 인증 · managed Play 는 직접 열어 확인. APNs 두 페이지는 JS 렌더라 Apple 문서 JSON 데이터로 확인. TestFlight 세부 · Android 키 분실 · Keychain 권장은 링크 미검증으로 문서에 표시.

## 미결·주의점
- M-1 설치 대상(회사 직원/고객 병원 직원 · 개인 폰/관리 기기)이 iOS·Android 배포 방식 전체를 가른다 — 사용자 답 필요.
- 도메인 소유 · Apple Team 내 역할 · API hostname 미확인.
- 기기 토큰 구분은 푸시 붙일 때 DAY-SPEC-000 device 개정 필요(이번엔 안 함).
- managed Google Play 비공개 앱 세부(심사·조건)는 요약만 확인 — 고를 때 재확인.
- 커밋·push·PR 안 함. 작업 시작 시 보였던 spec-001/002 · log.md 수정은 이 작업과 무관하며 손대지 않음(현재 status 엔 안 보임).
