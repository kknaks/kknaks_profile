# WORK-009 WP-FE 결과 보고 — 웹 front 닿는 곳

## 상태: done

작업 위치: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · branch `kknaksss/overall-board-2` · 범위 `procedure/front/**` 만 · 커밋 없음.

## 수행 — 파일 · 화면
| 파일 | 내용 |
|---|---|
| `components/reservations/Display.tsx` (새) | `useQuestionnaireRequest` — 「고객 기본 정보」 머리 [QR로 고객 입력 요청] / [QR 닫기] + QR 상자(W:276-289): QR(`ccc://display?t=<qrToken>` · 남은 시간 mm:ss) · [태블릿에 띄우기] → DS Popover 기기 목록(`targets` — 이름 · 폰/태블릿 · 접속 중 점 · 마지막 접속 시각) → 「{기기}에 표시 중」 · [닫기](요청 `canceled`) · 만료 / 제출 / 닫힘 뒤 [새 QR]. 단계 = 상세 `displays[]`(5초 폴링) — 대기 → 열림 → 「제출됨 · HH:MM」. 상자를 닫아도 머리에 최근 요청 단계 배지(문진 대기 · 열림 · 제출됨). [링크 복사] · [메신저 전송] 없음(D7-44) |
| 〃 | `ScanSteps` — 「신분 확인」 [스캔할 기기] 단계(W:308-342): idle = 기기 버튼(`targets` · 접속 점) + [QR] → qr(「QR로 다른 기기 연결」 · 10분 · [취소]) / wait(「{기기}에 보냈어요 · 여는 중…」 → opened 「{기기}에서 스캔 중 · 촬영 대기 중…」 · [취소]) → done = 썸네일 + 「{기기}에서 수신 · HH:MM · 자동 입력됨 (확인 후 수정 가능)」(`app_manual` = 「손으로 입력」) · `identity.photoKos === 'failed'` 면 「KOS 사진 실패」 배지 · [다시 스캔](접수 전만 — 시안). 다시 연 상세 · 다른 탭이 만든 열린 요청도 `displays[]` 로 이어 그림 |
| 〃 | `IdPhoto` — `api.idPhotoUrl()`(fetch + `Authorization: Bearer` → blob → `URL.createObjectURL`) · 언마운트 · 사진 바뀜 · 상세 닫힘 때 `revokeObjectURL` · 누르면 크게 보기(같은 blob) · `<img src>` 에 back 경로 · 쿼리 토큰 없음(스크린샷 때 src = `blob:http://localhost:13731/…` 확인) |
| `components/reservations/DetailModal.tsx` | 위 둘을 붙임(12줄) — QR = 취소 · 부도 예약 밖 · 스캔 = 취소 · 부도 밖 + (외국인 또는 이미 앱 스캔된 신분 — 여권만 D7-17) |
| `lib/api.ts` | `displayTargets` · `createDisplay` · `closeDisplay` · `displayQrText` · `idPhotoUrl`(법적 검토 주석) — back 호출은 이 모듈에서만(rules) |
| `lib/types.ts` | `Role` 에 `counselor` · `Identity.device?` · `photoId?` · `photoKos?` · `ResvDetail.displays?` · `DisplayItem` · `DisplayTarget` · `DisplayCreated` |
| `lib/session.ts` | `ROLES` 에 `counselor`(상담사 로그인 세션이 버려지지 않게) · 머리 주석 「웹도 다섯 역할」 |
| `package.json` · `package-lock.json` | `qrcode@^1.5.4` · `@types/qrcode`(dev) — QR 그리기(DS 에 QR 없음) |

