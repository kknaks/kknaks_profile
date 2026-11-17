---
type: work
id: WORK-002
title: "2층 판정 · 분석 — 언어 · 예약 단계 · 국적 · LLM 라벨 · 집계 · 보고서"
status: done
product: consult-analysis
work_type: new-feature
owner: kknaks
progress: 100
created_at: 2026-11-16
updated_at: 2026-11-17
tags:
  - product/consult-analysis
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-002-conversion-language|BASE-002]]"
  decisions:
    - "[[decision-002-layer2-analysis|DEC-002]]"
  specs:
    - "[[spec-002-layer2-analysis|SPEC-002]]"
  works:
    - "[[work-001-layer1-load|WORK-001]]"
  releases: []
  related: []
---

# 2층 판정 · 분석

SPEC-002 대로 1층 DB 위에 판정 테이블을 만들고, 「예약까지 가는 대화 · 언어별 특징」 통계를 낸다.

## Meta

| 항목 | 값 |
|---|---|
| 계약 | SPEC-002 0.2.0 |
| 입력 | `data/layer1.sqlite`(1층 · 읽기 — `l2_` 테이블만 쓴다) |
| 산출 | `scripts/{judge_layer2.py,label_layer2_llm.py,stats_layer2.py,requirements-layer2.txt}` · `50-report/{stats-001.json,report-001-conversion-language.md,README.md}` · 로컬 `data/review_queue.csv` |
| 범위 밖 | 1층 수정 · 차트 페이지(코디) · 첨부 파일 열기 |
| 선행 | SPEC-002 OQ-204 · OQ-205 는 WP1 전에 · OQ-201 은 WP3 전에 닫는다. OQ-202 · 203 은 권장(A)대로면 선행 아님 |

## Work Packages

| WP | 내용 | 계약 | 담당 | 선행 | 완료 조건 | 상태 |
|---|---|---|---|---|---|---|
| WP1 | **규칙 판정** — `judge_layer2.py`: `l2_message`(언어 · 자동응답 · 칸 수 · 이모지) · `l2_conversation_lang` · `l2_booking_stage` · `l2_nationality` ① ③. 번체 / 간체 건수 · 방까지 `zh` 로 남은 수 · 단계 건수를 SPEC §2.3 표와 나란히 보고 | SPEC §1 ~ §4 · §7 | etl | OQ-204 · 205 | 행 수 = 메시지 28,706 · 방 1,916 · 단계 건수가 §2.3 과 같거나 차이를 설명 | done |
| WP2 | **사람 확인 큐** — `l2_review_queue` + `data/review_queue.csv`(로컬 · 본문 포함) · `--decisions` 로 사람 판정 반영 | SPEC §2.4 | etl | WP1 | 큐 50건 안쪽(넘으면 멈추고 보고) · 사유별 건수 보고 — 큐 15건(E-1 12 · E-2 1 · E-3 2) · 사람 판정 반영(D-19 · 성공 93) | done |
| WP3 | **LLM 라벨** — `label_layer2_llm.py`: 표본 30방(haiku · 끝남 — 실패 0 · `other` 방 기준 57%) → **표본 재시험**(SPEC 0.2.0 §5 — 넓힌 목록 · 별칭 표 · `procedures_other` · 같은 30방 · `other` 비율 보고) → 코디 확인 → 전체 1,883방 → `judge_layer2.py` 다시(국적 ②) | SPEC §5 | etl | OQ-201 · WP1 | 라벨 행 + 실패 건수 = 1,883 · 목록 밖 값 0 — llm-0.3.0 · 1,883 · 실패 0 | done |
| WP4 | **집계 JSON** — `stats_layer2.py` → `50-report/stats-001.json` | SPEC §6 · §7 | etl | WP2(사람 판정 반영 뒤) · WP3 | §6 항목 전부 · 모든 비율에 분모 · `small` 표시 — stats-001.json | done |
| WP5 | **보고서** — `50-report/report-001-conversion-language.md` · `50-report/README.md` | SPEC §7 | etl | WP4 | 절 ① ~ ⑧ · 수치가 전부 JSON 과 같다 — check_report_numbers | done |
| WP6 | **검수** — SPEC 대조 · 수용 기준 전부 · 표본 방 20개를 DB 에서 직접 보고 단계 · 언어 판정 확인(결과는 건수만 보고) | SPEC 전체 | reviewer | WP5 | FAIL 0 | 생략 — 사용자 정리 지시(2026-11-17) · 1층 reviewer PASS · 2층은 코디 재실행 · 오염 점검으로 대신 |

사람 확인(WP2 뒤) · 표본 확인(WP3 중간)은 코디 · 사용자 몫이다. 차트 페이지는 `stats-001.json` 을 받아 코디가 만든다.

## 수용 기준

1. **행 수** — `l2_message` 28,706 · `l2_conversation_lang` · `l2_booking_stage` · `l2_nationality` 각 1,916 · `l2_llm_label` + 실패 = 1,883. 1층 테이블의 행 수 · 칸은 그대로다(SPEC-001 §7 대조 스크립트가 여전히 통과).
2. **판정 주체 · 근거 · 버전 빠짐 0** — 모든 `l2_` 행의 `judge` · `version` 이 NULL 아님. `evidence_message_id` NULL 은 SPEC §1 이 허용한 경우(고객 메시지 없는 방)뿐. `l2_llm_label` 은 `model` · `confidence` 도.
3. **고객 본문 · 이름 0** — 스크립트 · 주석 · 시험 · `stats-001.json` · 보고서 · 표준 출력 · 워커 보고에 고객 본문 · 이름 · 계정명 · 폴더명이 없다(1층 때와 같은 대조 — 두 채널 이름 전체 · 본문을 메모리에 올려 일치 0). `data/review_queue.csv` 는 커밋되지 않는다.
4. **사람 확인 50건 안쪽** — 넘으면 조건을 좁히지 않고 멈춘다.
5. **LLM 은 로컬 CLI 로만** — 방 본문을 파일로 쓰지 않는다. 목록 밖 값 · 깨진 JSON 은 실패로 세고 채워 넣지 않는다.
6. **다시 돌려도 같다** — `judge_layer2.py` 를 두 번 돌리면 규칙 테이블의 행이 같다. `l2_llm_label` 은 지워지지 않는다.
7. **분모 표기** — JSON 의 모든 비율이 `n` · `d` 를 갖고 `d < 10` 이면 `small`. 보고서에 분모 없는 비율이 없다.
8. **의존성 명시** — 외부 패키지는 `scripts/requirements-layer2.txt` 에만 · 버전 고정.

## 주의

- SPEC §2.3 의 건수는 planner 가 규칙을 한 번 돌려 본 값이다. 다르면 맞추려고 규칙을 비틀지 말고 차이를 보고한다.
- 시험 자료는 지어낸 문장으로 만든다 — DB 의 고객 본문을 시험 파일로 옮기지 않는다.
- 워커는 커밋 · push · PR 을 하지 않는다.

## 열린 것

SPEC-002 §8 의 OQ-201 ~ 205.
