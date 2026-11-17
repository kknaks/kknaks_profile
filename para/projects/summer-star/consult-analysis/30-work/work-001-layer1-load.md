---
type: work
id: WORK-001
title: "1층 적재 — 상담 DM(인스타그램 · 페이스북 메신저) 원본 → SQLite · 건수 대조"
status: done
product: consult-analysis
work_type: new-feature
owner: kknaks
progress: 100
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/consult-analysis
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-consult-data|BASE-001]]"
  decisions:
    - "[[decision-001-two-layers|DEC-001]]"
  specs:
    - "[[spec-001-layer1-schema|SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 1층 적재

SPEC-001 대로 원본(Meta 내보내기 JSON)을 로컬 SQLite 에 펼쳐 담고, 원본 건수와 맞는지 확인한다.
순서는 DEC-001 D-11 — 1층이 원본 건수와 맞은 뒤에야 2층을 시작한다.

## Meta

| 항목 | 값 |
|---|---|
| 계약 | SPEC-001 0.2.0 (범위 §1 · 스키마 §2 · 대응표 §3 · 키 §4 · 변환 §5 · 인터페이스 §6 · 건수 §7) |
| 원본 | `reference/2026-11-16-linky-data/` — gitignore · **read-only** |
| 산출 | `para/projects/summer-star/consult-analysis/scripts/{load_layer1.py,verify_layer1.py}` · 로컬 DB `data/layer1.sqlite`(gitignore · 커밋 안 함) |
| 범위 | **두 채널** — 인스타그램 DM 511방 + 페이스북 메신저 1,405방 = 1,916방 · 메시지 28,706건(D-13 · D-14). 테이블 **다섯 개** — `conversation` · `customer` · `message` · `attachment` · `reaction`(D-02 · D-12) |
| 범위 밖 | **2층 전부**(언어 · 국적 · 문의 유형 · 예약 단계 — D-05) · 첨부 파일 열기(DEC OQ-003) |
| 선행 | 없다 — SPEC OQ-101 ~ 103 은 D-12 ~ D-15 로 닫혔다. WP1 을 발주할 수 있다 |

## Work Packages

| WP | 내용 | 계약 | 담당 | 선행 | 범위(경로) | 완료 조건 | 검증(부분) | 상태 |
|---|---|---|---|---|---|---|---|---|
| WP1 | **적재 스크립트** — `load_layer1.py`: 두 채널 방 찾기(§1 · §4.1 — 방 폴더 + 보관함 바로 아래 JSON) → `channel` · `box` → **채널별** 우리 계정 판별(§4.3) → 복원(§5.1) → 다섯 테이블 적재(`sticker` 는 `attachment` 행) · 대체 키 순서(§4.5 — 채널 반영) · 멈추는 자리 G-1 ~ G-12(§5.4) · `<db>.tmp` 뒤 바꿔치기(§6.2) · 끝에 테이블별 행 수 | SPEC §1 ~ §6 | etl | — | `scripts/` | 종료 코드 0 · DB 생성 · 채널별 행 수 = §7 의 C-01 · C-11 · M-01 · A-07 · R-01 | `python3 -I scripts/load_layer1.py --source … --db …` 두 번 → 두 DB 의 테이블별 행 수 · id 범위 같음 | done |
| WP2 | **대조 스크립트** — `verify_layer1.py`: 원본을 **적재 코드를 쓰지 않고 따로** 다시 세어 §7 전 줄 · 전 칸(IG · FB · 합)을 「기준 · 원본 재집계 · DB」 세 값으로 비교 · 전부 같으면 0 · 아니면 1 | SPEC §6.3 · §7 | etl | WP1 | `scripts/` | §7 의 C · M · A · R · E **전 줄 · 전 칸 일치** · 종료 코드 0 | `python3 -I scripts/verify_layer1.py --source … --db …` | done |
| WP3 | **검수** — reviewer 가 SPEC 대조: ① 스키마(칸 · 타입 · NULL · UNIQUE · FK)가 §2 와 같다 ② §3 의 키 43개가 코드에서 전부 처분된다(모르는 키는 G-1 로 멈춤 — 통과시키는 `else` 없음) ③ G-1 ~ G-12 가 전부 있다 · 우리 계정을 채널별로 구한다(계정명이 코드에 없다) ④ `verify_layer1.py` 가 적재 코드를 불러 쓰지 않는다 ⑤ WP2 를 직접 다시 돌려 전 줄 일치 ⑥ **고객 정보 0**(아래 수용 기준 4 · 5) ⑦ 2층 값이 1층에 섞이지 않았다 | SPEC 전체 | reviewer | WP2 | 읽기만 | FAIL 0 | WP2 명령 재실행 + grep | done |
| WP4 | **reviewer WARN W-1 ~ W-3 반영** — ① W-1: 보관함 바로 아래의 폴더도 `*.json` 도 아닌 보통 파일(숨김 아님)은 G-12 로 멈춤 ② W-2: 원본 파일 읽기 실패(JSON 깨짐 · 비 ASCII 바이트 · 읽기 오류)는 G-13 으로 — 채널 · 보관함 · 몇 번째 방 · 규칙 번호를 찍음 ③ W-3: 시험이 안 닿던 분기(G-6 최다 발신자 동률 · 채널에 방 0개) 시험 추가 · ①② 의 시험도 | SPEC 0.2.1 §1 · §4.1 · §5.1 · §5.4 · 검수 리포트 WARN | etl | WP3 | `scripts/` | W-1 ~ W-3 시험 통과 · §7 전 줄 · 전 칸 일치 그대로 | 시험 실행 + WP2 명령 | done |

