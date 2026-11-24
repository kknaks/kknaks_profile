# [hub] 부작용 분류(일시적 · 주의 · 위급) + 모달용 칸 — silver · gold · 허브 (사용자 승인 11-22 「이 정도만 발주」)

너는 WP-H 를 한 허브 워커다. 허브 워크트리 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo` · silver 작업 사본 `S=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. 커밋 0 · push 0 · 서브에이전트 0 · stg · 원격 DB 0 · **18105 · 18222 손대지 마라**(재기동은 코디) · 허브 시험은 관련만. WP-H 때와 같은 꼴(작업 사본 gold-build · gold-check · 허브 headers · alembic · 회귀 조건 · 매핑 JSON meta 해시 갱신 — `$W/wph-report.md` 참고).

## 사용자 결정(11-22)
상담 모달의 효과 · 부작용을 고객이 보기 좋게 정리한다. 부작용은 **일시적 / 주의 / 위급**으로 나눈다. 기준은 허브에 둔다(모든 병원 · 시술 같은 기준).

## 할 일
1. **분류 기준표** — silver `adverse.csv` 에 칸 `severity_class`(일시적 · 주의 · 위급) 를 더한다. 기본 = 부작용 대분류(묶음)로: 일시적 = 국소 반응 · 근육 반응 · 결과 불만족 · 색소 변화 / 위급 = 과민반응(아나필락시스 · 알레르기 중증) · 눈 손상(시야 장애 · 실명) · 혈관 폐색 · 피부 괴사 · 호흡곤란 / 주의 = 그 사이(신경 손상 · 조직 손상 · 감염 · 전신 반응 중 위급 아닌 것 등). 하위 부작용은 원장 문장(심한 정도 · 대처법의 「즉시 · 응급 · 병원」 등)으로 보정. 근거 source_ref(「보충 · 분류 기준 2026-11-22 · 대분류 + 원장 문장」). **표 `$W/adverse-class.csv`(코드 · 이름 · 대분류 · 분류 · 근거) 와 「위급」 목록을 리포트 맨 앞에** — 사용자가 위급 목록을 확인한다.
2. **허브 응답 칸** — `facets?facet=adverse` 행에 `severity_class` · **대처법 원문**(`guidance_texts` — adverse_guidance text · timing · level 원문 · 순서 그대로 · 줄바꿈 이음)을 더한다(지금은 `n_guidance` 개수만). `facets?facet=outcome` 행은 이미 onset · peak · duration 있음 — 그대로. 기존 칸 · 행 같음(회귀).
3. silver-check → gold-build → gold-check PASS · 허브 headers · alembic(DB 판 칸) · 관련 시험 · 매핑 JSON v3 meta 해시만 갱신(두 경로 · items · products · sites 바이트 같음 · 새 sha).
4. 리포트 `$W/adverse-class-report.md`: **위급 목록(맨 앞)** · 분류 셈(대분류별 · 분류별) · 바뀐 파일 · 시험 · 회귀 · 새 gold · aux · JSON sha · 18105 재기동 env.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "hub 완료: 부작용 분류" --body "위급 수 / 해시 / sha"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] hub 부작용 분류 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] hub: <질문>" --enter`
