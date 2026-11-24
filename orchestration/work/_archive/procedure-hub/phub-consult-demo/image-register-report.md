# 새 그림 18 등록 — 리포트(2026-11-20 · data 워커)

브리프: `image-register-task.md`. 커밋 0 · 허브 레포 커밋 0 · DB · stg 0 · 18105 · 18222 손대지 않음.

## 요약

- 그림 시드 `image-map.csv` · `image-assets.csv` 에 18 행씩 더함(103 → 121 · 원리 55 · 방법 66). README · `image-validation.json` 수 갱신, 구조 재검사 PASS.
- silver 작업 사본 `concept_image` 103 → **121** · `concept_image_label` 787 → **949**(+162). 기존 행 바이트 그대로 · 끝 덧붙임 · `source_ref` 덧붙임 0.
- silver-check **PASS(WARN 5)** · I2(예외 지움) · I5(재현 대조함) 통과 · gold-check **PASS(FAIL 0 · WARN 10)**.
- **gold_hash · aux_hash 그대로**. gold 에는 그림이 안 들어가고, 허브 aux 입력(source_ref · concern · adverse · condition · concern_site · 원장 확인 목록)도 안 바뀌었다. 그래서 매핑 JSON 은 다시 쓰지 않았다(sha 그대로).
- 명동점 화면 기준 그림 빠짐 **원리 0 · 방법 0**. 등록 전에는 방법 10 이 빠져 있었다.

## 1. 그림 시드(`프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/` · gitignore 폴더)

| 파일 | 바뀐 것 |
|---|---|
| `image-assets.csv` | 끝에 18 행. stage `4` · alias 없음 · 1200×800 · transparent · text_count = SVG 의 `data-i18n` 요소 수(라벨 수와 같음) · sha256 실측 · review 「구조·한영 렌더 확인 / 의료 검수 전」 · `artwork_version` **`2026-11-20-native-svg-v1`** · complete. 기존 103 행 바이트 그대로(CRLF 유지) |
| `image-map.csv` | 18 행. MEC-108 은 마지막 원리 행(MEC-107) 뒤, 방법 17 은 끝에 silver `method.csv` 순서로 넣었다. 연결 수 = 지금 silver 기준(케이스 수 · 원리는 시술 수 — MEC-108 = 엑시머 레이저 1). 「2026-11-20 SVG 직접 제작」 · 있음(직접) · 새 규격 완료 |
| `README.md` | 103 → 121(원리 55 · 방법 66) · 라벨 949 · SVG 파일 204 · 4단계 줄 · 판 두 개 · 미리보기 `previews/2026-11-20.html` |
| `image-validation.json` | 수 갱신(121 · 204 · 949 · 55 · 66) · `stage_4_new_codes_20261120: 18` · render_audit 에 4단계(출처 = 제작 때 `previews/2026-11-20/validation.json` · 오류 0) · 구조 재검사 기록 |

검사 스크립트가 시드 폴더에 없어서 재검사 스크립트를 새로 짰다(scratchpad `seed_validate.py`). 121 대표와 별칭 83 을 대상으로 XML · viewBox · ID 유일 · 글자 요소 ↔ 라벨 CSV · 내부 참조 · 래스터 · 스크립트 0 · sha256 · 별칭 내용 일치 · 경로 꼴 · 전체 캔버스 배경 0 을 봤고 **모두 통과**했다. 제작 때 남은 `previews/2026-11-20/validation.json` 의 sha256 · 라벨 수 18 건도 표와 같다. 렌더(한영 경계 · 모서리 알파)는 이번에 다시 돌리지 않았다. 렌더 도구가 없어서다. 그 대신 사용자가 미리보기를 확인했다.

## 2. silver 작업 사본(`silver-model/`)

