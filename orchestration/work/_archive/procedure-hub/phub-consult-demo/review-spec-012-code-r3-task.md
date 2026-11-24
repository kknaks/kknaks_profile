# [reviewer · 읽기만] SPEC-012 구현 재검수 r3 — 고침 2 + 실물 after2 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 앱 · 허브 · 데이터 · 프롬프트 · `quality/` 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 값 출력 0 · **LLM 호출 0**(저장된 측정 결과로만).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`git -C $A diff 35b56e5`) · 고침 지시 `$W/spec-012-code-fix2-task.md` · 구현 리포트 `$W/spec-012-code-report.md` · 측정 `$W/quality/after2-report.md` · `$W/quality/out/after2-20261123-2034/` · 전 `$W/quality/out/base2-20261123-1942/` · 앞 측정 `$W/quality/after-report.md` · 정본 `$W/SPEC-012-consult-quality.md` 0.1.3 · 앞 검수 `$W/review-spec-012-code-r2.md` · 정해진 것 `$W/_RESUME.md` §2.

## 볼 것
1. **고침 2 지시 1 ~ 5 가 다 들어갔나** — 합집합 고르기 · HA1 조상 지움 · 계열 요약 이름만 · 구조로 고친 H10 · HD7 · H12 · 시간 초과 동작. diff 와 맞댐.
2. **낱말 · 문장 박기 0 · 새 고정 한도 0 · 시간 문턱 값 안 바꿈** — diff grep. 프롬프트 새 줄이 원칙인가.
3. **측정 재현** — `score.py out/after2-* --before out/base2-*` 를 스크래치 복사본으로 다시 돌려 1,382/1,410 · 떨어진 기준 0 · C3 · C4 통과가 같은가. 기계 판정이 너그러워 오른 것은 없나(표본 8 턴 원 화면 · 답으로 직접 판정 — 특히 13 · 11 · 8 이 크게 오른 턴).
4. **남은 실패** — S09 T4 「모발이식」 3/3 · **S10 T2 3/3(목록 ≠ T1 — 고침 1 측정엔 없던 실패인가? 정답이 틀렸나 코드가 틀렸나)** · S12 T4 · S08 T3 · S02 T1 까닭과 코드 자리.
5. 시험 직접 다시 돌림(관련 + 전체) · 화면 · 장부 칸 · `tokens.calls[]` 그대로.

## 산출
`$W/review-spec-012-code-r3.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 · 고칠 방향) · 재현 표 · 직접 판정 표본 표 · 남은 실패 까닭 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-012 구현 r3" --body "판정 / P0 · P1 · P2 / 재현 / S10 T2 까닭"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-012 구현 r3 완료 — <한 줄>. 상세는 인박스." --enter
```
