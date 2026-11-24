# [researcher] phub-consult-demo 착수 조사 — 상담 화면 · 명동점 상품 · 시술 그림: 있는 것 / 없는 것

너는 **procedure-hub `researcher` 워커**다. **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다. 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` (코디 워크트리 — 코디와 공유. **리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라**)

읽기만 하는 코드 워크트리:
- 허브: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo` (PROCEDURE-HUB · branch `kknaksss/phub-consult-demo` = `origin/release/v1.2.0` aa46a86 — stg 에 올라간 판)
- 앱: `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` (clinic_chat · branch `kknaksss/phub-consult-demo` = `origin/main` 97d964e — 상담 채팅 0.4 · **공개 레포**)

## 1. SSOT — 먼저 읽을 것

`A=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/_archive/procedure-hub/phub-gold-jev`

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/para/projects/company/procedure-hub/log/2026-11-18-phub-gold-jev.md` ← 앞 작업 회고(§4 결정 · §7 잔여)
- `$A/_RESUME.md` §2 ← 앞 작업 결정 표
- `$A/SPEC-007-image-data.md` ← 그림 데이터 계약(silver/DB 2표) · `$A/research-images.md` · `$A/research-images-v2.md`
- `$A/SPEC-003-hub-gold-db.md` §11(stg 판) · `$A/stg-runbook.md` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/docs/adr/0004-staging-runtime-configuration-and-cutover.md`
- `$A/SPEC-001-hub-gold-mcp.md`(0.8.2 · 허브 도구 계약) · `$A/SPEC-008-consult-entry.md`(0.2.1 · 상담 입구) · `$A/SPEC-004-consult-chat.md` · `SPEC-005` · `SPEC-006`(상담 앱 계약 층들)
- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/para/projects/company/procedure-hub/gold-api-guide.md` ← 허브 호출 안내서(도구 9 · REST · MCP)
- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/README.md` ← 상담 화면 실행 · env · 장부

기대는 개념: 해당 없음(조사).

## 2. 배경

이번 작업은 세 가지다. 순서 · 묶음은 이 조사 뒤 코디가 사용자와 정한다.

1. **상담 화면(GUI) 개선** — clinic_chat 상담 채팅(`clinic_chat/consult/`). 무엇이 불편한지는 사용자가 화면을 보며 말한다. 이 조사는 **지금 화면이 어떻게 짜여 있는지 지도**만 만든다.
2. **명동점 상품 연결(데모)** — 상담 시술 리스트에 명동점 실제 상품(시술 상위 데이터 · 최저가 · 이벤트)을 매핑해 보여 준다. **데이터는 사용자가 나중에 준다 — 꼴을 추측하지 마라.** 이 조사는 지금 코드 · 데이터에 상품 · 가격 · 지점 · 메뉴 관련으로 **무엇이 이미 있는지**(허브 silver/gold 의 제품 · 패키지 · 메뉴 「kind」 · 가격 칸 · 앱 리스트가 어디서 무엇을 그리나 · 앞 작업에 명동점 언급)만 센다.
3. **시술 이미지 응답** — 원리 · 방법 그림(SVG 103 · 라벨 787)을 허브 응답(도구) · 정적 서빙 · 상담 화면까지. 그림 원천은 허브 `assets/procedure-images/`. 지금은 silver/DB(`s_concept_image` · `s_concept_image_label`)에만 있고 응답에는 없다고 알려져 있다 — **실물로 확인**하라(허브 README 에 `GOLD_IMAGE_DIR` 이 보인다 — 무엇이 이미 되어 있나).

## 3. 계약

해당 없음(조사 · read-only).

## 4. 먼저 볼 자리(출발점 — 여기만 보라는 뜻 아님 · 전수는 grep 으로)

