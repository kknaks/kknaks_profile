# [code · 고침 3] SPEC-012 — 검수 r3 P2 7 닫기 + 실물 after3 (사용자 승인 11-23 「품질 먼저 · 쭉 진행해」 · 단계 끝 = open 0)

너는 앱 코드 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 에서만(+ `$W/quality/` 채점 스크립트 · 정답 규칙) · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 출력 0 · 시험은 관련만 + 끝에 전체 한 번.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **검수 `$W/review-spec-012-code-r3.md`(PASS · P2 7)** · 앞 지시 `$W/spec-012-code-fix2-task.md`(사용자 결정 · 금지 — 그대로 지켜라: 비용 안 줄임 · 새 고정 한도 0 · 낱말 · 문장 뜻 판정 0 · 판단은 소넷 · 시간 문턱 그대로) · 구현 리포트 `$W/spec-012-code-report.md` · 측정 `$W/quality/after2-report.md` · 정본 `$W/SPEC-012-consult-quality.md` 0.1.3 · 정해진 것 `$W/_RESUME.md` §2.

## 할 일
1. **P2-1 ~ P2-7 전부** 검수 「고칠 방향」 대로:
   - P2-1 S10 T2: 「목록 안 케이스 = 같은 말」 을 데이터로(1차가 시술 · 케이스 어느 쪽을 내도 지금 목록 안이면 같은 목록) · 정답 same_as 1 그대로.
   - P2-2 채점 낱말집에 매핑 밖 패키지 이름(`package.csv`) 더함 + 앱에서 밖 패키지가 상세로 들어온 자리 막음(이름만).
   - P2-3 고르기 포함 관계 양쪽(좁은 쪽이 이김) · S12 T4.
   - P2-4 H10: 손님 말 대상 · 명동점 0 을 블록 **사실 줄**로 · 프롬프트는 원칙만.
   - P2-5 채점 `ask_site` · `no_here` 엄한 곳 — 기준 뜻대로 고침(너그럽게 만들지 말 것 · 바꾼 판정 수 기록).
   - P2-6 묻지 않은 안전 먼저 꺼냄: 블록에 「물은 kinds」 사실 · 늘 읽은 안전 줄에 표지 · 원칙이 읽게. 채점에 「안 물은 턴 안전 먼저 꺼냄」 칸 더함(기준 8 · 16 하위 판정).
   - P2-7 스펙에 「구현 자리」 한 줄(H15) · 판 0.1.4.
2. 관련 시험 · 전체 pytest(기준 724 + 고침 2 시험).
3. **실물**: `run.py --runs 3` S01 ~ S13(gold `e8f02287…`) → `out/after3-<시각>/` · `score.py --before out/base2-20261123-1942` · 채점 규칙을 바꿨으면 **전(base2)도 같은 규칙으로 다시 채점**(전 · 후 같은 정답 · 같은 채점). 목표: 떨어진 기준 0 · 남은 실패 표.
4. `$W/quality/after3-report.md` + 구현 리포트 판 올림.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-012 고침 3 · after3" --body "확정 통과 전 → 후 / 떨어진 기준 / 남은 실패 / 턴당 $"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 고침 3 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] spec012-fix3: <질문>" --enter`
