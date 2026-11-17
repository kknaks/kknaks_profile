# Report Index

| ID | Title | 입력 | File |
|---|---|---|---|
| REPORT-001 | 상담 DM 예약 전환과 언어 — 어떤 대화가 예약까지 가나 | `stats-001.json` | [본문](report-001-conversion-language.md) |
| STATS-001 | 2층 집계 JSON(건수 · 비율만 · 차트 페이지 입력) | `data/layer1.sqlite`(로컬) → `scripts/stats_layer2.py` | [stats-001.json](stats-001.json) |

- 보고서의 수는 전부 `stats-001.json` 에서 온다. 대조: `python3 -I scripts/check_report_numbers.py --report 50-report/report-001-conversion-language.md --json 50-report/stats-001.json`
- 고객 본문 · 이름 · 계정명 · id 는 여기 없다(레포 PUBLIC). 본문이 필요한 확인은 로컬 `data/` 에서만 한다.
