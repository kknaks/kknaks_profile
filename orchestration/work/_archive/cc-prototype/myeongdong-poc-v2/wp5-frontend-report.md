# WORK-003 WP5 (front) 결과 보고

## 상태: done (커밋 · push · PR 안 함 — 워크트리 `procedure/front/` 에 변경만)

## 수행 — 파일 · 화면

`procedure/front/` 새로 만듦(allowed_paths 밖 수정 0).

| 파일 | 내용 |
|---|---|
| `package.json` · `package-lock.json` | cc front 의존성 버전 그대로 · 이름 `procedure-front` · dev/start 포트 3700 |
| `tailwind.config.ts` · `postcss.config.mjs` · `next.config.ts` · `tsconfig.json` · `eslint.config.mjs` · `global.d.ts` · `.gitignore` · `.dockerignore` | 그대로 복사(§2.4) |
| `Dockerfile` | 포트 3700 · 이름만 바꿔 복사(배포 WP 용) |
| `.env.example` | `NEXT_PUBLIC_API_BASE_URL=` 이름만 |
| `app/styles/ceramique-theme.css` · `app/globals.css` · `public/ceramique-logo-color.svg` | 그대로 |
| `app/styles/medikit-patches.css` | 그대로 + claude design `dda9a931` `medikit-patches.css` 에서 읽은 **`[Button-3]`(data-compact-buttons 26px) · `[Badge-1]`(data-badge-call 파랑 외곽선)** 블록 |
| `app/layout.tsx` | 스타일 import 순서 · `data-product="ceramique"` · 글꼴 |
| `app/page.tsx` · `app/(main)/procedures/page.tsx` | `/` · `/procedures` → `/procedures/live`(로그인 없으면 `/login`) |
| `app/login/page.tsx` | 아이디 · 비밀번호 · [로그인] — cc 로그인 틀(입력 · 버튼)만 |
| `app/(main)/layout.tsx` · `components/common/AppHeader.tsx` | 헤더 높이 57 · 메뉴 「시술 현황」 하나 · 시계 · 지점 · 「데스크」 · 로그아웃 |
| `app/(main)/procedures/live/page.tsx` | 사이드바 Menu · 제목 줄(동기화 · 조회 시간 밖 · 동기화 실패 · 범례 5 · 입실순/배치순) · 카드 격자 · 패널 · 토스트 · 팝오버 |
| `components/procedures/OrderCard.tsx` | 카드(§6.3) — 머리 · 고객 줄 · 수납 필요 · MemoCard · 마취 줄 · 선택 줄 · 시술 줄 · 큰 버튼 |
| `components/procedures/Aside.tsx` | 검색 + 탭 현황(6칸 필터 · 확인이 필요한 고객) · 호출(의국) · 고객 |
| `components/procedures/CallPopover.tsx` | 의사 호출 팝오버(§6.5) |
| `components/procedures/view.ts` | 문구 · 색 · 정렬 · 필터 칸 정의(표시만) |
| `lib/api.ts` | back 호출 한 곳 · Bearer · `{error}` 형식 · §7.1/§7.3 · SSE URL |
| `lib/hooks.ts` | `useNow` · `useWide` · `useSession` · `useBoardStream`(SSE) |
| `lib/session.ts` · `lib/time.ts` · `lib/types.ts` · `lib/memo.tsx` | 토큰 저장 · KST 표시 · 스냅샷 타입(back `schemas/board.py` 와 1:1) · MemoCard 복사 |

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 0 오류 |
| `npm run lint` | 0 문제 |
| `npm run build` | 성공 — 정적 5경로(`/` · `/login` · `/procedures` · `/procedures/live` · `/_not-found`) |
| `grep -rn "cc/" procedure/front --include=*.ts --include=*.tsx`(node_modules 제외) | **0** · 바깥 import 0(import 목록 = `@/…` · `./…` · react · next · medikit) |
| 브라우저(헤드리스 Chrome · Playwright) — back 가짜 스냅샷(`PROC_FAKE_BOARD=1`) | 시안 장면 8개 재현 — 아래 표 |
| 브라우저 2개(스테이션 · 의국) — 실 back(WP2 조작 API · 시험 DB 를 back `tests/helpers.py` 로 채움 · KOS 주소는 닿지 않는 곳) | §9 순서 축약 전부 통과 · 한쪽 조작이 다른 쪽에 새로고침 없이 보임 |
| SSE 재연결 — back 프로세스 재시작 | 다시 붙어 새 스냅샷(version 0 부터) 반영 · 로그인 유지 |
| 401 — 틀린 토큰 | SSE 닫힘 → `/api/auth/me` 401 → 세션 지움 → `/login` |

검증 때 띄운 것은 전부 내가 띄운 임시 포트(back 18700 · front 13700)이고 끝나고 정리했다. 사용자 포트(3600 · 3700 · 8600 · 8700)는 비어 있었고 건드리지 않았다.

### 장면 ↔ 스크린샷 (`orchestration/work/myeongdong-poc-v2/wp5-shots/`)

