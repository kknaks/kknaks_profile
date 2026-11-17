
# [planner] SPEC-002 0.2.0 — DEC-002 D-19 ~ D-21 반영 (작은 개정 · 빨리)

너는 consult-analysis `planner` 워커다(SPEC-002 를 쓴 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`. **사용자가 결과를 기다린다 — 바뀌는 절만 고치고 끝내라.**

## 입력
- `para/projects/summer-star/consult-analysis/10-decision/decision-002-layer2-analysis.md` D-14(haiku) · **D-19 ~ D-21**(새로)
- etl 보고 요약(코디): 단계 · 자동응답 건수 SPEC 과 일치 · 큐 15건(E-1 12 · E-2 1 · E-3 2 — SPEC 21 은 칸 값 정리 해석 차이 FB 3방 + E-2 FB 3방) · handoff 낱말 경계 IG 12 · FB 17 · 표본 haiku 30방 실패 0 · 방당 $0.0007 · procedures `other` 방 기준 57%

## 고칠 것
1. §5 `procedures` 목록에 D-20 의 다섯 값 추가 · 중화권 별칭 표(D-20 에 적힌 것 + 우리 상용 문구에 나오는 시술 별칭 — 1층 DB 의 **우리 메시지**에서만 뽑는다) · 새 칸 `procedures_other`(JSON 배열 · 원래 이름 짧게 · DB 만 · 통계 · 보고서에는 안 냄) → §1 `l2_llm_label` 칸에도
2. §5 모델 = haiku(D-14) · 「표본 → 사람 확인 → 전체」 순서는 표본 재시험(목록 넓힌 뒤 `other` 비율) 한 번 더 → 전체
3. §2.3 · §2.4 실측 표 옆에 etl 실측(큐 15 · 사유별) 과 차이 이유 한 줄 · §2.5 handoff 를 D-21 규칙 · 12 / 17 로
4. §2.4 사람 판정 결과: D-19(15건 중 3건 `form_filled` · 성공 93)
5. 변경 이력 0.2.0 · README 버전 칸 · WORK-002 WP3 행에 「표본 재시험」 · WP2 상태 done

## allowed_paths
- `para/projects/summer-star/consult-analysis/20-spec/` · `30-work/`

## 검증
- 바뀐 절만 바뀜(`git diff` 범위) · 고객 이름 · 본문 0 · 별칭은 우리 메시지 출처

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-002 0.2.0" --body "변경 / 별칭 수 / 미결"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] planner 완료 — SPEC-002 0.2.0. 상세는 인박스." --enter
```
