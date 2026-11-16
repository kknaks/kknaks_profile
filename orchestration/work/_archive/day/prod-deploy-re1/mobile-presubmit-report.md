# [mobile] ASC-3 — 정식 DAY 0.1.0 제출 전 점검

## 결론: ASC 쪽에서 제출을 막는 것 **0** (API 로 볼 수 있는 범위) — App Privacy 게시는 API 로 안 보여 「사용자 화면 확인 완료」(사용자 보고)

- 앱 DAY `day.medisolveai`(6833456680) · 버전 0.1.0(`e0ae563c-…`) · 2026-11-12 GET.
- 쓴 것: **appStoreReviewDetail.notes PATCH 1회**(블록 B 추가)뿐. 심사 제출 · reviewSubmission 생성 · 다른 메타데이터 변경 0. 데모 계정 · 연락처 값은 출력하지 않음.

## ① 앱 심사 정보 (appStoreReviewDetail `a120b122-…`)

| 칸 | 상태 |
|---|---|
| `demoAccountRequired` | **true** |
| 데모 계정 이름 · 암호 | **채워짐** · 채워짐 |
| 연락처 이름(성 · 이름) · 전화 · 이메일 | **채워짐**(4칸 모두) |
| notes — 블록 A | 있음(점검 전 notes = 블록 A 그대로 · 218자) |
| notes — 블록 B | **없었음 → 추가함**(②) |

## ② 블록 B 추가

- 원천: `app-store-preparation.md` §5-3 두 번째 코드 블록(175자) 원문 그대로.
- PATCH `/v1/appStoreReviewDetails/a120b122-…` — `notes` 한 칸만 = 「블록 A + 빈 줄 + 블록 B」 · 200.
- GET 대조: notes = 기대 문자열과 **완전히 같음**(395자) · 블록 A 보존 · 블록 B 포함 · **다른 칸 전부 변경 전과 같음**(비교 True).
- ⚠ 원천 §5-3 은 블록 B 를 「데모 자격 입력 + prod 데모 연결(D-1) · 데모 데이터 · 푸시 **실물 확인 뒤에만**」 붙이라고 적는다. 데모 자격 입력은 확인됐지만(채워짐), **D-1 · 데모 데이터 · 푸시 실물 확인은 이 워커가 하지 않았다** — 코디 지시로 추가. 확인이 아직이면 제출 전에 확인 필요(블록 B 는 「데모 계정으로 로그인하면 데모 병원 데이터가 열린다 · 시술 현황 · 상태 변경 · 호출 · 채팅 · 알림 · 통역을 확인할 수 있다」고 약속한다).

## ③ 제출 막는 것 점검

| 항목 | GET 값 | 판정 |
|---|---|---|
| 버전 상태 | 0.1.0 · `PREPARE_FOR_SUBMISSION` · `releaseType MANUAL` · IOS | OK |
| 빌드 연결 | `21071da9-…` = **0.1.0 (2)** · VALID · expired false | OK |
| 암호화 | 빌드 `usesNonExemptEncryption = false` | OK |
| 스크린샷 | ko · `APP_IPHONE_67` 5장 · `APP_IPAD_PRO_3GEN_129` 5장 · 전부 `COMPLETE` | OK |
| 설명 | ko 283자 · sha256 앞 8자 `85ed67f7`(원천과 같음) | OK |
| 키워드 | `병원,직원,시술현황,업무,채팅,알림,통역` | OK |
| 이름 · 부제 · 카테고리 | DAY · 「병원 직원을 위한 업무 앱」 · `BUSINESS` | OK |
| 지원 URL | `https://day.medisolveai.com/support` — **실제 200**(title 「DAY 지원 · DAY」) | OK |
| 개인정보처리방침 URL | `https://day.medisolveai.com/privacy` — **실제 200**(title 「DAY 개인정보 처리 안내 · DAY」 · Soniox · 지원 메일 문구 있음) | OK |
| 연령 등급 | 설문 null 칸 0 · 결과 `TWELVE_PLUS` | OK |
| 가격 | 수동 가격 customerPrice 0 · proceeds 0(무료) | OK |
| 판매 지역 | available 1개 = KOR(지역 id 디코드 `t: KOR`) | OK |
| 저작권 | `2026 Medisolve AI Co., Ltd.` | OK |
| 콘텐츠 권리 | `USES_THIRD_PARTY_CONTENT` | OK |
| 앱 심사 정보 | ① 전부 채워짐 · notes A+B | OK(② 주의 참고) |
| App Privacy 게시 | 공개 API 없음(`dataUsages` 404 · ASC-2) | **사용자 화면 확인 완료**(사용자: 게시함 · 사용자 ID 「연결됨」으로 고침) |
| 진행 중 reviewSubmission | 0개(만들지 않음) | 제출 가능 상태 — 새 제출 생성 가능 |
| 단계적 출시 | 없음(설정 안 됨 · 선택 사항) | 막지 않음 |
| 선택 칸(막지 않음) | 마케팅 URL · 프로모션 텍스트 · whatsNew(첫 버전) · privacyChoicesUrl 비어 있음 | 막지 않음 |

## 남은 것 · 주의
1. 블록 B 의 전제(prod 데모 연결 D-1 · 데모 데이터 · 푸시 실물)가 확인됐는지 — 제출 전에 코디/사용자 확인.
2. 판매 지역 KOR 의 `CANNOT_SELL` 표시(ASC-2)는 출시 전 상태로 보임 — 제출 화면 경고 시 알려 주기.
3. 제출 자체(Add for Review → Submit) · Unlisted 신청은 사용자 몫. 이 워커는 하지 않음.

## 정정 (코디 · ASC-3 — 블록 B PATCH 하지 말 것)
- 정정이 도착했을 때 **블록 B PATCH 는 이미 끝난 뒤**였다(200 · GET 대조 완료). 지시대로 **되돌리지 않고 그대로 둠**.
- 지금 ASC notes = 블록 A + 블록 B(395자). 블록 B 의 「…직원 채팅, **알림**, 통역을 확인할 수 있습니다」는 사실과 다르다 — 정식 앱이 데모(dev 서버)로 넘어가면 **푸시가 오지 않음**(사용자 결정 M-20 안 함).
- **제출 전 사용자가 notes 문안을 정해 고쳐야 함**(블록 A 만으로 되돌리기 · 「알림」을 뺀 문안 등). 이 워커는 더 쓰지 않음.
- 그래서 결론 「막는 것 0」 에 **notes 문안 확정 1건**을 더한다.
