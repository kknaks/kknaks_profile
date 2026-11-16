# progress — patient-education.json 1차 조사

- 시작: 2026-11-09 · 원본 sha256 6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac · 26,551 bytes · 13,043 코드포인트 · 한 줄 JSON · 이스케이프 0 · 중복 키 0
- 구획 계획: `segments.json` → `coverage.json` (S00 상위 메타 · S01~S17 = /categories/0~16, 카테고리 하나가 한 구획)
- 현재 구획: 없음 — **S00~S17 전부 직접 읽기 완료**(coverage.json `direct_read`, 기계 추출 `machine_extracted` 와 별도)
- 마지막으로 실제 읽은 Pointer: `/categories/16/common_concerns/2/a` (S17)
- 다음 구획: 없음
- 상태: **1차 범위 종료 · 원장 전체 완료 아님** — 열린 미결 issues.md (B 36 · P 42 · F 10 · I 1 · K 1+25출현 · A 0 · C 0)

## 구획 진행

| 구획 | 기계 추출 | 직접 읽기 | 기록 |
|---|---|---|---|
| S00 상위 메타 | ○ | ○ | manual/S00.json |
| S01 M1 보톡스 | ○ | ○ | manual/S01.json |
| S02 M2 필러 | ○ | ○ | manual/S02.json |
| S03 M3 바이오스티뮬레이터/콜라겐부스터 | ○ | ○ | manual/S03.json |
| S04 M4 스킨부스터 | ○ | ○ | manual/S04.json |
| S05 M5 PRP/자가혈 | ○ | ○ | manual/S05.json |
| S06 M6 지방이식 | ○ | ○ | manual/S06.json |
| S07 M7 실리프팅 | ○ | ○ | manual/S07.json |
| S08 M8 레이저 | ○ | ○ | manual/S08.json |
| S09 M9 기기 리프팅 | ○ | ○ | manual/S09.json |
| S10 M10 HIFES/EMS | ○ | ○ | manual/S10.json |
| S11 M11 니들RF | ○ | ○ | manual/S11.json |
| S12 M12 마이크로니들링(MTS) | ○ | ○ | manual/S12.json |
| S13 M13 플라즈마 | ○ | ○ | manual/S13.json |
| S14 M14 크라이오리포라이시스 | ○ | ○ | manual/S14.json |
| S15 M15 메디컬스킨케어 | ○ | ○ | manual/S15.json |
| S16 M16 수액치료 | ○ | ○ | manual/S16.json |
| S17 M17 줄기세포치료 | ○ | ○ | manual/S17.json |

## 재현 명령 (레포 루트)

```bash
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/patient-education/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/patient-education/verify.py
python3 orchestration/work/phub-ledger-redesign/first-pass/patient-education/reading_dump.py S01   # 구획 원문 읽기 보조(파일 안 씀)
```

## 재개 규칙

수동 기록은 `manual/` 만 고친다(S*.json · segmentation-review.json · regex-review.json · review-head.md · issues-head.md). 생성물(source-map·morphology·expressions·coverage·observations·issues.md·review*.md)은 직접 고치지 않고 build → verify 순으로 다시 돈다. validation.md·progress.md 는 손으로 쓴 기록이라 build 가 덮지 않는다.
