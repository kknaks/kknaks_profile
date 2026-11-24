# [researcher] 명동점 약물 · 기기 82 → 허브 제품 매핑 초안 (읽기만 · 사용자 승인 11-19)

너는 procedure-hub 조사 워커다. 앞 맥락 없음 — 이 문서만으로 일한다. **읽기만** · 산출 파일 2 개만 만든다 · 커밋 0 · 서브에이전트 0 · 웹 조사 0.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `R=$P/reference/2026-11-19-myeongdong-kos` · `W=$P/orchestration/work/phub-consult-demo`

## 입력
- 명동점 진료항목 CSV `$R/myeongdong-kos-medical-services-20261119.csv`(324 · utf-8-sig) — `구성1 ~ 구성9 약물·기기` · `구성n 출처` · 진료항목명 · KOS 약물 · 기기 칸. 서로 다른 이름 82(KOS 칸 73 · 세라핏 설명 배합 9).
- 허브 제품: 로컬 PG(SELECT 만 · `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 값 출력 금지) `s_product`(315 · code · name_ko · name_en · kind · parent_code · description) · 다른 이름(`g_entry` · silver `alias.csv` = `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model/silver/alias.csv` **읽기만** — 다른 워커가 같은 폴더의 site · alias 를 고치는 중이니 제품 행만 읽어라) · `s_product_organization` · `s_organization`(회사) · `s_product_procedure` · `s_case_product`.
- 앞 1 차 대조: `$R/match-gold-20261119.json`(KOS 약물 · 기기 72 중 정확 24 · 정규화 2).
- **사용자 확정(그대로)**: 밀리핏 = PRD-729(DCA) · 하프셀라인 = 0.45% 식염수 희석액(제품 아님) · KOS 약물 「보톡스」 = 국산 톡신 일반 이름표(앨러간 보톡스 아님) · 「앨러간」 = 회사 이름 · 「수입」 = 원산지 이름표 · 써마지FLX = PRD-417(써마지 PRD-416 의 하위).

## 할 일 — 82 이름마다 판정 하나
| 판정 | 뜻 |
|---|---|
| 허브 제품 있음 | 이름 · 다른 이름 · 하위 제품으로 바로 닿음(코드 · 근거 칸) |
| 다른 이름만 추가 | 허브에 같은 제품이 있는데 이 표기가 없음(예: 「앨러간」 → 회사 앨러간의 보톡스 제품인지 — 회사 표로 확인될 때만) |
| 허브에 없음(보강 후보) | 실제 제품 · 성분인데 허브 제품에 없음 |
| 제품 아님 | 희석액 · 이름표 · 원산지 · 일반 마취/보조 성분 등 — 무엇인지 적는다 |
| 확인 필요 | KOS · 허브만으로 못 정함 |
- 근거는 허브 표 · 칸 · 코드와 KOS 진료항목명(그 이름이 쓰인 대표 진료항목 1~2)으로만. **추정 금지.**
- 이름 하나가 진료항목에 따라 다른 제품을 가리키면(예: 「보톡스」 가 진료항목명에선 제오민 · 코어톡스) 그 사실을 메모에 · 판정은 「확인 필요」 또는 「제품 아님(이름표)」.
- 보강 후보에는 KOS 에서 알 수 있는 것만: 종류 추정이 아니라 KOS 칸(약물 / 기기) · 쓰이는 진료항목 수 · 대표 진료항목명.

## 산출
1. `$R/kos-product-map-draft.csv`(utf-8-sig) — 한 줄 = 이름 하나 · 칸: `이름 · 출처(KOS 약물칸 / KOS 기기칸 / 설명) · 진료항목 수 · 대표 진료항목명 · 판정 · 허브 제품 코드 · 허브 제품 이름 · 근거 · 메모`. 가격 · KOS id 0.
2. `$W/research-product-map.md` — 판정별 수 · 보강 후보 목록 · 확인 필요 목록 · 「보톡스 · 앨러간 · 수입」 처리 결과.

## 검증
82 줄(빠짐 0) · 허브 코드 전부 실재(SELECT 대조) · `git -C $P status --short` 로 새 파일이 위 2 개뿐(silver-model 은 다른 워커 · gitignore).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_95fc05b6-11b1-43b8-a6a1-995dac0b50b8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 제품 매핑 82" --body "판정별 수 / 보강 후보 / 확인 필요"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] researcher 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
