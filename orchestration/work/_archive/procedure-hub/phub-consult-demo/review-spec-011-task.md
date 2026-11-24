# [reviewer · 읽기만] SPEC-011 가져오기 계획 검수 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 앱 · 허브 · 데이터 · 프롬프트 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만) · 키 값 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 장부 `$A/runs/consult/turns.jsonl`

## 대상
`$W/SPEC-011-fetch-plan.md` 0.1.0 · `$W/fetch-plan-report.md` · 스크립트 `$W/fetch-plan/` · 작성 지시 `$W/fetch-plan-spec-task.md`(사용자 결정 — 기준) · 앞 조사 `$W/token-cause-report.md` · `$W/token-cause/`.

## 볼 것
1. **사용자 결정대로인가**: 1차 소넷 JSON → 2차 그 JSON 대로만 결정론 → 3차 소넷 · Jev 거르기 없음 · `--resume` 둠(끊는 안 0) · 출력 줄이지 않음 · 턴당 상한 고정 0 · 안전 · 명시 대상 늘 포함. 어긋나거나 정해진 것을 다시 묻는 것.
2. **수치 재현**: 스크립트를 직접 다시 돌려(소넷 호출이 들면 저장된 응답으로 다시 셈 · 오프라인 판이 없으면 대표 턴 3~5 개만 실제 호출) 리포트 표 — 자료 감소 −61.6% · 「얼굴에」 두 턴 빼면 −22.5% · 빠짐 0/276 · 출력 · 이해 호출 비용 몫 — 이 같은가. 빠짐 셈이 「인용 줄」 기준인데 그 판정이 너그럽지 않은가(넓은 인용 · 줄 번호 바뀜).
3. **과적합**: 규칙을 10 대화에 맞춰 여러 번 고쳤다면 그 10 개 밖 장부 턴(무작위 10~15 턴)에서도 빠짐이 0 에 가까운가 — 직접 셈.
4. **규칙표 전수**: 질문 꼴이 장부 실제 말을 다 덮나 · 빈 값 기본 · 꼴이 겹칠 때 · 「그중에서」 · 명동점 밖 물음 · 없는 것 · 부위만(첫 턴 / 주제 있음).
5. **JSON 계약 ↔ 코드**: 칸이 실제 코드 자리(`파일:줄`)와 맞나 · 사라지는 규칙(KD9 · KS5~7 · LC5 등)이 다른 곳에서 쓰이지 않나(grep) · 화면(주제 · 점 · 목록)이 이해 JSON 에 기대는 곳이 깨지지 않나.
6. **WP**: 순서대로 할 수 있나 · 완료 조건 시험 가능 · 관련 시험만 · 장바구니와 겹치는 자리.
7. 「사용자 결정 필요」 3 개: 기계가 정할 수 있는 걸 올렸나 · 추천 근거.

## 산출
`$W/review-spec-011.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 실측 · 고칠 방향) · 재현 표 · 과적합 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-011" --body "판정 / P0 · P1 · P2 수 / 재현 · 과적합"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-011 완료 — <한 줄>. 상세는 인박스." --enter
```
