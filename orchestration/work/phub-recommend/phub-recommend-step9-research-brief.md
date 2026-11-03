# 발주서 — 실버 9단계(설명 사실) 조사 · 설계(읽기 전용 · 데이터 수정 금지)

## 왜
hub-evals 실패 분류에서 「골드에 아예 없음」(A) = 2차 54건(문항 37) · rerun-v5a case3 27건. 대부분 **설명 사실**이다 — 효과 시작 · 지속(onset_duration), 작용 원리(mechanism), 시술 개요(overview), 적응증(indications.primary), 합병증 관리 · 예방(complications.management · prevention · duration), 반응 단계(post-procedure-timeline.reaction_levels), 제품 메모(products.*.note), 대안(problem-packages.alternatives), 관련 기법(related_techniques), severity_levels(SPEC-005 v3.2 에서 9단계로 넘김). 실버 1~8단계(제품 · 계열 · 부위 · 기법 · 단위 · 패키지 · 고민 · 관계)는 추천 · 안전 위주라 이 필드를 끌어올리는 단계가 없다.

## 입력(읽기)
- `reference/2026-10-30-hub-evals/build-out/fail-triage2.md` §6(A 잔여 원장 필드별 · 예) · `fail-triage.md` §2(1차 A 61) · rerun-v5a 실패(runs/quality.jsonl 배치 b202611011627-a76c8e · case3 · evidence.path)
- 원천 지도 `source-map.json/.md` · 원장(RAW_DIR) · 실버 step1~8 json · `semantic.json` · 골드 export(`PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json` · b031371c)
- 이전 단계 방식: `step8-research.md/.json` · `step8-decisions.json` · `step8-apply.py` · `step8-fixture-test.py` · 점검 스킬 `reference/2026-10-27-skills-procedure-hub/procedure-hub-*-check/`(SKILL.md · rules · record-schema · mistakes)
- `_RESUME.md` §2 결정표(원천 근거 · 충돌은 보수적으로 하나 · 결정론 · 단계 끝 = open 0)

## 산출(조사 · 설계만)
1. `step9-research.md/.json`: 대상 원장 필드 **전수**(필드 경로 · 원장 파일 · 행 수 · 붙을 실버 노드 종류(계열 · 단위 · 제품 · 합병증 · 부위) · 붙이는 키 · 원문 예) — A 실패에 나온 필드뿐 아니라 같은 종류 필드 전부를 grep 으로 셈. 중복 · 충돌(같은 노드 같은 칸에 다른 값) 건수 · 사례.
2. 실버 9단계 **설계안**: 레코드 꼴(record-schema) · 붙이는 규칙(규칙 번호) · 충돌 처리(보수적 하나 · 출처 우선순위) · 「사람 확인」이 필요한 자리(있으면 숫자와 이유 — 없앨 수 있으면 규칙으로) · 골드 빌드에서 어느 section 으로 나갈지(SPEC-005 §4-3 section 이름과 맞춤 · 새 section 이 필요하면 이름 제안 — V-4 `safety.management` 등).
3. **효과 추정**: 2차 A 54 · v5a A 27 중 이 단계로 닫히는 행 수(행 단위 표 · 결정론).
4. `step9-decisions.json` 초안(결정 필요한 것만 · 추천값과 근거) · 「아직 안 정한 것」 목록.
결론은 숫자 · 근거로. 적용 · 골드 빌드 · 데이터 수정은 하지 말 것(설계 승인 뒤 별도 발주).

## 제약
읽기 전용 · 원장 인용은 work/ 파일 안에만(공개 레포 — 커밋 안 함) · worker_done(대상 필드 수 · 행 수 · 닫히는 A 행 수 · 사람 확인 자리 수 · 아직 안 정한 것).