| 파일 | 바뀐 것 |
|---|---|
| `silver/concept_image.csv` | +18 · `CIM-0104` MEC-108 · `CIM-0105` MET-008 · `CIM-0106 ~ 0121` MET-110 ~ 125 · 판 2026-11-20-native-svg-v1 · medical_review 「검수 전」 |
| `silver/concept_image_label.csv` | +162 · `CIL-0788 ~ 0949`(ko) |
| `gold/silver-image.py` | 정렬을 (표, 코드)에서 **(판, 표, 코드)** 로 바꿨다. 예전 정렬로는 MEC-108 · MET-008 이 중간에 끼어 기존 방법 그림 49 개의 CIM id 와 라벨 CIL id 가 밀렸다. 바꾼 뒤에는 기존 103 · 787 의 바이트가 그대로이고 새 판은 끝에 붙는다 |
| `drafts/clinic-supplement/clinic-a-20261119/build_batch7.py` · `batch7-log.json` | 새 묶음 7 재현 스크립트. 기준 b7 을 받아 silver-image.py(시드 = env `SILVER_IMAGE_SEED`, 없으면 형제 워크트리 경로)를 돌린다. 두 표가 끝 덧붙임인지 스스로 검사한다. 두 번 돌려도 같은 바이트 |
| `archive/silver-before-clinic-a-20261119-b7/` | 기준 사본(묶음 7 전 silver 59 표 + user.csv) |
| `archive/scripts-before-batch7/` · `archive/gold-before-batch7/` | 바꾸기 전 스크립트 5(silver-check · schema · gold-build · gold-check · silver-image)와 gold CSV |
| `drafts/silver-check/silver-check.py` | I2 의 「묶음 4 새 방법 · 묶음 6 새 원리(MEC-108)」 그림 예외를 **지웠다**. 기준 이름도 「사전 코드(mechanism ∪ method) 전부에 그림 하나」로 바꿨다 |
| `notes/silver-tables.md` | `--write-docs` 로 다시 썼다(concept_image 121 · label 949) |
| `notes/vocabulary.csv` | `glossary-build.py` 로 다시 뽑았다(셈 칸만: mechanism 200 · method 709 · ko 1044 · 검수 전 121). `--check` PASS |
| `gold/gold-check.py` | 묶음 7 을 넣었다. A1 은 b6 → b7 대조 후 b7 → 지금 대조(그림 두 표만 끝 덧붙임 허용). A3 는 묶음 6 재현을 b7 과 대조하고 묶음 7 재현을 지금 silver 와 batch7-log 에 대조한다 |
| `silver/source_ref.csv` | **안 바뀜.** 기존 그림 행에도 source_ref 가 0 이다(silver-check: 매체는 원장 근거 대상이 아니고 sha256 · 판 · 시드로 되짚는다). 그래서 기존 꼴대로 0 행 |

## 3. 검사 · 해시

```
SILVER_IMAGE_SEED=<시드 폴더> python3 drafts/silver-check/silver-check.py   → PASS (WARN 5 — G3 작업 사본 밖 git 변경)
  I1 · I2 · I3 · I4 · I5 통과 · 그림 재현(I5) 대조함
python3 gold/gold-build.py   → gold CSV 15 + questions 바이트 = gold-before-batch7 (바뀐 파일 0)
python3 gold/gold-check.py   → PASS (FAIL 0 · WARN 10) · A1 · A3(묶음 7 재현 포함) · H1 통과
```

⚠ silver-check 의 시드 기본 경로(`상담봇/reference/2026-11-17-procedure-images`)는 이 워크트리에 없다. env 없이 돌리면 I5 가 「건너뜀(시드 폴더 없음)」으로 나온다. 재실행할 때는 `SILVER_IMAGE_SEED=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images` 를 준다. gold-check A3(build_batch7)는 env 가 없어도 형제 경로를 기본값으로 쓴다.

| 해시 | 값 | 바뀜 |
|---|---|---|
| gold_hash | `57b420ad10d34ff7d3764fd7afbf7d1d731b1d27a1d29984d011d3a61586ec44` | 그대로 |
| aux_hash | `51e3760a82df45de2011b59868a723532af9c7732163e1eee31472ceb8a93b34` | 그대로 |
| silver 해시(59 표) | `f672a39bfc79e98a882d730526b61fa15767c0a0d9477fb8d3261bceda147dda` | 새 값 |

