# [researcher] 실버 5단계 검수 FAIL · WARN 수정

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 먼저 `review-step5-report.md` · `step5-units.md` 머리 · `step5-decisions.json` · `step5-apply.py` 구조를 읽어라.

결정 `_RESUME.md` §2 2026-10-29 「5단계 검수 FAIL 1 · WARN 2 처리」 행(사용자 「추천으로 가자」):
1. **F1**: `step5-decisions.json` `product_link_rule.inherit` 에 **기법 호환** 조건 — 근거 = `step2-families.json` technique_hint · `step4-techniques.json` device_attrs(펄스 · 박피 · 가능 방식) · 매질(하위) 일치. 매질 미지정 키는 기법 근거가 있는 제품만 상속, 근거 없으면 상속 안 함. `step5-apply.py` 에 같은 규칙 · PIH 의 「제품 층 PIH 는 쓰는 제품에서」 문구는 고친 상속 결과로 재생성. 리포트가 든 잘못된 후보(LED 7 · IPL 7 · PDL → 제모 · 프락셀 · PDT · 토닝)가 사라졌는지 확인
2. **W1**: 단위 시술 2 추가 — M9 마이크로웨이브 × 얼굴 전체 × K05 (온다) · M9 SUPERB 초음파 × 얼굴 전체 × K05 (소프웨이브) · 부위 얼굴 전체 기본값 표시 · 쓰는 제품 = 해당 장비
3. **W2**: 시장가 「진정관리 (시술 후 재생팩)」 → U5-034 의 **후보 동의어**로 낮춤(이름 「얼굴 전체 필링」 유지)
4. 재실행 · open 0 · 결정론 · 고정 시험(필요하면 F1 케이스 추가) · md 맨 위 셈 · 바뀐 것 목록. 다른 것은 바꾸지 마라

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_90209fd9-0fef-4040-9ad0-2e8021e34785 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 검수 수정" \
  --body "F1 상속 전후 / 키 N / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 검수 수정. 상세는 인박스." --enter
```