## 검증
- `cd procedure/front && npx tsc --noEmit` → 0 오류 · `npm run lint` → 0 문제
- 로컬 E2E(임시 포트 · 사용자 3700 · 8700 안 씀): back `:18731`(실제 back · 스크래치 DB · 스크래치 `PROC_PHOTO_DIR`) + front `next dev -p 13731` · Playwright headless 1600×1000 · 관리자 세션. 코디 계정 기기 2(태블릿 · 폰 — 지어낸 토큰) 등록 · 태블릿은 SSE 를 열어 `online` (폰에는 보내지 않음 — 가짜 토큰 푸시 방지)
- 스크린샷 `fe-shots-reservation/app-fe-*.png` 16장:
  - 00 예약 현황 표(회귀) · 01 QR 상자(남은 시간 09:5x) · 02 기기 목록(접속 중 점 · 폰/태블릿) · 03 「데스크 태블릿 1에 표시 중 · 대기」 · 04 앱 쪽 `pending?deviceId=1` 흉내 → 「열림 · 고객 입력 중」 · 05 `close done` → 「제출됨 · 21:25」 · 06a 상세 다시 열기 → 머리 단계 배지 · 06 [닫기] → 요청 `canceled`(상세 `displays` 로 확인)
  - 07 스캔 idle · 08 스캔 QR · 09 「데스크 태블릿 1에 보냈어요」 · 10 「데스크 태블릿 1에서 스캔 중」 · 11 done 썸네일(지어낸 파란 「TEST」 JPEG · 사람 · 신분증 아님) + 「…에서 수신 · 21:25 · 자동 입력됨 (확인 후 수정 가능)」 · 12 크게 보기 · 13 `kos_status=failed` → 「KOS 사진 실패」 · 14 다른 예약 상세(회귀)
  - 스캔 저장은 **ccc 스크래치 DB 에 `id_photo` · `identity_check` 행을 직접 넣어 흉내**(KOS 쓰기 0 · `passport-scan` 안 부름). 띄우기 요청 만들기 · 닫기는 실제 back API
- KOS 쓰기 0(읽기 폴링만) · 스크래치 DB · 사진 폴더는 레포 밖 · 서버 둘 다 끔

## 계약 대조 (§6.17 · §5-3 · §3.4)
| 항목 | 결과 |
|---|---|
| [QR로 고객 입력 요청] → QR 상자 · QR = `ccc://display?t=` · 10분 · 남은 시간 | 같음 |
| [태블릿에 띄우기] → `targets`(이름 · 폰/태블릿 · 접속 중 점) → 「{기기}에 표시 중」 | 같음 |
| [닫기] → `close {status:"canceled"}` | 같음 |
| [링크 복사] · [메신저 전송] 없음 | 같음 |
| 상태 = `displays[]` 5초 폴링 · 대기 → 열림 → 「제출됨 · HH:MM」 | 같음(상세 모달의 기존 5초 폴링) |
| [스캔할 기기] idle(기기 · QR) → 대기(「{기기}에서 스캔 중」 · [취소]) → done | 같음 |
| 썸네일 = fetch + Bearer → blob URL · 닫으면 revoke · 쿼리 토큰 · 쿠키 · 공개 URL 없음 | 같음 |
| 「{기기}에서 수신 · HH:MM · 자동 입력됨(확인 후 수정 가능)」 · 손 입력 = 「손으로 입력」 | 같음 |
| 「KOS 사진 실패」 | 같음 — `identity.photoKos`(코디 결정 2026-10-27 · back 이미 반영 확인 `schemas/reservations.py:221`) |
| [다시 스캔] 접수 전만 | 같음 |
| 역할 `counselor` · 웹 다섯 역할 | 같음(웹은 역할로 화면을 가르지 않음 — 세션 허용 목록만) |
| 건강 정보 빈 상태 문구 | 그대로(안 건드림) |

## 이슈 · 코디가 확인할 것
1. **허용 경로 밖 2곳**: WP-FE 줄 경로는 `components/reservations/**` · `lib/types.ts` · `lib/session.ts` 이지만, rules 「back 호출은 `lib/api.ts` 에서만」 때문에 `lib/api.ts` 를, QR 그리기 때문에 `package.json` · lock(`qrcode`)을 고쳤다(둘 다 `procedure/front/**` 안).
2. **기본값(시안 · SPEC 에 없음)**: QR 머리 버튼은 취소 · 부도 예약에선 숨김(시안은 「수정 풀림」일 때만 — 웹 구현은 `can.editPersonal` 과 묶지 않음) · [스캔할 기기]는 외국인(여권)만 + 이미 앱 스캔된 신분 · 상세 모달을 닫아도 띄우기 요청은 닫지 않음(10분 뒤 back 이 `expired`) · 머리의 최근 문진 단계 배지 · 사진 크게 보기 오버레이 · 문진 제출 뒤 QR 자리에 「제출됨」 + [새 QR].
3. QR 은 만들 때 받은 `qrToken` 으로만 그린다(back 에 다시 읽는 길 없음) → 상세를 다시 열면 열린 요청은 단계 글 · 배지만 보이고 QR 은 [QR로 고객 입력 요청]으로 새로 만든다(앞 요청은 back 이 `canceled`).
4. `npm audit` 이 2건(moderate 1 · critical 1)을 알리고 `next dev` 도 Next 16.4.0 보안 권고를 띄웠다 — 이번 판에서 업그레이드하지 않음(범위 밖 · 결정 필요).
5. `npm run build` 는 브리프 검증 목록에 없어 돌리지 않음.