gold_hash · aux_hash 는 허브 코드(`app.modules.gold.inputs.read_inputs`)에 작업 사본을 물려 실측했다.

## 4. 허브가 그림을 읽는 자리

- **허브 서버(gold_main · 18105)는 그림을 읽지도 내보내지도 않는다**(`backend/README.md` 168 · `assets/procedure-images/README.md`: 「서빙 · 바인드 마운트는 다음 스펙」). 그래서 18105 는 다시 띄울 필요가 없다. gold · aux 해시도 그대로다.
- 그림을 쓰는 곳은 적재기 V13 하나다. `GOLD_IMAGE_DIR=<레포>/assets/procedure-images` 를 주면 silver `concept_image` 의 경로 · sha256 이 폴더의 `images/**/*.svg` 와 정확히 같아야 한다.
- 상담 앱(clinic_chat)도 아직 허브 그림을 읽지 않는다(grep 0 — `_face.svg` 만).

허브 워크트리 `PROCEDURE-HUB/phub-consult-demo` 에 18 파일을 뒀다. 추적 안 함 · 커밋 0. 그 뒤 적재기 dry-run 을 돌렸다:
`GOLD_SILVER_DIR=<작업 사본 silver> GOLD_IMAGE_DIR=<허브>/assets/procedure-images scripts/load_medallion.py --dry-run` → **`image_files 121 checked`** · rc 0 · DB 접속 0.

### 배포 때 반영할 파일(허브 레포)

1. 그림 18 개(지금 `??`):
   - `assets/procedure-images/images/mechanism/MEC-108.svg`
   - `assets/procedure-images/images/method/MET-008.svg`
   - `assets/procedure-images/images/method/MET-110.svg` ~ `MET-125.svg`(16)
2. `assets/procedure-images/README.md`: 파일 103 → 121(원리 55 · 방법 66) · 판 `2026-11-20-native-svg-v1` 추가. **고치지 않았다.**
3. `backend/tests/test_medallion_image.py`: 103 · 54 · 49 고정값 → 121 · 55 · 66(161 ~ 182 줄). 지금 로컬 실행은 **2 failed · 13 passed** 다. 하나는 이번 수 변경(`121 == 103`)이다. 다른 하나는 로컬 `.DS_Store`(무시된 파일 · 원래 있던 것)가 걸린 것이다. **고치지 않았다.**
4. 레포 `data/medallion/silver/` 의 `concept_image.csv` · `concept_image_label.csv`: silver 를 반영할 때 이 작업 사본 값으로 바꾼다.

## 5. 명동점 화면 기준 그림 빠짐

매핑 JSON 의 허브 연결 항목 305 를 봤다. 시술 · 케이스 → 시술 `mechanism_code`, 케이스 `case_method`, 제품 `product_method` 순으로 닿는 코드를 모았다(scratchpad `screen_missing.py`).

| | 닿는 코드 | 그림 빠짐(지금) | 등록 전(b7) |
|---|---|---|---|
| 원리 | 26 | **0** | 0 |
| 방법 | 29 | **0** | 10(MET-008 · 110 · 111 · 112 · 113 · 114 · 117 · 120 · 122 · 124) |

MEC-108(엑시머)은 명동점 항목에는 닿지 않는다. 그래도 사전 전체 기준(I2)으로 그림이 있다.

## 6. 매핑 JSON

`build_mapping_json_v2.py 57b420ad… 51e3760a… <scratchpad>` 로 다시 만들어 대조했다. items · groups · sites 는 같고 meta 는 `made_at` 하나만 다르다. 해시 두 개가 그대로라 **두 경로 모두 다시 쓰지 않았다**. sha 는 그대로 **`8ca88c9a008b1cdb91031516132da50d64caca22b85cf8ad395c0128587d1863`** 이다(`/Users/kknaks/git/clinic_chat/data/kos/…` · 앱 워크트리 같은 파일).