WP1 · WP2 는 한 워커가 이어서 한다(같은 폴더). 전체 검증은 WP3 에서 한 번이다.

## 수용 기준

1. **건수 대조표 전부 일치 — 채널별로** — SPEC §7 의 모든 줄(C-01 ~ C-15 · M-01 ~ M-18 · A-01 ~ A-21 · R-01 ~ R-05 · E-01 ~ E-04)의 **IG 칸 · FB 칸 · 합 칸 각각**이 기준 = 원본 재집계 = DB. 합만 맞고 채널 칸이 다르면 끝이 아니다(D-03 · D-15).
2. **표준 라이브러리만** — 스크립트의 `import` 가 전부 표준 라이브러리. `requirements` · 가상환경 없음. `python3 -I` 로 돈다.
3. **담을 칸 없는 키 0** — SPEC §3 에 없는 키가 나오면 멈춘다(G-1). 조용히 버리는 경로가 없다.
4. **출력에 고객 정보 0** — 표준 출력 · 표준 오류에 이름 · 계정명 · 본문 · 폴더명 · `thread_path` · `uri` 가 없다. 검사: 두 스크립트의 출력을 받아 두 채널 원본 `participants[].name` 전체(우리 계정 둘 포함) · 방 폴더명 전체와 대조해 일치 0(목록은 메모리에서만 · 어디에도 쓰지 않는다).
5. **레포에 고객 정보 0** — 스크립트 · 주석 · 테스트 · 보고서에 계정명 · 고객 이름 · 본문이 없다. `data/` 는 커밋하지 않는다(`git status` 에 DB 파일이 안 보임 — gitignore 확인).
6. **다시 돌려도 같다** — 같은 원본으로 두 번 적재하면 테이블별 행 수 · 최소/최대 id · `message_id` ↔ (`conversation_id`, `source_idx`) 대응이 같다.
7. **원본을 건드리지 않는다** — 적재 앞뒤로 원본 폴더의 파일 수 · 총 크기가 같다.
8. **판단이 섞이지 않았다** — 1층 테이블에 SPEC §2 밖의 칸이 없다(언어 · 국적 · 단계 · 자동응답 여부 같은 것 금지 — D-01).
9. **테이블 다섯 개 · 채널 값** — DB 의 테이블이 `conversation` · `customer` · `message` · `attachment` · `reaction` 다섯뿐이고(D-02 · D-12), `conversation.channel` 은 모든 행이 `instagram` · `facebook` 중 하나다(NULL 0 · D-15).

## 주의

- SPEC 의 건수는 2026-11-16 원본 기준이다. 원본을 다시 받으면 SPEC §7 부터 다시 센다.
- `verify_layer1.py` 가 기준과 다른 값을 내면 **스크립트를 기준에 맞추지 않는다.** 어느 쪽이 틀렸는지 원본에서 확인하고, SPEC 이 틀렸으면 코디네이터에게 올린다.
- 멈추는 자리(G-1 ~ G-12)는 실측에서 두 채널 다 전부 0건이다. 시험은 임시 폴더에 지은 가짜 방 JSON 으로 한다 — 원본을 복사해 고치지 않는다(고객 본문이 시험 파일로 번진다).
- 워커는 커밋 · push · PR 을 하지 않는다. DB 파일과 원본은 git 에 올라가지 않는다.

## 열린 것

없다. SPEC-001 OQ-101 ~ 103 은 DEC-001 D-12 ~ D-15 로 닫혔고 SPEC 0.2.0 에 반영됐다.
