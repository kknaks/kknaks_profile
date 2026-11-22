# [researcher] 새 HAR 7개로 2차 「확인 안 됨」 메우기 · 예약 현황 · 병원 설정 경로 대조

너는 **day `researcher` 워커**다. **맥락이 없다고 가정하라.** 먼저 읽을 것:

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:AGENTS.md`
- **앞 판 리포트 2개** — `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-cc-ext-report.md`(1차 · ext API) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-report.md`(2차 · KOS 키 전수 — **판정 기준 · 표 형식 · 부록 A 스크립트 방식을 그대로 따른다**)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2 결정 표 — 사용자 2026-11-20 결정(「KOS 키 다 저장」 · 미래 일정 + **예약 현황 화면** · 칸 정원은 병원 설정에서 · 병원 설정 그대로 DB · 통화 KOS 와 같게 · CARD 매핑 · created_at ← KOS)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig` (코디네이터와 공유 — 리포트 1개 외에 만들거나 고치지 마라)
DAY 코드 기준: `origin/dev` = `844eace4`(fetch 해서 새로우면 새 sha 를 적고 그걸 쓴다).

## 1. 원천 — 새 HAR 7개 (사용자 2026-11-20 KOS 데모 테넌트에서 캡처)

`/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/reference/2026-11-20-day-cc-mig/har/` — gitignore 라 git 에 없다. 파일 그대로 읽기만.

| 파일 | 사용자가 한 일(2차 리포트 뒤 코디가 요청한 목록 기준) |
|---|---|
| `예약현황.har` | 예약 현황 미래 날짜 · 예약 그룹 정원 · 그룹 휴무 |
| `병원설정.har` | 병원 설정 — 기본 휴무 · 언어 · 운영 시간 |
| `예약등록.har` | 예약 등록 — 희망 시술(옵션 · 시술권) · 희망 의사 · 귀가 희망 시각 |
| `상담기록.har` | 상담 기록 — 상담 시술 · 상담사 · 원장 여러 명 |
| `시술결제환불.har` | 시술 · 결제 · 환불 관련(데모라 결제 승인은 안 된다 — 사용자) |
| `시술기기약품.har` | 약품 · 기기가 든 상품 옵션 · 수가 유형별 가격 |
| `예약내역.har` | 고객 상세 — 예약 이력 · 문진 · 일정 변경 이력 |

각 파일이 실제로 무엇을 담았는지는 위 설명을 믿지 말고 HAR 안 경로로 확인하라.

**범위에서 뺀 것(사용자 2026-11-20)**: 시술 타이머 · 리액션 — 「KOS 타이머 안 쓴다」 → `taskTimers[]` · `reactions[]` 는 대조하지 않고 「사용 안 함(사용자)」으로 적는다. 로그인 세션 관리 화면은 KOS 에 없다 → `get-active-sign-ins` 는 HAR 로 못 본다(2차 그대로 「확인 안 됨」 · 사유 갱신). 결제 승인은 데모라 불가 → 앱 결제 · 간편결제의 KOS 문자열은 모른다(지어내지 마라 · 화면 근거 `reference/2026-11-20-day-cc-mig/2026-11-20-kos-payment-screen.png(기본 체크아웃 · 개인정보 · 커밋 안 함)` — 결제 수단 6개: 카드 · 현금 · 계좌이체 · 앱 결제 · 간편결제 · 선불카드).

## 2. 조사

- **N1. 새 HAR 경로 목록** — 7개 파일의 읽기(queries) 경로 · 엔트리 수 · 200 수. 2차 P01 ~ P34 · K1-2(HAR 에만 43) 중 어디에 해당하는지, 둘 다 아니면 「새 경로」.
- **N2. 2차 「확인 안 됨」 · K5 재판정** — 2차 K3-3(24키) · K5-1(6경로) · K5-2(11) · K5-3 #2 ~ #5 를 새 HAR 로 다시 본다. 항목마다: 이번에 봤나(HAR 파일#엔트리) · 본 키 경로 · 모양 · 2차 판정 기준의 판정. 못 봤으면 「여전히 확인 안 됨」 + 이유.
- **N3. 기존 경로의 새 키** — P01 ~ P34 경로가 새 HAR 에 있으면 2차 합집합에 없던 **새 키만** 2차 K2 형식으로(키 · 모양 · DAY 칸 · 판정).
- **N4. 예약 현황 · 칸 정원 · 병원 설정 재료** — 사용자가 예약 현황 화면을 만들고 칸 정원을 병원 설정에서 가져온다고 정했다. 이에 필요한 **내부 경로**(예약 그룹 정원 · 그룹 휴무 · 기본 운영 시간 · 기본 휴무 · 미래 날짜 일정 · 칸/슬롯 관련 내부 경로)를 모아 키 전수 대조(2차 K2 형식). 공개 경로 P28(`get-reservation-slots-by-groups`)을 대신할 내부 경로가 있는지 · 같은 정보(정원 · 예약 수)를 주는지 사실만.
- **N5. 고객별 일정 · 문진 · 일정 이력의 내부 경로** — 공개 P29 · P30 · P31 과 내부 P32 를 대신할 내부 경로(예: `get-schedule-list-items` · `get-questionnaire-submit/legacy` 등)를 키 전수 대조. 공개 경로와 같은 정보인지는 cc 코드(`/Users/kknaks/git/toy_pr2/cc-prototype` `origin/main` — 공개 경로 응답을 읽는 곳)와 대조해 사실만.
- **N6. 결제 화면 경로** — `get-payment-settings` · `initialize-purchase`(읽기라면) · 그 밖 수납 화면 읽기 경로의 키 · 결제 수단 · 결제 단말 설정이 어떤 모양인지. 쓰기(commands)는 목록만.
- **N7. 갱신 집계** — 2차 요약 표의 수(판정별 · DB 확장 후보 테이블별 · 확인 안 됨)가 이번 결과로 어떻게 바뀌는지 「2차 → 3차」 두 칸으로. DB 확장 후보 표(K3-2)에 새로 들어오는 행은 테이블별로.
- **N8. 정할 것** — 사용자 판단이 필요한 것만. 2차 K6 과 겹치면 번호. 결정하지 않는다.

## 3. 계약

해당 없음. 산출물은 리포트 1개.

## 5. allowed_paths

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-3-report.md`
- 파싱 스크립트는 네 scratchpad 에만 · 부록에 명령 기재.

## 7. 범위 제약 — 하지 말 것

- **HAR 에는 실제 개인정보 · 토큰 · 쿠키가 있다. 값을 한 글자도 리포트에 옮기지 마라** — 키 경로 · 타입 · 모양 · KOS 코드값 enum 만. 요청 헤더 · Authorization · Cookie 는 읽지도 적지도 않는다.
- HAR 이동 · 복사 · 수정 금지. 사본 남기지 마라.
- KOS · DAY 서버 실호출 금지. 레포 수정 · 커밋 금지. 설계안 · 마이그레이션 초안 금지.
- 근거 없는 판정 금지 — 「확인 안 됨」.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · HAR 파일#엔트리). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 새 HAR 파일 수 7 · 경로별 스크립트 키 수 = 표 행 수(빠진 키 0).
- 리포트 맨 위 요약: N1 경로 수 · N2 메운 항목 / 남은 항목 · N3 새 키 수 · N4 · N5 · N6 경로와 키 수 · N7 2차 → 3차 · 정할 것 수.
- 리포트에서 이메일 · 전화 · 한글 이름 꼴 값 grep 0 (명령 · 결과 부록).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_749389fa-9664-4aac-990c-c765f0ea2c5a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료(3차 · 새 HAR 대조): <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
