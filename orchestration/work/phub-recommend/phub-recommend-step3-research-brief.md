# [researcher] 실버 3단계(부위) 조사 — 근거 · 원천 부위 문자열 전수 매핑 · 트리 밖 판정

너는 앞 판 맥락이 없을 수 있다. 아래부터 읽어라.

## 읽을 것
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 — 특히 10-27 「부위 트리 확정」 · 「DEC-002 OQ-206 처리」 · 「이름은 상담 용어…」 · 10-28 「3단계(부위) 시작」 행. **정해진 트리는 다시 논의하지 않는다**
- 부위 정본 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-002.md` D-04 · D-05 · D-07 · 「부위 트리」 · 「노드별 원천 근거」 · 「위험 부위 11곳 대응」 · OQ-202 · OQ-206 / `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-003.md`(「전신」 두 뜻 · 수액 「해당 없음」)
- 초안 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/procedure-master-v3.json` site_tree · site_special · site_out_of_tree · unit_procedures 의 where
- 원천(stg) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`: anatomy-danger-zones.json · market-pricing.json · problem-packages.json · problem-combos.json · taxonomy.json(name · detail · extracted) · procedure-profiles.json · contraindications.json · literature-evidence.json · 그 밖 부위 문자열이 있는 파일 전부
- 레포 문서 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/docs/`(reviews · references · architecture) — 부위 · 해부학 기준이 있는지
- 2단계 교훈(`para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md` §5): **기준은 레포 근거부터** · 기본값이 open 을 만들지 않게(칸 모양 문제면 칸을 고칠 안을 낸다) · 끝 조건 open 0

## 할 일
### A. 근거
- 레포 안 부위 · 해부학 근거를 전부 찾는다(파일:키). anatomy-danger-zones 의 name_en · 출처 · 문헌 인용 등
- 트리 노드마다 **해부학 이름 후보**(영문 · 한글) + 근거(레포 파일 · 해부학 표준 용어 출처 URL/문헌). 근거 수준 강/약. 근거 없으면 「없음」 — 지어내지 않는다

### B. 원천 부위 문자열 전수 매핑
- 위 원천 파일 전부에서 부위를 가리키는 문자열을 **빠짐없이** 뽑는다(파일 · 키 · 원문 · 등장 수). 「팔자주름」처럼 부위+고민이 붙은 것은 D-07 대로 나눈다
- 문자열마다 → 트리 노드(동의어) / 트리 밖 / 부위 아님(고민 · 기법 · 제품 등 — 어느 단계로) 판정 + 근거
- 붙지 않는 것은 open 후보로 모으되 **행마다 해결 안**(동의어로 · 새 노드 · 부위 아님)을 낸다

### C. 트리 밖 판정
- 등 · 브라라인 · 엉덩이 · 옆구리 · 콧망울 · 페이스 · 하관 + B 에서 나온 트리 밖 문자열: 기존 노드 동의어 / 새 노드(D-05 쪼개는 규칙 ① 원천이 따로 부름 ② 가능 시술 · 안전이 다름 — 근거) / 부위 아님
- 묶음 노드와 전체 노드의 경계(얼굴 ↔ 얼굴 전체 · 바디 ↔ 전신 · 「(묶음)」 이름) — 정해진 것은 그대로, 원천 문자열이 어디로 가는지만

### D. 노드 속성안
노드마다: id · 이름(상담 용어) · 상위 · 동의어[](원천 표기 · 구어) · 해부학 이름 후보 · 위험 부위 대응(anatomy-danger-zones id) · 원천 근거(등장 수)

## 산출 — 이 두 파일만
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step3-research.json` · `step3-research.md`. 원장 · 결정 · 원천 수정 금지.
md 맨 위: ① 결정 묶음 목록(묶음마다 추천 한 줄 · 근거 · 영향 — 「N행/N노드/N문자열」 단위 밝힘 · 최종 판단이 사용자인지) ② 사용자가 최종 판단할 것만 ③ 셈(원천 문자열 수 · 노드로 감 · 트리 밖 · 부위 아님 · open 후보 — 모든 open 후보에 해결 안 있음)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_16898dfd-67ba-45ea-81ba-e60d37fd48e4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 부위 조사" \
  --body "결정 묶음 N / 사용자 판단 N / 문자열 셈"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 부위 조사. 상세는 인박스." --enter
```
