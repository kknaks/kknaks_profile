# [backend] D39 — 내보내기 HTML 을 「주제 스레드형」 페이지 조판 템플릿으로 이식

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = d939dae). `backend/` 만. 커밋 금지.

## 정본
- 디자이너 템플릿 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/export-thread-template.html`(정적 샘플, CSS 인라인, A4 페이지 나눔) + 규격·치환 자리 `design/REPORT-export-template.md`.
- SPEC-004 0.4.5 §8-10(주제 스레드형 페이지, 표로 늘어놓지 않음) · WP-004 Scope.

## 할 것
- `modules/meetings/export.py` 를 템플릿과 **같은 마크업·CSS** 로 다시 쓴다(템플릿의 `{{…}}` 치환 자리에 실제 값: 회의명|제목 후보 · 일시(요일·시작~종료, Asia/Seoul) · 참석자 · 요약(없으면 생략) · 안건(순서·제목·결론 칩·근거 시각 칩 최대 3+N) · 줄(우측 시각 = started_at + evidence 시작, 없으면 빈칸) · 다음 할 일(「액션」 칩·제목·기한·근거 시각|「근거 없음」·승격이면 「요청됨」) · 꼬리(「SCAX · 회의록」, 내보낸 시각, **페이지 번호는 BE 가 채운다** — Chrome 이 @page 마진 박스를 지원하지 않는다. `.page` 나누기는 REPORT-export-template.md 의 요소별 소모 높이표로 서버가 계산해 안건/줄 단위로 끊는다).
- 외부 자원 참조 0(폰트 시스템 스택, 이미지 없음) · 링크·내부 값(id·storage key·계정) 없음 유지 · XSS 이스케이프 유지.
- 템플릿을 리포 안(`backend/src/ax_workspace/modules/meetings/templates/export_thread.html`)에 두고 문자열 치환/간단 렌더러로(Jinja 등 새 의존성 추가 금지 — 이미 있으면 사용).
- 테스트: 기존 export 테스트 갱신 + 스냅샷성 검사(핵심 마크업 존재·이스케이프·내부 값 미노출·페이지 나눔 CSS 존재).

## 덤 1건(D40 미결 ④)
- `graph.py` 가 requester_id 로 person 노드를 만들어 승격 요청은 `person:system:meeting` 노드가 생긴다 — 시스템 행위자(`system:` 접두)는 person 노드로 만들지 않고, 대신 회의 노드(있으면)와 요청을 잇는다. 테스트 1.

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 내보내기 스레드형 템플릿 이식" \
  --body "변경 파일 / 템플릿 위치 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 내보내기 템플릿. 상세는 인박스." --enter
```
