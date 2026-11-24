# [code · 마감 측정] SPEC-012 — 검수 r4 P1 · P2 닫기 + 최종 전체 실측 after6 (사용자 「다 끝내」)

너는 앱 코드 워커다(고침 4 · 5 를 한 사람). 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(+ `$W/quality/`) · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **검수 `$W/review-spec-012-code-r4.md`(FAIL · P1-1 · P2 7)** · 측정 `$W/quality/after5-report.md` · 앞 지시 `$W/spec-012-code-fix4-task.md`(금지 그대로).

## 바뀐 것 — 허브 gold 가 최종본으로 바뀌었다
코디가 18105 를 **gold `8f65957f…`** 로 재기동했다(허브 데이터 J28 · J29 · J34 · PRP × 볼 꺼짐 · 검수 r4 PASS). 이 측정이 마감 측정이다.

## 할 일
1. **P2 7 전부** 검수 「고칠 방향」 대로(코드 · 채점 · 리포트). 낱말 뜻 판정 0 · 새 고정 한도 0 · 비용 안 줄임.
2. **P1-1**: 일부만 돌린 결과를 섞지 않는다. 최종 코드 · 최종 프롬프트로 **S01 ~ S13 전체 × 3** 을 한 번 돌린다 → `out/after6-<시각>/`(meta 에 gold `8f65957f…` · 프롬프트 해시 · diff 해시).
3. 정답표를 새 gold 로 다시 만든다(`build_answers.py` · 바뀐 칸 표). 비교:
   - **after6 vs base2**: base2 는 옛 gold(`e8f02287…`)다. base2 를 새 정답으로 다시 채점한 값과 맞대고, 「데이터만 바뀐 칸」 을 따로 표시(WP-0 리포트 §2 방식). 데이터 변경은 작으니(볼 꺼짐 · 목 처짐 · 팔자 · 턱선 처짐) 떨어진 칸이 그 고민 턴인지 아닌지 가른다.
   - **after6 vs after5(합친 것)**: 같은 규칙 채점.
   - 목표: 코드 탓으로 떨어진 기준 0.
4. `$W/quality/after6-report.md`(마감 측정) + 구현 리포트 판 올림.

## 완료 보고 — 2채널(둘 다) · 코디 handle `term_3ef63b09-be83-4efa-a79c-abda533d9064`
```bash
orca orchestration send --to term_3ef63b09-be83-4efa-a79c-abda533d9064 --from <내 handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-012 마감 측정 after6" --body "확정 통과 / 떨어진 기준(코드 · 데이터) / 턴당 $"
orca terminal send --terminal term_3ef63b09-be83-4efa-a79c-abda533d9064 --text "[worker_done] SPEC-012 마감 측정 완료 — <한 줄>. 상세는 인박스." --enter
```
