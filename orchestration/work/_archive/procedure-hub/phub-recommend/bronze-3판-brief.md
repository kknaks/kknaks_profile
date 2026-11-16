# 원장 3판 수정 발주 — synergy 줄임말 18값 정식 이름화 · taxonomy M8 항목 2 신설 (2026-11-06 · 사용자 결정)

읽을 것: `bronze/phub-ledger/README.md` · `CHANGELOG.md` · `HASHES.txt` · `silver-v3/lib/load.py`(bronze_hashes · HASHES 형식 `<sha256 앞 16자리> <파일>`).

## 절대 규칙
- 고치는 파일은 `bronze/phub-ledger/synergy.json`·`taxonomy.json`·`README.md`·`CHANGELOG.md`·`HASHES.txt` 다섯만. 다른 원장 파일·`silver-v3/`·ERD 파일 수정 금지. 커밋 금지.
- 아래 표의 값만 바꾼다. 표 밖의 글자는 한 자도 바꾸지 않는다(JSON 키 순서·공백·들여쓰기도 원본 그대로 — 바이트 diff 로 확인). 추정 금지.
- 끝에 `python3 -c 'import json;json.load(open(...))'` 로 두 파일 파싱 확인 · HASHES.txt 전 파일 재계산 · `cd silver-v3 && python3 build.py && python3 check.py` 가 돈다(① 입력 해시 검사가 3판 HASHES 와 맞아야 함). 결과가 7차와 달라지는 건 당연하다(원장이 바뀌었으니) — 바뀐 수치만 보고하고 해석하지 않는다.

## 1. synergy.json — from/to 값 18종(59자리) 교체. `Mxx-` 접두는 뺀다(from_category/to_category 칸에 이미 있음). 부위는 이름 뒤에 띄어 적는다.
| 현재 | → 3판 |
|---|---|
| M12-MTS | 마이크로니들링(MTS) |
| M12-MTS(두피) | 마이크로니들링(MTS) 두피 |
| M14-크라이오 | 크라이오리포라이시스 |
| M17-줄기세포 | 줄기세포치료 |
| M10-HIFES | HIFES/EMS |
| M10-HIFES(바디) | HIFES/EMS 바디 |
| M3-바이오스티뮬레이터 | 바이오스티뮬레이터 |
| M9-써마지 | 써마지FLX |
| M8-CO2레이저 | CO2프락셔널 |
| M8-혈관레이저 | 혈관 |
| M8-저출력레이저(두피) | 저출력레이저(LLLT) 두피 |
| M8-다이오드 | 다이오드 레이저 |
| M9-리프팅기기 | 기기 리프팅 |
| M15-필링 | 필링 |
| M4-리쥬란 | 리쥬란힐러 |
| M1-사각턱보톡스 | 보툴리눔 톡신 사각턱 |
| M2-턱필러 | 필러 턱 |
| M2-코필러 | 필러 코 |
교체 전 각 값의 자리 수를 세어 표에 적고, 교체 뒤 옛 값이 0 임을 확인. from_category/to_category 는 건드리지 않는다. 표에 없는 from/to 값(34종 · taxonomy 이름과 이미 일치)은 그대로.

## 2. taxonomy.json — M8(레이저) › 하위분류 label 「기타」(id M8-6) 의 items 끝에 항목 2 추가
- 「저출력레이저(LLLT)」
- 「다이오드 레이저」
항목 레코드 꼴은 같은 하위분류의 기존 항목(예 「알렉산드라이트」)과 같은 키 집합으로 만들되, **값은 name 만 채우고 나머지 키는 그 하위분류 기존 항목에서 비어 있을 때 쓰는 빈 값(null·[]·{} 중 원본이 쓰는 꼴)** 으로 둔다. 설명·safety·가격 등 어떤 내용도 지어 넣지 않는다. id 가 있는 꼴이면 기존 id 규칙(`auto-new-…` 또는 순번)을 README 에 적힌 대로, 없으면 하위분류 안 다른 항목과 같은 방식으로 — 확인해서 그대로.

## 3. README.md 작성 규칙에 추가
- synergy 의 from/to 는 taxonomy 정식 이름(계열 name · 하위분류 label · 항목 name · 제품 name) 그대로. `Mxx-` 접두 금지(category 칸이 담당). 부위가 붙으면 「이름 부위」로 띄어 적는다(「마이크로니들링(MTS) 두피」). 시술 튜플이면 「계열 부위」(「필러 턱」).
- taxonomy 에 없는 이름을 synergy 에 쓰지 않는다. 필요하면 taxonomy 에 항목을 먼저 세운다.

## 4. CHANGELOG.md 에 3판 행 1줄
| 3 | 2026-11-06 | 2판 | synergy from/to 줄임말 18종(N자리) → taxonomy 정식 이름 · taxonomy M8›기타 항목 2 신설(저출력레이저(LLLT) · 다이오드 레이저 — name 만) · README 규칙 2 | 사용자(이건학) 결정 · 워커 적용 |

## 5. HASHES.txt 전체 재계산(21 파일 + step1 포함 여부는 지금 파일 그대로 · 형식 유지).

## 보고
표 1 의 자리 수 · 바뀐 파일 5개의 diff 통계(줄 수) · 두 JSON 파싱 OK · HASHES 바뀐 파일 2 · build/check 결과 요약(①~⑨ PASS 여부 · 개체·엣지 수 7차 대비 증감만).
