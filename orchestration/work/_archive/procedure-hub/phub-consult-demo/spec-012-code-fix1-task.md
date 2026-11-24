# [code · 고침 1] SPEC-012 구현 — 검수 FAIL 반영 (사용자 승인 11-23 「품질 먼저 · 쭉 진행해」 범위)

너는 앱 코드 워커다(앞 구현을 한 사람). 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 에서만 · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 출력 0 · **LLM 호출 0** · 시험은 관련만 + 끝에 전체 한 번.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-spec-012-code.md`(FAIL · P1 1 · P2 5) · 정본 `$W/SPEC-012-consult-quality.md` 0.1.2 · 앞 구현 지시 `$W/spec-012-code-task.md` · 리포트 `$W/spec-012-code-report.md`.

## 할 일
1. **P1-1 · P2-1 ~ P2-5 전부** 검수 「고칠 방향」 대로. P1-1: 프롬프트에 금지 문구를 예문으로 박지 마라 — 원칙만(낱말 · 문장 박기 0). P2-5: HF2 케이스 부위는 스펙대로 매핑 `hub.case_codes` → 케이스 부위 우선 · 허브 GET 호출 수를 장부에 기록.
2. **P2-4**: 스펙 `$W/SPEC-012-consult-quality.md` 를 0.1.3 으로 — HU1 보강 규칙(구현 그대로)과 검수 r3 P2-3(표 머리 · S11 T6 칸)만 옮겨 적고 판 기록. 그 밖 계약은 고치지 마라.
3. 리포트 `$W/spec-012-code-report.md` 판 올림(바뀐 파일:줄 · 시험 수).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-012 구현 고침 1" --body "P1 · P2 닫음 / 시험 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 구현 고침 1 완료 — <한 줄>. 상세는 인박스." --enter
```
