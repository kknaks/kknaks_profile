
# 재개 노트 — ext-api-charty1 (cc-prototype)

**지금**: 운영 배포 끝 — 코드 #24 `969f44f` · infra #60 `88220d5` · Synced Healthy · 운영 읽기 경로 확인(board · clinic · staff · menu · 상세 · lookup 200 · 키 없음 401 · ext_view 2 · consult_wait_first 6/6) · 운영 DB 사본 `/data/procedure.db.bak-20261116-charty1` · 개발자 안내문 전달
**다음**: 문서 PR(profile · deploy.md 기록 줄) → 마감(archive-work.sh · 회고 · 개념) · charty 에 없는 칸 회신(예산 · 동행자 · 통역 · 진단 · 시술권 만료일) · 로컬 e2e 서버(18700) 끄기 · 워커 터미널 정리

세팅: `scripts/new-work.sh cc-prototype ext-api-charty1` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_aad33590-4323-443d-9c17-3541475ee5f5`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] planner — DEC-012 · SPEC-008 0.4.0 · WORK-014 (API 8개)
- [x] reviewer_doc r1 = FAIL(`review-doc-r1.md`) · 사용자 답 받음
- [~] planner 2차 수정(`spec-fix-r2-instructions.md`) → reviewer_doc r2
- [x] 조사 결과로 항목별 추천표 → 사용자: 승인 묶음 / 최종 판단(3-8 직원 구분 · 1-2·3-2 D-03 넘기 = 연동처별 권한 · 1-3·4 외부 쓰기 범위 · 3-4 시술권 차감 범위)
- [ ] 승인 뒤 DEC-012 → SPEC-008 0.4.0 → WORK-014 → reviewer_doc → backend → reviewer → 데모 KOS 실호출 → 코드 PR → infra imageTag PR → sync → 운영 확인 → 문서 PR · 마감
- [!] 오더 메모 HAR 없음 — 조사에서 못 찾으면 사용자에게 받는다
- [!] 로컬 profile main(#125) · cc-prototype 체크아웃(dbf0b53)이 뒤처짐 — 사용자 pull 필요. 워커는 `git show origin/main:` 로 읽음

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-16 | 구조는 KOS → CC → 서비스. 값은 CC 가 KOS 에서 가져온다 · 기존 ext 에 있는 건 필드 추가 | 사용자 |
| 2026-11-16 | 이번 쓰기는 지금 구조 그대로 — KOS 먼저 쓰고 CC 는 event_log · 사본 갱신. 「KOS = 저장소 · CC 가 원본」 전환은 고도화 버전에서(이번 범위 밖) | 사용자 |
| 2026-11-16 | API 목록 = lookup 수정 1 + 새 4(board · 예약 상세 · 언어 · 오더 메모) + 차트 메모(charty 답 뒤) | 조사 `research-charty1-sources.md` · 사용자 |
| 2026-11-16 | **권한 분기 없음** — 프로토라 ext 전부 연동처 공통(linky · charty). DEC-011 D-03(메모 · 의사 미노출) · 이름+이메일 필수는 이번에 푼다. 권한 · 원본 전환은 별도 고도화 작업에서 | 사용자 |
| 2026-11-16 | 「차트 메모」 = 상담 메모(공개 `updateScheduleConsultationInfo`) — 오더 메모 · 상담 메모 쓰기 | 사용자(「오더 메모 상담 메모」) |
| 2026-11-16 | 병원 정보 · 직원 목록 API 추가. 외주 직원 = KOS 계정(CS팀 · 콜센터 역할) — CC 별도 저장 없음 | 사용자 |
| 2026-11-16 | 코디 기본값 통보: 열람 기록 = 헤더 직원 id → event_log(신고값 · 검증 없음) · 시술권 차감 제외 · 직원 목록 `clinics/{clinicId}/staff` · 2-3 은 예약 이력 HAR 받을 때까지 열림 | 코디 기본값 |
| 2026-11-16 | 2-3 첫 상담 대기 시각 원천 = KOS 단계 변경 이력. (11-16 바로잡음: 이 결정을 받치는 HAR 은 없다 — 이력 호출은 KOS 웹 JS 로만 봄. 경로 `get-schedule-event-logs` · 저장 규칙은 코디 기본값) | 사용자 |
| 2026-11-16 | r1 답(「추천대로」): DQ1 원천=사용자 · 경로/저장=코디 · DQ2 이력 조회 대상 = 접수 뒤 일정 전부(CC 판정 아님) · DQ3 DEC-010 D-12 고침 명시 · DQ4 선불카드 실패여도 lookup 200 + `prepaidCards` null + 부분 실패 칸 · DQ5 상세에 오더 · 상담 메모 넣음 · DQ6 차감 제외 = 코디 기본값 · Q2 병원 칸 = 이름 · 주소 · 전화 · 운영 시간 · 휴무만 · 나머지 Q 는 planner 제안 | 사용자 |
| 2026-11-16 | 코디 기본값(로컬 e2e 2): KOS 는 상담 메모를 `""`·`null` 로 못 비움(200 인데 그대로) → 상담 메모 빈 값 = 400 · 오더 메모는 비움 그대로 · 예약 직후 상세 404 는 Swagger 안내 한 줄만 | 코디 기본값 |
| 2026-11-16 | 코디 기본값(로컬 e2e): 내부 시술권은 거르기 먼저 · `price` 객체에 `value` 없음 = 0(protobuf 0 생략 · 데모 실물) · `price` 없음/숫자 아님은 502 그대로 | 코디 기본값 |
| 2026-11-16 | 코디 기본값(코드 r1): Q1 처음 봄 때 이미 귀가면 ⓒ 겸함 · Q2 고객 없음 = 404 또는 400+NotFound → `customer_not_found` · Q3 상세 `customerId` 사본 없으면 null · W5 board 의 event_log 읽기를 그날 예약 id 로 거름(이번에 고침) · W3 · W4 시험 보강 | 코디 기본값 |
| 2026-11-16 | 코디 기본값(KOS0 `kos0-report.md`): D-16 그대로(D-17 안 씀) · `eventType` 끝 조각 `FlowStepChanged` · `flowStep` 문자열 · 원소 시각 최솟값 · `daysOff` = `{startDate, endDate}` KST 날짜(KOS 에 이름 없음) · 선불카드 금액 객체 확인 · 내부 시술권은 다 쓴 묶음도 줌 → 우리가 거름 | 코디 기본값 |
| 2026-11-16 | 코디 기본값(planner Q17): 귀가 뒤 1번이 실패하면 실패 재시도(≤3)가 받는다 | 코디 기본값 |
| 2026-11-16 | 코디 기본값(r2 DQ7): DQ2 「한 번씩」 뜻대로 첫 상담 대기 재조회는 사건 때만 — 처음 접수 뒤 1 · 못 찾음 뒤 상담 대기 새로 관찰 1 · home 뒤 1 · 실패만 5분 재시도(일정당 하루 3). 「못 찾음 → 5분마다」 버림. 겹친 요청은 시도 예약(먼저 기록) | 코디 기본값 |
| 2026-11-16 | 코디 기본값(planner Q15 · Q16): Q15 board `partialErrors.consultationHistory` = 대상 줄 중 null 이면서 마지막 시도 실패이거나 요청당 상한으로 못 부른 줄이 있을 때(못 찾음만은 안 넣음) · Q16 귀가 등 끝난 단계로 간 일정은 그 뒤 1번 더 부르고 멈춤(호출 줄이기) | 코디 기본값 |
| 2026-11-16 | 코디 기본값: 첫 상담 대기는 찾은 값만 굳힘 · ~~못 찾음/실패는 일정마다 5분 간격 재시도~~(11-16 뒤집음: r2 DQ7 — 못 찾음은 사건 때만 · 실패만 5분 재시도 ≤ 3) · 요청당 상한 · 날짜 지나면 멈춤. 열람 헤더는 lookup · 상세 · 쓰기에만 · lookup 은 틀린 헤더를 없는 것으로 · 새 경로는 400 · `@` 뺌 | 코디 기본값 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_623737c8-c73b-4d48-a30c-244d3c8521de` | `task_e931e79dfff9` | `ctx_18c37a39a117` | `planner-r6-spec.md`(= 원 브리프 + `spec-fix-e2e1-instructions.md`) | 6차 진행(옛 터미널 죽음 → 재기동) |
| ~~reviewer_doc~~ (터미널 죽음 · r3 PASS 로 끝) | `term_7afd8629-5aa7-426f-add3-72325ed1f994` | `task_15bb6725ba54` | `ctx_ba981fd5ecd0` | `ext-api-charty1-review-doc-brief.md` · `review-doc-r3-instructions.md` | r3 PASS · 대기 |
| backend | `term_0729bfce-b08e-41e2-9218-165f550e86ed` | `task_02c119230711` | `ctx_5931eaf6e8f1` | `ext-api-charty1-be-brief.md` | 완료 · 대기 — 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-charty1` (`kknaksss/ext-api-charty1`) |
| reviewer | `term_a1d4dd8c-fb2e-484e-977f-a305b43f844e` | `task_14fef94c58f0` | `ctx_8b7d377d2de3` | `ext-api-charty1-review-brief.md` | 진행 — `review-code-r1.md` |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
