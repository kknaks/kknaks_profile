# 지시서 — 사전 보강 판단 9 반영

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 읽을 것

- `drafts/dict-fill/` 전부(특히 `dict-fill-notes.md` §4 판단 9건) · `dict-fill-build.py` · `dict-fill-check.py`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 사용자 결정 (11-14 「추천대로」 — 9건 모두 (a))

- 1 · 3 · 4 · 5 · 6 · 7 · 9 = 지금대로(데이터 변경 없음).
- **2 = product_method 로 잇기**: 비접촉 → 슬렌더엑스(PRD-336) · 도트 조사 → 울트라셀Q+(PRD-413) · 다중 깊이 조사 → 더블로골드S(PRD-406) · 듀오타이트(PRD-437). 방법 코드는 dict-fill 에서 만든 행. id 는 silver/product_method.csv 의 관례 다음 번호, 근거 source_ref(target_table = product_method, 원장 그 제품 문장 자리). 원장 문장으로 다시 확인하고, 그 제품에 그 방법을 원장이 말하지 않으면 잇지 말고 notes.
- **8 = 코그실 3 케이스(CAS-3006 · 3010 · 3012) description 고침** — tissue = SMAS 상층(TIS-012)과 맞게, 원장 문장(supraSMAS 문장) 근거 · 「」 인용 글자 그대로 · source_ref field = description 추가(옛 근거는 남김).

## 쓰기 · 검증

- 고치기 전 바뀔 silver 파일(product_method · procedure_case · source_ref)을 `archive/silver-before-dict-fill-finalize/` 에 복사.
- `dict-fill-build.py` 에 반영해 다시 돌리거나 별도 `dict-fill-finalize.py` — 어느 쪽이든 재실행 해시 같음.
- `dict-fill-check.py` 갱신: 기존 검사 전부 + product_method 새 행 4(또는 notes 에 이유) 참조 · 근거 · 중복 0 · CAS-3006/3010/3012 description 에 「」 인용 원장 글자 그대로 · 그 밖 silver 바이트 불변.
- 결과를 `dict-fill-notes.md` 끝에 「## 6. 확정(11-14)」으로(무엇을 · 검증 출력).
- 원장 변경 · 커밋 · push 금지. 범위를 넓히지 않는다.

## 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/dict-fill/dict-fill-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "사전 보강 확정 완료: drafts/dict-fill/dict-fill-notes.md §6" --enter`
