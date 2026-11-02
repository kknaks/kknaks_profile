# [planner] 스펙 워크트리 origin/main 머지 충돌 해소 — 문서 3개

너는 **sc-ax planner 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`. **코디가 `git merge --no-ff --no-commit origin/main` 을 걸어 둔 상태다(MERGE_HEAD 있음).** 커밋·push·`merge --abort`·`reset` **절대 금지** — 충돌 파일을 풀고 `git add <파일>` 까지만.

## 충돌 3 (main 쪽 변경은 작다)
- `products/sc-ax/10-decision.md` — main #720(보호 Linux 납품 계약) +3/-2 · 우리 D41~D51 +67
- `products/sc-ax/20-spec/spec-004-meeting-note.md` — main #722(AX interaction 계약 동기화) +8/-2 · 우리 0.4.5→0.4.11 +702
- `products/sc-ax/40-architecture/system.md` — main #711·#720 +15/-6 · 우리 +13/-5

## 원칙
- **둘 다 살린다.** 우리 것(0.4.11, D41~D51)이 회의 정본이고 main 은 다른 스펙(AX interaction·자료 검색·보호 납품)의 동기화다. 같은 표/절에 양쪽이 줄을 더했으면 둘 다. main 이 spec-004 의 구절을 옛 회의 모델 기준으로 고쳤으면(채팅 회의 만들기/공유 등) 우리 0.4.11 기준으로 맞추고 어디인지 보고에.
- 충돌 마커 0 · `lint --strict` exit 0(sc-ax ERROR 0). 판 번호는 0.4.11 유지(머지는 내용 변경이 아님). 변경 이력 줄은 손대지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "planner 완료: 스펙 main 머지 충돌 해소" \
  --body "푼 파일 / 양쪽 살린 자리·우리 기준으로 맞춘 자리 / lint / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] planner 완료 — 스펙 main 머지. 상세는 인박스." --enter
```
