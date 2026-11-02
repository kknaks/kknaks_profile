# [mobile · 시안] 구현 반영 시안 동기화 — slug 마감 전

너는 cc-prototype `mobile` 워커. claude design(DesignSync) `dda9a931`. **코드 수정 금지.**
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 산출물 경로 말고 건드리지 마라.

## 왜
명동 PoC v2 를 닫는다. 확정 시안 이후 E2E 로 바뀐 것이 코드(main `329b543`)에만 있다. **시안이 구현을 그대로 보여 줘야 한다 — 정보가 다 들어가 있어야 한다**(사용자).

## 대상 · 방식
- `Ceramique 시술실 태블릿.dc.html` · `Ceramique 간호사 모바일.dc.html` · `Ceramique 의료진 앱.dc.html`(앱 — 로그인 폼 · 목록/필터 · 룸 상세 태블릿 두 열 · 통역 바 · 알림/수락). 실제 앱 화면은 시뮬레이터(배포 서버) 스크린샷 기준 — 시뮬레이터는 하나씩
- **원본은 덮어쓰지 않는다.** 같은 이름 뒤에 ` (구현 v3)` 를 붙인 **새 파일**로 올린다. 원본 = 사용자가 고친 확정 시안이라 남긴다
- 값의 기준 = **코드**(read-only: `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` = origin/main) + 배포 화면(`https://ccc.medisolveai.xyz` · 로그인 `procedure/.env` 의 CCC_ADMIN_ID/PASSWORD — 값 출력 금지)
- 바뀐 것 출처: `orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 · `e2e-feedback-batch-1.md` · `e2e-app-feedback-batch-1.md` · `e2e-device-feedback-batch-1.md` · `fix-decisions-r1.md` — **처분 줄마다** 시안에 반영됐는지(화면에 안 보이는 순수 로직은 '해당 없음')
- 장면: 원본 장면 유지 + 새로 생긴 화면/상태(정상 로그인 폼 · 실패/잠금 문구 · 귀가 칩 · 귀가 대기 흐림 등)

## 산출물
- claude design 새 파일 · 로컬 사본 `orchestration/work/myeongdong-poc-v2/design-sync/`
- 리포트 `orchestration/work/myeongdong-poc-v2/design-sync-mobile-report.md` — 파일 이름 · 장면 목록 · **출처 줄 → 시안 반영 대응표(누락 0)** · 코드와 다른 곳 0

## 하지 말 것
- 원본 시안 수정 · 삭제 · 코드 수정 · 커밋 · 실명/연락처/키 값

## 검증
- 업로드 뒤 다시 받아 `truncated:false` · 배포 화면 스크린샷과 나란히 비교(리포트에 경로)

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "mobile 완료: 시안 구현 동기화" \
  --body "찾은 파일 / 바뀐 것 수 / 정책 후보 수 / 코드 어긋남 수 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] mobile 시안 구현 동기화 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] mobile: <질문>" --enter`