---

# E2E batch 1 — frontend 몫 (#4 휴대폰 표시 · #1 기기 목록) · 2026-10-28

## 상태: done (back · app 규칙 맞춤 확인은 코디 몫 — 아래)

작업 위치: 같은 워크트리 · branch **`kknaksss/overall-board-3`**(base `f8a3751`) · 범위 `procedure/front/**` 만 · 커밋 없음.

## 수행
| 파일 | 내용 |
|---|---|
| `lib/phone.ts` (새) | `phoneDisplay(countryCode, number)` · `phoneToSend(v)` — 규칙 정본(아래) |
| `components/reservations/DetailModal.tsx` | 「휴대폰 번호」 칸 = `phoneDisplay` 값으로 보임(읽기 전용 · 편집 둘 다). 저장 본문: 번호를 **고쳤을 때만** 하이픈 · 공백 뺀 입력값, 국가번호만 고쳤으면 번호 = KOS 값 그대로(표시용 0 · 하이픈을 보내지 않음). 고치지 않은 칸은 지금처럼 안 보냄 |
| `lib/types.ts` · `lib/api.ts` | `DisplayTarget.installId?` · `displayTargets()` 가 `installId` 가 실려 오면 installId 당 첫 줄(최근 순)만 남김 — back 이 이미 하나로 주면 아무 일 없음 |

## #4 휴대폰 규칙 (front 정본 — 코디에게 decision_gate 로 보냄 · back · app 이 같은 규칙이어야 함)
1. `cc` = countryCode 숫자만(`+82` · `82` → `82`) · `n` = number 숫자만
2. `cc ≠ 82` 이거나 `n` 이 비면 → number 원래 값 그대로
3. `cc = 82` 이고 `n` 이 0 으로 시작 안 하면 `n = '0' + n`
4. `n` 이 `01` 로 시작 · 11자리 → `3-4-4`(`010-5511-3764`) · `01` 로 시작 · 10자리 → `3-3-4` · 그 밖 → `n`(하이픈 없음)
- 보내는 값: 0 을 붙이지도 떼지도 않음(KOS 가 뗌) · 사용자가 고친 번호는 하이픈만 뺌
- 확인(스크래치 node): `82/1055113764 → 010-5511-3764` · `+82/01055113764 → 010-5511-3764` · `82/105511376 → 010-551-1376` · `82/25551234 → 025551234` · `1/4155550100 → 그대로` · cc 없음 → 그대로
- **back 이 `phoneDisplay` 필드를 더하기로 하면** front 는 그 값을 쓰도록 한 줄 바꾸면 됨(지금 back 워크트리 · 보고서에 batch 1 흔적 없음 — 보낼 때 확인 못 함)

## #1 기기 목록
- 웹은 이미 targets 의 `name` 을 그대로 보인다(「iPhone」은 back · 앱이 보낸 이름). 이름 · 한 줄 정리는 back(installId 바꿔 끼우기) + app(첫 로그인 이름 입력) 몫 — front 는 installId 가 실려 오면 중복을 한 번 더 거른다
- 실제 「installId 당 하나 · 기기 이름」 화면 확인은 back · app 변경이 들어온 뒤(이번 판 로컬 E2E 안 함)

## 검증
- `cd procedure/front && npx tsc --noEmit` → 0 · `npm run lint` → 0

## 코디 확인
1. 휴대폰 규칙을 back · app 이 위와 같이 쓰는지(또는 back `phoneDisplay` 필드로 갈지)
2. 0 을 붙인 번호를 편집 칸에도 보이므로, 사용자가 그 칸을 손대면 `01055113764` 꼴(0 포함)로 보낸다 — KOS 가 0 을 떼므로 결과는 같음

