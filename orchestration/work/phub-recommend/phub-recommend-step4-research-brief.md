# [researcher] 실버 4단계(기법) 조사 — 「어떻게」 축 · 원천 표현 전수 · 넘겨받은 것 정리 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 전부 — 특히 10-27 단위 시술 정의(무엇을 × 어디에 × 어떻게) · 10-28 4단계 시작 행 · 해부학 용어 행 · 「단계로 넘길 결정」 줄 · source-map 승인 행. **정해진 것은 다시 논의하지 않는다**
- `DEC-002.md`(D-02 · D-03 · OQ-201 기법 목록은 원천 표현에서) · `DEC-003.md`
- 행선지 지도 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/source-map.json` · `.md` — **4단계로 정해진 칸만 입력**(destinations 에 4단계)
- 재료(초안 · 확정 아님): `procedure-master-v3.json` techniques(큰 기법 65) · unit_procedures 의 how · `taxonomy-classify-v2.json` how
- 넘겨받은 것: `step2-families.json` technique_hint 25행 · families[M8].deferred · `step3-sites.json` deferred(4단계 기법) · handoff_note(대상 근육)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` 중 지도가 4단계로 가리킨 파일 · 칸
- 앞 단계 교훈: `para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md` · `-step3-site.md` §5 — 기준은 레포 근거부터 · **설명 문장 전체를 훑지 않는다(지도가 정한 칸만)** · 기본값이 open 을 만들지 않게(칸 모양 문제면 칸을 고칠 안) · 끝 조건 = 지금 원천 기준 open 0 · **가상 문장 시험 없음**

## 할 것
A. **기준 근거**: 기법 분류의 레포 안 근거(literature-evidence moa · procedure-profiles mechanism · docs) — 2단계처럼 근거가 있으면 그것을 기준으로
B. **기법 축 구조안**: 큰 기법(전달 방식 — 주입 · 조사 · 도포 · 삽입 · 흡인 등 원천 표현에서) + 깊이 · 층 / 에너지 방식(피코초 · 프락셔널 · 롱펄스 · Q스위치 · 집속) / 대상 근육을 **속성으로 둘지 하위 노드로 둘지** — 안 2개 이상 + 추천 + 근거(단위 시술 키가 몇 개가 되는지 셈 포함)
C. **원천 표현 전수**: 지도가 4단계로 정한 칸의 표현을 전부 뽑아(파일 · 키 · 원문 · 등장 수) → 기법 노드 / 속성 값 / 다른 단계로 넘김(어디로) 판정. 붙지 않는 것은 행마다 해결 안
D. **넘겨받은 것 처리**: technique_hint 25 · 층 · 깊이 · 대상 근육 · 도포 제약 각각의 행선지
E. **계열 기본 기법**: 18계열마다 기본 기법 + 근거
F. 초안 큰 기법 65 를 새 구조로 대응(유지 · 합침 · 버림 + 이유)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step4-research.json` · `step4-research.md`. md 맨 위: ① 결정 묶음(추천 · 근거 · 영향 「N행/N노드/N표현」) ② 사용자 최종 판단만 ③ 셈(표현 수 · 노드로 · 속성 · 넘김 · open 후보 — 전부 해결 안)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_b60e17a7-b33e-4262-8b43-f9aca6dd96ac \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 4단계 기법 조사" \
  --body "결정 묶음 N / 사용자 판단 N / 표현 셈"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 4단계 기법 조사. 상세는 인박스." --enter
```
