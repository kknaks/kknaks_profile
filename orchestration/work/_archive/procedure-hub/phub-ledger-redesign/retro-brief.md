# 발주서 — phub-ledger-redesign 회고 쓰기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 1. 배경

`orchestration/work/phub-ledger-redesign/` 작업(Procedure Hub 원장 21개 → silver 56표 · gold 15표)의 한 단계가 끝났다. 회고를 쓴다. **이 작업은 실험용이라 회사 레포에 머지하지 않고, 다음 작업(gold 데이터 + jev + LLM 연결 시험)으로 이어진다** — 그래서 archive-work.sh 는 돌리지 않고 회고만 지금 남긴다.
**이 레포(kknaks_profile)는 PUBLIC 이다.** 회사 데이터(원장 문장 · 시술 설명 원문 · 제품 사실 원문)는 회고에 넣지 않는다 — 숫자 · 코드 id · 표 이름 · 결정 · 방법만. 키 · 토큰 · 실명 · 내부 URL 0.

## 2. 읽을 것

- 꼴: `templates/orchestration/work-summary.md`(규칙 전부 — 「무엇을 완성했다」로 끝나는 줄 금지 · §2 · §3 이 알맹이) · 같은 자리 선례 `para/projects/company/procedure-hub/log/2026-11-01-silver-step9-explanations.md` · `2026-10-30-gold-decisions.md`
- 정본: `orchestration/work/phub-ledger-redesign/_RESUME.md` 전부(결정 표 · 목표 참고 문서 §1~5 · 끝 줄들 11-09 ~ 11-16 이력 — 가장 중요)
- 단계 notes(숫자 · 결정 확인용): `orchestration/work/phub-ledger-redesign/silver-model/notes/*-notes.md` · `drafts/*/…-notes.md` · `gold/gold-final-notes.md` · `gold/README.md` · `notes/glossary.md` · 지시서 `orchestration/work/phub-ledger-redesign/*-brief.md` · `*-instructions.md`
- 앞 작업 `orchestration/work/phub-recommend/_RESUME.md` 의 끝(11-08 「ERD 설계 바탕 틀림」 판정 — 이 작업이 시작된 이유)
- 개념 맵 `para/areas/area.md` §3.4(§2 항목 이름을 맵의 기존 개념 이름과 맞출 수 있으면 맞춤 — 개념 노트는 쓰지 않음)

## 3. 쓸 것

파일 하나: `para/projects/company/procedure-hub/log/2026-11-16-phub-ledger-redesign.md` — 템플릿 §0~5 꼴(선례처럼 맨 위 「한 장 요약」 있어도 됨).
- **작업 전체를 덮는다**(11-09 원장 조사 ~ 11-16 용어집 · 데이터 보관 결정). 결과 줄만 쓰지 말고 **가장 오래 막혔던 구간**을 §2 · §3 에: 예 — 앞 작업 ERD 실패 뒤 「값부터 쪼개기」로 다시 세운 것 · ①사전 → ②조합 → ③관계 순서 · 시범 → 표 구조 확정 → 묶음 병렬 → 합치기 → 보완 흐름 · 묶음 경계에서 빠진 잎 · 단계 검사가 시점 고정이라 앞 검사가 FAIL 나는 문제 → 통합 검사 · 정규화 칸 추가 지적 · 동명이물 · 원장 오류(「원장이 틀릴 수 있다 — silver 만 제대로」) · 외부 조사(fable) 반영 기준 · 아발란체 FDA 인용 누락으로 결정 전제가 틀린 일 · 코디가 「원장 갈래」라고 잘못 말한 일 · 같은 날 판정 · gold 질문 시범(구조 문제 0) · PUBLIC 레포라 데이터를 gitignore + 로컬 보관한 결정. 각 사실은 _RESUME · notes 로 확인한 것만.
- §4 결정 표: 큰 결정만(20~30행) — 날짜 · 결정 · 왜(사용자 말 · 조사).
- §5 날짜별 로그: 11-09 ~ 11-16 하루 한 줄 이상.
- 결과 줄: 「실험용 — 회사 레포 머지 안 함 · 다음 작업 gold + jev + LLM 연결 시험으로 이어짐 · 데이터는 로컬 보관」.
- 회사 데이터 원문 인용 0(원장 문장 · 제품 설명 · 시술 설명을 「」 로 옮기지 않음). 숫자는 notes 에서 다시 확인한 것만.

## 4. 검증 · 금지

- 새 파일 하나 말고 레포 변경 금지(다른 파일 · silver · notes 수정 금지). 커밋 · push 금지.
- 끝나면 스스로 grep: 「」 안에 원장 문장이 없는지 · http 내부 주소 · 키 꼴 · 실명이 없는지 — 결과를 완료 보고에.

## 5. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path para/projects/company/procedure-hub/log/2026-11-16-phub-ledger-redesign.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "회고 완료: para/projects/company/procedure-hub/log/2026-11-16-phub-ledger-redesign.md" --enter`