- **(추가 · 2026-10-28) back `phone.display` 우선**: 상세 「휴대폰 번호」 = `personal.phone.display` 먼저 · 없을 때만 `lib/phone.ts` `phoneDisplay` — 함수를 back `app/domain/phone.py` 규칙으로 맞춤(위 규칙 표 대신: 11자리 3-4-4 · 10자리 02 면 2-4-4 그 밖 3-3-4 · 9자리 02 2-3-4 · 82 밖 = 숫자만) · 시험 `lib/phone.test.mjs`(`npm run test:phone` — 16 표본을 back `uv run` 결과와 대조) **2 pass** · tsc 0 · lint 0 · 바뀐 파일 `lib/phone.ts` · `lib/phone.test.mjs`(새) · `lib/types.ts`(`PhoneValue.display?`) · `DetailModal.tsx` · `package.json`(스크립트 `test:phone`)
- **(되돌림 · 2026-10-28) #4 휴대폰 = KOS 그대로(사용자 결정)**: `lib/phone.ts` · `lib/phone.test.mjs` 지움 · `DetailModal.tsx` · `package.json` git 원래대로(휴대폰 칸 = KOS `number` 그대로 · 보내는 값도 batch 1 전 그대로) · `PhoneValue.display` 줄 뺌. 남은 front 변경 = #1 만(`lib/types.ts` `DisplayTarget.installId?` · `lib/api.ts` installId 거르기) · 코드에 phone 함수 흔적 0(grep) · tsc 0 · lint 0. 위 #4 절 · 추가 줄은 지난 기록

---

# WORK-010 WP-FE — 고객 문진 웹 /q · 데스크 QR 상자 (2026-10-28)

## 상태: done (화면 먼저 · 가짜 응답) — 실제 back 붙이기 확인은 WP-BE 공개 API 뒤

작업 위치: 같은 워크트리 · branch **`kknaksss/overall-board-6`**(base `fad8b56`) · 범위 `procedure/front/**` 만 · 커밋 없음.

## 수행
| 파일 | 내용 |
|---|---|
| `app/q/page.tsx` (새) | `(main)` 밖 공개 페이지 · **법적 검토 주석 ②**(SPEC-006 §7.6 문구 그대로) · 메타: 제목 `Céramique` · `robots noindex,nofollow` · `referrer no-referrer` · viewport 모바일(빌드 HTML 에서 확인 · 외부 스크립트 0) |
| `components/q/QuestionnairePage.tsx` (새) | 토큰 = `location.hash`(`useSyncExternalStore` · SSR 은 스피너) · 꼴(base64url 43자) 틀리면 back 안 부름 · 단계 ①~⑦ · 언어 칩 6(받은 번역 안에서 바꿈 · 다시 안 부름) · 기본 정보 미리 채움(이름 · 생년월일 date 칸 ↔ `yyyyMMdd` · 성별 · 국가번호 + 번호(KOS 값 그대로) · 주소 · 상세 주소 · 주민번호 · 발음 칸 없음) · KOS 양식 쪽마다(`CHECK_BOX` 여럿 · `SELECT_BOX` 하나 · `INPUT_BOX` · `isSubText` 고르면 글칸(placeholder = `translsMap.subText`) · 필수 = KOS 값 · 안 채우면 [다음] 꺼짐) · 동의(번역 키 ja · en · zh · 필수 안 하면 [제출] 꺼짐 · 2개 이상이면 [모두 동의]) · 제출 실패 = 입력 유지 + 「제출하지 못했어요」 [다시 제출] · 끝 「감사합니다 · 이 창을 닫으셔도 돼요」 · §5 오류 화면(문구만 · 코드는 `data-code`) · 응답 전 오류 = 브라우저 언어 · 진행 막대 n / N · 16px · 최대 560px · 브라우저 저장 0(OQ-806) · DS = medikit `Button` · `Input` · `Checkbox` · `RadioGroup` · `Progress` · `Loading` |
| `lib/publicApi.ts` (새) | `X-Questionnaire-Token` 헤더만 · `Authorization` 0 · `credentials:'omit'` · `referrerPolicy:'no-referrer'` · `lib/session.ts` · `lib/api.ts` 안 씀 · 오류는 코드만 들고 감 |
| `lib/q/text.ts` (새) | 앱 `questionnaire_text.dart` 옮김(6언어) + 끝 · 오류 화면 문구 8종 · `AGREEMENT_KEY` · `browserLang()`(§4.1 표) |
| `lib/q/form.ts` (새) | 앱 `model/questionnaire.dart` 옮김 — 번역 · 필수 · 답 모으기 · 제출 `answers[]`(title · parentQuestionTitle = 원문 · 키 7개 = 앱 · AK§5.1 과 같음) |
| `components/reservations/Display.tsx` | 문진 QR 상자(§8.1): QR = **`qrUrl`**(`ccc://` 안 씀 — 스캔 종류는 그대로) · `pending` = QR + 「고객 휴대폰 카메라로 찍어 주세요 · 남은 시간 mm:ss」 → `opened` = 「고객이 입력 중 · HH:MM」(QR 숨김) → `done` = 「제출됨 · HH:MM」 → `expired` = 「시간이 지났어요」 + [다시 만들기] · `canceled` = 상자 닫힘 · 「오늘 이미 제출함 · HH:MM」(상자 위 · 닫혀 있으면 머리) · 새로고침 = `displays[].qrUrl` 로 다시 그림(살아 있는 요청은 상자가 저절로 열림) · [태블릿에 띄우기] 그대로 · [닫기] = `canceled` · 「코디 폰 [QR 읽기]」 안내 뺌 |
| `lib/types.ts` | `DisplayCreated.qrToken: string \| null` · `qrUrl?` · `DisplayItem.qrUrl?` · `openedAt?` |

