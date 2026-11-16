# 발주서 — 재료 · 기전 · 조직 사전 확정본 만들기

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표

초안 `orchestration/work/phub-ledger-redesign/silver-model/drafts/atoms/` 의 `material.csv`(137) · `mechanism.csv`(54) · `tissue.csv`(24) 를 아래 수정만 해서 **확정본**으로 만든다. 새로 조사하지 않는다 — 초안의 행·basis 를 그대로 쓰고, 고칠 때 원문이 필요하면 basis 포인터로 원장을 확인한다.

## 2. 산출물

`orchestration/work/phub-ledger-redesign/silver-model/silver/` 아래에 새로 쓴다:
- `material.csv` · `mechanism.csv` · `tissue.csv` · `method-candidates.csv` · `atoms-notes.md`

CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. `drafts/` 와 `silver/modality.csv` 등 다른 파일은 고치지 않는다(읽기만). 커밋·push 금지.

## 3. 읽을 것

- 초안: `silver-model/drafts/atoms/material.csv` · `mechanism.csv` · `tissue.csv` · `atoms-notes.md`
- 원장(필요할 때만, basis 로): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json`

## 4. 수정 (사용자 확정)

**① 이름 칸을 셋으로: `name_ko` · `name_en` · `abbr`. 이름 안의 괄호를 없앤다.**
- 괄호 안이 약어면 → `abbr` (히알루론산(HA) → 히알루론산 / Hyaluronic Acid / HA · 고주파(RF) → 고주파 / Radiofrequency / RF)
- 영어 약어가 바깥, 한국어가 괄호 안이면 뒤집는다: **SMAS(근막층) → name_ko 근막층 · abbr SMAS** · AHA(알파하이드록시산) → 알파하이드록시산 / AHA
- 괄호 안이 같은 것의 다른 한국어 표기면(젖산(락틱산) · 미세바늘(마이크로니들) · 망상진피(그물진피)) → `aliases` 칸(`;` 로 여럿)
- 괄호 안이 분류·설명이면(트리암시놀론(스테로이드) · 5-ALA(광감작제) · 천연 허브(식물 추출물)) → 상위 행이 사전에 있으면 `parent_code`, 없으면 `description` 에 넣는다. 상위 행을 새로 지어 만들지 않는다
- 괄호 안이 구성 성분이면(오메가3(EPA·DHA)) → `aliases` 가 아니라 `description` 에 원문대로. PN/PDRN 처럼 원장이 섞어 쓰는 것은 한 행 유지, notes 에 한 줄
- `name_en` 은 원장에 영어 이름이 있을 때만(초안 `name_en`·원장 영문 표기). 없으면 비운다 — 지어 넣지 않는다
- 한국어 이름이 원장에 없고 영어로만 쓰이는 것(PMMA · PLCL · NAD+ 등)은 `name_ko` 에도 원장 표기 그대로

**② 수치 속성은 칸으로.** 레이저·광 파장(755nm · 10600nm · 415nm · 1540·1550nm …) → `wavelength_nm`(범위·여럿이면 원문대로 `1540;1550`). 이름에서는 뺀다(알렉산드라이트 레이저(755nm) → 알렉산드라이트 레이저 · wavelength_nm 755). `1064nm` · `808·810nm` 처럼 파장만 이름인 하위 행은 name_ko 를 `1064nm` 로 두고 wavelength_nm 도 채운다.

**③ 기전에 섞인 전달 방식은 기전에서 뺀다.** `MEC-080 성분 전달` 과 그 하위(정맥 투여로 성분 공급 · 진피 국소 주입 · 니들리스 고압 분사 주입 · 경피 흡수 촉진 및 그 하위 · 미세 채널 형성 등)처럼 **어떻게 넣느냐**를 말하는 행은 `mechanism.csv` 에서 빼고 `method-candidates.csv`(다음 단계 「방법」 사전의 후보)로 옮긴다. 칼럼: `code`(초안 코드 유지) · `name_ko` · `name_en` · `abbr` · `parent_code` · `description` · `basis`. 작용 원리(아세틸콜린 차단 · 채움 · 선택적 광열 · 광음향 · 열응고 · 항산화 · 멜라닌 생성 억제 …)는 기전에 남긴다. 경계가 애매한 행은 notes 에 근거와 판정.

**④ 판단 2건 반영.**
- 레이저 펄스(Q-스위치 · 롱펄스) · 프락셔널 · RF 극성(모노폴라 · 바이폴라)은 **케이스의 방법**이다. 재료에 하위 행으로 이미 있는 모노폴라 RF · 바이폴라 RF 는 재료에서 빼서 `method-candidates.csv` 로 옮긴다. 펄스·프락셔널이 재료·기전 행으로 있으면 같이 옮긴다.
- 수액 성분별 작용(케라틴 합성 · 단백질 합성 · 항염 등)은 기전 행으로 **추가하지 않는다**. 지금 있는 항산화 · 멜라닌 생성 억제 · 세포 대사 촉진은 둔다.

**⑤ 그 밖에는 초안 그대로.** 코드(MAT-·MEC-·TIS-)는 유지한다(옮긴 행 코드도 유지 · 빈 번호 생겨도 됨). 행을 새로 추가하지 않는다. basis 포인터는 그대로 옮긴다.

## 5. 최종 칼럼

- `material.csv`: code · name_ko · name_en · abbr · aliases · kind · parent_code · wavelength_nm · description · basis
- `mechanism.csv`: code · name_ko · name_en · abbr · aliases · parent_code · description · basis
- `tissue.csv`: code · name_ko · name_en · abbr · aliases · kind · parent_code · description · basis
- `method-candidates.csv`: code · name_ko · name_en · abbr · parent_code · description · basis

## 6. notes (짧게)

1. 행 수: 초안 → 확정(옮긴 행 수 · 대상)
2. 괄호 처리 표: 원래 이름 → name_ko / name_en / abbr / aliases / description / parent (괄호 있던 행 전부)
3. 기전에서 방법 후보로 옮긴 행과 이유 · 경계 판정
4. 대표 5사례(보톡스 · HA 필러 · HIFU · 레이저토닝 · 백옥주사)가 확정본으로도 표현되는지 한 표

## 7. 완료 기준

- 세 사전의 `name_ko` 에 괄호가 0 · 약어는 abbr · 파장은 wavelength_nm.
- 전달 방식 · RF 극성 · 펄스·프락셔널이 재료·기전에 남아 있지 않다(method-candidates 에 있다).
- 초안에서 사라진 행이 없다(확정 3개 + method-candidates 합 = 초안 합). 모든 행에 basis.
- 산출물 외 변경 없음(`git status` — `silver-model/` 은 미추적 폴더라 산출물 경로만 새로 생겼는지 확인).

## 8. 질문 · 완료 보고

막히면 원문을 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/silver/atoms-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "atoms 확정본 완료: orchestration/work/phub-ledger-redesign/silver-model/silver/" --enter`
