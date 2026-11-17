
# 재개 노트 — consult-layer1 (consult-analysis)

**지금**: 마감 — WORK-001 · 002 done · 보고서 accepted · stats meta 0.3.0 · reviewer WP6 생략(사용자 정리 지시 2026-11-17) · 차트 https://claude.ai/artifact/5UqayvZkQedPhAibo1m6eW
**다음**: PR 머지 → ignored(data · reference) 메인 로컬로 → archive-work.sh → 회고 · 개념

세팅: `scripts/new-work.sh consult-analysis consult-layer1` · 설정 SSOT `config/projects/consult-analysis.json`
코디handle: `term_1e2044b5-cf36-479a-9750-9d7adba63b4c`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- 코디 = 워커 공용: `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석` (브랜치 `kknaksss/상담데이터분석`) — 워커 전부 workspace=coordinator, 직렬만
- run: `run_4a3678c55634`


## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] planner — SPEC-001 · WORK-001
- [ ] SPEC 사용자 확정 → etl 발주(스크립트 `scripts/` · DB `data/`) → reviewer
- [!] 레포 PUBLIC — 고객 이름 · 본문 · 사진 금지. 원본 · DB 는 gitignore(`.gitignore` 반영, 미커밋)
- [!] 2층(언어 · 국적 · 예약 단계)은 1층 건수 일치 뒤(DEC-001 D-11)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-16 | 개인 프로젝트 `consult-analysis` 신설 · SQLite 로컬 · 스크립트는 프로젝트 `scripts/` | 사용자 「개인 프로젝트야」 · 「db는 로컬 sqlite, 파서랑 스크립트 다 개인 프로젝트에」 |
| 2026-11-16 | DEC-001 accepted — 두 층 분리 · 예약 성공 = 고객 예약표 회신 · 국적 출처 순서 · 1층 먼저 | 사용자 「응 !!」 |
| 2026-11-16 | DEC-002 accepted — 2층 판정 · 분석 | 사용자 「결과 달라고 이거 하는 거 아니야? 데이터 분석 한다니까」 |
| 2026-11-16 | SPEC-001 0.2.0 accepted — 분석 중심은 고객 문의 · 우리 계정은 발신 구분용 | 사용자 「응 … 고객문의 데이터가 중요한 거야」 |
| 2026-11-16 | D-12 reaction 테이블 · D-13 폴더 밖 JSON 포함 · D-14 페북 메신저 포함 · D-15 채널 칸 | 사용자 「응 그리고 어떤 메신저로 왔는지도 필요」 · OQ-101/102 권장안 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| etl (opus) | `term_9302817b-ff80-4ec8-a40d-24df9ca10071` | `task_d523320479c7` | `ctx_5567cfea4b30` | `consult-layer1-etl-l2r2-brief.md` | 진행 (라벨 전체 · stats · 보고서) |
| planner (fable) | `term_6fdf42b4-b64e-4bc5-b01b-0fcd8b0de135` | `task_fb3fc4f86c1b` | `ctx_7e916e05f4bd` | `consult-layer1-spec-l2r2-brief.md` | 완료 (SPEC-002 0.2.0) |
| etl (opus) | `term_9302817b-ff80-4ec8-a40d-24df9ca10071` | `task_b43cf2c3d636` | `ctx_344f1c4afa2b` | `consult-layer1-etl-l2-brief.md` | 완료 (WP1~WP3 표본) |
| planner (fable) | `term_6fdf42b4-b64e-4bc5-b01b-0fcd8b0de135` | `task_1220061f64d4` | `ctx_62408e5a19de` | `consult-layer1-spec-l2-brief.md` | 완료 (SPEC-002) |
| etl (opus) | `term_9302817b-ff80-4ec8-a40d-24df9ca10071` | `task_e932ccd7d064` | `ctx_27bcdf4b36d2` | `consult-layer1-etl-r2-brief.md` | 완료 (WP4 · 시험 38) |
| planner (fable) | `term_6fdf42b4-b64e-4bc5-b01b-0fcd8b0de135` | `task_8801f3a0cc89` | `ctx_1bde8787e147` | `consult-layer1-spec-r3-brief.md` | 완료 (SPEC 0.2.1) |
| reviewer (opus) | `term_70123566-4d18-40a3-893d-919f461a0726` | `task_d588e0388342` | `ctx_f5e61932e413` | `consult-layer1-review-brief.md` | 완료 PASS · WARN 3 |
| etl (opus) | `term_9302817b-ff80-4ec8-a40d-24df9ca10071` | `task_85d0610da02d` | `ctx_eb5b50c39231` | `consult-layer1-etl-brief.md` | 완료 |
| planner (fable) | `term_6fdf42b4-b64e-4bc5-b01b-0fcd8b0de135` | `task_f4bf15bed33b` | `ctx_d3635aece362` | `consult-layer1-spec-r2-brief.md` | 완료 (0.1.0 = task_eae830298f58 · 0.2.0 = task_f4bf15bed33b) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-17` 사용자 「정리하자」 — 표기 고침 · 상태 done/accepted · 재현 확인(stats 같음 · 보고서 수 611 · 시험 OK) · 커밋 · PR
- `2026-11-16` 이모지 오염(예약표 기호) → SPEC 0.2.2 · 주제 오염(예약표가 LLM 입력) → SPEC 0.3.0 · D-23 · 전체 다시 라벨($0.72 · 실패 0 · 오염 점검 0) · 차트 Artifact 만들고 새 숫자로 갱신
- `2026-11-16` etl 2층 1차 완료(단계 SPEC 일치 · 언어 Hant 1,650 · 큐 15 · haiku 표본 $0.0007/방 · other 57%) · 사용자 haiku · 큐 판정안 · 목록 넓힘 승인(D-19~D-21)
- `2026-11-16` SPEC-002 검증 · accepted · OQ 5건 권장 A(D-14~D-18) · config etl allowed 에 50-report/ · .venv ignore · etl 2층 발주
- `2026-11-16` etl WP4 완료 · 코디 재실행(새 DB · 기존 DB 둘 다 274/274 · unittest 38 OK · 이름 · 폴더명 0) · WORK-001 done
- `2026-11-16` reviewer PASS · WARN 3(W-1 보통 파일 건너뜀 → G-12 멈춤 · W-2 읽기 실패 → G-13 · W-3 시험 분기) — 단계 끝 = open 0 이라 전부 닫기로 · BASE-002/DEC-002(proposed) 작성
- `2026-11-16` etl 완료 · 코디 재실행 verify 274/274 · unittest 28 OK · 행: conv 1,916 · msg 28,706(고객 8,726) · attach 3,461 · reaction 359 · reviewer 발주
- `2026-11-16` SPEC 0.2.0 검증 — 코디 독립 재집계 일치(IG 511/7,094 · FB 1,405/21,612 · sticker 115 · 채널별 우리 계정 1 · 키 합 43) · 이름 grep 1건은 「Links」 안 「Lin」 오탐
- `2026-11-16` SPEC 0.1.0 검증(키 40 처분 · 이름 0) · 코디 BASE 실수(페북 대화 없음 → 1,405방) 정정 · r2 발주
- `2026-11-16` 착수 · 원본 실측 · BASE-001/DEC-001 · config/roles · planner 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