## 검증
- `cd procedure/front && npx tsc --noEmit` → 0 · `npm run lint` → 0 · `npm run build` → 성공(`/q` 정적 · Next 16.4.0 보안 권고로 한 번 멈춘 뒤 다시 돌려 통과 — 아래 이슈 3)
- 스크린샷 28장 `fe-shots-reservation/q-*.png`(임시 포트 front `:13731` · back `:18731` 스크래치 DB · 사용자 포트 0 · 서버 끔):
  - **고객 페이지(가짜 응답 — Playwright 가로채기 · 레포에 가짜 코드 0)** 아이폰 390 폭: `02` 첫 화면 ko / `02b` ja 칩 · `03` 기본 정보 · `04a~c` 양식 2쪽(빈 · 체크 + 기타 글칸 · 선택 + INPUT_BOX) · `05` 동의 · `06` 제출 실패(입력 유지 · [다시 제출]) · `07` 끝 / 안드로이드 412 폭: `02` en 첫 화면 · `04` 양식
  - **오류 화면 9**: 꼴 틀림(ko) · 404(ja) · 410 만료(ko) · 410 새 QR(zh-TW → 繁體) · 409 제출됨(en) · 409 제출 중 [다시 열기] · 429 [다시 시도](id) · 502 불러오기 실패 [다시 시도](zh-CN → 简体) · 403 fake_board(제출 때) — 브라우저 언어 고르기 확인
  - 제출 본문 확인: 헤더 `X-Questionnaire-Token` 있음 · `Authorization` 없음 · `deviceId` · `displayRequestId` 없음 · `dateOfBirth` = `19900101` · 답 title 원문 한국어
  - **데스크 상자**(실제 back 상세 + `displays[]` · 만들기 · 닫기 응답만 가로채기 — WP-BE 전이라): `01` pending(QR 흐림 처리 · 남은 시간) · `02` 태블릿 표시 중 · `03` 고객이 입력 중 · `04` 제출됨 + 오늘 이미 제출함 · `05` 새로고침 뒤 `qrUrl` 로 다시 그림 · `06` 시간이 지났어요 + [다시 만들기] · `07` [닫기] 뒤 · `08` 예약 현황 표(회귀)
  - 토큰 = 지어낸 43자(`T…`) · QR 은 흐림 · 고객 = 데모 `[ccc 시험]` 고객 · 지어낸 이름 `Test Customer`