| 시안 scene | 스크린샷 | 확인한 것 |
|---|---|---|
| `board` | `01-board.png` | 흰 카드 · 확인 필요 빨간 테두리 · 배지(대기/진행/마취 중/확인 필요/귀가 대기) · 경과 글자 · 수납 필요 · KOS 반영 중/실패 · 호출함 외곽선 배지 · 상태 수 6칸 · 확인이 필요한 고객 3건(막대 · 기준) |
| `board-placement` | `02-board-placement.png` | 배치순(방 순서) · 귀가 대기 맨 뒤 |
| `memo-expanded` | `03a-memo-collapsed.png` · `03b-memo-expanded.png` | 가짜 메모가 120자 미만이라 SSE 를 가로채 긴 메모를 넣어 확인 — 3줄 접힘 · [펼치기/접기] |
| `call-modal` | `04-card-picked.png` · `05-call-modal.png` | 선택 줄 「2개 선택됨」(–) · 「의사 호출 · 2건」 · 팝오버(버튼 위로 · 모든 의사 + 원장 비어 있는 순 · 「의사를 선택하세요」 꺼짐) |
| `call-modal-specific` | `06-call-modal-specific.png` | 원장 하나 고름 · 선택됨 칸 · 「나 원장 호출」 |
| `all-done` | `08-all-done.png` · `e2e-03-all-done.png` | 다 끝나면 큰 버튼이 [귀가 대기] |
| `panel-doctors` | `09-panel-doctors.png` · `e2e-02` · `e2e-04` · `e2e-06` | 호출 1건 = 카드 1장 · 전체/지정 배지 · 호출 N분(5분↑ 빨강) · 담당의 선택 → [<원장> 수락] · 지정 → [다른 원장에게] · [수락] · 최근 수락(되돌리기 없음) |
| `panel-customers` | `10-panel-customers.png` | 고객 줄 · 번호 원 시술 줄 · 누르면 그 카드만 남기고 흐림 |
| (필터) | `11-filter-need.png` | 「확인」 칸 → 카드 필터 · 파랑 2px |

E2E 순서(실 back): [마취 시작] → 2건 체크 · 모든 의사 호출 → 의국 탭 「수락 대기 1건」 → 가 원장 수락(시작 가능 · 최근 수락 1줄) → [시작] → [종료] → 담당의 있는 고객 시작 · 종료 2회 → [귀가 대기](흐림 · 맨 뒤) → 나 원장 지정 호출 → [다른 원장에게](전체 호출 새 줄) → 다 원장 수락. 토스트 문구 = 시안(「A-룸1 2개 시술 · 전체 호출」 · 「… · 나 원장 호출」 · 「A-룸1 마취 시작」 · 「A-룸2 고객2 귀가 대기」).

## 계약 대조 — SPEC 항목별

| SPEC | 같음/다름 | 메모 |
|---|---|---|
| §2.4 테마 복사 | 같음 | patches 2블록 추가 · cc import 0 |
| §6.1 경로 | 같음 | |
| §6.2 헤더 · 사이드바 · 제목 줄 | 같음 | 「조회 시간 밖」 · 「동기화 실패」(기본값 자리 = 동기화 문구 옆) |
| §6.3 카드 | 같음 | KOS 반영 중/실패 = 경과 글자 아래 오른쪽 작은 글자(실패 빨강 · 마우스 올리면 op · 오류) · 수납 필요 = 고객 줄 끝 Badge warning sm |
| §6.4 패널 3탭 | 같음 | 칸 수 = 스냅샷 `counts` · 필터 = §6.4 칸 정의 그대로(need · state · runningSince · calls) |
| §6.5 팝오버 | 같음 | |
| §6.6 갱신 | 같음 | SSE 하나 · 폴링 없음 · `useNow` 1초 + 스냅샷 `now` 와의 차이 보정 |
| §6.7 시안≠DEC | 같음 | 마취 버튼 대기 · 진행 모두(스냅샷 `canStart/canEnd`) · 수락 = 호출 1건 · 되돌리기 없음 · 호출함 배지 못 누름 · 메뉴 하나 · 카드에 [시작]/[종료] |
| §5.11 버튼 | 같음 | 켜짐은 전부 스냅샷 값(`pickable` · `canStart` · `canFinish` · `canCall` · `canHome` · `anesthesia.canStart/canEnd`). front 는 「보임」만 판단(귀가 대기 카드 · state) |
| §7.1 ~ §7.3 | 같음 | 401 → `/login` · 409 등은 토스트에 back `message` |
| §7.5 SSE | 같음 | `?token=` · `board` 하나 · 통째 교체 · version ≤ 버림 · 재연결 때 version 새로(back 재시작 대비) |

## 이슈 · 코디가 확인할 것

1. **스냅샷에 없는 값 1개를 front 상수로 둠** — 호출 탭 「호출 N분」 빨강 · 「기준 5분 / 기준 도달 / +N분 초과」의 기준 5분(`CALL_LIMIT_MIN`, SPEC §5.8 · §6.4 D-20). 카드 쪽 확인 필요는 스냅샷 `need.limitMin` 을 쓴다. `calls[]` 에 `limitMin` 이 있으면 그걸로 바꾸면 된다.
2. **compose front 서비스**(backend 몫 파일) — `procedure/docker-compose.yml` 의 front 블록이 주석이다. 열 때 `NEXT_PUBLIC_*` 는 **빌드 때** 들어가므로 `environment:` 가 아니라 `build: { context: ./front, args: { NEXT_PUBLIC_API_BASE_URL: http://localhost:8700 } }` 로 넘겨야 한다(Dockerfile 의 ARG 기본값은 cc 배포 주소 그대로).
3. **폭 760px 미만** — 사이드바 · 오른쪽 패널을 숨기고 카드만 보인다. 시안 · SPEC 에 폰 화면이 없다(D-34 2단계).
4. `procedure/.env` 에 실 데모 KOS 값이 이미 있다 — 처음 back 을 띄웠을 때 내 실행이 그 값을 읽어 **조회만** 1회(토큰 2종 · 직원 · 방) 했다. 바로 끄고 그 뒤는 KOS 주소를 닿지 않는 곳으로 덮어 실행했다(쓰기 0).
5. 국적 칩은 KOS 값(`nationality`)을 그대로 보인다(가짜 스냅샷은 `JP` 같은 코드). 시안은 「대만」처럼 한글 — 코드 → 이름 대응은 정한 데가 없어 하지 않았다.
