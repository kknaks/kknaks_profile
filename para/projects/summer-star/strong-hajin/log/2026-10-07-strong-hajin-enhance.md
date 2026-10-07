# 작업 요약 — strong-hajin-enhance (strong-hajin)

기간: `2026-10-07` ~ `2026-10-07`
결과: 머지·운영 반영·dmg 공증·운영 E2E·2루프 반영까지 완료 (코드 PR #16 `5c8345e` · #17 `d2a06fa` · 문서 #85 · #86 · 인프라 MediSolveAIDev/k8s_infra_mac #12 · #13)

## 1. 무엇을 했나

운영(`ax.medisolveai.xyz`)·데스크톱 앱(medi-ax)을 쓰며 쌓인 개선 20건(SH-IMP-001~020)을 사용자와 항목별로 논의해 방향을 정하고, BE·FE 읽기 전용 조사와 코디의 운영 DB·로그 확인으로 원인을 확정했다(회의록 「누락」 은 누락이 아니었고, 기한 10/06 은 같은 날 다른 회의의 전날이었고, 메일 이미지는 프록시가 SVG 를 거절한 것이었다). BASE-008 → DEC-009(결정 37) → SPEC-008 v0.6.0 · SPEC-010 · WORK-012 로 내리고, WP1 운영 버그 → WP2 회의록 생성 고도화(단계별 timeout · AI 맥락 목록 · 정정 pass · 용어 보정 표) → WP3 AX 흐름(회의실 셀렉트 · Connect 방 변경 · AX 회의 생성/수정 카드) → WP4 메시지함 → AX(호버 막대 · 메일 AX 단추 · 메시지 맥락) → SHELL 을 WP 마다 구현·코드 검수·관련 시험으로 쌓았다. 1루프를 일반 머지로 운영에 반영해 운영에서 E2E 를 했고, 지적 4건(E-2 · E-3 · E-4 · E-6)을 같은 브랜치 2루프로 고쳐 다시 반영했다. 019 화자 분리는 보류했다.

## 2. 적용한 기술·개념

- **CLI 프롬프트를 argv 대신 stdin 으로** [[argv-length-limit]] — 회의록 최종 합성에 재전사 전량 + AI 맥락 목록을 매번 싣게 되면서 프롬프트가 커졌다.
  - 왜 이걸 골랐나: 검수가 「argv 한 칸 128KiB(리눅스 `MAX_ARG_STRLEN`)」 를 짚었고, BE 가 셈해 보니 **이번 운영 회의 크기(23.5분)만으로도 169KB** — 배포했으면 첫 회의부터 합성이 실패했다. 크기를 줄이는 쪽(요약·잘라 싣기)은 정정 pass 의 원문을 잃는다
  - 무엇이 어려웠나: 로컬 CLI(Codex 0.160 · Claude 2.1.284)로 확인했는데 운영 이미지는 Codex 0.146 이었다 — 운영 파드에서 `echo … | codex exec -` 실호출로 `STDIN_OK` 를 받고서야 닫았다. 같은 판에 stdin 이 안 되면 옛 argv 호출로 되돌아가는 `TypeError` 낱말 맞추기가 있어 **프로세스가 두 번 뜰 수 있는** 결함도 검수가 잡았다
  - 근거: `backend/src/ax_workspace/platform/cli_process.py` · `W/be-wp2-fix1-report.md` · `W/review-wp2-r2-report.md` W-r2-3
- **AI 맥락 목록 = 테이블이 아니라 호출 때 DB 조회** [[context-catalog-injection]] — 회의록(중간·최종·용어 보정 근거)과 AX 업무 생성이 같은 목록을 받는다(프로젝트 전부 · 완료·취소 안 된 업무 · 구성원 전부).
  - 왜 이걸 골랐나: 메디니스 동적 카탈로그(서버 전량 주입)를 보고 왔다. 도구 조회만으로는 AI 가 제목 부분 일치·상한 없는 목록에서 연관 업무를 놓쳤다(조사 017). 「카탈로그」 라는 말이 별도 테이블로 들려 사용자가 막았다 — 이름을 「AI 맥락 목록(호출 때 DB 조회)」 으로 바꿨다
  - 무엇이 어려웠나: 코디가 「호출자 시야」 로 기본값을 좁혔다가 사용자 결정 「전부」 와 어긋나 검수가 잡았다(정정). AX 대화에 「매 턴」 실으면 세션 기록에 쌓여 **세션 첫 턴·새 세션에만** 싣는 것으로 바꿨다
  - 근거: `WorkflowApplication.ai_context_catalog` · DEC-009 D-13 · SPEC-010 OQ-1002
- **최종 합성 = 정정 pass → 다시 쓰기 + 용어 보정 표(null / [] / 행)** [[transcript-term-correction]] · [[synthesis-rewrite]] — 메디니스 방식을 가져왔다.
  - 왜 이걸 골랐나: STT 오인식(「세라믹 홈페이지」 · 「캐스티」)이 회의록에 그대로 남았다. 등급(auto = 고유명사 치환 · presumed = 인명·숫자·일정은 표에만)으로 틀리면 피해가 큰 범주를 막는다
  - 무엇이 어려웠나: 「정정이 안 돎」 과 「돌았는데 바꿀 게 없음」 을 화면에서 가르려 했는데 행 표로는 둘 다 0행 — 회의에 `term_corrected_at` 을 둬서 갈랐다(검수 r2 N-1)
  - 근거: `migrations/manual/2026-10-07-meeting-term-corrections.sql` · SPEC-010 §4.7
- **같은 카드의 다음 회차(v+1)로 고치기 — 누가 고치든 같은 「수정」** [[proposal-revision]] · [[human-in-the-loop]] — AX 가 초안을 고치는 길.
  - 왜 이걸 골랐나: AX 초안을 채팅으로 못 고쳤다(E-6). 처음엔 「옛 카드 닫고 새 카드」(대체형)로 정했는데 새 상태값(`superseded`)이 필요했다. 메디니스 워크플로우 런의 안건 교정(`merge_intake_patch` → Subject v+1 · 같은 카드 재상정)을 보고, 우리 카드에 **이미 회차가 있다**는 것을 다시 봤다 — 사용자: 「AX 가 수정하든 사람이 수정하든 수정 아니야?」 → 사람의 `save_draft` 를 AX 에게도 열고, 서버가 **바뀐 칸만 지금 회차 위에 덮는다**(모르는 칸 422)
  - 무엇이 어려웠나: 원인은 `mcp.py:460` 이 「AX 가 자기 제안을 확정하지 못하게」 하려고 `ax.*` 항목의 **모든** 명령을 막은 것 — 수정까지 막혔다(업무도 같았다). 거절이 `ToolError` 가 아니라 사유 없는 오류로 가서 모델이 같은 호출을 4번 되풀이했고 실행 기록은 「failed」 뿐이었다
  - 근거: `entrypoints/mcp.py` · `platform/action_center.py` `_save_draft` · `W/be-loop2-report.md` · `W/be-loop2-e6b-report.md`
- **동시성 — 합성 lease 와 웜스타트 경주** [[job-lease]] · [[optimistic-lock]] — 최종 timeout 900초 × 최대 5호출을 담는 lease 바닥 6000초 + heartbeat 연장 · 웜스타트를 회의 락 안으로 + 세션 기록 CAS.
  - 무엇이 어려웠나: 시험이 「셈식」 만 단언해 루프의 실제 최대 호출 수와 어긋났다 — 최악 경로를 돌려 센 호출 수와 셈을 대조하는 시험으로 바꿨다. heartbeat 예외가 루프를 끊어 합성이 고아가 되는 것도 재검수가 잡았다
  - 근거: `bootstrap/meeting_worker.py` · `modules/meetings/batch_service.py` · `W/review-wp2-code-report.md` F-1 · F-2
- **운영 SQL 은 칸(트랜잭션) → 이미지 → 인덱스(CONCURRENTLY) 세 판으로** [[online-schema-change]] · [[database-index]] — 칸 추가와 `tasks` 인덱스가 한 파일에 섞여 있으면 `psql -1` 로 통째로 돌릴 때 `tasks` 쓰기가 막힌다(검수 WP4 W-2). 칸 판 · `.concurrent.sql` · 격리판으로 갈라 머리에 순서를 적고, 운영은 그 순서로 적용했다(인덱스 `indisvalid=t` 확인)
  - 근거: `migrations/manual/2026-10-07-inbox-message-origin*.sql`

## 3. 막혔던 것 / 사고

- **코디 핸들이 죽었다 살아났다** → new-work.sh 가 env 핸들을 stale 로 보고 list 에서 다른 핸들을 골라 브리프에 박고 워커에게 「preamble 의 값은 stale」 이라고까지 알렸다. 몇 시간 뒤 그 핸들이 죽고 env 값이 다시 살아났다(워커 핸들도 셋 다 바뀜) — `terminal send` 가 `terminal_handle_stale` 로 튕겨서 알았다. 정정 메시지 · 브리프·_RESUME 일괄 치환 · 이후 발주 직전마다 `terminal list`. 인박스 `[Reply: … --from]` 값이 처음부터 진짜였다
- **결정과 다른 구현을 문서에 받아 적었다** → 회의실을 드롭다운 셀렉트로 정했는데 FE 가 라디오 카드로 만들었고, 검수 W-8 이 짚은 것을 코디가 「화면은 라디오 목록」 으로 SPEC 에 적고 넘어갔다 — 운영 E2E 에서 사용자가 잡았다(E-3). 검수가 「결정과 다르다」 를 짚으면 SPEC 을 고칠 게 아니라 코드를 결정에 맞춘다
- **좁은 서랍 폭을 시험이 못 본다** → AX 회의 수정 카드가 서랍에서 가로로 몰려 깨졌다(E-4). DOM 시험은 통과했다 — 폭은 앱 실물로만 보인다
- **E2E 중 새 버그에 수정까지 발주했다** → 사용자 「원인부터 확인하라고, 구현은 나중에」. 원인 확인 브리프만 내고, 방향은 원인을 보고 정한다
- **원인 가설이 틀렸다** → E-6 을 「회의 draft 모양이 판정 함수와 안 맞음」 으로 짐작했는데 실제는 위임 턴 일괄 거절이었다. 재현 시험으로 가렸다
- **WP 마다 전체 시험** → 워커와 코디가 각자 `make test`(4~5분)를 돌려 겹쳤다. 사용자 지시로 WP 마다 관련 시험만, 전체는 마지막 한 번으로 바꿨다. 마지막 전체 검증이 WP4 새 칸(`label`)을 정확 비교하던 기존 시험 1건을 잡았다
- **병렬 vitest 가 로컬 스택을 죽인 전례** → 프론트 전체 시험은 `--no-file-parallelism` 직렬로만 돌렸다

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-07 | 항목별 방향 — DEC-009 결정 37 · OQ-901~909 · SPEC OQ 812~819 · 1001~1017(코디 기본값 · 사용자 통보) | 사용자 논의 · 조사 리포트 |
| 2026-10-07 | 완료 판정은 데스크톱 앱 실물 — 웹 확인은 서버 쪽 근거일 뿐 | 사용자 질책(007) |
| 2026-10-07 | 014 받기 = UI 그대로, `download`·`_blank` 를 빼 회의록 내보내기와 같은 셸 길 · 받기는 `attachment` | 사용자 · FE 조사 |
| 2026-10-07 | 018 원격 SVG 허용(inline + sandbox CSP + nosniff) | 운영 로그 · 사용자 |
| 2026-10-07 | AI 맥락 목록 = 프로젝트 전부 · 완료 안 된 업무 · 구성원 전부(호출 때 DB 조회) · ~~호출자 시야~~(코디 기본값이 틀림 — 검수) · ~~매 턴~~ → 세션 첫 턴·새 세션에만 | 사용자 D-13 · 검수 |
| 2026-10-07 | 001 AX 회의 생성 = 업무 생성과 흐름·디자인만 같게, 내용은 회의 고유 필드 | 사용자 OQ-901 |
| 2026-10-07 | 008 메일로 좁힘 · 수동 [AX 업무 생성][AX 요약] 먼저 · 자동 추천은 같은 로직을 이벤트로(다음) | 사용자 |
| 2026-10-07 | 검증 = WP 마다 관련 시험만 · 전체 `make verify` 는 마지막 한 번 | 사용자 |
| 2026-10-07 | E2E 는 운영에서 · PR 은 일반 머지(스쿼시 아님) · 같은 브랜치로 2루프 | 사용자 |
| 2026-10-07 | ~~E-6 = 옛 초안 닫고 새 초안(대체형 · superseded)~~ → AX 도 같은 `save_draft` → 같은 카드 다음 회차 · 바뀐 칸만 덮기 · 확정·거절은 사람만 | 사용자(같은 날 뒤집음 — 회차가 이미 있다) |
| 2026-10-07 | 019 화자 분리 보류 · 013 ① 범위 밖 | 사용자 |

## 5. 날짜별 로그

- `2026-10-07` improvements 17건 항목별 논의 → BE·FE 조사 · 운영 DB·로그 확인 → BASE-008 · DEC-009 → SPEC-008 v0.6.0 · SPEC-010 · WORK-012(검수 FAIL 5→1→0)
- `2026-10-07` WP1 `e51fe3b` · WP2 `e58fb25` · WP3 `cfc2e1c` · WP4+SHELL `90788ab` — WP 마다 코드 검수
- `2026-10-07` 전체 검증 → PR #16 · #85 일반 머지 → 운영 SQL 칸 → 이미지 `5c8345e` → Argo → 인덱스 CONCURRENTLY → 운영 Codex stdin 실호출 → dmg 공증
- `2026-10-07` 운영 E2E 지적 E-2 · E-3 · E-4 · E-6 → 2루프 PR #17 `d2a06fa` → 인프라 #13 → 운영 반영 · 문서 마감 #86

## 6. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/85 · https://github.com/kknaks/kknaks_profile/pull/86
- code PR: https://github.com/kknaks/Strong_hajin/pull/16 · https://github.com/kknaks/Strong_hajin/pull/17
- 인프라 PR: MediSolveAIDev/k8s_infra_mac #12 · #13
- 커밋: 문서 `e87e9ef` · `a19e4c8` · `7941bea` · `6129b09` · `1313089` / 코드 `e51fe3b` · `e58fb25` · `cfc2e1c` · `90788ab` · `cc5d46d` · `6e6bb3f`
- 리포트: `be-survey-report.md` · `fe-survey-report.md` · `review-spec-work-report.md` · `review-spec-work-r2-report.md` · `review-wp1~4-code-report.md` · `review-wp2-r2-report.md` · `review-wp3-r2-report.md` · `review-loop2-report.md` · `e2e-feedback-batch-1.md` · BE/FE WP·수정 리포트들
- dmg: `~/Downloads/medi-ax_0.0.1_arm64-enhance.dmg`(서명·공증 Accepted)

## 7. 잔여

- **E-6 목록 칸**(검수 2루프 W-1): 참석자·체크리스트는 「목록 전체 교체」 를 프롬프트로만 지킨다 — AX 가 추가분만 보내면 기존이 빠질 수 있다. 운영에서 「참석자 추가」 실물 확인 뒤 필요하면 추가·삭제를 따로 받는 서버 안전장치
- 2루프 검수 WARN: W-2 회차의 「AX 수정」 표지 응답 미노출 · W-3 드롭다운 줄에 정원 · 그 밖 경미 셋
- WP 검수에서 2루프로 넘긴 것: 웹 같은 탭 받기 실패 화면(WP1 W-1) · 422 `detail` 문구(WP1 W-6) · 메시지함 사건 뒤 최신 페이지만 다시 읽음·짚기 3쪽 한도(WP4 W-4) · AX 수정 카드 사외 참석자 입력 모양(WP3 W-7)
- SPEC-006 「이동 허용」 개정 — 셸이 프레임을 못 가려 주 프레임 `about:*` 도 허용(근거 넷, WP4 W-5)
- 슬랙 앱 user events 구독 7개(나간 방 계열) 운영 설정 — 사용자
- 008 메일 자동 추천(같은 맥락 조합 로직을 메일 도착 이벤트로) · 업무 「업데이트」 추천
- 보류: 019 화자 분리(Soniox 옵션 · 메디니스 방식) · 013 ① 이름 없는 방
- 데스크톱 최종 관문 G5 증거 파일(M-5 로그인 유지 등) — 사용자 확인 뒤 `resolved`
