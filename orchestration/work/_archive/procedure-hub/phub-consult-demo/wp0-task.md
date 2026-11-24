# [app] SPEC-010 WP-0 — 실측(코드 0) (사용자 승인 11-20 「응!!!」)

너는 clinic_chat 앱 워커다. 앞 맥락 없음 — 스펙과 이 문서만으로. 작업 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(branch kknaksss/phub-consult-demo). **이 WP 는 코드 0 · 리포트 1 개.** 커밋 0 · push 0 · 서브에이전트 0 · 사용자 포트 18222 손대지 마라(허브 18105 는 GET 만).

정본: `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **`$W/SPEC-010-consult-myeongdong.md` 0.2.2(검수 PASS · `$W/review-spec-010-r5.md`)** — §13 WP 표 · 「WP-0 실측 항목」 · 결정 표 `$W/_RESUME.md` §2 11-19 ~ 11-20. 데이터 `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120-v3.json`(94b88022 · `$A/data/kos/` 에도 같은 파일) · 허브 `http://127.0.0.1:18105/procedure-hub/gold`(gold 57b420ad) · 시안 `$W/design-consult-20261120.html` · 그림 시드 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/images/`.

## 할 일
스펙 「WP-0 실측 항목」 전부를 실측해 **`$W/research-v05-facts.md`** 표 하나로. 각 항목: 무엇을 · 어떻게(호출 · 셈) · 결과(값 · 수) · 스펙과 다른 점(있으면 스펙 절 번호 · 고칠 방향). 검수 r5 P2 3 개(e2e C3 옛 글 · WP-5 옛 덮개 0 시험 · CO 겹침 10)도 실측으로 맞는 값을 적어 둔다(스펙 고침은 코디가 따로).
그 밖에 WP-1 ~ WP-7 을 시작하기 전에 0.4 코드(`$A/clinic_chat/consult/*` · `prompts/consult.json` · tests)에서 재사용할 함수 · 손댈 파일 목록 · 0.4 시험 중 회귀 위험 목록을 같은 리포트에.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-0 실측" --body "항목 수 / 스펙과 다른 점 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-0 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] app: <질문>" --enter`
