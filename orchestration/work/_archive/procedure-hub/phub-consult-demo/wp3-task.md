# [app] SPEC-010 WP-3 — 조건 누적 · 주제 → 진료항목 (사용자 승인 11-20)

너는 WP-0 ~ WP-2 추가분을 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **`$W/SPEC-010-consult-myeongdong.md` 0.2.7(검수 PASS · `$W/review-spec-010-r8.md`)** — §5-0 조건(CD) · 주제(TP1 ~ TP14) · §5-1 ~ §5-3 감지 · 입력 전수 표(E · C · T) · §13 WP-3 행 · 결정 표 `$W/_RESUME.md` §2. 실측 `$W/research-v05-facts.md`. 데이터 `$A/data/kos/myeongdong-mapping-20261120-v3.json`(1af2216c) · 허브 18105(gold caa03560 · GET 만).

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라(시험 서버는 빈 포트) · 시험은 `tests/test_v05_detect.py` · `tests/test_v05_topics.py`(있으면) + §13 WP-3 회귀 목록(이해 호출 · pick 판 · 장부 · list 등)만 — 전체 pytest 금지 · ruff 손댄 파일.

## 할 일
§13 WP-3 행 그대로: 조건 칸 누적(CD) · **주제**(TP1 ~ TP14 — 규칙 A · B 셈 + 이해 호출 ① JSON `topic{move, to}` 칸 · 합치기 · 저장 · 되돌림 · 장부 `consult.topics` · `active_topic` · 재기동 복원) · 고민 길 reach 「케이스 직접」 만 · 효과 길(케이스 · 시술 행만) · 이름 일치(NM) · 부위 거르기(SF) · 0 일 때(LS) · 턴 줄기 `items` 이벤트 · 이해 호출 목록에 effect · procedure_case · pick country(pick 판 `0.5.0-draft`).
완료 조건: 시험 통과 · **실물 허브 표본 기대 표 대조**(스펙 WP-3 행 — 팔자주름 · 턱살 · 기미 · 리프팅 130 등 — 수 · 엉뚱 0) · 주제 시나리오(볼 필러 → 기미 새 주제 → 「아까 볼 필러」 되돌림 · 마지막 상태 그대로) 실물 이해 호출 한 번 이상(빈 포트 서버) 장부로 확인.

리포트 `$W/wp3-report.md`: 바뀐 파일 · 시험(명령 · 통과 수) · 실물 표본 대조 표 · 주제 시나리오 장부 발췌 · 스펙과 다른 점.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-3" --body "파일 / 시험 / 표본 / 주제"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-3 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] app: <질문>" --enter`
