# [reviewer_spec] 검수 3 — 0.4.1 수정분만 (검수 2 FAIL 2·WARN 9 해소 확인)

너는 **sc-ax `reviewer_spec` 워커**다. 검수 2 를 한 세션이다 — 그 맥락 위에서 **수정분만** 본다. 전체 재검수가 아니다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` — 읽기만.

## 1. 기준

- 검수 2 리포트 `orchestration/work/sc-meeting/review-02-spec-004-report.md` 의 F-A · F-B · WARN 9 · §7
- 코디 결정 D16(검수 2 반영 기본값): 회의 정보 편집 = 참석자 전원, 회의록 편집 = 만든 사람 · 「기타」 블록은 시안에서 제거(SPEC §4.1-7 유지, §12 R-24 충돌 기록) · 삭제 갈래 = [회의 취소](회의 취소) / [회의록만 삭제](회의록+자료 삭제, 예약 유지) · 안건 출처 = 직접 입력·지난 회의에서 넘어옴·AI 정리 · 화자 매핑 BE = WP-002 · POST /end = WP-001 선언·WP-004 소비 · 회의실 판정·the Connect = 데모 범위 밖(정적 목록) · 10-decision 제목 D1~D14 · §4.2-5 결론 열
- **시안 최신본**(디자이너가 검수 2 뒤 고침): `design/회의실.dc.html`(기타 블록 제거·출처 셋·완료·장소 칸) · `design/REPORT-회의실-v2.md`

## 2. 확인할 것 — 각각 PASS/FAIL

1. F-A 해소: §3.3·§3.1-7·work-001 PATCH actor 게이트가 「참석자 전원」인가. 시안 `btnHeadEdit` 조건과 일치하는가.
2. F-B 해소: 시안에서 「기타」 가 사라졌는가(`grep -n 기타 design/회의실.dc.html` — 화면 노출 0). SPEC §12 R-24 에 충돌 기록이 있는가.
3. WARN ①~⑧ 각각의 처리 위치(파일:줄). ①삭제 갈래(SPEC 본문 + work-001 DELETE scope) ②출처 값·R-19 ③화자 매핑 WP-002(entity·invariant·Phase·검증) + WP-006 화면만 ④/end 소유 표기 양쪽 ⑤10-decision 제목 ⑥§4.2-5 결론 열 ⑦§2.2 회의실 행 + §1·§3.1-4 + work-001/006 판정 BE 제거 ⑧owner TBD 유지.
4. 수정이 **새 어긋남**을 만들지 않았는가 — 특히 삭제 갈래 문구가 시안 `회의록.dc.html` 의 모달(×·[회의록만 삭제]·[회의 취소]·토스트)과 정확히 같은가, WP-002 와 WP-006 사이 화자 매핑 계약이 모순 없는가.
5. `document_version` 0.4.1·판 이력, lint --strict sc-ax 0/0, git status = 4 M + 6 ??.

## 3. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-03-spec-004-report.md` — 짧게: 총평(PASS / FAIL — 재발주) · 항목 1~5 표 · 남은 사용자 결정(있으면). 리포 파일 수정 금지.

## 4. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_a551cbf0-0d02-43f1-a84b-4e00ed5fb398 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_spec 완료: 검수 3 SPEC-004 0.4.1" \
  --body "총평 / 항목 1~5 / 남은 결정 / lint / git status"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_spec 완료 — 검수 3: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
