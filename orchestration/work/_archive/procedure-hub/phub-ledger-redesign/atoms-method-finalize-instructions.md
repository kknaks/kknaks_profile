# 방법 사전 확정 수정 (사용자 승인 2026-11-10)

## 고칠 것 — `silver-model/drafts/method/method.csv`
1. MET-063 저에너지 반복 조사: aliases 에서 「토닝」「레이저 토닝」 삭제(레이저토닝은 케이스 이름이지 방법이 아니다). 남은 aliases 는 그대로.
2. MET-001 정맥 투여: aliases 에서 「수액」 삭제(수액은 시술·계열 이름이다).
3. MET-004 피내 주사: aliases 에서 「intradermal」 삭제. name_en 이 비었으면 원장 표기에 맞춰 name_en 에 넣고 name_en_source 를 원장/보충으로 판정해 채운다.
4. MET-040 니들 주입: aliases 에서 「미세 니들」 삭제(재료 MAT-301 미세바늘과 혼동).
5. 니들 정리 결정: **재료 MAT-300 니들(바늘 자체가 조직을 자극·절단 — 서브시전 등)과 방법 MET-040 니들 주입(약을 넣는 통로 — 캐뉼러와 선택지)은 다른 개념으로 둘 다 둔다.** MET-040 description 은 이 구분이 보이게 유지·다듬는다.

## 고칠 것 — `silver-model/silver/material.csv` (확정본, 이 한 칸만)
6. MAT-300 니들의 `description` 을 역할이 보이게 바꾼다: 「바늘 자체가 조직을 자극·절단하는 경우의 바늘(예: 서브시전에서 피하 섬유 밴드 절단). 약을 넣는 통로로서의 바늘은 방법 사전 MET-040 니들 주입.」 이름·다른 칸·다른 행은 건드리지 않는다. UTF-8 BOM 유지.

## 확정본으로 쓰기
7. 고친 `method.csv` 를 `silver-model/silver/method.csv` 로, `method-notes.md` 를 `silver-model/silver/method-notes.md` 로 쓴다(notes 에 이번 수정 6건을 한 절로 추가). UTF-8 BOM.
8. 이름 괄호 0 · basis 빈 행 0 · 행 수 43 유지를 확인한다.

## 완료
`git status` 로 위 파일 외 변경 없음 확인 후 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "method 확정 완료" --enter`
(worker_done 은 다시 보내지 않는다.)