## 계약 대조 (SPEC-006 §2 · §4 · §5 · §7 · §8.1)
| 항목 | 결과 |
|---|---|
| `/q#<토큰>` · `(main)` 밖 · 세션 분리 · `publicApi.ts` · 헤더 토큰만 | 같음 |
| 메타 noindex · no-referrer · 제목 Céramique · 외부 스크립트 0 | 같음 |
| 꼴 틀림 = back 안 부름 · 「링크가 올바르지 않아요」 | 같음 |
| ①~⑦ · 언어 칩 6 · 미리 채움 · 양식 · 동의 키 · 제출 · 끝 | 같음 |
| 오류 화면 표(§5) · 고객 정보 · 코드 · 영어 원문 0 · `data-code` | 같음 |
| 응답 전 오류 = 브라우저 언어 | 같음 |
| 데스크 QR = `qrUrl` · 단계 · 만료 [다시 만들기] · 오늘 이미 제출 · 새로고침 · 닫기 · [링크 복사] 없음 | 같음 |
| 법적 검토 주석 ② | 같음(`app/q/page.tsx` 머리) |

## 이슈 · 코디가 확인할 것
1. **실제 back 붙이기 미확인** — WP-BE 공개 API(`/api/public/questionnaire`)가 아직 없다(워크트리에 `qrUrl` 스키마만 보임). 응답 모양은 SPEC-006 §6.1 그대로 가정 — WP-BE 뒤 같은 시나리오를 실제 back 으로 한 번 더(특히 CORS `X-Questionnaire-Token` · `qrUrl` · `openedAt`)
2. **기본값(SPEC 에 없음)**: 성별은 여성 · 남성 둘(필수 · `GENDER_UNSPECIFIED` 미리 채움이면 안 고른 채) · 이름 · 생년월일 · 성별 필수(앱과 같음) · 데스크 상자 아래 「QR 은 10분 · 연 뒤 60분」 한 줄 · 새로고침 뒤 남은 시간 = `createdAt` + 10분(상세 `displays[]` 에 `expiresAt` 없음 — 운영 `PROC_DISPLAY_TTL_MIN` 을 바꾸면 어긋남) · 살아 있는 요청이 있으면 상세를 열 때 상자가 저절로 열림 · 제출 때 429 는 화면을 바꾸지 않고 입력 유지 + 「잠시 뒤 다시 시도」
3. `next build` · `next dev` 가 Next 16.4.0 보안 권고를 띄우고 한 번 멈춘다(다시 돌리면 통과) · 업그레이드 안 함(범위 밖)
4. 고객 페이지 가로 스크롤 칩 6개 — 390 폭에서 English · Bahasa Indonesia 는 밀어서 보임

## WORK-010 — 실제 back 붙이기 확인 (2026-10-28 · WP-BE 뒤)

- 환경: 실제 `procedure/back`(이 브랜치 · 임시 `:18731` · 스크래치 DB · `PROC_FRONT_ORIGIN=http://localhost:13731`) + front 임시 `:13731` · 사용자 포트 0 · 끝나고 둘 다 끔
- **고친 것 1건 — `lib/q/form.ts`**: 데모 KOS 실제 양식은 질문 `questionId` · 답 **`answerId`**(`id` 키 없음 · 필수 표시 없음)라, 앞 판(가짜 응답 · 앱 모델 그대로 `id`)대로면 답 id 가 모두 `''` → 한 질문에서 하나 고르면 전부 골라지고 제출 400 `answers.0.id: Field required`. → 답 id = `answerId ?? id` · 질문 id = `questionId ?? id` · 제출 `id` = `answerId`(KOS 제출 키 `id` 그대로)
- 흐름(Playwright · 아이폰 390 · 데스크 1600) — 스크린샷 `fe-shots-reservation/q-real-*.png` 11장(QR 흐림 · 토큰은 로그 · 파일 이름에 0):
  - 데스크 [QR로 고객 입력 요청] → 응답 `qrToken: null` · `qrUrl` = `http://localhost:13731/q#<43자>` → `q-real-desk-01-pending`
  - 고객 폰 `qrUrl` 열기 → 공개 `GET` 200 → 첫 화면(언어 `en` · source default) `q-real-01-start` · 데스크 5초 폴링 「고객이 입력 중 · HH:MM」 `q-real-desk-02-opened`
  - 기본 정보 미리 채움 그대로 → 양식 4쪽(질문마다 첫 선택지 · 이메일 칸 `ccc-test@example.com`) → 동의 → 공개 `POST` **200 `{ok:true}`** → 「감사합니다」 `q-real-05-thanks` · 데스크 「제출됨 · 13:41」 + 「오늘 이미 제출함」 `q-real-desk-03-done`
  - 같은 링크 새로고침 → 409 `q_submitted` 화면 `q-real-06` · [다시 만들기] 뒤 [닫기] → 그 링크 = 410 `q_canceled` 「새 QR …」 화면 `q-real-07`
  - 공개 요청 4건 모두 헤더 `X-Questionnaire-Token` 있음 · `Authorization` 없음 · 주소에 토큰 0
  - ccc DB: 요청 `done` 1 · 이력 `web_submit` 1행(`language=en` · `device_id` null · `display_request_id` 그 요청 · 답 15) · `event_log` `qweb_open` 4 · `qweb_denied` 2 · `questionnaire_submit` 1 · back 로그에 토큰(nonce) 0
