
# [docs] 소수정 4건 — source_group·error_code 등재 + 드리프트 2건 청산

너는 **ontology-demo `docs` 워커**다. 정확히 4건 (검수 W1·네 드리프트 보고, 코디 확정):

1. **SPEC-003** (v0.0.6→0.0.7): `/api/layers/{layer}/tables` 응답에 `source_group` 필드 등재 —
   브론즈 테이블의 원천 축(`vegas` | `review` | `nexus`), 실버·골드는 null. FE 브론즈 2단 칩의 계약 근거(검수 W1).
2. **SPEC-003** (같은 patch): 채팅 실패 응답에 `error_code` 등재 — Case Matrix 의 `AI_TIMEOUT`·`AI_FAILED` 를
   메시지 객체 필드로 노출(FE 가 상태 5종을 문구가 아니라 코드로 분기 — AC-12 근거).
3. **SPEC-005** (v0.0.3→0.0.4): 160행대 used_edges 예시 sign 을 U+2212 로 정정(네가 보고한 드리프트 가 —
   SPEC-003 과 같은 경고 문구 불요, 표기만).
4. **work-002-tools-and-api.md**: P2 작업 항목의 옛 판정 라벨('채택·산출0·외생'→'채택·자동 확정·선언')과
   옛 lag 규칙('<정수>d'→'원형 보존+lag_days')을 현행 정본 문구로 정정(드리프트 나).

version·updated_at·README Spec List 동기·log 1줄. 그 밖 수정 금지. 커밋·push 금지.
완료 보고 동일 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: source_group·error_code".
