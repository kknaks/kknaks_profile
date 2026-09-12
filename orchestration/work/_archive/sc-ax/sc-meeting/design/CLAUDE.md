# 타이포 기준 (SCAX 보완)

SCAX 코드에 실재하는 크기만 쓴다. Pretendard · 행간 145% · 자간 −2% 고정.

| 단 | 크기 · 굵기 | 자리 |
|---|---|---|
| Display | 28 Bold | 페이지 제목 `.page-head h1`, 화면당 1개 |
| Title | 17 Bold | 워드마크, 드로어/상세 패널 제목, 밀도 높은 목록 화면의 페이지 제목 |
| Section | 16 Bold | 카드 제목 `.card-title h3` |
| Sub | 15 Bold | 본문 소제목 `.section-title` |
| Body | 14 Regular/Bold | 본문, 표 셀, 목록 제목 `.t-item`, 사이드바, 기본 버튼 |
| Label | 13 Regular | 메타·설명 `.t-meta`, 카드 부제, 탭 |
| Caption | 12 | 필터 칩, h30 버튼, 브레드크럼, 타임스탬프 |
| Micro | 11 Bold | 배지 `.badge`, `.count-badge` 전용 |

규칙
- 18 · 20 · 22 · 24 는 쓰지 않는다. 강조는 굵기와 색(`--text-primary`)으로 올린다.
- 한 화면에서 쓰는 단은 최대 4개.
- 11 은 배지 전용. 본문 최소는 12.
- 목록 한 행은 Caption(시각·상태) → Body Bold(제목) → Caption/Label(요약) 순.
