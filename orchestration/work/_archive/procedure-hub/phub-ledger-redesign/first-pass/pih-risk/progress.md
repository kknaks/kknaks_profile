# progress — pih-risk.json 1차 조사

- 시작: 2026-11-09 · 원본 sha256 cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8 · 11,875 bytes · 한 줄(minified) JSON · 백슬래시 이스케이프 0 · 중복 키 0
- 구획 계획: `segments.json` → `coverage.json` (S0 상위 메타 · S1~S8 procedures 카테고리/하위분류 경계)
- 현재 구획: 없음 — **S0~S8 전부 직접 읽기 완료**(기계 추출 완료와 별도로 coverage.json `direct_read`)
- 마지막으로 실제 읽은 Pointer: `/procedures/25/prevention` (S8)
- 다음 구획: 없음
- 상태: 1차 범위 종료(원장 전체 완료 아님) — 열린 미결은 issues.md (B8 · I3 · P2 · F7 · K3, C 0)

## 구획 진행

| 구획 | 기계 추출 | 직접 읽기 | 기록 |
|---|---|---|---|
| S0 상위 메타 | ○ | ○ | manual/S0.json |
| S1 0–3 색소/토닝 | ○ | ○ | manual/S1.json |
| S2 4–8 프락셔널 | ○ | ○ | manual/S2.json |
| S3 9–11 IPL·혈관 | ○ | ○ | manual/S3.json |
| S4 12–14 제모 | ○ | ○ | manual/S4.json |
| S5 15–17 M9 | ○ | ○ | manual/S5.json |
| S6 18–20 M11·M12 | ○ | ○ | manual/S6.json |
| S7 21–22 M13 | ○ | ○ | manual/S7.json |
| S8 23–25 M15 | ○ | ○ | manual/S8.json |

## 재현 명령 (레포 루트)

```bash
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/pih-risk/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/pih-risk/verify.py
```

## 열린 문제

issues.md 참고. 재개 시 수동 기록은 `manual/S*.json` 만 고치고 build.py → verify.py 순으로 다시 돈다(생성 파일은 직접 고치지 않는다).