- **데모 흔적**: 대상 = `[ccc 시험]` 고객(예약 1 · 이름 접두 assert 뒤에만 제출) · KOS 문진 제출본 1건 덮어씀 — 미리 채운 값 그대로(성별 칸이 비어 있어 시험이 「여성」을 고름 → KOS 고객 성별 = 여성) · 이메일 답 `ccc-test@example.com`. 되돌리지 않음
- tsc 0 · lint 0 · build 성공(Next 보안 권고로 한 번 멈춘 뒤 통과)

### 코디 확인 (back 몫으로 보임 — front 안 고침)
1. 제출 뒤 상세 `health` = `state:"ok"` · **`items` 0개** · `submittedAt` = 어제 21:08 그대로(제출 전에도 같은 모양). 이력 행 `kos_submitted_at` 도 어제 값 — KOS 가 제출본을 덮어쓰면서 `createdDateTimeUtc` 를 그대로 두는 것으로 보임 · 건강 7칸 매핑이 데모 양식 질문과 안 맞아 0개일 수도. 웹 「건강 정보」는 `ok` + 0개면 빈 칸으로 그린다(기존 화면 · 이번 WP 밖)

---

# E2E batch 3 — 웹 예약 상세 (frontend 몫 · 2026-10-28)

## 상태: done — #1 · #2 는 back 작업 중 코드(워크트리) 모양에 맞춤 · 실제 쓰기는 화면 시험에서 가로챔(KOS 쓰기 0)

작업 위치: 같은 워크트리 · branch **`kknaksss/overall-board-8`**(base `113c5e1`) · 범위 `procedure/front/**` 만 · 커밋 없음.

## 수행
| 파일 | 내용 |
|---|---|
| `components/reservations/autosave.tsx` (새) | 자동 저장 한 규칙 `useAutoSave` — 글자 칸 = 입력 멈춤 **1초** · 칸 벗어날 때(blur) · 모달 닫을 때(등록된 칸 전부 flush) / 고르는 칸(드롭다운 · 날짜) = 바로 · 같은 값이면 안 부름 · 저장 중 더 고치면 끝난 뒤 한 번 더 · 실패 = 쓴 글자 유지 · 칸 옆 `SaveState`(저장 중… · 저장됨 · **저장 못 함 [다시]**) · 서버 값이 따라오면(또는 저장 뒤 서버 값이 바뀌면 — KOS 가 다듬는 칸) 고친 값을 버림 |
| `components/reservations/DetailModal.tsx` | **#3 주의사항 · #5 예약 메모** = `AutoText`(자동 저장 · [저장] 없음) · **#4 고객 기본 정보** = [수정] · [저장] 없음 · **늘 편집 가능**(`can.editPersonal` 만 봄 — 접수 뒤 잠금 · unlock 없앰) · 칸마다 `PersonalField`(그 칸만 `PUT personal` — 묶음 칸 휴대폰 · SNS · 주소는 `personalPatch` 가 지금 값과 합침) · 닫기(× · 바깥 · Esc · [닫기]) = 남은 저장 먼저 · 실패는 표 화면 토스트 / **#2 유입 채널** = `FunnelField`: DS 드롭다운(`funnelCodes` · 지금 값 `customer.funnel.funnelId`) 고르면 바로 `PUT /api/customers/{id}/funnel {funnelId}` · 「미입력」 = `null` · KOS 값이 목록 밖이면 「{이름} (목록 밖)」으로 보임(고르기 전까지) · 상세 글칸 = 자동 저장(`{funnelId, funnelDetail}` · 채널 고른 뒤만) · 옛 back(코드 목록 없음)이면 예전 글 표시 |
| `components/reservations/Display.tsx` | **#1** 신분 확인 done 단계 [삭제] → medikit `ConfirmModal`(「ccc · KOS 사진을 지우고 미확인으로 · 자동 입력된 고객 정보는 그대로」) → `DELETE /api/id-photos/{photoId}` → 토스트 「여권 사진을 지웠어요 · KOS 사진도 지움 / KOS 에는 이미 없었어요 / KOS 로 올라가지 않은 사진」(`kos` = deleted · not_found · skipped) + 상세 다시 부름 · **추가 — [스캔할 기기]의 [QR] 칸 뺌**(기기 버튼만 · QR 단계 · `ccc://` QR 코드 지움 · 열려 있던 옛 요청은 「대기」 줄로만) · 문진 QR 은 그대로 |
| `lib/api.ts` | `deleteIdPhoto` · `saveFunnel` · `request` 에 `DELETE` · 안 쓰게 된 `displayQrText` 지움 |
| `lib/types.ts` | `VisitorFunnel` · `FunnelItem` · `customer.funnel?` · `funnelCodes?` |

