# q-web-spec 결과 보고 — 고객 문진 웹 계약(SPEC-006 · DEC-008 · WORK-010)

## 상태: done (문서만 · 코드 0 · 커밋 0)

## 수행 내용

| 문서 | 무엇 |
|---|---|
| `para/projects/summer-star/cc-prototype/20-spec/spec-006-customer-questionnaire-web.md` **(새 · 0.1.0)** | 주소 `{PROC_FRONT_ORIGIN}/q#<token>`(front `app/q/page.tsx` · `(main)` 밖 · `lib/publicApi.ts` 가 직원 세션을 안 읽음) · 토큰 = HMAC(`PROC_SESSION_SECRET`, 요청 id · nonce)이고 DB 엔 nonce · 해시만 · 여는 시한 10분 · 쓰는 시한 60분(`PROC_QWEB_FILL_MIN` 새) · `opened` = 고객이 엶 · 한 번 제출 · 새로고침으로 다시 열기 · 새 요청이 옛것(`pending` · `opened`)을 닫음 · 화면 ①~⑦ + 오류 화면 8 · 언어 원천 그대로(+ 응답 전 오류 화면만 브라우저 언어) · 공개 `GET` · `POST /api/public/questionnaire`(헤더 `X-Questionnaire-Token` · BE4 서비스의 「누가」만 바꿈) · 직원 문진 경로 2 · unlock 없앰 → 경로 49 · KOS 제출 · 이력 `web_submit` · 보안(허용 키 응답 · id 입력 없음 · 속도 제한 4줄 · 로그에 토큰 0) · 법적 검토 주석 3곳 · QR 이 뜨는 곳(데스크 웹 상자 · 직원 앱 QR 화면 · `qrUrl` 은 로그인 응답에만 · 푸시 payload 엔 없음) · KOS 없이 갈 자리(세 함수 · 표는 그때) · E2E Q1 ~ Q8(배포 뒤 고객 폰) · OQ-801 ~ OQ-814 · 부록 A(D8 → 절) |
| `10-decision/decision-008-customer-questionnaire-web.md` **(새)** | D-01 ~ D-08 · 「DEC-007 에서 바뀌는 줄」 표(D-01 · D-13 · D-43 ~ D-47 · D-71 — DEC-007 본문은 안 고침) · 부록 A `_RESUME` 줄 → D |
| `30-work/work-010-customer-questionnaire-web.md` **(새)** | 계약 고정점 9 · WP-BE · WP-FE · WP-APP · WP-REVIEW · WP-E2E(대상 파일 · 완료 조건 · 부분 검증 명령) · 병렬 그림 · 완료 = 배포 주소에서 사용자 고객 폰 Q1 ~ Q7 |
| `20-spec/spec-004-procedure-app.md` 0.4.1 → **0.4.2** | 문진 줄만: 머리 변경 줄 · §1.1 「QR 문진」 · §3.3 unlock 표 줄 · 글머리 · §3.4 두 줄 · §5-3 QR(스캔만) · 열기 · 닫기 · 기기 확인 · §6.10 [QR 읽기] · §6.11 [태블릿에 띄우기](문진) · **§6.15 = 「빠짐 → SPEC-006 · 아래는 기록」** · §6.17 QR 상자 · §7.3 문진 · unlock · 새 공개 경로 · 경로 수 49 · §7.4 `display_request` · `questionnaire_history` · §8.6 문진 · §8.7 두 곳 · §8.8 E6. 줄 끝 `(0.4.2)` · links · sources |
| `20-spec/spec-005-reservation-board.md` 0.4.0 → **0.4.1** | QR 상자 줄만: 「0.4.1 변경」 머리 · §1.2 첫 줄 · §6.6 「고객 기본 정보」 머리 · §6.8 #10 · §7.3 머리 메모. links · sources |
| `10-decision/README.md` · `20-spec/README.md` · `30-work/README.md` · `README.md`(최근 로그) · `log.md` | 행 · 버전 · 한 줄씩 |

## 검증

**결정 줄 → 절 대조(빠짐 0)**

