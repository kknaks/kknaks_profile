# [frontend] 소수정 — 안건 번호는 자리(1부터)로, order 값 그대로 쓰지 않는다

너는 **sc-ax `frontend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = f463f5d 이후). `frontend/` 만. 커밋 금지.

## 발견 (코디 브라우저 실물 e2e 3차)

AI 요약 탭에 「**안건 0.** 안건 1」·「안건 1. 온보딩 자료」 — 화면이 `agenda.order` 값을 번호로 그대로 쓴다. 바로 시작 기본 안건은 order 0, 예약 안건은 1부터라 값이 갈린다. 시안은 「안건 1.」부터.

## 할 것

- 안건 번호 = **정렬된 목록에서의 자리 + 1**(order 로 정렬만 하고 값은 쓰지 않는다). 안건 블록·AI 요약 탭·패널·내보내기 링크 등 번호를 그리는 자리 전부. 테스트 1(order 0·1 인 안건 둘 → 「안건 1.」「안건 2.」).

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 안건 번호 자리 기반" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 안건 번호. 상세는 인박스." --enter
```
