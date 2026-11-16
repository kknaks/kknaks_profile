# progress — market-pricing.json 1차 조사

- 원본 sha256 601d7e7b4db29731bf15304ff3ec9489ba38838e9f5ba2144c2c181cfd15e477 · 12,214 bytes · 한 줄 JSON · 백슬래시 0 · 중복 키 0
- 구획 계획: segments.json → coverage.json (S00 루트 메타 · S01~S17 카테고리 1개씩)
- 현재 구획: 없음 — **S00~S17 전부 직접 읽기 완료**(기계 추출 완료와 별도로 coverage.json `direct_read`)
- 마지막으로 실제 읽은 Pointer: `/categories/16/items/5/high` (S17)
- 다음 구획: 없음
- 상태: 1차 범위 종료(원장 전체 완료 아님) — 열린 미결 issues.md (B30 · I4 · P12 · F7 · K4, C0)

## 구획 진행

| 구획 | 기계 추출 | 직접 읽기 | 기록 |
|---|---|---|---|
| S00 루트 메타 | ○ | ○ | manual/S00.json |
| S01 M1 보톡스 | ○ | ○ | manual/S01.json |
| S02 M2 필러 | ○ | ○ | manual/S02.json |
| S03 M3 바이오스티뮬레이터/콜라겐부스터 | ○ | ○ | manual/S03.json |
| S04 M4 스킨부스터 | ○ | ○ | manual/S04.json |
| S05 M5 PRP/엑소좀 | ○ | ○ | manual/S05.json |
| S06 M6 지방이식 | ○ | ○ | manual/S06.json |
| S07 M7 실리프팅 | ○ | ○ | manual/S07.json |
| S08 M8 레이저 | ○ | ○ | manual/S08.json |
| S09 M9 에너지기기(HIFU/RF) | ○ | ○ | manual/S09.json |
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
python3 orchestration/work/phub-ledger-redesign/first-pass/market-pricing/read_segment.py S03   # 구획 원문 다시 읽기
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/market-pricing/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/market-pricing/verify.py
```

## 열린 문제

issues.md 참고. 재개 시 수동 기록은 `manual/*.json` 만 고치고 build.py → verify.py 순으로 다시 돈다(생성 파일 review*.md·issues.md·*.json 은 직접 고치지 않는다 — validation.md·progress.md 는 손으로 쓴 파일).
