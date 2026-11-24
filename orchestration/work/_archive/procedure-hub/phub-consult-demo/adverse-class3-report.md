# 부작용 분류 마무리 리포트(코디 기본값 11-22)

- 앞 판 = `adverse-class2-report.md`((나) 기준 · 위급 34)
- 커밋 0 · 18105 · 18222 손대지 않음 · **허브 코드 0 바뀜**(칸 그대로) · 서브에이전트 0

## 1. 바뀐 5 — 위급 → 주의(대개 회복)

| 코드 | 이름 | 대분류 | 앞 → 지금 | 「이럴 땐 바로 병원」 경고가 된 원장 응급 줄 |
|---|---|---|---|---|
| ADV-041 | 헤르페스 재활성화 | 염증 반응 | 위급 → **주의** | ADG-2449 · ADG-2984 「헤르페스 재활성화 (수포 군집)」 |
| ADV-060 | 혈관외유출 | 혈관 합병증 | 위급 → **주의** | ADG-1063 「주사 부위 심한 부종 및 통증(혈관외유출 의심)」 |
| ADV-064 | 감각저하 | 신경 손상 | 위급 → **주의** | ADG-1859 「시술 부위 감각 소실」 |
| ADV-076 | 발음 장애 | 근육 반응 | 위급 → **주의** | ADG-0341 「발음 장애 또는 시력 변화」 |
| ADV-090 | 복시 | 눈 손상 | 위급 → **주의** | ADG-0376 「시야 변화/복시」 · ADG-0387 「시야 장애/복시 악화」 |

- 뇌졸중(ADV-061)은 위급 그대로다(응급 줄 없음 · 앞 판 사용자 목록).
- 어떻게 반영했나:
  - `judge_adverse_lines.py` 에서 다섯을 새 사람 판단 묶음 **H5**(「규칙상 자체지만 대개 회복 — 코디 기본값 11-22」 · 추천 = 악화 조건)로 옮겼다. 그래서 그 줄 7 이 `alert = true` 가 됐다.
  - 발음 장애는 대분류가 근육 반응(기본 일시적)이다. 그래서 `build_batch8.py` 의 `UP_CAUTION` 에 넣어 **주의**로 맞췄다.
- `adverse-class.csv` 의 class_basis: 넷 = 사람 판단(추천) · 발음 장애 = 대분류(보정 근거 「코디 기본값 11-22」).

## 2. 셈

| | (나) | 마무리 |
|---|---:|---:|
| 위급 | 34 | **29** |
| 주의 | 88 | **93** |
| 일시적 | 66 | 66 |
| 경고 줄(adverse_guidance.alert) | 107 | **114**(+7) |
| source_ref 묶음 8 덧붙임 | 295 | 302 |

gold `g_adverse`: 일시적 1974 · 주의 582 · 위급 362 · 빈칸 5 · 경고 줄 125(빈도 행마다 겹침).

## 3. 바뀐 것 · 검사

- silver 작업 사본:
  - `judge_adverse_lines.py`(다섯 → H5) · `build_batch8.py`(UP_CAUTION 에 ADV-076)
  - 다시 지음: `adverse-emergency-lines.csv` · `adverse.csv` · `adverse_guidance.csv` · `source_ref.csv` · `user.csv` · `batch8-log.json` · `$W/adverse-class.csv` · `$W/adverse-emergency-lines.csv`
  - glossary(`vocabulary.csv` 셈) · silver 문서 · gold 재빌드
- 앞 판 대비 gold 차이는 정확히 이것뿐이다:
  - `g_adverse.severity_class` 22 행(다섯 부작용의 위험 행)
  - `guidance_alerts` 6 행
  - 새 경고 줄 7 의 근거 종류(`g_adverse_detail` · `g_evidence` 각 7 — 원장 → 원장 + 사용자 제공)
  - 그 밖 표 · 칸 0
- silver-check PASS(WARN 5 — 앞서부터).
- gold-check **PASS**(FAIL 0 · 묶음 8 재현 바이트 같음). WARN = 묶음 7 재현 건너뜀(그림 시드 없음 — 앞 판과 같음).
- 허브(코드 그대로):
  - `test_medallion_model` · `test_gold_contract` 19 passed. 실물 silver 헤더 대조 시험이 포함되어 있다.
  - 실물 gold 를 프로세스 안에서 적재해 보니 `facets adverse:ADV-041` 이 `severity_class = 주의` 로 나온다.

## 4. 해시 · JSON

| 항목 | (나) | 마무리 |
|---|---|---|
| 허브 gold_hash | `c02d3ae8…` | **`661335b6e979d0044afd36cfd22fdc55c4366c2adfc6ea0142ee28191d83265a`** |
| 허브 aux_hash | `60788233…` | **`9905dea772f9d7fd877da9ac208ac00c483a811d6d1b544b06ca8e5f0ef502f4`** |
| silver 해시(59표) | `9d426e69…` | `0ee7bb66d46f13f219cde9fc4f2e31b56670866672a697ce70afe37661f726aa` |
| 매핑 JSON v3 sha256 | `27f37eaf…` | **`d21903f594792c2b94533195e615264c152bdb5d07bf96258898b1ca0d5304be`** |

- JSON 은 두 경로(앱 워크트리 · `~/git/clinic_chat`)가 같은 sha 다. 데이터 다섯 덩이는 같고, meta 세 줄(gold · aux · made_at)만 바뀌었다.
- 앞 판 백업은 scratchpad `v3-before-27f37eaf.json`.

## 5. 18105 다시 띄우기(코디)

(나) 판과 같은 명령이다. 해시만 바뀐다.

```sh
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend
S=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model
GOLD_CSV_DIR=$S/gold GOLD_SOURCE_REF_PATH=$S/silver/source_ref.csv GOLD_HIERARCHY_DIR=$S/silver \
GOLD_LEDGER_CHECK_PATH=$S/notes/ledger-check-list.csv \
GOLD_EXPECTED_HASH=661335b6e979d0044afd36cfd22fdc55c4366c2adfc6ea0142ee28191d83265a \
uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18105
```

- 18222: `CHAT_KOS_MAP_SHA=d21903f594792c2b94533195e615264c152bdb5d07bf96258898b1ca0d5304be`.
