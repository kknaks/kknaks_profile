# [hub] SPEC-010 WP-H — 허브 칸 셋(method_codes · method_texts · country) (사용자 승인 11-20 「응!!!」)

너는 procedure-hub 허브 워커다. 앞 맥락 없음. 허브 워크트리 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo`(branch kknaksss/phub-consult-demo) · silver 작업 사본 `S=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model`. **커밋 0 · push 0 · 서브에이전트 0 · stg · DB(원격) 0 · 사용자 포트(18105 · 18222) 손대지 마라**(18105 재시작은 코디). 시험은 관련 파일만(전체 pytest 금지). 허브 워크트리의 미추적 그림 18 파일(`assets/procedure-images/...`)은 건드리지 마라(다른 작업 산출).

정본: `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **`$W/SPEC-010-consult-myeongdong.md` 0.2.2 §13 「WP-H 계약」 WH1 ~ WH7** · D-12 · 검수 `$W/review-spec-010-r2.md` N1 · `$W/review-spec-010-r5.md`.

## 할 일
1. WH1 ~ WH7 그대로: 작업 사본 `$S/gold/gold-build.py` · `gold-check.py`(새 칸 셋 · 되짚기) → gold 재빌드 · gold-check PASS · 새 gold_hash · aux_hash.
2. 허브 백엔드(`$H/backend`): `headers.py` 등 g_profile 칸 계약 · alembic migration 하나(DB 판 칸 — 로컬 시험 DB 만) · 관련 시험(gold CSV 판 · 실물 gold 판 env 로) 통과.
3. WH6 회귀 넷 + 케이스 3 표본(방법 하나 · 둘 · 그림 없던 방법) · 제품 country 표본 대조.
4. WH5: `$P/reference/2026-11-19-myeongdong-kos/build_mapping_json_v3.py`(P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇) 로 매핑 JSON v3 meta 해시만 갱신(두 경로 · items · groups · sites · products · product_categories 바이트 같음 확인 · 새 sha).
5. 리포트 `$W/wph-report.md`: 바뀐 파일(허브 diff 요약 · 작업 사본) · 시험 · 회귀 · 새 해시 · JSON 새 sha · 18105 재시작에 필요한 env(코디가 함).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "hub 완료: WP-H" --body "시험 / 회귀 / 해시 / JSON sha"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] hub WP-H 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] hub: <질문>" --enter`
