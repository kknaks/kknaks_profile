# 지시서 — ③ 관계 보완: 빠진 잎 ~160 채우기 + 조합 메뉴 진술을 package 로

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

③ 관계(적응 · 효과 · 부작용 위험 · 금기 · 시술 간 관계 · 패키지 · 문헌)를 다섯 초안으로 만들어 silver 에 합쳤다(검증 PASS — `notes/relation-notes.md`). 합치며 두 가지가 남았다(같은 notes §5-1 · §5-3).

## 2. 읽을 것

- `notes/relation-notes.md`(특히 §1 · §3 · §5) · `notes/relation-judgment.csv` · `notes/relation-id-map.csv` · `notes/relation-conflicts.csv`
- `drafts/relation-merge/`(merge-build · merge-check · build-log.json) · 표 구조 정본 `drafts/relation-pilot/relation-notes.md` §9-2 · 초안 규칙 `../relation-pilot-brief.md` · `../relation-a-brief.md`(§0 · 숫자 · 원문 · 충돌 규칙)
- `silver/` 전부 · `notes/combo-item-judgment.csv`(② 판정)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15 「그렇게 하자」)

**A. 아무 초안도 담지 않은 관계 잎 채우기**(notes §5-1 — 약 160잎 · 25 항목: 신펄 · 소프라노 티타늄 · LDM · 엑소좀 두피주사 · 스킨보톡스 · 두피 PRP · 하모니카 · 볼뉴머 · 미녹시딜 두피 메조 · 프로락틴주사 · 알렉스필 · LDM초음파관리 · 그 밖 13 항목 — 이브아르 · 쥬비덤 · 레스틸렌 · 벨로테로 제품 항목 등).
- 대상: `relation-judgment.csv` 에서 이유가 「다른 계열(② 판정 …)」이고 그 잎을 관계 행으로 담은 초안이 없는 잎 **전부**(목록을 다시 뽑아 notes 에 — 위 이름은 예시). 
- 처리: ② 판정이 가리키는 시술 · 케이스 · 제품(그 항목이 제품이면 제품 층)에 붙여 관계 행을 만든다. 규칙은 초안과 같다 — 원장 글자 그대로 · 숫자는 원문에 있을 때만 · 서술 등급 그대로 · 원장 충돌은 보수적 · 전용 원장(같은 대상 · 같은 코드에 이미 행이 있으면 근거만 합치거나 값이 다르면 행을 나누고 충돌 기준대로 · `relation-conflicts.csv` 에 새 RCF).
- 판정 행은 합본 행 id 로 바꾸고 이유에 옛 판정을 남긴다.

**B. 코드 있는 조합 메뉴의 진술 → package 대상으로**(notes §5-3 — C 의 브라이트닝레이저 · 여신토닝 등 · 다른 초안에도 같은 꼴이 있으면 함께): 메뉴를 이루는 케이스 · 시술마다 같은 진술을 붙여 둔 행을 그 메뉴의 package 행(없으면 package + package_item 을 ② 판정 코드로 만듦)에 붙는 행 하나로 모은다. 메뉴 원문에 없는 값은 비운다(§5-2 와 같은 기준). 케이스 자신의 진술(메뉴가 아닌 원장 자리)은 그대로 둔다.

**C. 그대로**: §5-2 메뉴 행 빈 값 · §5-4 「고려 가능」 polarity 해당 없음 · §5-5 package 항목 13.

## 4. 쓰기 · 검증

- 고치기 전 silver 관계 20표 · `source_ref.csv` 와 notes 의 relation-* 를 `archive/silver-before-relation-gapfill/` 에 복사.
- silver 관계 표에 행 추가 · 대상 변경(B)만. id 는 이어서 매김(기존 id 는 바꾸지 않는다 — B 로 모은 행은 남는 id 하나 · 없어진 id 는 대응표 `notes/relation-id-map.csv` 에 덧붙임). source_ref 는 덧붙임(앞쪽 행 바이트 그대로) · B 로 대상이 바뀐 행의 근거는 남는 행으로.
- 스크립트 · 작업 notes 는 `drafts/relation-gapfill/`(`gapfill-build.py` · `gapfill-check.py` · `gapfill-notes.md`). 원장 변경 · 커밋 · push 금지.
- `gapfill-check.py`: merge-check 기준 전부를 갱신된 silver 에 대해 다시(참조 · id · 근거 · 원문 · 숫자 대조 · polarity) + A 대상 잎 전부가 관계 행 또는 「안 담음 — 이유」(담을 칸 없음 0) · B 로 모은 행의 원래 값 보존(대응표) · 관계 밖 silver 표 바이트 불변 · **입구 · 매핑 현황 다시 집계**(notes §4 와 같은 셈법, 전/후 — 특히 고민 192 / 50 / 18 이 어떻게 바뀌었나).
- 결과를 `drafts/relation-gapfill/gapfill-notes.md` 에: A 대상 잎 목록 · 처리 수(표별) · B 로 모은 메뉴 · 행 수 · 새 충돌 · 매핑 전/후 · 사용자 판단(새로 나온 것만) · 검증 출력. `notes/relation-notes.md` 끝에 「## 7. 보완(11-15)」 요약 몇 줄 + 링크.

## 5. 완료 보고

범위를 넓히지 않는다(새 판정은 A 대상 잎만 · 사전 행 추가 · ② 코드 변경 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/relation-gapfill/gapfill-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "관계 보완 완료: drafts/relation-gapfill/gapfill-notes.md" --enter`
