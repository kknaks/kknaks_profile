# 엑시머 레이저(PRC-030) — overview · mechanism · 원리 코드 후보 (researcher · 읽기만 · 2026-11-20)

`silver/procedure.csv` 의 PRC-030 행은 `mechanism_code` · `overview` · `mechanism` 이 비어 있다. 아래는 넣을 문안이다(silver 는 고치지 않았다). 문체는 같은 계열 M8 시술(PRC-002 · PRC-007)을 따랐다.

## overview(문안)

> 308nm 파장의 자외선(UVB)을 내는 레이저로, 백반증 · 건선처럼 병변이 있는 부위에만 빛을 좁게 쏘는 광선치료다. 주변 정상 피부는 거의 쬐지 않아, 전신 광선치료보다 적은 횟수로 국소 병변을 치료할 수 있다.

## mechanism(문안)

> 308nm 자외선이 피부에 흡수되면 병변에 모여 있는 T세포가 스스로 사멸(세포자멸사)하도록 유도해 면역 염증을 가라앉힌다. 백반증에서는 이와 함께 멜라닌세포와 그 줄기세포의 증식 · 이동 · 멜라닌 생성을 자극해 하얗게 빠진 자리에 색소가 다시 차오르게 한다.

## mechanism_code 후보

| 후보 | 판단 | 이유 |
|---|---|---|
| **새 MEC — 자외선 광면역조절 (UVB phototherapy · photoimmunomodulation)** · 상위 없음 | **추천** | 사전 55 행에 맞는 원리가 없다. 엑시머의 원리는 「표적을 골라 파괴」가 아니라 「자외선으로 T세포 자멸 유도 + 멜라닌세포 자극」이다. 설명 문안: 「308nm 자외선(UVB)이 병변의 T세포 자멸사를 유도해 면역 염증을 줄이고, 멜라닌세포를 자극해 색소 재생을 돕는다.」 |
| MEC-040 선택적 표적 파괴 | 비추천 | 「특정 파장의 빛을 표적이 흡수하면 그 표적만 파괴」 — 엑시머는 색소 · 혈관을 겨누는 광열이 아니다. 계열 M8 기본 원리 문장이 이것이라 넣기 쉽지만 틀린 원리다. |
| MEC-043 광생물조절 | 비추천 | 적색광 · 근적외선이 미토콘드리아(시토크롬 C 옥시다아제)를 활성화하는 원리 — 파장 · 표적 모두 다르다. |
| MEC-101 항염 작용 | 보조 후보 | 「염증 매개체 생성 억제」 — 결과는 맞지만 성분(약물) 원리로 쓰는 행이라 빛 시술에 붙이면 뜻이 섞인다. 새 MEC 를 안 만들 때만 차선. |

## 출처

- 원장: `phub-ledger/extracted.json:/M8/indications/extended/4` 「백반증, 건선 치료 (엑시머 레이저)」 · `phub-ledger/problem-packages.json:/problems/13/complaints/5` 「백반증」 · cc_detail 「엑시머 308nm」 · role 「광선치료」 · combo reason 「자외선 치료」 · `phub-ledger/taxonomy.json:/problem/13/subcategories/3/items/0` 「백반증 · 엑시머 308nm」(같은 자리 건선 「UVB 광치료」).
- 논문:
  - Use of the 308-nm excimer laser for psoriasis and vitiligo — https://pubmed.ncbi.nlm.nih.gov/16427504/ (국소 백반증에서 NB-UVB 보다 높은 재색소율)
  - The role of excimer light in dermatology: a review (An Bras Dermatol) — https://new.scielo.br/j/abd/a/VfsxDMmDdh4VTHqyG5rKTFL/?lang=en (308nm 흡수 → DNA 손상 · p53 증가 · Bcl-2 감소 → 각질세포 · T림프구 주기 정지)
  - Excimer laser for the treatment of psoriasis: safety, efficacy, and patient acceptability — https://www.dovepress.com/excimer-laser-for-the-treatment-of-psoriasis-safety-efficacy-and-patie-peer-reviewed-article-PTT (병변 T세포 자멸사)
  - PMC5683125 — https://pmc.ncbi.nlm.nih.gov/articles/PMC5683125 (멜라닌세포 줄기세포 분화 · 멜라닌 생성 · 멜라닌세포 증식 · 이동)
- 참고(이 작업 범위 밖): 시술 PRC-030 케이스 고민은 원장대로면 백반증 CON-236 · 건선 CON-237 이다.
