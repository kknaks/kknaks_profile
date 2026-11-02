# 앱 실기기 E2E 피드백 batch 1 (2026-10-28 · 운영 ccc + TestFlight 빌드 4)

사용자가 「응 수정하자」(2026-10-28). reviewer_doc 터미널(`term_ec508ae4…`)이 사용자와 본 것을 모았다 — 코드는 읽기만, 수정 0. 발주 · 범위는 코디.

| # | 무엇 | 근거(코드 · 화면) | 성격 · 방향(제안) |
|---|---|---|---|
| 1 | 웹 [스캔할 기기]에 같은 폰이 「iPhone」 2대로 뜬다(하나는 접속 중 ● · 하나는 ○) | 기기 = APNs 토큰 1개 = 행 1개(`back/app/service/devices.py:21-29`). 토큰이 바뀌면(Xcode sandbox ↔ TestFlight production · 재설치) 옛 행이 남고 지우는 때는 로그아웃 · 푸시 실패뿐. targets = 코디 계정 기기 24시간(`service/display.py` `targets`) | 수정 — 앱이 설치 단위 id(예: `identifierForVendor`)를 보내 같은 기기의 옛 토큰 행을 바꿔 끼우기 · 또는 같은 계정 · 같은 이름 옛 행 정리 규칙. SPEC-004 §5-1.1 한 줄 |
| 2 | 기기 이름이 전부 「iPhone」 | iOS 16+ 는 entitlement(`com.apple.developer.device-information.user-assigned-device-name`) 없으면 `UIDevice.name` = 「iPhone」 | 수정 — entitlement 신청 또는 첫 로그인 때 이름 입력(설정 「기기 이름」은 있음 · `screens/settings_screen.dart:123`) |
| 3 | 웹에서 여권 스캔을 다시 보냈는데 폰에 알림이 안 옴 | 앱이 앞(SSE 열림)이면 푸시 대신 SSE(`display.py` `reach`) · 이미 스캔 · 대기 화면이면 기다림(OQ-621) · 기기 버튼 아닌 QR 이면 푸시 없음 · ○(옛 행)로 보냈으면 옛 토큰 | **원인 확인 먼저** — 운영 `push_log` · `display_request` · back 로그(`ssh medi-me`). #1 과 같이 볼 것 |
| 4 | 휴대폰 번호 맨 앞 0 빠짐(웹 상세 「1055113764」) | KOS 가 저장 때 0 을 뗀다(`app-kos-report.md` §5.3 · review-doc r1 W8) | **결정: KOS 그대로**(사용자 2026-10-28 「kos 그대로로 갈래」) — 수정 없음 · 표시 · 전송 꼴 안 바꿈 |
| 5 | iOS 기본 카메라로 웹 QR 을 찍으면 「사용 가능한 데이터가 없음」 | QR 내용 `ccc://display?t=…` · `ios/Runner/Info.plist` 에 `CFBundleURLTypes`(ccc 스킴) 없음 — 설계는 앱 [QR 읽기]만 | 수정 — `ccc` 스킴 등록 + 딥링크 열기(로그인 · claim). 또는 웹 QR 안내를 더 크게. SPEC-004 §5-3 |
| 6 | 앱 여권 스캔 — 초점이 이상하고 MRZ 인식 0(1/3 실패 화면) | `ios/Runner/TextScanner.swift` — `UIImagePickerController` 한 장 촬영 · 가이드 틀 = 화면 폭 86%(가까이 10 ~ 15cm 필요 → 13 Pro 이후 메인 렌즈 최소 초점거리 밖 · 피커는 매크로 자동 전환 없음) · 찍은 사진 전체를 Vision(틀 영역 자르기 없음) | 수정 — `AVCaptureSession`(자동 매크로 되는 가상 기기 `builtInTripleCamera`/`DualWideCamera`) · 영상 프레임에서 MRZ 영역 연속 인식 → 검사 숫자 맞으면 자동 촬영 · 틀 크기 조정. **실기기에서만 확인 가능** |

- 설계대로(수정 아님): 내국인(KR) 상세엔 [스캔할 기기] 없음 — 「스캐너 = 여권만」(D7-17 · `DetailModal.tsx:436`)
- 함께 볼 것: review-doc r1(`app-review-doc-r1.md`) FAIL · WARN 중 이미 코드에서 고친 것(F1 `push_log` 재생성 = `db.py` `_rebuild_push_log` 확인) 외 나머지 처분
