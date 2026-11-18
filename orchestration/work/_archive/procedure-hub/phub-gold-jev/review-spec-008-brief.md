# [reviewer] SPEC-008 상담 입구(0.4) · SPEC-001 0.8.0 검수

너는 **procedure-hub 문서 검수 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/` 아래 reviewer(없으면 researcher) `role.md` · `rules.md`.

경로: `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱(읽기만) `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev` · 허브(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`.

검수 대상: `$W/SPEC-008-consult-entry.md`(새) · `$W/SPEC-001-hub-gold-mcp.md` 0.8.0 변경분(맨 위 변경 기록 · §4-1 · §5-1 · §5-11 · 시험 표). 작성 브리프 `$W/spec-008-brief.md`.
정본: `$W/_RESUME.md` §2 맨 위 11-18 행 전부(D-1~D-15 · 「소넷으로만 — Jev 뺌」 · 「resolve 최소 목록 꼴」 · 「워커 모델 opus」). 근거: `$W/research-input-space.md` · `$W/review-input-space.md` · `$W/research-input-space/scripts/README.md`(8 검사 · 3 검사 정의).

## 볼 것

1. **결정 대조**: D-1~D-15 · 「소넷으로만」 가 SPEC 에 빠짐없이 · 다르지 않게 들어갔나(부록 A 대조표를 그대로 믿지 말고 결정 행 하나씩). 결정에 없는 것을 새로 정한 곳(예: 출력 `out` 필드 · 걷기 ② 결정론 함수 재사용 · 「모두 통과한 턴 비율」 해석)은 표로 — 그것이 결정과 부딪히나.
2. **코드 근거**: §3-0 「걷기가 상담에서 하던 일」 · §5 AR-1~12 처분 · §2-5 조회 · §6 장부 필드가 실제 앱 코드와 맞나(`file:line` 표본 10 이상 열어 확인). 「없어짐」 으로 판정한 것이 실제로 다른 곳에서 쓰이지 않나(grep).
3. **표면 전수**: Jev · resolve 맞춤 꼴을 부르는 곳을 앱 전체에서 grep 으로 다 세어 SPEC 이 상담 켠 경로에서 전부 다뤘나(빠지면 그 자리) · 시험 앱 B 열 · 끈 상태 경로와 코드가 섞이는 곳 · SPEC-001 0.8.0 이 깨뜨리는 허브 시험 · 앱 코드(쓰는 곳별 영향 표가 맞나).
4. **계약 빈틈**: 이해 호출 입출력 계약이 구현 가능할 만큼 닫혔나(필드 · 타입 · 빈 값 · 순서 · 검증 실패 처리 · 실패 길 D-10) · 객체 갱신 규칙(D-5 · D-6 · D-9 · D-12) 이 모호하지 않나 · 부위 거르개 「이번 턴 부위만」 · 점 「말한 고민만」 의 정의가 채점 스크립트 8 검사 정의와 같은 뜻인가.
5. **시험 · 완료 조건**: §8 이 D-14 를 재는가(8 검사 · 3 검사 · 앞 답 가리키는 7 턴 = 답 LLM 실제 호출로 잼 — 코디 기본값) · 단위 시험이 계약 줄마다 닿나.
6. **프롬프트 초안 §7**: 예문이 입력 전수 표(334 턴 `research-input-space/conversations.jsonl`) 와 겹치지 않나 — 직접 대조.
7. 화면 문구를 지어 넣은 곳(시안 · SPEC 에 없는 손님에게 보이는 글).

## 판정 · 산출

`$W/review-spec-008.md` 1개: 머리 = PASS / WARN / FAIL + 한 줄 · 결함 표(번호 · 심각도 · SPEC 자리 · 근거 경로 · 고칠 방향) · 「구현 발주 전에 꼭 고칠 것」 목록.

## allowed_paths · 하지 마라

쓰기는 `$W/review-spec-008.md` 1개(임시는 scratchpad). SPEC · 코드 · 데이터 수정 금지. 서버 · DB · LLM · Jev 호출 금지. 결정하지 마라.

## 완료 보고 — 문구 변경 금지

> 핸들 · taskId · dispatchId 는 dispatch preamble 값을 믿어라.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer(SPEC-008) 완료: <PASS|WARN|FAIL> <한 줄>" \
  --body "결함 수(심각도별) / 구현 전 꼭 고칠 것 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] reviewer(SPEC-008) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
