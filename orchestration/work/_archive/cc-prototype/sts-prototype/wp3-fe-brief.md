# [frontend] WORK-001 WP3 — cc/front 뼈대 · 로그인 · 데스크 현황판 · 직원 첫 화면 · 환자 상세

너는 **cc-prototype `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` (브랜치 `kknaksss/sts-prototype`)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리의 `cc/back/` 에서 병렬 작업 중 — `cc/back/` 는 건드리지 마라.** back 이 아직 없을 수 있다 — 계약(SPEC §5)대로 짜고, 확인은 계약 모양의 목업으로.
너는 앞 맥락이 없다. 맥락은 아래 파일에만 있다.

## 1. SSOT — 먼저 읽을 것

- **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`** ← 계약의 SoT. 이번 판은 §1 · §2 · §5 · §6 · §8. **§2 「시안과 다른 점」이 시안보다 우선**(데스크 [초기화] 추가 · 의사 일정 「예정」 없음 · 비밀번호 미검증)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/30-work/work-001-cc-poc.md` — WP3 행
- **시안(화면의 정본)** — claude.ai/design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23` 에서 **DesignSync 로 받아라**: `Ceramique 현황판 v3` · `Ceramique 직원 - 로그인` · `Ceramique 직원 - 의사` · `Ceramique 직원 - 코디` (· `- 통역 모달 상태` 는 WP4 — 받아만 두어도 된다)
  - 로컬 사본(현황판 v3 · 의사 모바일만): 워크트리 `cc/design/` — `README.md` 먼저(medikit · 테마 · 패치 CSS)
  - 직원 시안이 무엇을 담는지: `orchestration/work/sts-prototype/` 의 `design-staff-report.md` · `design-staff-r2-report.md` · `design-staff-r3-report.md` (프로필 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/` 아래)
- 결정: `.../10-decision/decision-002-cc-poc.md`

**기대는 개념** — 해당 없음.

## 2. 배경

2026-10-16 지점 시연용 PoC. `cc/front` 는 아직 `.gitkeep` 뿐이다. 이번 판(WP3)은 통역 모달을 **뺀** 화면 전부. 통역 모달(SPEC §7)은 WP4 — 환자 상세의 [통역] 버튼은 자리만 두고 누르면 아무것도 안 해도 된다.

## 3. 계약 — backend 워커가 이대로 제공한다

SPEC-001 §5.2 · §5.3 · §5.5 · §6 의 경로 · 필드 그대로. JSON camelCase · 오류 `{ error: { code, message } }`.
- 데이터는 전부 back 에서. 시안 안의 샘플 배열(`C0` · `ST0` · `RESV` · `PATIENTS` 등)을 화면에 남기지 마라
- 화면 갱신: `GET /api/events`(SSE) 의 `state` 이벤트 → 그 화면의 GET 을 다시 부른다
- 조작은 §5.3 POST 만. 시안의 `commit` 계산을 front 에서 다시 하지 마라 — 결과는 back 응답이 정본
- 계약 모양이 이상하면 바꾸지 말고 `[질문]`

## 4. 먼저 읽을 핵심 파일

- `cc/design/Ceramique 현황판 v3.dc.html` — 마크업 · 클래스 · `renderVals` 가 화면에 내는 값

## 5. allowed_paths — 이 밖은 건드리지 마라

- `cc/front/` 전부 (`.env.example` · `.gitignore` 포함)
- `cc/back/` · `cc/design/` · 레포 루트 금지

## 6. 구현 단계

1. `cc/front` 뼈대 — Next.js(App Router) · TypeScript strict · `@medisolve-ai/medikit@1.4.0` · `pretendard` · `data-product="ceramique"` + `ceramique-theme.css` + `medikit-patches.css` · 포트 3600 · `NEXT_PUBLIC_API_BASE_URL`(기본 `http://localhost:8600`) · `lib/api.ts` 한 곳에서만 fetch · SSE 훅
2. `/login` — 시안대로. 계정 목록 `GET /api/staff`, 시연 카드 3장, 로그인 → `localStorage` · 역할별 이동(§6)
3. `/desk` — 현황판 v3 시안 그대로(도면 · 진행 목록 · 직원/고객/예약 탭 · 방 패널 · 접수 모달 · 토스트 되돌리기) + 헤더 [초기화](§5.4)
4. `/staff` — 의사: 지금 진행 중 + 오늘 내 일정(완료 · 진행 중 · 다음, **예정 없음**) / 코디: 지금 내원 환자 목록
5. `/staff/patient/[scheduleId]` — 환자 상세(§5.5 순서 · 역할별 기본 펼침 · 메모 접어도 폭 그대로) · 의사 [진료 시작]/[진료 완료] → §5.3
6. `cc/front/README.md` — 설치 · 실행

## 7. 범위 제약 — 하지 말 것

- 통역 모달 · 마이크 · WS 는 WP4 — 만들지 마라
- 시안에 없는 화면 · 장식 추가 금지(§2 표의 추가 1건 빼고). 시안이 애매하면 리포트에 적고 시안 쪽으로
- dev 서버로 확인하려면 **3600 이 아닌 임시 포트**로, 끝나면 그 프로세스만 끈다. 사용자 포트 · 프로세스를 건드리지 마라
- 커밋 · push · PR 금지

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- **이번 WP 항목만**(통합 시험은 WP5). 위 세 명령 + 화면별 시안 대조표(화면 · 같음/다름)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp3-fe-report.md` (rules.md 형식)
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_1bd4c892-2253-4670-9a5f-c6412cf15a9d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
