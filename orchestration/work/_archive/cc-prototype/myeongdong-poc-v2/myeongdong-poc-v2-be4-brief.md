# [backend] SPEC-004 WP1 → WP2 — 계정 · 권한 · 통역

같은 cc-prototype `backend` 워커 · 같은 워크트리(`/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2`). frontend(`procedure/front` WP3) · mobile(`procedure/app` WP4~5)이 동시에 일한다 — 그 폴더는 건드리지 마라.

- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` §2(env · 0.0.0.0) · §3(계정 · 역할 검사표 · 수락 규칙 · actor) · §4(통역 복사 · WS 토큰 인증) · §8.1(back 단위 시험). **작업**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-004-procedure-app.md` WP1 · WP2 완료 조건
- 통역 원천(read-only): `/Users/kknaks/git/toy_pr2/cc-prototype` `git show origin/main:cc/back/...` — **복사**(import 금지). `SONIOX_API_KEY` 값은 `/Users/kknaks/git/ax-clinic-project/scripts/.env` 에 있다 → 로컬 `procedure/.env` 에 넣고 값은 출력 · 커밋 금지
- PoC 의사 카드 = **KOS 데모 지점 실제 원장 1명**(시스템 계정 X) — 고른 원장 이름 · kos id 는 보고에 쓰지 말고 env 에만
- **WP1 끝나면 중간 알림**(frontend WP3 · mobile 이 로그인 API 를 쓴다): `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[WP1 완료] backend 계정 · 권한 — auth API 모양 한 줄" --enter` → 멈추지 말고 WP2
- allowed_paths: `procedure/back/**` · `procedure/docker-compose.yml` · `procedure/.env.example` · `procedure/README.md`
- 검증: WP 마다 그 시험만(역할 3 × 조작 8 허용/403 · 수락 · 토큰 · WS 인증) · 끝에 전체 pytest · ruff 1회 · back 재기동. 데모 KOS 쓰기 금지 · 커밋 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: SPEC-004 WP1·WP2" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
