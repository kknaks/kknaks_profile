# [reviewer · 읽기만] SPEC-012 마감 검수 — after6 (마지막 검수 · 11-24)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만 · gold `8f65957f…`) · 키 값 출력 0 · **LLM 호출 0**.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(`git -C $A diff 35b56e5`) · 마감 측정 `$W/quality/after6-report.md` · `$W/quality/out/after6-*` · 지시 `$W/spec-012-final-task.md` · 앞 검수 `$W/review-spec-012-code-r4.md`(FAIL · P1-1 · P2 7).

## 이번 검수의 규칙(사용자 지시)
- **마지막 검수다.** 판정 기준: P1-1(최종 코드 · 프롬프트 · gold 로 전체를 쟀나) 닫힘 + **코드 탓으로 base2 대비 떨어진 기준 0** 이면 **PASS**. P2 는 고치라고 하지 말고 「다음 단계로 넘길 목록」 으로만 적는다.
- P1 은 「잰 값이 틀렸다(재현 안 됨)」 · 「코드 탓 하락을 흔들림으로 잘못 갈랐다」 · 「일부만 잰 결과를 섞었다」 처럼 마감 판정을 뒤집는 것만.

## 볼 것
1. after6 이 최종 코드 · 프롬프트 · gold 로 192 턴 전부인가(meta · 장부 해시).
2. `score.py` 를 스크래치 복사본으로 다시 돌려 1,400 / 1,410 · base2 대비 떨어진 기준 0 재현.
3. after5f 대비 떨어진 11 · 16 과 새 하위 칸 24 하락을 「코드 탓 0 · 흔들림」 으로 가른 근거(§4 · §5)가 맞나 — 원 답 직접 대조.
4. 검수 r4 P2 7 처리 확인(목록만).

## 산출
`$W/review-spec-012-final.md`: 판정 PASS / FAIL · P1(있으면) · 다음 단계로 넘길 목록 · 재현 표.

## 완료 보고 — 2채널(둘 다) · 코디 handle `term_3ef63b09-be83-4efa-a79c-abda533d9064`
```bash
orca orchestration send --to term_3ef63b09-be83-4efa-a79c-abda533d9064 --from <내 handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-012 마감" --body "판정 / P1 / 넘길 목록 수"
orca terminal send --terminal term_3ef63b09-be83-4efa-a79c-abda533d9064 --text "[worker_done] review SPEC-012 마감 완료 — <한 줄>. 상세는 인박스." --enter
```
