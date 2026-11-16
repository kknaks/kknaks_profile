# 지시서 — 고민 사전 v2: 대·중·소 3단 분류 + 명사형 이름 + 자세한 설명 (silver 직접 수정)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 배경

Procedure Hub 시술 원장의 실버 고민 사전 `silver/concern.csv`(252) · `concern_site.csv`(95) + 공통 `alias.csv` · `source_ref.csv` 의 고민 행. 사용자 지적:
- 최상위가 120행이라 분류가 평평하다(볼 꺼짐 · 사각턱 · 셀룰라이트가 「주름」과 같은 층). 대분류는 `kind` 칸에만 있고 행이 아니다.
- 이름에 형용사형(칙칙한 피부톤 · 불분명한 턱선 · 굵은 종아리 …)과 명사형이 섞여 기준이 없다.
사용자 결정: **대분류 · 중분류 · 소분류 3단 + 이름은 명사형 + 자세한 것은 설명(description)에.**

## 읽을 것

- `silver/concern.csv` · `concern_site.csv` · `alias.csv` · `source_ref.csv`(target_table = concern · concern_site 행) · `site.csv`
- `drafts/concern/concern-notes.md`(§1 kind 규칙 · §3 · §5 · §6) · `concern-build.py` · `concern-check.py`
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(설명 근거 · 분류 근거 — 고치지 않음). 특히 taxonomy `problem[]`(category > subcategories[].label > items[])

## 할 일

고치기 전 판을 `archive/concern-v1/`(concern · concern_site · alias · source_ref)에 복사.

**A. 3단 분류**
- **대분류** = 지금 `kind` 16종(주름 · 처짐 · 볼륨 · 색소 · 여드름 · 모공 · 홍조/혈관 · 흉터 · 윤곽 · 체형 · 두피/탈모 · 피부결 · 노화 · 피부질환 · 기타 · 전신 · 체모 — 실제 값 그대로)을 **행으로** 둔다(이미 같은 이름 행이 있으면 그 행을 대분류로). 칼럼 `level`(대분류 / 중분류 / 소분류) 추가, `kind` 칼럼은 대분류 코드와 겹치므로 지운다.
- **중분류** = 원장 taxonomy subcategory label 이 고민이면 그대로(표정주름 · 깊은주름 · 잔주름 · 얼굴 처짐 · 바디 처짐 …), 그 밖에 원장 문맥이 묶는 상위 말(동적 주름 등)이 이미 행으로 있으면 그것. **새 중분류 이름을 지어 넣지 않는다.**
- **소분류** = 구체 고민. **모든 행은 반드시 대분류 하나 아래**에 있다. 중분류가 없으면 대분류 바로 아래. 깊이는 최대 3(대 > 중 > 소). 지금 4단이 되는 곳이 있으면 notes 에 목록 + 추천.
- 어느 대분류에 넣을지는 지금 `kind` 값을 따른다. kind 가 원장 문맥과 어긋나 보이면 바꾸지 말고 notes 에.

**B. 명사형 이름**
- 원칙: name_ko = **「대상 + 상태 명사」** 명사형(예: 칙칙한 피부톤 → 피부톤 칙칙함 · 불분명한 턱선 → 턱선 불분명 · 굵은 종아리 → 종아리 굵음 · 짧은 인중 → 인중 짧음 · 꺼진 눈 → 눈 꺼짐 · 거친 피부 → 피부 거칠음 · 원치 않는 체모 → 체모 과다? 아님 — 뜻이 바뀌면 바꾸지 않는다).
- 원장에 같은 뜻의 명사형 표현이 이미 있으면 그것을 이름으로.
- 바꾼 행의 원장 표현(형용사형)은 alias(kind 별칭)로 남긴다 — 원장 말로 찾아도 닿게.
- **뜻이 바뀌거나 명사형이 어색해 판단이 안 서는 것은 바꾸지 말고 notes 「사용자 판단」 목록**(원문 · 후보 이름 · 이유). 「검은 점」 같은 굳은 명사구, 「구진」 같은 이미 명사는 그대로.
- 대상 쪽 말은 부위 사전 이름(일반 용어)에 맞춘다(예: 「중면부 하강」 → 부위 사전 이름이 「중안면」이면 「중안면 하강」, 원장 표기는 alias).

**C. 자세한 설명 (description)**
- 모든 행에 **원장 문장을 근거로** 자세하게: 무엇인지 · 어디에 생기는지 · 원장이 말하는 원인/유형 · 비슷한 고민과의 차이(예: 잔주름 vs 미세주름, 볼처짐 vs 불독살 — 원장이 가르는 대로) · 합쳐진 말(별칭)이 무엇이었는지.
- 대분류 · 중분류 행은 그 아래 범위를 원장 분류 문장으로 설명.
- **원장에 없는 임상 사실은 쓰지 않는다**(외부 보충 금지). 「드물게」 「얕게」 같은 말을 수치로 바꾸지 않는다. 설명에 쓴 근거 포인터는 source_ref(field = description)로 추가.
- 괄호는 설명 안에서는 써도 된다(이름 칸만 괄호 금지).

## 검증 (`drafts/concern/concern-check.py` 갱신 — 코디가 다시 돌린다)

- 모든 행 level 있음 · 대분류 행은 parent 없음 · 그 밖 모든 행은 대분류까지 거슬러 닿음 · 깊이 ≤ 3 · 대분류 수 = kind 종류 수.
- 이름 괄호 0 · `;` 0 · name_ko 중복 0 · 형용사형 이름 남은 것 = notes 판단 목록과 정확히 같음.
- 모든 행 description 있음 · 모든 concern · concern_site 행 근거 ≥ 1 · 참조 전부 존재.
- 보존: v1 ref 집합 ⊆ v2 · v1 이름(name_ko ∪ alias) ⊆ v2 이름 · concern_site 짝 보존(코드 바뀌면 대응표로).
- silver 의 고민 밖 표 · alias/source_ref 의 고민 밖 행 바이트 불변.
- 결과를 `drafts/concern/concern-notes.md` 끝에 「## 7. v2(11-12)」로: 단계별 행 수 · 대분류별 수 · 이름 바꾼 표(전 → 후) · 판단 목록 · 검증 출력.

## 완료 보고

범위를 넓히지 않는다(효과 · 관계 · 외부 조사 하지 않음). preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/concern/concern-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "concern v2 완료: drafts/concern/concern-notes.md §7" --enter`
