# [reviewer · 읽기만] SPEC-012 구현 재검수 r2 — 고침 1 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 앱 · 허브 · 데이터 · 프롬프트 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 값 출력 0 · **LLM 호출 0**(실물 측정은 코디가 따로 — WP-4).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(기준 `35b56e5` · 커밋 안 된 변경이 대상 — `git -C $A diff 35b56e5`) · 정본 `$W/SPEC-012-consult-quality.md` 0.1.3 · 앞 검수 `$W/review-spec-012-code.md`(FAIL · P1 1 · P2 5) · 고침 지시 `$W/spec-012-code-fix1-task.md` · 검수 `$W/review-spec-012-r3.md`(P2 4 → 코드에 반영 지시) · 구현 지시 `$W/spec-012-code-task.md` · 구현 리포트 `$W/spec-012-code-report.md` · 정해진 것 `$W/_RESUME.md` §2.

## 볼 것
1. **계약대로인가** — H1 ~ H16 마다 스펙 계약(§3)과 diff 를 맞대라. 빠진 것 · 더 한 것(스펙 밖 변경 · 비용 쪽 변경 · 새 고정 한도).
2. **낱말 판정 0** — 새로 낱말 · 문장 목록으로 뜻을 가르는 코드 · 프롬프트 줄이 없나(diff grep) · 기존 낱말 판정 자리 목록(리포트)이 전수인가 · `TOGETHER` 처리.
3. **결정 칸 연속 재생** — §3-D 시험이 실제로 S05 T1 → T4 · S06 T1 → T3 · S10 T3 · T4 · 「있어」 · 「잇어」 를 덮나(시험 코드를 읽고, 기대값이 정답표 `quality/answers.json` 과 같은가).
4. **시험** — 관련 시험 + 전체 pytest 를 직접 다시 돌려 리포트 수(724 통과 · 옛 실패 1)와 같은가. 시험이 구현을 그대로 베껴 너그럽지 않은가(표본 5).
5. **깨질 자리** — 화면(주제 · 점 · 목록 · 모달 · 장바구니) · 장부 칸 · SPEC-011 장부 `tokens.calls[]` · `fetch` 칸이 그대로인가.
6. 프롬프트(`prompts/consult.json`) 변경이 대본 · 문장 박기가 아니라 원칙인가 · 「물은 종류에서만」 범위.

## 산출
`$W/review-spec-012-code-r2.md`: 앞 지적 P1 1 · P2 5 가 다 닫혔나(지적마다 닫힘/열림 · 근거) + 새로 생긴 것 · 0.1.3 스펙 변경이 HU1 · 표 머리만인가 · 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 고칠 방향) · 구멍 × 구현 대조 표 · 시험 재현 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-012 구현 r2" --body "판정 / P0 · P1 · P2 수 / 시험 재현"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-012 구현 r2 완료 — <한 줄>. 상세는 인박스." --enter
```
