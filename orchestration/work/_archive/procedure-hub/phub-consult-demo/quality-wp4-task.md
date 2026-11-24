# [측정] SPEC-012 WP-4 — 고친 코드 전 → 후 (사용자 승인 11-23 「품질 먼저 · 쭉 진행해」)

너는 측정 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 · 프롬프트 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만 · gold `e8f02287…`) · 키 · 토큰 값 출력 0.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(**작업 트리 = SPEC-012 구현 · 커밋 안 됨 · 검수 r2 PASS** — 읽기만 · 쓰기 0) · 측정 `$W/quality/` · 스펙 `$W/SPEC-012-consult-quality.md` 0.1.3 §4 완료 조건 C1 ~ C7 · §5 WP-4 · 「전」 기준선 = WP-0 `$W/quality/out/base2-*`(다른 워커가 돌리는 중 — 끝났는지 `base2-report.md` 로 확인 · 안 끝났으면 「후」 만 먼저 돌리고 채점은 끝난 뒤).

## 할 일
1. `$A` 작업 트리 그대로 빈 포트에 띄워 `run.py --runs 3` S01 ~ S13 → `out/after-<시각>/`. meta 에 gold_hash · 앱 `35b56e5` + `git -C $A diff 35b56e5 | shasum` 기록(커밋이 없으니 diff 해시로 판을 박는다). 기동 env 는 18222 와 같게(`CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images`) · 장부는 따로 `CHAT_DIR`.
2. `score.py --before out/base2-*` → 기준 22 × 전 → 후 · 시나리오별 · 흔들림 · 비용(턴당 $ 전 → 후) · 구멍 H1 ~ H16 별 걸린 턴 전 → 후.
3. 완료 조건 C1 ~ C7 판정 표(통과 / 못 함 · 근거). **확정 칸 기준 하나라도 떨어지면** 그 턴 · 까닭 · 코드 자리를 따로 표로.
4. 화면 대표 3 장(새 브라우저 프로필) `$W/e2e-shots/spec012-after-*.png`(주제 나누기 · 볼 처짐 연속 · 부작용 질문).
5. `$W/quality/after-report.md`.

## 검증
`git -C $A status --short` 시작 전과 같음 · 18222 · 18105 그대로 · 띄운 포트 끔 · 키 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "측정 완료: WP-4 전 → 후" --body "확정 통과 전 → 후 / 떨어진 기준 / C1~C7 / 비용"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] WP-4 전 → 후 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] wp4: <질문>" --enter`
