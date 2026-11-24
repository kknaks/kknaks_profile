# [hub] 부작용 분류 다시 — (나) 기준 (사용자 승인 11-22 「응 그렇게 해」)

너는 부작용 분류를 한 허브 워커다. 앞 작업 `adverse-class-hub-task.md` · 리포트 `adverse-class-report.md` · 표 `adverse-class.csv` 위에서 고친다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `S=$W/silver-model` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo`. 커밋 0 · 서브에이전트 0 · stg · 원격 DB 0 · **18105 · 18222 손대지 마라**.

## 사용자 결정(11-22)
- 앞 분류(대분류 기준 · 원장은 보정만)는 원장 응급 신호를 놓쳤다(응급 대처 · 중증인데 위급 아님 58 — 코디 대조).
- **(나) 기준:** 원장 응급 대처(adverse_guidance level `emergency` · `emergency_signs`)와 중증 표시(adverse_risk severity critical · severe · 「심각」 · 「생명」 · 「중대한」)를 줄마다 원문으로 본다.
  - 그 줄이 **부작용 그 자체**가 응급 · 중증이라는 뜻이면(예 아나필락시스 · 혈관 폐색 · 감염 파급 · 봉와직염 · 화상 · 신경 마비) → 그 부작용 **위급**.
  - 그 줄이 **악화 조건**(「~가 심해지면」 · 「~가 동반되면」 · 「~가 지속되면 즉시 내원」)이면 → 부작용 분류는 올리지 않고, 그 원문을 **「이럴 땐 바로 병원」 경고**로 둔다.
  - 응급 · 중증 줄이 없는 부작용은 앞 분류(대분류 기준) 그대로.
- 판정은 줄마다 원문 근거로 · 지어내기 금지 · 애매하면 「사람 판단」 목록(50 안쪽 · 묶어서 · 추천).

## 할 일
1. `adverse-class.csv` 다시: 칸 더함 — `class_basis`(대분류 / 원장 응급 · 중증 자체) · 근거 원문.
2. 줄 판정 표 `$W/adverse-emergency-lines.csv`: 응급 · 중증 줄마다 adverse 코드 · 이름 · 줄 원문 · 판정(자체 / 악화 조건 / 사람 판단) · 근거.
3. silver: `adverse.severity_class` 다시 · 「이럴 땐 바로 병원」 은 새 칸 없이 **adverse_guidance 의 그 줄을 표지**(칸 `alert` = true · 앞 작업 허브 응답 나란한 칸에 `guidance_alerts` 하나 더 — 같은 순서 · 개수)로. gold-build · gold-check · 허브 headers · alembic(앞 작업 b202611220001 고침 — 새 파일 만들지 말고) · 관련 시험 · 매핑 JSON meta 해시.
4. 리포트 `$W/adverse-class2-report.md` 맨 앞: **위급 목록**(앞 13 대비 더함 · 뺌) · **「이럴 땐 바로 병원」 문구 목록**(부작용별 원문) · 사람 판단 묶음 · 셈(분류별) · 해시 · JSON sha.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "hub 완료: 부작용 분류 (나)" --body "위급 수 / 경고 수 / 사람 판단 / 해시"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] hub 부작용 분류 (나) 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] hub: <질문>" --enter`
