# [reviewer · 읽기만] SPEC-010 0.1.0 검수 (자동 검수 · 11-20)

너는 procedure-hub 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 다른 파일 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0 · 사용자 포트(18105 · 18222) 손대지 마라(읽기 GET 은 허브 18105 만 허용).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 대상
`$W/SPEC-010-consult-myeongdong.md` 0.1.0 · 작성 지시 `$W/spec-010-task.md`(목표 · 정본 순서 · 담을 것) · 11-20 추가 지시(모달 그림 2 개 — 원리 + 방법).

## 대조 기준(정본)
1. 디자인 시안 `$W/design-consult-20261120.html`(사용자 확정 · 큰 파일 — 필요한 부분만) — 화면 구성 · 문구 · 칸이 시안과 같은가 · 시안에 없는 문구를 지어 넣었나.
2. `$W/gui-feedback.md`.
3. 매핑 JSON `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120.json`(8ca88c9a) · `$W/mapping-json-v2-report.md` — 스펙이 말하는 칸 · 셈 · status 값이 실제와 같은가.
4. 로컬 허브 `http://127.0.0.1:18105/procedure-hub/gold`(57b420ad · README `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/README.md`) — 스펙이 부르는 도구 · 인자 · 응답 칸이 실제로 있는가(GET 몇 번으로 확인).
5. `$W/_RESUME.md` §2 결정(11-19 ~ 11-20) — 정해진 것과 어긋나거나 다시 묻는 것.
6. 앱 0.4 코드(`$A/clinic_chat/consult/*` · `prompts/consult.json` · tests) — 스펙이 기대는 기존 함수 · 경로가 실제로 있는가.

## 볼 것
- 목표 달성: 고민 · 부위 · 시술 → 진료항목 · 모달(원리 + 방법 그림 · 개요 · 효과 · 부작용 · 제품 · 옵션) · 장바구니 · 최저가 · LLM 컨텍스트 — 빠진 경로.
- 입력 전수 표(§5-3)가 말 꼴 × 데이터 조합을 다 덮나 · 빈 결과 화면.
- 사용자 결정 필요(§11) — 이미 정해진 것을 다시 묻나 · 추천이 근거 있나 · 기계가 정할 수 있는 것을 사람에게 올렸나(사람 몫 50 안쪽).
- WP(§13) — 코드 워커가 순서대로 할 수 있나 · 완료 조건이 시험 가능한가 · 시험은 WP 관련만(전체 pytest 금지).
- 데이터 지어 넣기 · 가격 추정 · 시안 밖 문구.

## 산출
`$W/review-spec-010.md`: 판정(PASS / FAIL) · 지적 목록(P0 막힘 / P1 고쳐야 함 / P2 권고 · 각각 절 · 근거(파일:줄 또는 실측) · 고칠 방향) · 사용자에게 올릴 결정 중 정리 제안.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_dbc58c9f-06a3-4337-9ad3-b1f7102f121a --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-010" --body "판정 / P0 · P1 · P2 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 완료 — <한 줄>. 상세는 인박스." --enter
```
