
# 재개 노트 — api-swagger-docs (cc-prototype)

**지금**: 1차 · 2차(add1) 모두 운영 배포 · 운영 E2E 완료(코드 #22 · #23 / infra #49 · #50) → 남은 것: 협업자 키 전달 · admin 회수 시점(D-26 사용자) · 문서 PR(DEC-010 · 011 · SPEC-008 0.3.3 · WORK-012 · 013) · slug 마감
**다음**: planner done → reviewer_doc 검수(자동) → 사용자 리뷰 → 코드 워크트리(`kknaksss/api-swagger-docs` 를 origin/main 위로) backend 발주 → reviewer → 실물 e2e → PR · 배포

세팅: `scripts/new-work.sh cc-prototype api-swagger-docs` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` (branch `kknaksss/api-swagger-docs`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] 정적 `reference/2026-10-27-cc-app/api-reference.html` 처리(재생성 or Swagger 링크로 대체) — 사용자 확인
- [ ] 협업자 답장(호스트 · admin 계정 · 문서 링크 · 시술/상품 미완) — 비밀번호는 사용자가 채움
- [x] 조사 1 `research-procedure-menu.md` — 3~4단 · id 일치 · 정할 것 12
- [x] 조사 2 `research-purchase-snapshot.md` — 스냅샷(부분) · 연결 키 · 고객 1명 1~3호출 · 정할 것 7
- [x] 조사 3 `research-har-product-edit.md` — Q-K1 유지 · Q-K2 id 유지(가격 수정 기준 · 이름/구성 수정은 미관찰)
- [ ] 시술 · 상품 API 범위 결정(사용자) — 코디 추천: 카테고리 · 상품(옵션) · 시술 / closed·deleted 제외 / 1시간 마스터 루프 캐시
- [ ] Swagger 기본 탭 Schema 로(사용자 답 대기)
- [x] 조사 4 `research-name-email-lookup.md` — 검색 응답 email 유무 · 이름 일치 성질 · email 채움 비율 · 호출 비용

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-11 | API 문서는 코드 기준 · back 에 Swagger 로, 설명 자세하게 | 사용자 지시 |
| 2026-11-11 | 경로 `/api/docs` · `/api/redoc` · `/api/openapi.json`(ingress `/api`→back 이라 인프라 무변경) · 인증 없이 공개 | 코디 기본값(ingress 확인) · 데모 계정 공유 방침과 같음 |
| 2026-11-11 | 협업자 인증 = 우리 admin 계정 공유(새 계정 안 만듦) · 호출 = 백엔드 | 사용자 |
| 2026-11-11 | 시술 · 상품 종류 API 미완 — 이번 범위 아님 | 사용자 |
| 2026-11-11 | 메뉴 = 지금 기준(getProducts) · 고객 보유 = KOS 구매 · 시술권 값 그대로(산 시점 유지 확인) — 메뉴로 덮지 않음 | 조사 2 · 3 |
| 2026-11-11 | 메뉴 정가 = 부가세 별도 · 계산(구매)할 때 포함 | 사용자 |
| 2026-11-11 | 시술권 그룹 통계 API 불필요 — 보유 시술권은 남은 것만(`getTicketBundlesQuery`) | 사용자 질문 · 코디 추천 |
| 2026-11-11 | 동작 불변 — 설명 · 예시 · tags · security · 문서용 응답 모델만 추가 | 코디 기본값 |
| 2026-11-11 | KOS 메뉴는 우리 DB 에 **전부** 저장(카테고리 · 상품 · 옵션 · 구성 · 시술 · 진료항목 · 기기/약물 · 모든 칸). 밖으로 내줄 칸은 API 계약에서 따로 | 사용자 |
| 2026-11-11 | 링키 · 차티 니즈: 상품 가격 · 기존 고객 남은 시술권 · 이름+이메일(둘 다 필수)로 예약 · 조회 · 외부 연동용 별도 API + 보안 | 협업자 슬랙 · 사용자 |
| 2026-11-11 | 이름+이메일 조회 = **KOS 이름 검색 → 우리 쪽 이메일 거르기** | 사용자 |
| 2026-11-11 | 조사 4 정할 것 2~8 코디 추천대로 · email 없는 기존 고객 = 「없음」(보조 키 없음 · 예약으로 email 쌓임 · 중복은 데스크 정리) → DEC-010 D-15~D-22 | 사용자(「추천으로 가자」) |
| 2026-11-11 | planner 질문: Q1 외부 예약 중 KOS 중복 고객 검사에 걸리면 예약 안 함 · 409 customer_ambiguous(candidate 없음) / Q2 메뉴 · 시술권 id = KOS id 문자열, 고객 · 예약 id = ccc 정수 / Q3 기본 그룹 env 비었거나 사라지면 예약만 503 ext_not_configured | 코디 기본값(planner 추천) |
| 2026-11-11 | planner Q4: SINGLE 진료항목 id = `getProductOptions` 추가 호출로 채움(DEC-010 D-05 문구 고침) | 코디 기본값 · D-03 |
| 2026-11-11 | planner Q5: 메뉴 응답 칸 = 각 층 id · 기본 이름 · translsMap + 카테고리 order · 상품/옵션 description · 옵션 type · 정가(부가세 별도 · CONSULTATION null) · count · **unit** · 구성 title/count/unit/정가 · 상품 **isEvent**. 그 밖 칸 안 냄 | 코디 기본값(planner 추천 A + unit · isEvent) |
| 2026-11-11 | review-doc r1 DEC 질문 — Q-A 이름 검색 한 페이지(1000) · 넘으면 「없음」 · KOS id 중복 제거 · 우리 쪽 이름 정확 일치(공백·대소문자 무시 · name 또는 phoneticName) / Q-B 예약이 이메일 존재를 드러내는 것 수용 · Swagger 에 명시 / Q-C 시술권 가격 = KOS 묶음 가격(부가세 표기 없음) / W11 syncedAt 유지 → DEC-010 D-16 · D-19 · D-31 고침 · D-35 · D-36 추가 | 사용자 승인(추천안) |
| 2026-11-11 | 사용자: 「코드 구현 배포까지 다하고 api 스웨거도 · 빨리」 → 코드 · 리뷰 · e2e · 배포까지 묻지 않고 진행(SPEC 사용자 리뷰 게이트 생략 승인). planner r2 끝나면 reviewer_doc r2 와 backend 를 **병렬** 발주(`ext-api-be-brief.md`) | 사용자 지시 |
| 2026-11-11 | infra 사실: back env 는 ConfigMap(비밀 아닌 것) + Secret `cc-prototype-secret` envFrom. KOS_* 는 전부 Secret → 새 env 3개(`PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` · `KOS_EXT_RESERVATION_GROUP_ID`)도 **Secret 에 넣고 infra 차트 변경 없음**(배포는 `back.imageTag` PR 하나) | 코디 확인(infra origin/main `ebfcb6c`) |
| 2026-11-11 | 코드 워크트리 `kknaksss/api-swagger-docs` 를 origin/main `c9f30ac` 로 reset(#21 스쿼시 머지와 내용 같음 · diff 0) | 코디 |
| 2026-11-11 | 외부 예약 기본 그룹 = 데모 KOS 「기타」(order 5 · 켜진 구역 1 · 30분). 연동처 키 2개 생성. 값 3개는 `~/.config/cc-prototype/ext-api.env`(chmod 600 · 레포 밖) → 배포 때 Secret `cc-prototype-secret` 에 patch. 그룹은 env 만 바꾸면 교체 가능 | 코디 기본값(사용자 「빨리 다 해」) |
| 2026-11-11 | review-doc r2: N1 키 없는 거절 = client null 인 모든 /api/ext 오류(400 깨진 본문 · 405 포함)에 IP 카운트 · 1분 1줄 / N2 fake_kos 검색 규칙 그대로 · T12 공백은 KOS 가 돌려준 경우만 · 문서에 「띄어쓰기 그대로」 / N3 syncedAt = 실패해도 이전 last_ok_at 유지(① 안) / N4 DEC D-09 · Consequences 고침 | 코디 기본값(검수 추천) |
| 2026-11-11 | **로컬 E2E(데모 KOS · compose -p ccc-ext-e2e · back 8700)**: 메뉴 200(카테고리 15 · 상품 101 · 옵션 323 · syncedAt 있음) · 키 없음/직원 토큰 401 · 조회 3명 200(이메일 대문자+공백도 맞음) · 틀린 이메일 404 · 1글자 이름 404 · 기존 고객 예약 200 · 새 고객 예약 200 → 같은 이름+이메일 조회 200 isNew · 두 예약 직원 API 로 취소 200 · 키당 61번째부터 429 · ext_call 기록(키 없는 401 은 1분 1줄로 접힘) · event_log actor ext:linky · 메뉴 표 9개 행 수 조사 1 과 같음 · Swagger 외부 tag · ExtApiKey. 새 고객 1명(시험 이름 · example.com)은 데모 KOS 에 남음(D-22) | 코디 실물 확인 |
| 2026-11-11 | 코드 검수 r1 WARN 7 → 수정 1 · 2 → r2 PASS(599 passed) · SPEC 0.2.3. 코드 PR #22 스쿼시 `e0e4a16` · Secret patch(31키) · infra #49 `55ea48c`(back.imageTag + env.example 이름) · ArgoCD Synced Healthy · **운영 E2E**: health · /api/docs 200 · ops 73 · 키 없음 401 · 두 키 메뉴 200(15/101/323 · no-store) · 파드 안 조회 200 / 틀린 이메일 404 / 한 글자 404 · ext_call 기록 · 메뉴 9표 행 수 같음. 운영 예약은 안 함(로컬에서 확인) | 코디 |
| 2026-11-12 | 2차 add1: 협업자 요청 3개를 외부 API 로 · 가능 시간대 = 외부 예약 기본 그룹만 · 남은 0 칸 · 지난 시각 제외 · 과거 시술 = 날짜 · 결과 · 시술 이름(메모 · 의사 이름 없음) · 예약 내역 = 오늘 이후 · 상태 포함 · 고객 찾기 = DEC-010 규칙 → DEC-011. 같은 slug 에서 진행(new-work.sh 가 진행 중 slug 있으면 새 slug 거절) · 배포까지 묻지 않고 | 사용자 승인(추천안) |
| 2026-11-12 | **add1 로컬 E2E(데모 KOS · compose -p ccc-ext-e2e · back 8700 · 코드 리뷰 전 판)**: 가능 시간대 오늘 200(15칸 · 지난 시각 빠짐) · 내일 200(20칸 · 30분) · no-store · 어제 / 91일 뒤 / `20261113` / 빈 값 / 없음 → 400 · 키 없음 401 · 기존 고객 2명 과거 시술 200(8 · 3건 · 최신 순 · 메모 · 의사 · 그룹 칸 0) · 예약 내역 200 · 틀린 이메일 404 세 경로 바이트 같음 · 새 고객 예약 200 → 그 칸 남은 자리 3→2 · 예약 내역에 같은 reservationId · reserved · 과거 시술 [] · 직원 API 취소 200 → canceled. 새 시험 고객 1명(example.com) 데모 KOS 에 남음 | 코디 실물 확인 |
| 2026-11-12 | add1 코드 검수 r1 WARN 1 · 경미 3 → 고침 2 → r2 PASS(647 passed) · SPEC 0.3.3 · 코드 PR #23 스쿼시 `0a58aba` · infra #50 `125d3a9`(back.imageTag) · ArgoCD Synced Healthy · **운영 E2E**: health · ops 76 · 두 키 가능 시간대 200(내일 20칸 · no-store) · 키 없음 401 · 어제 400 · 파드 안: 오늘 14칸 · 잘못된 날짜 5가지 400 · 기존 고객 2명 과거 시술 · 예약 내역 200(메모 · 의사 · 그룹 0) · 틀린 이메일 404 세 경로 같은 바이트 · ext_call 새 경로 기록. 운영 예약은 안 함(로컬에서 확인) | 코디 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_017631b3-d1ab-44a0-8ad0-ce0db6b1f236` | `task_7a231fb11084` | `ctx_d84c1f44cd08` | `be-fix-2-instructions.md` | 수정 2판 완료 — 유지 |
| reviewer | `term_d8cdd196-896b-47da-a1ac-21f8ad0a0109` | `task_126589b8c148` | `ctx_bbad1edd912c` | `review-2-instructions.md` | 재검수 PASS 완료 |
| reviewer_doc | `term_910582a6-b1f7-440a-bd00-771330034070` | `task_90e484cc2356` | `ctx_a2cbd9bc4e41` | `api-swagger-docs-review-doc-brief.md` | r1 WARN 완료 — 유지 |
| planner | `term_27edb4d7-d9d2-4754-8b00-602019165dde` | `task_3c80464673a0` | `ctx_ef7ff04672cd` | `api-swagger-docs-spec-brief.md` · r2 `spec-fix-r2-instructions.md`(`task_00fc98ab839b` · `ctx_ebbf87b4068c`) | r2 수정 중 |
| researcher | `term_47223a51-6547-4f31-91c3-45e230b57eb3` | `task_b96e0034362b` | `ctx_3980ba4e9415` | `research-4-instructions.md` | 조사 4 완료 — 유지 |

Run: `run_7bfc5c5180f7`

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- code PR: kknaksss/cc-prototype#21(스쿼시 `c9f30ac`)
- infra PR: MediSolveAIDev/k8s_infra_mac#48(`back.imageTag` c9f30ac · ArgoCD sync Synced Healthy)
- 리포트: `be-report.md`(1판 · 수정 1 · 2판) · `review-report.md`(WARN 34 → 재검수 PASS)

## 5. 이력 (최신이 위)

- `2026-11-11` review-doc r1 WARN — W1 페이지 중복 · W2 페이지 상한 · W3 키 없는 기록 폭주 · W7 구역 0 → 503 · W8 시술권 가격 단정 · W9 actor · DEC 질문 Q-A(짧은 이름) · Q-B(예약이 이메일 존재 노출) · Q-C(가격 칸 이름)

- `2026-11-11` planner done — SPEC-008 0.1.0(경로 3 · X-Api-Key · 시험 T1~T30) · WORK-012(BE1~BE6 → REVIEW → INFRA → E2E) → reviewer_doc r1 발주

- `2026-11-11` 사용자 DEC-010 승인 → accepted · 같은 slug 로 이어감(런북 §1 · new-work.sh 가 새 slug 거부) → planner 발주

- `2026-11-11` 사용자: 「열린 게 왜 남아 있지」 → DEC-010 열린 것 0 — D-27~D-34 추가(메뉴 응답 · 고객/예약 계약 · 호출 제한) · 비율 · 수정 유지는 결정에 무관으로 정리

- `2026-11-11` 사용자: 메뉴 DB 전부 저장 · 링키 니즈(가격 · 남은 시술권 · 이름+이메일) · 이름 검색 → 이메일 거르기 결정 → 조사 4 발주
- `2026-11-11` 조사 4 done — 그대로 가능(내부 API 필수 · 공개 API 엔 email 없음) · 데모 email 1% · countInPage 20 이면 21건↑ 놓침

- `2026-11-11` 사용자: 구조 갱신 — 상품에 고객 연결 필요 · 「산 고객은 산 시점 상품」 우려 → 조사 2 발주
- `2026-11-11` 사용자: 시술/상품은 KOS 공개 API 로 · 깊이 확인 요청 → researcher 발주
- `2026-11-11` 재검수 PASS(N1 경미 → 수정 2판) → #21 머지 · infra #48 · 운영 `/api/docs` 200 확인
- `2026-11-11` 수정 1판 done(34 고침 · 544 passed) → 재검수 발주
- `2026-11-11` review WARN 34(`review-report.md`) → backend 수정 1판 발주
- `2026-11-11` backend done — 70 op · 683 필드 설명 · 구조 변화 0 · 버그 목록은 be-report §7(범위 밖) → reviewer 발주
- `2026-11-11` 협업자 요청(호출 도메인 · 인증 · API 설명 · 반환값 정의 · 시술/상품 API) → 세팅 · backend 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