| `_RESUME` 줄 | DEC-008 | SPEC-006 |
|---|---|---|
| §2 10-27 「문진 = 고객이 웹에서 한다」(뒤집음 · ccc 고객용 웹 · 나중에 KOS 없이 · 지금 판은 끝까지) | D-01 · D-02 · D-04 · D-08 | 머리말 · §1 · §2 · §9 · WORK-010 Meta |
| §1 「문진 다시 하기」(웹 [QR 전송] → 직원 폰 · 데스크 태블릿에 QR · 띄우기 길 재사용 · 앱은 QR 만 · 고객 폰 · 로그인 없는 토큰 링크 · BE4 재사용 · 나중 ccc · APP5 정리 · SPEC-004 §6.15 · DEC-007) | D-03 · D-04 · D-05 | §2 · §3 · §6.2 · §8 · §9 · SPEC-004 0.4.2 |
| §2 10-28 「문진 다시 하기 착수」(웹 상세 [QR] → 데스크 웹 · 직원 앱 · 토큰 링크 · 지금 KOS · 나중 ccc · APP5 뺌 · 문서부터) | D-01 ~ D-05 · D-08 | §1 · §3 · §6 · §8 · §9 |
| 문진 언어 원천(KOS language → 국적표 → en · 10-27) | D-06 | §4.1 |
| 방문별 이력(10-26 · D7-47) | D-06 | §6.4 |
| 주민번호 안 넣음(Q-152) | D-06 | §4 ③ · §6.2 · §1.2 |
| 법적 검토 주석(§1 · 10-27 촬영 가이드 줄) | D-07 | §7.6 · OQ-807 |

**grep**
- 새 3문서 + SPEC-004 · SPEC-005: 키 · 토큰 값 · JWT · 휴대폰 꼴 · 이메일 · 24자 넘는 hex · `KOS_API_tenent` → **0**
- SPEC-006 절 번호 참조 25개 → 모두 있음(빠진 제목 0) · OQ-801 ~ OQ-814 쓰인 것 14 = 정의 14
- 새 links 대상 3개 파일 있음

**frontmatter**: 새 3문서 최소셋(type · id · title · status · product · feature · created_at · updated_at · tags · links · sources · DEC 은 up) 채움 · 상태 draft / proposed

**린트**: `rules/document-pipeline.md` · `scripts/lint-pipeline.py` 는 이 워크트리에 **없다**(planner tools.md 가 가리키는 경로) — 돌리지 못했다. `rules/` 에는 개념 맵 pre-commit 만 있음(개념 파일 안 건드림)

## 미결 · 주의점

- **정할 것(SPEC-006 §12 — 모두 기본값 붙임)**: 사용자 몫은 **OQ-808**(링크 복사 · 메신저 — 이제 https 라 만들 수 있음 · 기본 없음) · **OQ-810**(안드로이드 E2E) · **OQ-811**(KOS 없이 갈 때 고객 기본 값 원천 — 이번 판 밖) · **OQ-807**(링크만 있으면 미리 채운 개인정보가 보임 — 법적 검토). 나머지(OQ-801 토큰 fragment + HMAC · OQ-802 unlock 없앰 · OQ-803 시한 · OQ-804 메모리 속도 제한 · OQ-805 · 806 · 809 · 812 · 813 · 814)는 planner 기본값
- **브리프 예시와 다른 것**: 경로를 `/q/<토큰>` 대신 **`/q#<토큰>`(fragment)** 로 기본값 — 토큰이 front · ingress · back 접근 로그와 `Referer` 에 남지 않게. 되돌리면 §2 · §6.1 · §7.4 세 줄만 바뀜(OQ-801)
- **토큰 원천 바꿈(문진 종류만)**: 지금 무작위 + 해시는 직원 화면이 링크를 다시 그릴 수 없어(데스크 새로고침 · 직원 앱이 나중에 받기) HMAC 으로 — 스캔 종류는 그대로
- **코드와 SPEC-004 가 이미 다른 곳(이번 판 밖 · 고치지 않음)**: `service/display.py` `reach()` 는 SSE 가 열려 있어도 **늘 푸시도 보낸다**(E2E batch 2) — SPEC-004 §5-3 「기기에 닿기」 ② 는 「아니면 푸시」. 다음 SPEC-004 판에서 맞출 것
- DEC-007 본문은 고치지 않았다(브리프 목록 밖) — DEC-008 「DEC-007 에서 바뀌는 줄」 표가 읽는 법. DEC-007 줄에 화살표를 달지는 코디 판단
- SPEC-004 제목의 「QR 문진」 · 부록 C D-45 ~ D-47 · D-71 줄은 기록으로 두었다(「그 줄만」)
- 이 워크트리에 다른 판의 커밋 안 된 변경(DEC-006 · SPEC-003 · SPEC-005 앞선 판 · WORK-007 등)이 같이 있다 — 커밋 때 나눌 것
