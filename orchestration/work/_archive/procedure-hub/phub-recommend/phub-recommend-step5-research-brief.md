# [researcher] 실버 5단계(단위 시술) 조사 — 계열 × 부위 × 기법 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 전부 — 특히 10-27 단위 시술 정의 · 이름 원칙 · extracted 는 5단계 · 장비 이름 = 시술 동의어 · 1단계 「제품 → 시술 범위는 5단계」 · DEC-003 시장가 · 10-28 source-map 승인(U1 단계 경계 · U5 도포 가드) · 10-29 5단계 시작 행. **정해진 것은 다시 논의하지 않는다**
- `DEC-002.md` · `DEC-003.md` · `SPEC-004.md`(단위 시술 노드 · uses_product · has_product · 이름 해석 §3.3.2)
- 정본(고정): `step1-products.json` · `step2-families.json` · `step3-sites.json` · `step4-techniques.json` · 각 `*-decisions.json`
- 지도 `source-map.json` · `.md` — **5단계로 정한 칸 45 가 입력**(+ B10 · B16 · B17)
- 재료(초안 · 확정 아님): `procedure-master-v3.json`(unit_procedures 236 · ledger_map 521 · provisional · market_rows · rejected_combinations)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` 중 지도가 5단계로 가리킨 파일 · 칸 · taxonomy modality 원장 항목 521(이름 · 꼬리표 · extracted)
- 앞 단계 교훈: `para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md` · `-step3-site.md` · `-step4-technique.md` §5 — 기준은 레포 근거부터 · 지도가 정한 칸만 · 칸 모양이 open 을 만들면 칸을 고칠 안 · **끝 조건 = 지금 원천 기준 open 0 · 가상 문장 시험 없음**

## 할 것
A. **원장 항목 521 행선지**: 항목마다 단위 시술(키) / 6단계 패키지 / 7단계 목적 / 다른 단계 / 버림 + 근거. 판정 규칙을 먼저 세우고(초안 ledger_map 은 재료) 규칙 → 행
B. **단위 시술 키**: 계열 × 부위 × 기법 — 하위 계열(재질 · 매질)을 키에 넣는 안 / 안 넣는 안 비교(키 수 · 무엇이 갈리나) + 추천. 원천에 있는 조합만
C. **이름**: 「부위 + 상담 용어」 규칙 · 원장 이름 · 메뉴명(1단계 moved_to 24) · 장비 이름(포텐자 등) · 시장가 이름 → 동의어. 이름 겹침 · 모호 목록
D. **붙는 것**: 제품 연결(라인 / 품목 단위 추천 · 1단계 recommendable 반영 · 도포 가드 U5) · extracted(「이 제품/장비로 했을 때」 — 붙는 단위) · 시장가(시술 + 제품 등급 + 규격 · 1단계 제품 행 시장가 사본 옮김) · PIH · 운영 정보 · 4단계 속성(safe_layers · 대상 근육 · 도구 · pulse_scope)
E. **넘겨받은 것 전수**: step1 moved_to 24 · step2 deferred 13 · step3 → 5단계 2 · step4 → 5단계 3 · 지도 미정 9칸 — 행선지
F. **못 정하는 것 한곳에**(사용자 지시 「모아서 한 번에」): 출처로 닫히지 않는 것 · 사람 판단이 필요한 것을 묶음 하나로 모으고 묶음마다 추천을 붙인다(빈 추천 금지)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step5-research.json` · `step5-research.md`. md 맨 위: ① 결정 묶음(추천 · 근거 · 영향 「N행/N키/N항목」) ② **사용자 최종 판단 — 한 표에 전부**(F) ③ 셈(원장 521 행선지 · 단위 시술 키 수 · 붙는 것 연결 수 · open 후보 — 전부 해결 안)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_7a9b28b8-7a77-46da-a0e2-8fc0cdc4fae7 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 단위 시술 조사" \
  --body "결정 묶음 N / 사용자 판단 N / 키 N / 셈"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 단위 시술 조사. 상세는 인박스." --enter
```
