# [backend] WP10 코드 쪽 — cc 아카이브 · Actions 이미지 procedure-*

같은 cc-prototype `backend` 워커 · 같은 코드 워크트리. **배포 먼저**(사용자) — 접근 제한은 배포 뒤.

- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-004-procedure-app.md` WP10 · SPEC-004 §2 · DEC-005 D-03(기존 주소 교체 · `cc/` → `_archive/cc/`)
- 할 일: ① `git mv cc _archive/cc`(내용 그대로 · README 에 '아카이브 — 배포 안 함') ② `.github/workflows/cc-back-image.yml` · `cc-front-image.yml` → **`procedure-back-image.yml` · `procedure-front-image.yml`**(같은 방식 — main push · arm64 · ghcr · 경로 필터 procedure/back|front · 이미지 이름 `procedure-back` · `procedure-front`) · front 빌드 인자 `NEXT_PUBLIC_API_BASE_URL` = 배포 주소(`https://ccc.medisolveai.xyz` — back 을 같은 도메인 /api 로 둘지 차트와 맞춰라: infra 워커가 같은 도메인 /api → back 으로 라우팅하면 front 는 같은 주소) ③ Dockerfile 이 배포에 맞는지(back uvicorn --factory · 0.0.0.0 · 포트 · /data DB 경로 · APNs 키 경로 env) ④ 루트 README 기능 표 갱신
- allowed_paths: `.github/workflows/**` · `_archive/cc/**`(이동만) · `cc/`(삭제 = 이동) · `procedure/back/**` · `procedure/front/Dockerfile` · `README.md`
- 검증: back/front docker build 1회씩(arm64 가능하면) · Actions yaml 문법 · 비밀값 0 · **커밋 금지**(코디가 커밋 · PR)

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
  --subject "backend 완료: WP10 코드 쪽(아카이브 · Actions)" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
