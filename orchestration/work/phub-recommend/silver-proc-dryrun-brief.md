# 시술 축 드라이런 1차 발주 — ⑧ 시술 조각 · ⑨ 미해결 참조 · 분류 항목 부분 해석을 규칙으로 얼마나 닫히는지 세기 (2026-11-08 · 사용자 승인 대기)

읽을 것(순서): `HANDOFF-2026-11-05.md`(원칙 · 「11-06」 절 · 마지막 「순서 재변경」 줄) → `erd-v3.3.md` §1.3(분해 · 분석기 V3.3-B) · §1.4(시술 튜플 what 규칙 · 장비 · 성분 · V3.3-F) · §9.24(세분 설계안 F) · §12 → `silver-dryrun-brief.md` · `silver-dryrun3-brief.md`(부작용 축 드라이런 — 같은 방식) → `silver-v3/out-dryrun3/report.md` §0 → `silver-v3/README.md` → `silver-v3/out/report.md` §4 · §16.

## 목적
8차(`silver-v3/out/`) 시술 축에 남은 세 묶음이 아래 규칙을 넣으면 몇 자리가 기계로 닫히고 몇 자리가 남는지 **센 값**으로 보고한다. 결정이 아니라 **드라이런**이다 — 규칙과 ERD 문장은 사용자 결정 뒤 ERD v3.3 에 들어간다.

| 묶음 | 8차 수 | 출처 |
|---|---|---|
| ⑧ 미등록 조각(procedure 축) | 453 묶음(자리 544) | `out/conflicts.jsonl` kind=unregistered_value · target_type=procedure_fragment |
| ⑨ 미해결 참조 | 240 | kind=unresolved_reference — reason: unregistered 185 · 고민 사전 일치 없음(질문 12) 29 · multi_primary 18 · 하위분류 사전 없음(질문 23) 6 · combo_outside_fragment 2 |
| 분류 항목 부분 해석(catalog_partial) | 251 | `out/report.md` §4 |

⑧ 의 다른 사전 27(problem 7 · pih_risk_level 5 · severity 4 · reaction_level 4 · manufacturer 2 · modality 2 · country 2 · accuracy_rubric 1)과 ⑨ 의 「고민 사전」 29 는 시술 축이 아니다 — **세기만 하고 규칙을 적용하지 않는다**(행선지 표에 「시술 축 아님」으로).

## 도구 · 절대 규칙
- `silver-v3/.venv-kiwi/bin/python`(kiwipiepy 0.24.1) 만. 없으면 `python3 -m venv silver-v3/.venv-kiwi && silver-v3/.venv-kiwi/bin/pip install kiwipiepy==0.24.1`.
- 코드 `silver-v3/dryrun-proc/`, 산출 `silver-v3/out-dryrun-proc/` 에만 쓴다. `out/`·`decisions/`·`baseline/`·`build.py`·`lib/`·`dryrun*/`(기존)·`out-dryrun{,2,3}/`·`erd-v3.*`·`bronze/` 수정 금지. 기존 lib 는 import 해서 쓰고 고치지 않는다(필요하면 dryrun-proc 에서 감싸거나 복사).
- 끝에 8차 불변 확인: `python3 build.py && python3 check.py && python3 tests/run_tests.py` 출력 그대로 · determinism key 가 `baseline/manifest-8차.json` 과 같음.
- 추정 매칭 금지 · 임상 동치 금지(「비슷해 보여서」 같은 시술로 묶지 않는다). 수치는 센 값만 · 추정이면 「추정」.
- 원장에 없는 분류·등급·라벨을 만들지 않는다(unreviewed · 2등급 · 묶음 라벨 금지). 임시 사전 값은 드라이런 전용 표로만.
- 애매하면 적용하지 않고 「애매 — 사용자」로 센다. 남는 수를 줄이려 규칙을 넓히지 않는다.
- 게시 · 커밋 · 아티팩트 금지. 보고는 `out-dryrun-proc/report.md` + `dryrun-proc.json` 과 종료 메시지.

