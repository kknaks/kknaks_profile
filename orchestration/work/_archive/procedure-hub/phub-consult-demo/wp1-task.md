# [app] SPEC-010 WP-1 — kos_map(매핑 JSON v3) + 설정 + 장부 칸 (사용자 승인 11-20)

너는 WP-0 을 한 clinic_chat 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md`(0.2.2 — §3 데이터 읽기 · §2-3 설정 · §13 WP-1 행) · 네 실측 `$W/research-v05-facts.md`. 스펙 워커가 실측 19 를 반영해 0.2.3 을 쓰는 중이다 — **WP-1 범위는 바뀌지 않는다**(바뀌면 코디가 알림).

커밋 0 · push 0 · 서브에이전트 0 · 사용자 포트 18222 손대지 마라(시험 서버는 빈 포트) · 시험은 `tests/test_v05_kos_map.py` + 손댄 파일 관련 0.4 시험만(전체 pytest 금지) · ruff 손댄 파일.

## 할 일
§13 WP-1 행 그대로: `kos_map.py`(v3 — `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120-v3.json` 94b88022 · `$A/data/kos/` 같은 파일 · products · option_refs · covers 색인 · sites · groups) · 설정 칸(경로 · sha) · 장부 `kos_map` 칸 · `tests/test_v05_kos_map.py`(작은 고정본 · 실물 v3 시작 성공 · 꼴 어긋난 사본 시작 실패).
WP-H(허브 워커)가 끝나면 JSON meta 해시가 바뀐다(items · products 바이트는 같음) — sha 설정은 그때 코디가 알려 준다(지금은 94b88022).

리포트 `$W/wp1-report.md`: 바뀐 파일 · 시험 결과(명령 · 통과 수) · 실물 시작 확인 · 다음 WP 메모.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-1" --body "파일 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-1 완료 — <한 줄>. 상세는 인박스." --enter
```
