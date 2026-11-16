# [researcher] 허브 품질 수정 — 원인 14 고치기 → 다시 측정 → 목표까지 반복

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
측정 리포트 `quality-report.md` · `.json`(원인 A ~ O) · 문항 `quality-eval-set.json` · 측정 `quality-eval.py`. 결정표 `_RESUME.md` §2(10-30 「품질 목표」 행). 8단계 충돌 정리는 끝난 판(`step8-relations.json` resolved · by_direction)에서 시작.

## 목표(사용자 승인 10-30) — 이걸 넘을 때까지 고치기 → 측정 반복
| 지표 | 목표 |
|---|---|
| 질문 세트 재현율 · 정밀도(전체) | ≥ 0.95 |
| I-01 고민 × 부위 재현율 · 정밀도 | ≥ 0.95 |
| 문항 안전 누락 | 0 |
| 원천 안전 원문 실버 누락(M4) | 0(싣거나 · 안 싣는 이유를 규칙으로 명시) |
| 말 → 노드 찾기 | ≥ 97% |
| 엣지 표본 오류율 | ≤ 1% 유지 |
- 의료진 질문 5문항 · 정답 미정 1문항은 목표 계산에서 뺌(리포트에 따로)
- **문항 세트 · 정답 · 채점 기준을 고쳐서 목표를 맞추지 말 것**(정답이 원천 근거와 다르다고 판단되면 고치지 말고 보고)

## 고칠 것(원인 → 단계 결정 · 규칙으로 · 행별 결정 금지)
- **A · C · N(7단계)**: 원천 문구 부위 낱말로 거르기 · 원천 계열 밖 엣지 금지 · **원천 제품 이름 → 2단계 하위 계열로 단위 시술 하위 거르기**(하위 안 정하면 계열만)
- **B(U-1 = ② · 사용자 결정 10-30)**: 부위 고민에 상위 「얼굴 전체」 층 단위 시술을 같이 내되 `layer: 상위` 표시 · 하위 계열은 N 규칙(원천 제품)으로 거름
- **E · I · K · L · O(8단계)**: 끝점 부위 낱말 · 원천 안전 칸 1:1 셈 가드(빠진 index open) · 안전 0 단위 시술 gap 명시 · 쌍 이름 사전 · 방향별 same_day 유지 확인
- **F · G · H · M(시맨틱 사전)**: 원천 이름 칸(시장가 · CC · 환자용 · products · 샘플 영문)을 사전 출처에 · 괄호 · 「/」 낱말 나눔 · 「쳐짐 → 처짐」 등 입력 정규화 · 접두 일치는 대상 계열 하나일 때만 · 정규화 문서 = 코드
- **J(5 · 8단계)**: 브론즈 안전 원문(extracted aftercare · safety · taxonomy 안전 칸 · 타임라인)을 실버 칸에 싣기(붙는 수준 · 원문 그대로)
- 단계 순서대로 5 → 7 → 8 → semantic-build 재실행 · 각 단계 open 0 · cmp · 고정 시험(원인마다 1건) · 스킬 9종 errors 0

## 끝나면
- `quality-eval.py` 최종 판 지표 표(1차 → 최종) · 원인별 고침 · 남은 것 · `quality-report.md` 를 2차로 갱신(1차는 보관)
- `silver-graph-build.py` · `silver-questions-build.py` 재생성(코디가 게시)
- 원천 · DEC 수정 금지 · 가상 문장 금지 · 실명 · 키 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_39f6cf28-b4a6-4dfc-b9e3-373afae49d25 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 허브 품질 수정" --body "재현율 N → N · 정밀도 N → N · I-01 N → N · 안전 누락 N → N · M4 N → N · 말 찾기 N → N · 엣지 오류 N / 목표 달성 N/6"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 허브 품질 수정. 상세는 인박스." --enter
```