## 적용할 규칙(드라이런 가정 — 사용자 승인 필요 · 부작용 축 V3.3-B · R2 · R4 와 같은 꼴)
P1 **분석기 토큰화.** 시술 라벨을 V3.3-B 와 같은 분석기(판 고정)로 나눈다. 사전 값(계열 · 하위분류 · 분류 항목 523 · 제품 · 성분 · 기법 · 부위 · 고민)은 사용자 단어로 등록해 쪼개지지 않게 한다. 통째 일치가 먼저(§1.3 그대로).
P2 **원장 전체 씨앗.** 원장 21 파일 전부에서 **시술 이름 칸**(taxonomy 항목 name · products name · market-pricing items name · procedure-comparison procedures name · treatment-* · problem-packages · synergy · post-procedure-timeline name)에 **그 말 하나로** 쓰인 값을 씨앗으로 모은다(파일 · locator · 횟수). 씨앗은 기존 사전과 대조만 — 사전 추가는 제안 표로(결정 dictionary_add 는 사용자).
P3 **부위 말은 부위 칸.** 라벨 안의 부위 말(바디 · 턱라인 · 두피 · 전체얼굴 · 힙 · 이마 · 입술 …)은 site 로 — 사전에 있으면 그 값, 없으면 드라이런 임시 부위 값(표). 괄호 안 부위(「이모드 (힙)」「제네시스 (전체얼굴)」)도 같다.
P4 **규격 · 수량 · 가격 단위는 시술이 아니다.** 「1cc」「부위당」「수입」「810nm」 같은 규격·단위 말은 spec 메모로 보존(칸 아님 · 세분 F 가 정해지면 다시 본다). 목록은 원장에서 실제로 라벨 안에 붙은 말을 뽑아 표로.
P5 **괄호 병기는 동의어.** 원장이 「리쥬란 (PN주사)」「PDT (광역동치료)」「HIFU 울쎄라」처럼 나란히 쓴 쌍은 같은 값으로 본다(부작용 R4 · ERD 병기 쌍 처리와 같음). 괄호 안이 부위(P3) · 규격(P4) · 깊이·세기(P6)면 병기가 아니다.
P6 **깊이 · 세기 · 실 재질/형태는 떼지 않는다.** 저출력 · 심부 · 얕은 · 딥 · 약한 · 중간 깊이 · PDO · PCL · PLLA · 코그 · 모노 · 볼륨실 은 수식어로 버리지 않고 「세분 F 대기」로 따로 센다(떼면 심부/얕은 필링이 같은 튜플이 됨 · §9.24). F-1/F-2/F-3 중 어느 안이 몇 자리를 받는지 **안별로 세기만** 한다(적용 0).
P7 **`+` · `/` · 콤보는 §1.3 규칙 그대로.** 새 규칙을 만들지 않는다 — 콤보 멤버로 갈린 뒤 멤버마다 P1~P6.
P8 **사전에 없으면 새 값 후보(미연결 없음).** P1~P7 뒤에도 사전에 안 닿는 핵심어가 시술 · 제품 · 성분 이름이면 「새 값 후보」로 세운다(이름 · 원장 횟수 · 원문 예 · 어느 사전 후보 · 비슷한 기존 값 = ⑦ 접기 후보). 시술 이름이 아닌 일반 말(주사 · 시술 · 후 · 리프팅 · 재생 · 회복력 …)은 기법 · 목적 · 메모 중 어디로 가는지 원장 칸으로 판정하고, 판정이 안 서면 「애매 — 사용자」.

## 보고(`out-dryrun-proc/report.md` + `dryrun-proc.json`)
1. 묶음 × 규칙 표: ⑧ 453 · ⑨ 240(reason 별) · catalog_partial 251 × P1~P8 로 닫힌 수(겹치면 먼저 적용된 규칙에 셈 · 적용 순서 P1→P7→P3→P4→P5→P6→P2 대조→P8) · 시술 축 아님 · 애매 — 사용자 · **남는 자리 수**.
2. **사람이 볼 최종 목록**(산출물의 핵심 · 각 표 머리에 행 수): (가) 새 값 후보 전부(P8) / (나) ⑦ 접기 후보 쌍 / (다) 애매 전부(원문 · 왜) / (라) 세분 F 대기 전부(P6 · 라벨 · 말 · 안별로 받는지) / (마) multi_primary 18 · 질문 23 의 6 · combo 2 각각의 원문과 왜 규칙으로 안 닫히나.
3. 규칙이 만든 변경 전수: 분석기 사용자 단어 목록 · P2 씨앗(말 · 파일 · 횟수 · 기존 사전 여부) · P3 임시 부위 값 · P4 규격 말 · P5 병기 쌍 · P8 일반 말 판정 표.
4. 8차 ⑧ 453 · ⑨ 240 · catalog_partial 251 → 드라이런 행선지 전수(「이유 없음」 0).
5. 시술 튜플 수 · complete/partial 재계산(8차 partial 322 · complete 288 대비).
6. 8차 불변 확인 출력.
7. 빌더 반영 설계 메모(사실만): 규칙을 `lib/` 에 넣으려면 어느 모듈(decompose · anchors · entities32 …)의 어느 함수가 바뀌는지 · 새 결정 kind 가 필요한지 · ERD v3.3 소개정 문장 초안 한 단락.

## 하지 말 것
- P1~P8 밖의 판단(임상 동치 · 의미 동의어 · 「같은 시술 같다」)을 넣지 않는다.
- 세분 F 안을 고르거나 적용하지 않는다(세기만).
- 시술 축 아닌 묶음(⑧ 다른 사전 27 · ⑨ 고민 29)에 규칙을 넓혀 적용하지 않는다.
- 원장(bronze) 값을 고치지 않는다 — 원장 오기로 보이는 자리는 「4판 후보」 표로만(locator · 원문 · 왜).
