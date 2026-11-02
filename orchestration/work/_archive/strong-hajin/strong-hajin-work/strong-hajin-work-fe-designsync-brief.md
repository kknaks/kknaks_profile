# [frontend] MyWork.html 디자인 싱크 — 내려받기만

## 1. SSOT

Claude Design 프로젝트 **`7e839512-977c-4142-b4b5-d992df566ffc`** (TheSC AX Design System).
이 워크트리의 `.design-sync/config.json` 의 `projectId` 와 같은 프로젝트다 — 우리가 부품 35종을
올려 둔 그 통이고, 이번엔 **반대 방향(내려받기)** 이다.

- 대상 파일: `MyWork.html`
  (URL: `https://claude.ai/design/p/7e839512-977c-4142-b4b5-d992df566ffc?file=MyWork.html`)
- 그 파일이 import 하는 것: `_ds_bundle.css` · `_ds_bundle.js`
- 배경 참고(읽기만): `.design-sync/NOTES.md` · `.design-sync/conventions.md`

## 2. 목적

**이번 발주는 내려받기까지다.** 시안을 워크트리에 떨어뜨리고 무엇이 왔는지 보고한다.
구현·이식·분석·스펙 반영은 **이번 범위가 아니다.** 시안을 보고 다음 판을 코디가 정한다.

## 3. 도구

`DesignSync` 를 쓴다. 이 세션(워커 터미널)은 사용자 로그인이라 도구가 붙어 있다.
- 목록에 안 보이면 **deferred** 라 그렇다 — `ToolSearch` 에 `select:DesignSync` 로 스키마를 먼저 불러라.
- 인증이 안 되어 있으면 `/design-login` 이 필요하다. **네가 우회로를 찾지 말고** §9 (2) 로 즉시 코디에게 보고하라.
- 서브에이전트(Agent tool)에는 이 도구가 전파되지 않는다 — **네 세션에서 직접** 받아라.

## 4. 받는 것과 놓는 자리

`.design-sync/screens/` 를 새로 만들어 그 아래 **원본 그대로** 떨어뜨린다. 손으로 고치지 않는다.

| 원격 파일 | 놓을 자리 |
|---|---|
| `MyWork.html` | `.design-sync/screens/MyWork.html` |
| `_ds_bundle.css` | `.design-sync/screens/_ds_bundle.css` |
| `_ds_bundle.js` | `.design-sync/screens/_ds_bundle.js` |

`MyWork.html` 이 위 둘 말고 **다른 파일도 참조하면**(이미지·폰트·추가 css/js) 그것도 같은 자리에
받고 보고에 적는다. 상대경로가 깨지지 않게 파일명은 바꾸지 않는다.

## 5. allowed_paths

**`.design-sync/screens/` 만.** 새로 만드는 디렉토리다.

- `frontend/` · `backend/` 를 **건드리지 않는다.** 시안을 앱에 이식하지 않는다.
- `.design-sync/` 의 **기존 파일**(config.json·conventions.md·NOTES.md·previews/·fonts/·flatten-css.mjs)을
  수정·삭제하지 않는다.
- 문서 경로(`para/`·`orchestration/`)는 코디 소유 — 접근 금지.

## 6. 제약 — 이 워크트리는 깨끗하지 않다

이 트리에는 **W1 미커밋 변경 20+ 파일**이 살아 있고 사용자 E2E 대기 중이다. 날리면 복구 못 한다.

- **`git stash` · `git checkout` · `git reset` · `git clean` 금지.** 공유 트리다.
- 같은 워크트리에 **다른 에이전트가 동시에 돌고 있다.** 네 자리(`.design-sync/screens/`) 밖을 쓰지 마라.
- 커밋·push·PR 금지. 변경만 남긴다.
- 테스트·빌드 실행 불필요 — 이번엔 코드를 안 고친다.

## 7. 보고에 담을 것

1. 받은 파일 목록 — 경로 · 바이트 크기 · 줄 수
2. `MyWork.html` 이 참조하는 외부 자원 전부 (`<link>`·`<script>`·`src=`·`url(` 를 **grep 으로 세서**
   하나도 빠뜨리지 말 것). 그중 못 받은 것이 있으면 그 사실과 이유
3. 시안 한 줄 요약 — 어떤 화면인지 (자세한 분석·차이 비교는 하지 마라)
4. `_ds_bundle.css/js` 가 우리가 올린 것과 같은 판인지 판단이 서면 한 줄. 안 서면 「모름」

## 8. 하지 말 것 (명시)

시안 구현 · 부품 이식 · DS-gaps 작성 · 스펙/WP 수정 · 기존 코드 리팩터 · 테스트 추가.
전부 다음 판이다. **시킨 것만 한다.**

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d0d0454a-1ab6-484f-b125-d67fe035c803 --from term_758e0ac7-53e6-4313-bf71-f39d7b971a19 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: MyWork.html 디자인 싱크" \
  --body "받은 파일 목록(경로·크기·줄수) / 참조 자원 전수 / 못 받은 것 / 시안 한 줄 / 번들 동일성"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d0d0454a-1ab6-484f-b125-d67fe035c803 \
  --text "[worker_done] frontend 완료 — MyWork.html 디자인 싱크. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d0d0454a-1ab6-484f-b125-d67fe035c803 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
