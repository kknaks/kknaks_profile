# [reviewer_code] 코드 검수 6 — FE P4·P4 소수정 + BE 후속(E1~E6) + WP-005 (차분만)

너는 **sc-ax `reviewer_code` 워커**다. 검수 1~5 를 한 세션이다. 범위 = `git diff 8397d8f..59e1102`(FE P4 9644e7c · BE 후속 96d5312 · FE 소수정 ad4da8a · WP-005 59e1102). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` 읽기만 · 격리본(`git archive`) 필수(FE P5 병렬) · 서버·reset·포트 금지.

## 1. 기준

- SPEC 0.4.1 §3.2 · §5.3(드레인·keepalive 는 §13 OQ 잠정) · §6 · §8 · §9-5(D29) · §10 · §12 R-36/R-37 · 10-decision D25~D31. WP-005 계약(정렬본) · WP-006 Phase 4.
- 브리프: `sc-meeting-fe-p4-brief.md` · `sc-meeting-fe-p4-fix-brief.md` · `sc-meeting-be-wp002-fix-brief.md`(E1~E6) · `sc-meeting-be-wp005-brief.md`(§0 evidence 키 + 자료·공유·검색). 리포트: `report-fe-p4.md` · `report-be-followup.md` · `report-be-wp005.md`.
- 코디 실물: E1 드레인 후 transcript 2블록(301+34자, 41.4초) · E4 참석자 승격 201 · E5 due ISO 환산 · 화면 근거 칩 NaN(→§0, 이제 `start_ms/end_ms`) · WP-005: 혼합 업로드 201(attached 1, failed 2 사유) · 전부 실패 422 `meeting_materials_rejected` · 진행 중 409 · shares basis · 참석자 삭제 409 · 열람자 상세 shared/can_edit_info false · 열람자 자료 삭제 404 · 검색 소유자·열람자 1건씩 · 검수 5 WARN 이월 W-a(D26 소비) 해소 확인.

## 2. 확인 — PASS/FAIL(파일:줄)

1. **FE P4** — transcript 소비·at_ms 축 · 근거 칩→탭 전환+하이라이트 · promote 제출 이음매가 다른 화면 무영향(WorkModals) · finalize 버그 수정 · export a href 하나 · title_candidate 표시·확정 · 409 `meeting_agenda_stale` 처리 · 작성자 표시 이름 · `can_write_memo`·`started_at` 소비(W-a 닫힘) · hex 0 · 시안 밖 요소 0.
2. **FE 소수정** — D31 벽시계(started_at+at_ms) · NaN 가드.
3. **E1~E3** — `finish` 한 번만 · 정상 종료에서만 드레인 · `finally` flush · 상한 8초 상수 한 곳 · keepalive 10초 펌프가 오디오 경로와 경합하지 않는가(순서 보존 유지) · 스모크가 키·본문을 출력하지 않는가.
4. **E4~E6** — `eligible_member_ids` 기본값 빈 집합·회의 경로만 참석자 ∪ 만든 사람 · 기준일 프롬프트 · 스탬프 title_candidate · 팀장 capability 한 줄 + 뒤집은 테스트가 D30 을 명시.
5. **WP-005** — evidence 키 `start_ms/end_ms` 투영(detail·transcript·export 전부) · 자료 4 라우트 게이트(참석자·in_progress 409·올린 사람 삭제·열람 축)·20MB·PDF/MD·부분 성공 201/전부 실패 422 · 저장 위치 리포 밖·응답에 storage key 없음 · `GET /shares` basis · 중복 건너뜀 · 참석자 삭제 409 · 검색 갈래(resource_type meeting, 회의당 하나, 열람 축, 검색 회귀 0).
6. **회귀·경계** — `uv run pytest -q tests/contract/test_meeting_*.py tests/contract/test_material_search_public.py <work 계약 5> tests/architecture -m 'not integration'` · `npx tsc --noEmit && npx vitest run src/meetings/` · 리포트 주장 vs 코드.

## 3. 산출물

`review-code-06-report.md` — 총평 · 항목 1~6 표 · FAIL 파일:줄+방향 · WARN 이월.

## 4. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 6" \
  --body "총평 / 항목 1~6 / FAIL·WARN / 검증 수치"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 6: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
