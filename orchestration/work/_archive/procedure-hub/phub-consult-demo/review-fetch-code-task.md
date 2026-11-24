# [reviewer · 읽기만] SPEC-011 구현 검수 (자동 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만) · 실물은 빈 포트에 따로 띄워서(끝나면 끈다) · 키 값 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 18222 기동 env(같은 값 · 빈 포트 · 따로 `CHAT_DIR`): `CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images uv run python -m clinic_chat.consult --port <빈 포트>`

## 대상
발주 `$W/fetch-plan-code-task.md`(사용자 결정 · DQ1 = 예 · 호출마다 토큰 기록) · 정본 `$W/SPEC-011-fetch-plan.md` 0.1.2 · 리포트 `$W/fetch-code-report.md` · `$W/fetch-code/` · 스크린숏 `$W/e2e-shots/fetchplan-*.png` · 바뀐 코드 `git -C $A diff`(이번 변경 위주).

## 볼 것
1. 스펙 WP-1 ~ WP-4 · 사용자 결정대로인가(`--resume` 둠 · 출력 안 줄임 · Jev 거르기 없음 · 안전 · 명시 늘 · DQ1). 스펙 밖 고침(`verify.parse` 맨 끝 객체 · `layers` 칸 없앰 · `CHAT_FETCH_CUT` · renumber 를 감지 뒤로 옮김)이 안전한가.
2. **호출마다 토큰**: 상담 경로 LLM 호출이 이해 · 답 둘뿐인가(grep) · `tokens.calls[]` · `tokens.sum` 값이 CLI 원 usage 와 같은가(재생 장부 몇 턴 대조) · null 처리 · 옛 칸 읽는 곳이 안 깨졌나.
3. **실물 직접**: 빈 포트에서 03b8 · ecc6 · 73bd(발주서 말 그대로)를 실제로 다시 돌려 리포트 전 → 후 표와 대조 — 턴마다 calls 네 칸 · 「## 자료」 크기 · 답 앞 2 줄 · 빠짐 · 이름만 줄 지어낸 상세 0. 리포트 −50.9% 가 재현되나(답 길이 차이는 감안).
4. **답 품질**: 전 → 후 답을 나란히 놓고 사람 눈으로 — 빠진 정보 · 틀린 말 · 명동점 밖을 잘못 말함 · 「정보 없어요」.
5. **화면 직접**: 새 브라우저 프로필로 세 대화 마지막 화면 — 주제 · 점 · 목록 · 모달 · 스피너가 앞 고침(D · E)대로인가.
6. 시험: 관련 시험 + 「1 옛 실패」가 정말 이번 변경 전부터인가(HEAD 에서 확인).

## 산출
`$W/review-fetch-code.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 실측 · 스크린숏 · 고칠 방향) · 실물 대조 표 · 스크린숏 `$W/e2e-shots/review-fetchplan-*.png`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-011 구현" --body "판정 / P0 · P1 · P2 수 / 실물 재현"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review SPEC-011 구현 완료 — <한 줄>. 상세는 인박스." --enter
```