## 검증
- `npx tsc --noEmit` → 0 · `npm run lint` → 0
- 스크린샷 12장 `fe-shots-reservation/b3-*.png` — 임시 포트(back `:18731` 실제 · 스크래치 DB · front `:13731`) · 대상 = 데모 `[ccc 시험]` 고객(예약 1) · **쓰기 요청(memo · remark · personal · funnel PUT · 사진 DELETE)은 Playwright 가로채기로 응답(KOS 쓰기 0)** · 사진 = 지어낸 TEST 그림 · 서버 끔
  - `01` [저장] · [수정] 버튼 0개 · `02` 메모 저장 중 · `03` 저장됨 · `04` 주의사항 실패(502) — 글자 유지 · 「저장 못 함 다시」 · 토스트 · `05` [다시] → 저장됨 · `06` 이메일 칸 벗어날 때 저장됨 · `07` 유입 채널 드롭다운(13 코드) · `08` 고름 → 저장됨 · `09` [스캔할 기기] QR 버튼 0 · `10` 사진 썸네일 + [삭제] · `11` 확인 창 · `12` 지움 토스트
  - 보낸 쓰기 7건: memo 1 · remark 2(실패 + 다시) · personal `{"email":…}` 1(그 칸만) · funnel `{"funnelId":2}` 1 · DELETE 1 · **닫기 직전 친 메모 1(Esc 로 닫자마자 flush)** — 같은 값 · 중복 호출 0

## 이슈 · 코디가 확인할 것
1. **#1 · #2 back 모양은 작업 중 코드에서 읽음**(보고서 batch 3 절 아직 없음): `DELETE /api/id-photos/{id}` → `{ok, kos}` · 상세 `customer.funnel {funnelId, name, detail}` · `funnelCodes[{funnelId, name}]` · `PUT /api/customers/{id}/funnel {funnelId, funnelDetail?}`. back 이 이름을 바꾸면 front 맞춤 필요 — 실제 쓰기(KOS) 화면 확인은 back 데모 실호출 뒤
2. **기본값(처분에 없음)**: 유입 채널 편집 = `can.editPersonal` 일 때 · 상세 글칸(funnelDetail) 더함 · 고객 기본 정보 칸마다 따로 PUT(같은 고객 묶음을 칸마다 back 이 다시 읽음 — 한 칸씩이라 KOS 호출이 늘 수 있음) · 사진 [삭제] = 접수 전후 모두 · [다시 스캔]은 그대로 접수 전만
3. 접수 뒤에도 편집 가능한 모습은 `[ccc 시험]` 고객이 접수 전이라 스크린샷 없음(코드: 잠금 = `!can.editPersonal` 만)
4. back 쪽 「앱 QR claim 경로를 남길지」는 back 보고 몫(front 는 이제 스캔 QR 을 만들지 않음 — `qrToken` 을 쓰는 곳 0)
