
# [frontend] WORK-004 프론트 3페이지 — 셸·모니터링·데이터·채팅 (P1~P4)

너는 **ontology-demo `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/ontology-demo/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation`
브랜치: `kknaksss/work-001-data-foundation` (이미 체크아웃돼 있다 — **이동·리베이스 금지**) → 코드 PR 은 전 WP 완료 후 코디가 한 번에.

⚠ **이 워크트리는 BE 워커와 공유다.** BE 는 `app/ontology-agent/` 에서 작업한다(WORK-001 미커밋 산출물 존재, 이후 WORK-002·003 병행). 너는 **`app/front/` 만** 만진다 — 그 밖을 건드리면 FAIL. git 조작(add·commit·stash 포함) 금지 — BE 산출물이 섞인다.

## 1. SSOT — 먼저 읽을 것 (전부 read-only 절대경로)

- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/30-work/work-004-frontend-three-screens.md` ← 이번 작업의 SoT (P1~P4·완료 증거)
- 같은 폴더의 `../20-spec/spec-004-three-screens.md` (**v0.1.0 ready** — 화면 계약: U-1~U-15·S-1~S-7·AC 23·파생 카운트 표·§7.3 예문 소재) · `spec-003-api-and-chat-contract.md` (API·폴링·게이트) · `spec-001-data-layer-contract.md` (enum·마스킹 표기·node_id 25종+좌표) · `spec-005-agent-loop-and-gates.md` (답변 객체 — used_edges·citations·drilldown·followups)
- **디자인 패키지**: `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/design/` — `01`~`08` 문서와 `data/*.json` 이 시각·값의 SoT. 프로토타입은 **Chat.dc.html 만 최신** — 나머지 4종은 옛 데이터라 문서·JSON 이 이긴다. `reference/ontology_demo/` 의 design 밖은 열지 마라(PII).

**기대는 개념** — 해당 없음 (계약·디자인이 충분히 구체적이다).

## 2. 배경

BE 는 WORK-001(DB)까지 완료, WORK-002(API)는 이제 시작이라 **실 API 가 아직 없다.**
mock 선행으로 P1~P4 를 전부 완성하고, 실연결은 스위치 한 번으로 되게 만든다.

## 3. 계약

- **mock 전략**: SPEC-003 응답 shape **그대로**의 픽스처를 `app/front` 데모 전용 lib 에 두고,
  값은 디자인 `data/*.json`(정본 재키잉 완료)에서 가져온다. API 호출은 전부 데모 전용
  클라이언트 한 곳을 경유 — env(예: `NEXT_PUBLIC_ONTOLOGY_API_BASE`) 유무로 mock/실 API 를
  전환한다. 흩어진 fetch 금지.
- 라우트: `app/front/app/(ontology)/ontology/{monitoring,chat,data}` — 기본 진입 monitoring.
  기존 포트폴리오 파일·`globals.css` 수정 금지(역할 rules).
- 접속 게이트: SPEC-003 U-1 — 비밀번호 1칸, mock 모드에선 아무 값 통과로 두되 검증 로직은
  실 API 스위치에 물려 둔다.
- edge_id `<from>__<to>` · 마스킹 표기 · 파생 카운트(하드코딩 = FAIL) 전부 spec 그대로.

## 4. 먼저 읽을 핵심 파일

- `app/front/app/globals.css` — 전역 토큰(읽기만) · `app/front/app/layout.tsx` — 셸 분리 대상 확인
- `app/front/app/chat/page.tsx` — 기존 `?q=` 패턴 · `app/front/lib/` — API 클라이언트 컨벤션

## 5. allowed_paths — `app/front/` (그 안에서도 기존 파일 수정 금지 — 라우트 그룹·전용 파일 신설만. 예외 필요하면 질문)

## 6. 구현 단계 — P1→P4, phase 마다 [진행] 보고

1. **P1** 셸 — `(ontology)` 라우트 그룹 레이아웃(`--ont-*` 토큰 스코프·`color-scheme:light`·Pretendard next/font·전역 헤더), 접속 게이트 화면, 최소 폭 안내 (U-1~3)
2. **P2** 모니터링 — KPI 카드(파생 카운트·스파크)·원인 분석 그래프(정적 SVG, 25노드 좌표·판정별 엣지·범례)·인스펙터·예보 카드 (U-4~7)
3. **P3** 데이터 — 계층 탭(브론즈16·실버6·골드5 파생)·nexus 2단 칩·표·마스킹 표시·컬럼 상세·계층 역추적 (U-13~15)
4. **P4** 채팅 — 빈 상태 카드·메시지 상태 5종(2초 폴링)·답변 6블록(칩·citations·drilldown·followups)·`?edge=` 점프·컴포저(1,000자) (U-8~12)

## 7. 하지 말 것

- `app/front/` 밖 수정 금지 · 기존 포트폴리오 파일·globals.css 수정 금지 · git 조작 금지
- 시안 숫자 하드코딩 금지(SPEC-004 파생 표) · 미니그래프 금지 · 스트리밍 금지 · PII 원값 금지
- spec 에 없는 API 필드를 전제하지 마라 — 비면 질문 채널로

## 8. 검증

```
cd app/front && npx tsc --noEmit && npm run build (1회 — 통과하면 반복하지 마라). 시각 확인은 dev 서버 기동 후 라우트 3종 렌더 확인
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 아래가 다르면 preamble 이 맞다.

- **커밋·push·PR·git 조작 금지.** 워크트리에 변경만 남긴다.
- phase 완료마다: `orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[진행] FE P<n> 완료 — <요약>" --enter`
- 전체 완료 시 **아래 두 명령 모두**:

```bash
orca orchestration send \
  --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done \
  --task-id <taskId — preamble> --dispatch-id <dispatchId — preamble> \
  --subject "frontend 완료: WORK-004 3페이지" \
  --body "변경 파일 / phase 별 요약 / tsc·build 수치 / 계약 준수(파생·마스킹·토큰 스코프) / 미결"

orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] frontend 완료 — WORK-004 P1~P4. 상세는 인박스." --enter

# 막히면: orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --text "[질문] frontend: <질문>" --enter
```