- 앱: `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/clinic_chat/consult/` (templates · static · 서버 라우트 · 리스트 · 얼굴 SVG · `sites.py`) · `prompts/consult.json`
- 허브: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/app/` 의 gold 모듈 · `gold_main` · `app.main` 의 gold 부착 · 이미지 적재 · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/data/medallion/` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/Dockerfile` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/.github/workflows/`
- 로컬 PG(읽기만 · SELECT 만): docker `phub-medallion-pg` 127.0.0.1:18432 — 접속 값은 `set -a; . ~/.config/phub/medallion-pg.env; set +a` 로만 싣고 **값을 출력하지 마라**
- stg 허브(읽기만 · GET 만): `https://api-stg-csp.medisolveai.com/procedure-hub/gold/health` 등 — 안내서 §2

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/research-start.md` — 그 외 생성 · 수정 0. 스크래치가 필요하면 네 세션 scratchpad.

## 6. 할 일 — 질문마다 답 + 근거(파일:줄 · 표/칸 · 응답 실물)

### Q1. 상담 화면 지도(GUI)
1-1 화면 구성 요소 전수 — 왼쪽 대화 목록 · 얼굴 패널 · 시술 리스트 패널 · 채팅 · 입력 · 드로어 · 객체 패널(디버그) · 그 밖. 각 요소가 **어느 템플릿 · CSS · JS · 서버 라우트 · SSE 이벤트**에서 나오는지(파일:줄).
1-2 화면 문구의 출처 — 문구가 템플릿 · `prompts/consult.json` · 코드 중 어디에 있나(나중에 「문구 지어 넣기 금지」 확인용).
1-3 스타일 체계 — 벤더링한 `static/`(CENTURION_DAY 사본 · 고치지 않는 파일) vs 앱 자체 CSS · 토큰 · 폰트 출처.
1-4 지금 화면에서 눈에 띄는 이상(코디 스크린숏 기준): 왼쪽 목록 맨 아래 줄 글자가 깨져 보인다(mojibake) — 원인 자리만 찾아라(고치지 마라). 그 밖에 템플릿 · 코드 읽다 보이는 「사람 눈에 이상해 보일 자리」.
1-5 화면을 띄우고 대화를 재생하는 길 — 가짜 턴(`CHAT_FAKE_TURN`) · 옛 대화 열기 · 헤드리스 스크린숏 가능 여부. (코디가 18222 에 앱을 띄워 두었다 — **그 프로세스를 끄거나 재시작하지 마라.** 너는 GET 만.)

### Q2. 명동점 상품(데모) — 있는 것만 센다
2-1 허브 silver/gold 의 상품 쪽 표 · 칸 전수: 제품 · 패키지 · 메뉴(`kind`) · 가격 · 지점 · 병원 · 이벤트 비슷한 칸이 있나(표 이름 · 칸 · 행 수 · 표본 3줄 — 표본은 리포트에 코드 · 이름 정도만).
2-2 허브 응답(도구 9 · REST)에서 상품 · 메뉴가 어디로 나가나(어느 도구의 어느 칸).
2-3 앱 상담 리스트가 지금 무엇을 그리나(고민 · 계열 · 시술 · 숨기는 것 `list.hidden`) — 상품을 붙일 자리가 될 곳의 지도(파일:줄). 「시술」 의 키가 무엇인가(코드 체계).
2-4 앞 작업 · 프로필 레포 · 허브 레포에서 「명동」 · 「명동점」 · 「지점 상품」 · 「최저가」 · 「이벤트」 언급 전수(grep · 경로:줄). 메모: 사용자 메모리에 「통키 요금제를 명동점 데이터로 짜서 작업 취소」 사례가 있다 — 명동점 데이터가 어디 이미 있는지 찾되 **그걸로 꼴을 정하지 마라.** 있는 자리만 적는다.
2-5 받을 데이터 꼴을 정할 때 사용자에게 물어야 할 질문 목록(정할 것) — 추측한 꼴 제안 금지, 질문만.

### Q3. 시술 그림 응답
3-1 원천 `assets/procedure-images/` 실물: 파일 수 · 확장자 · 크기 합 · 매핑 csv · 검수 상태 칸 값 분포 · 외부 사진(MEC-070 등 라이선스).
3-2 silver/DB: `s_concept_image` · `s_concept_image_label` 칸 · 행 수(로컬 PG 실측) · gold 표에 그림 칸이 있나 · 코드 체계(mechanism/method → 시술 · 계열 연결 경로).
3-3 허브 코드: 그림을 읽는 곳 · `GOLD_IMAGE_DIR` 이 하는 일 · 정적 서빙 라우트가 이미 있나 · 도구 응답에 그림 칸이 있나(SPEC-001 0.8.2 · 코드 파일:줄 · stg 응답 실물로 확인).
3-4 stg 서빙 자리: 지금 stg 이미지(Dockerfile)에 `assets/` 가 들어가나 · 볼륨 마운트가 있나 · SPEC-003 §11 · ADR 0004 · stg-runbook 이 이 문제에 대해 정한 것 / 열어 둔 것. 「마운트 vs 이미지 포함」 선택지별 사실(크기 · 배포 절차 · 되돌리기)만 — 결정하지 마라.
3-5 앱 쪽: 상담 화면에 그림을 띄울 자리 후보(드로어 · 리스트 · 채팅) — 지금 코드 지도만.
3-6 SPEC 쪽 공백: 그림 출력에 대해 어떤 계약이 이미 있고(SPEC-007 · SPEC-001) 무엇이 「다음 작업」 으로 열려 있나(문서:줄).

### Q4. 묶음 · 순서에 영향 주는 사실
세 가지가 서로 같은 파일 · 같은 계약을 건드리는 자리(겹침) · 선후 의존(예: 그림 화면은 GUI 개선과 같은 템플릿) — 사실만. 추천은 「코디 참고」 한 절로 짧게.

### 리포트 꼴
`research-start.md` 머리에 **한눈 표**(세 가지 × 있음 / 없음 / 정할 것) → Q1 ~ Q4 → 「정할 것」 모음(번호 · 사용자 몫 / 코디 몫 구분) → 「확인 안 됨」 목록.

## 7. 범위 제약 — 하지 말 것

- 파일 생성 · 수정 0(리포트 1개 외). 커밋 · push 0.
- DB 는 SELECT 만 · stg 는 GET 만 · VM ssh 금지 · 18222 앱 프로세스 · 사용자 포트 건드리지 않기.
- 접속 값 · 키 · 토큰 출력 금지. 회사 데이터 본문(원장 글 · 답 문장)은 리포트에 길게 옮기지 마라(코드 · 이름 · 수 정도).
- 결정 · 설계 · 꼴 제안 금지 — 「정할 것」 으로 모은다. 명동점 상품 데이터 꼴은 추측 금지.
- 서브에이전트(Agent · Explore) 쓰지 마라 — 직접 읽어라.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · 테이블/컬럼 · API 응답 실물). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 리포트 뒤 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/상담봇 status --short` 로 리포트 1개 외 변경 0 확인.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_9bee503c-1efc-46de-8f5c-44f015f30a25 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
