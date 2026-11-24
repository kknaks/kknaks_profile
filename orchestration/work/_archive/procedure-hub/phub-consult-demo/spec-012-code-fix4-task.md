# [code · 고침 4] SPEC-012 — after3 에서 떨어진 칸 · 남은 실패 닫기 + 실물 after4 (사용자 「추천으로 가라니까 다 끝내」)

너는 앱 코드 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 에서만(+ `$W/quality/` 채점 · 정답 규칙) · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 GET 만) · 키 출력 0 · 시험은 관련만 + 끝에 전체 한 번.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **측정 리포트 `$W/quality/after3-report.md` §3 · §4**(떨어진 것 · 까닭 · 고칠 방향) · 앞 지시 `$W/spec-012-code-fix3-task.md` · `$W/spec-012-code-fix2-task.md`(사용자 결정 · 금지 그대로: 비용 안 줄임 · 새 고정 한도 0 · 낱말 · 문장 뜻 판정 0 · 판단은 소넷 · 시간 문턱 그대로) · 정본 `$W/SPEC-012-consult-quality.md` · 구현 리포트 `$W/spec-012-code-report.md` · 정해진 것 `$W/_RESUME.md` §2.

## 할 일 — after3 §3 · §4 전부
1. **S10 T1 「턱에 보톡스 맞아도돼 ?」 안전 빠짐(12 · 8 × 3)** — 고침 3 이 만든 하락. 「맞아도 되나」 는 금기 · 부작용을 묻는 것이다. 1차 pick 규칙(20-2)이 효과 확인으로 읽는 자리를 고친다(판단은 소넷 — 규칙 문구가 「해도 되나 · 맞아도 되나」 류를 안전 물음으로 보게 원칙으로) · R25 와 맞물림 확인.
2. **S06 T4 「그중에서 티타늄리프팅이랑 포트라만」 기준 10 × 3** — 고침 3 이 만든 하락. 명동점 진료항목 이름과 일치하면 1차 `out` 표지를 앱이 지운다(데이터 판정).
3. **S10 T2 흔들림(6 × 3)** — `_case_same_targets` 가 주제 시술 칸이 계열(`modality`)일 때도 보게(계열 → 그 아래 시술 · 케이스 포함 관계 · 데이터).
4. **S08 T3 턱보톡스 국산 줄 값 빠뜨림(14 × 2)** — `kos_block.item_line` 에 매핑 제품 표시(리포트 §4 「다음 판」).
5. 하위 23 의 4/177 · 한 실행 흔들림 5 칸은 까닭만 표로(고칠 구조가 있으면 고침).
6. 관련 시험 · 전체 pytest.
7. **실물**: `run.py --runs 3` S01 ~ S13(gold `e8f02287…` 그대로 · 18105 는 지금 그 gold) → `out/after4-<시각>/` · 채점 0.4 로 base2 · after2 · after3 · after4 넷을 맞대 → **base2 대비 떨어진 기준 0 · after3 대비 떨어진 기준 0** 이 목표. 비용 기록.
8. `$W/quality/after4-report.md` + 구현 리포트 판 올림.

## 완료 보고 — 2채널(둘 다) · `<내 handle>` 은 네 터미널 handle(`orca terminal list` 또는 preamble)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from <내 handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-012 고침 4 · after4" --body "확정 통과 base2 → after4 / 떨어진 기준 / 남은 실패 / 턴당 $"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-012 고침 4 완료 — <한 줄>. 상세는 인박스." --enter
```
