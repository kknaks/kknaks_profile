
# [frontend] 앱 아이콘 교체 — 메디솔브 M 로고, macOS 규격으로 조금 작게

너는 **strong-hajin `frontend` 워커**다. **너는 앞 맥락이 하나도 없다.** 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 rules·skills·tools·workflow)
- `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy` — 지금 `origin/main`(cdb0f3f) detached 일 수 있다. 시작할 때 `git fetch && git checkout -B kknaksss/strong-hajin-icon origin/main`.
⚠ infra 워커가 이 워크트리를 이미지 빌드 소스로 읽었다(빌드는 끝남). `frontend/src-tauri/icons/`·`tauri.conf.json` 외엔 건드리지 마라.

## 1. SSOT
- 사용자 지시(2026-10-01): 「mediness-rust 의 회사 로고 아이콘을 **크기 좀만 줄여서** 만들자」
- 원본: `/Users/kknaks/git/harness_works/mediness-rust/src-tauri/icons-prod/icon.png` (512×512, 흰 바탕 가득 + 파란 그라데이션 M). **읽기만** — 그 레포는 건드리지 마라. `icons/`(dev 배지판)는 쓰지 않는다
- 기대는 개념: 해당 없음

## 2. 배경
지금 `frontend/src-tauri/icons/*` 는 파란 단색 정사각형 자리표시다(#3 에서 임시). dmg·Dock 에 그게 뜬다.

## 3. 계약
- macOS 앱 아이콘 격자: 1024 캔버스에 둥근 사각형 몸통 약 824(여백 ~100), 모서리 반경 ~185, 흰 바탕. M 로고는 그 몸통 안에서 원본 대비 **조금 작게**(원본 여백보다 넉넉히 — M 이 몸통 폭의 약 60%)
- 원본이 512 라 확대하면 흐려진다 → M 을 **줄이는 방향만** 쓰고, 1024 마스터는 고품질 리샘플링(Pillow LANCZOS 등)
- 산출: 1024 마스터 → `npx tauri icon <master>` 로 세트 생성. `tauri.conf.json` `bundle.icon` 목록이 가리키는 파일이 전부 갱신돼야 하고, macOS 번들용 `icons/icon.icns` 가 목록에 없으면 추가
- 생성 부산물 중 Windows Store·iOS·Android 용 등 conf 가 안 쓰는 파일은 두지 마라

## 4. 먼저 읽을 파일
- `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/frontend/src-tauri/tauri.conf.json:16-21` · `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/frontend/src-tauri/icons/`

## 5. allowed_paths
- `frontend/src-tauri/icons/` · `frontend/src-tauri/tauri.conf.json`(icon 목록만). 마스터 PNG 는 scratchpad 에(레포에 넣지 않는다). 커밋·push 금지

## 6. 단계
1. 원본 읽고 M 영역 bbox 추출 → 1024 마스터 합성(둥근 사각형 흰 몸통 + 축소 M, 바깥은 투명)
2. `npx tauri icon` → 필요한 파일만 남김 → conf 목록 정리
3. 검증: 생성 png 들을 눈으로 확인(너가 Read 로 본다) · `cd frontend/src-tauri && cargo check` · `make shell-verify` · 가능하면 `.app` 번들만 빌드해 Finder 아이콘 확인(`npx tauri build --bundles app` — 시간 오래 걸리면 생략하고 사유 보고)
4. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/work/strong-hajin-deploy/report-fe-icon.md` — 크기·여백 수치, 바뀐 파일, 1024 마스터 경로

## 7. 하지 말 것
- 원본 레포 수정 · `shell.config.json`·capabilities·운영 origin 건드리기(dmg 운영 빌드는 다음 판) · 서명·공증

## 8. 검증
```
make shell-verify · cargo check. 실제 실행 못 한 검증은 사유와 함께 pending.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --from term_0b24189f-a312-4c9e-9aa5-f50bb1d20908 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
