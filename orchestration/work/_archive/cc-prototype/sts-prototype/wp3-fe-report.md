# WORK-001 WP3 결과 보고 (frontend)

## 상태: done

`cc/front` 를 새로 세웠다 — 로그인 · 데스크 현황판 · 직원 첫 화면(의사/코디) · 환자 상세. 통역 모달(WP4)은 없다([통역] 버튼은 자리만).
커밋 · push · PR 은 하지 않았다. 워크트리 `cc/front/` 에만 변경이 있다(`cc/back` · `cc/design` · 루트는 건드리지 않음).

## 수행 — 파일 · 화면 목록

| 파일 | 내용 |
|---|---|
| `package.json` · `package-lock.json` | Next 16(App Router) · React 19 · TS strict · `@medisolve-ai/medikit` **1.4.0 고정** · `pretendard` 1.3.9 고정 · Tailwind 3(medikit preset 이 v3 요구) · 포트 3600(`dev`/`start`) |
| `tsconfig.json` · `next.config.ts` · `tailwind.config.ts` · `postcss.config.mjs` · `eslint.config.mjs` · `global.d.ts` | 설정. `next.config` 에 `agentRules: false`(next dev 가 AGENTS.md 를 만들지 않게) |
| `.env.example` · `.gitignore` | `NEXT_PUBLIC_API_BASE_URL=http://localhost:8600` / `.next` · `node_modules` · `.env*` 제외 |
| `app/layout.tsx` · `globals.css` · `styles/ceramique-theme.css` · `styles/medikit-patches.css` · `public/ceramique-logo-color.svg` | 루트 `<html data-product="ceramique">` · medikit styles · 테마 · 패치 CSS(`cc/design` 에서 **복사** — 기능 폴더 밖 import 없음) |
| `lib/types.ts` | 응답 모양 — 코디 결정으로 **WP1↔WP3 계약**이 됨(`wp1-wp3-contract-addendum.md`). `since` = epoch ms |
| `lib/api.ts` | back 호출 전부(fetch 는 여기만) · SSE 구독(화면 안 구독자는 EventSource 하나 공유, 재연결 `open` 때 다시 읽기) |
| `lib/hooks.ts` · `session.ts` · `time.ts` · `board.ts` | `useLive`(GET + SSE `state` 마다 다시 GET) · `useSession`(localStorage, 없으면 `/login`) · 경과 포맷 · 현황판 시안의 **읽기 계산**(LAYOUT · capOf · statusOf · waitLabel · stepView · buildOrder) |
| `app/page.tsx` | `/` → 세션 역할에 따라 `/desk` · `/staff`, 없으면 `/login` |
| `app/login/page.tsx` | 로그인 |
| `app/desk/page.tsx` + `components/desk/*` | 현황판(FloorGrid · Aside 탭 4개 · RoomPanel · CheckInModal · 토스트 되돌리기 · [초기화]) |
| `app/staff/layout.tsx` · `page.tsx` · `patient/[scheduleId]/page.tsx` + `components/staff/*` | 직원 틀(StaffShell) · 의사/코디 목록 · 환자 상세(PatientView) |
| `README.md` | 설치 · 실행 |

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과(오류 0) |
| `npm run lint` (eslint 9 + eslint-config-next 16) | 통과(오류 0 · 경고 0) |
| `npm run build` | 통과 — `/` · `/login` · `/desk` · `/staff` 정적, `/staff/patient/[scheduleId]` 동적 |
| 기능 폴더 밖 import | 없음(`../../..` 상대 import 0 · `cc/design` 파일은 복사본 사용) |
| 컴포넌트 직접 fetch | 없음(`fetch(` 는 `lib/api.ts` 만) |
| 화면 눈 확인 | back 이 아직 없어 **계약 모양 목업 서버**(스크래치패드, 임시 포트 18611)와 `next dev`(임시 포트 13611)로 띄워 headless 크롬으로 10장 캡처 — 로그인 · 데스크 · 방 패널 · 배정 후 토스트 · 직원 탭 경로 화살표 · 접수 모달 · 의사 넓은 폭 · 의사 폰 목록/상세 · 코디 폰. 콘솔 오류 0. 확인 뒤 두 프로세스만 종료(3600 · 8600 · 사용자 프로세스 무관) |
| 실제 back 과 통합 | **pending** — WP5(통합 시험) 몫. back 응답이 `lib/types.ts` 와 다르면 그때 드러난다 |

## 계약 대조 — SPEC 항목별

| SPEC | 항목 | 결과 |
|---|---|---|
| §2 `/login` | 시안 그대로 · 비밀번호 미검증 | 같음 — 비번 칸은 그려지고 비어 있으면 시안의 오류 문구, 값은 서버로 보내지 않음 |
| §2 `/desk` | 현황판 v3 + 헤더 [초기화] | 같음 — [초기화]는 제목 줄 오른쪽 끝, medikit `Button` outlined/gray/sm(「진행 목록」과 같은 모양) · 확인 1회 → `POST /api/admin/reset` |
| §2 `/staff` | 의사 「오늘 내 일정」에 예정 없음 | 같음 — `done[] + current + next` 만, 배지 완료/진행 중/다음 |
| §2 `/staff/patient/[scheduleId]` | 환자 상세 | 같음 — 폭 ≥760 이면 목록 + 상세 두 칸(시안 `wide`), 좁으면 상세만 + 「‹ 오늘 내 일정/지금 내원 환자」 |
| §2 디자인 시스템 | medikit 1.4.0 · ceramique · 패치 CSS | 같음 |
| §5.2 `GET /api/board` | 화면 원재료 | 같음 — 배지 · 색 · 진행 목록은 front 계산. `rooms` 가 오면 방 이름은 그 값, 없으면 시안 LAYOUT |
| §5.2 `GET /api/staff/{id}/home` | 의사 current/next/done · 코디 목록+요약 | 같음 — 모양은 `types.ts`(`'patients' in home` 이면 코디 화면) |
| §5.2 `GET /api/patients/{id}` | §5.5 | 같음 — 칸 순서 상단 카드 → 환자 메모(①②③④) → 환자 차트(접힘) → 시술 이력 → 오늘 고객 동선 |
| §5.2 `GET /api/events` | SSE → 그 화면의 GET 다시 | 같음 — 데스크는 board, 직원은 home + 열린 환자 상세 |
| §5.3 조작 | assign · complete · remove-staff · place · check-in · undo · start · finish | 같음 — front 는 결과를 계산하지 않고 응답 뒤 다시 읽음. 토스트 「되돌리기」는 그 조작 응답의 `version` 으로 `undo` |
| §5.4 | 초기화 버튼 | 같음 |
| §5.5 기본 펼침 | 의사 ②③ · 코디 ④ · ① 항상 | 같음 — ② 접힘 때 마취 한 줄 보임 · 메모 접어도 폭 그대로(`width:100%`) |
| §5.5 | 값 없는 차트 줄 숨김 · 아웃 시각 없으면 숨김 · 원장 없으면 줄에서 뺌 | 같음(값은 back 이 계산) |
| §6 | `POST /api/login {staffId}` → localStorage · 역할별 이동 · 미로그인 → `/login` | 같음 — `home` 이 `/` 로 시작하면 그 경로, 아니면 역할(데스크 → `/desk`, 그 밖 → `/staff`) |
| §6 | 시연 카드 3장(데스크 · 권태윤 · 곽태린) | 같음 — `GET /api/staff` 에서 이름으로 찾음(없으면 그 역할의 첫 계정) |
| 데이터 | 시안 샘플 배열 미사용 | 같음 — C0 · ST0 · RESV · PROFILE · PATIENTS 없음. 남긴 상수는 도면(LAYOUT) · 상태 이름/색 · 국적 이름뿐 |

### 화면별 시안 대조

| 화면 | 같음 | 다름(이유) |
|---|---|---|
| 로그인 | 레이아웃 · 문구 · 시연 카드 · 오류 문구 | 시안의 「○○ 계정 → ○○ 화면으로 이동」 토스트 대신 **실제로 이동**(§6). 토스트는 로그인 실패 알림으로만 씀. Enter 로도 로그인 |
| 데스크 — 도면 · 범례 · 진행 목록 탭 4개 · 방 패널(점유/넣기/라운지) · 접수 모달 · 토스트 | 마크업 · 클래스 · 문구 · 좁은 폭(<1280) 서랍 | ① [초기화] 추가(§2) ② 직원/고객 탭 처음 열 때 고르는 사람: 시안은 샘플 이름(정해린 · 노예진) 고정 → **큐가 있는 첫 직원 · 방에 있는 첫 고객** ③ 예약 탭 지연/임박 기준: 시안 `DEMO_NOW`(10:55) → **지금 시각** ④ 예약 상태 `canceled`(SPEC 에만 있음) → 「취소」 회색, 정렬은 노쇼 뒤 ⑤ 조작이 실패하면 같은 토스트 자리에 오류 문구(되돌리기 버튼 없이) ⑥ 헤더 로그아웃 → 세션 지우고 `/login`(시안은 빈 함수) |
| 데스크 — 방 패널/접수 모달의 고객 줄 정보 | 「성별 · 나이 · …」 · 주의 · 시술권 | 시안 `#C-20418`(차트번호) 자리에 **첫 방문/재방문** — 차트번호는 응답에 없음(§4.1). 정보는 환자 상세 API 에서 가져옴 |
| 접수 모달 기본 선택 | 시술권 있으면 첫 시술권 선택 · 없으면 상담 필요 | 시안 `pre` 는 샘플별 값 → 「잔여 있는 첫 시술권」으로 일반화 |
| 현장 접수 | 「현장 고객 N」 · 예약 없음 | N = 예약 목록 중 시술 「현장 접수」 수 + 1. 요청 `{scheduleId:null, name, order}`(계약 보충) |
| 의사 첫 화면 | 지금 진행 중 카드 · 오늘 내 일정 · n / m 완료 | 「예정」 없음(§2). 헤더 이름은 로그인한 사람 |
| 코디 첫 화면 | 「n명 · 외국인 n명」 · 대기/상담/시술 요약 · 경과 긴 순 · 국적 칩 | — |
| 환자 상세 | 상단 카드 · 아웃 칩 · 버튼 · ⚠ 주의 · 메모 접기 · 차트 · 시술 이력 · 동선(취소 회색 · 담당자 메모) | [통역] 은 누르면 아무것도 안 함(WP4). [진료 시작/완료] 는 `start`/`finish` 호출 뒤 다시 읽음 |

## 이슈 · 코디가 확인할 것

1. **응답 모양은 `cc/front/lib/types.ts` 가 계약**(코디 결정). back 이 다르게 내면 화면이 비거나 깨진다 — WP5 전에 back 리포트와 대조 필요. 특히 `GET /api/staff/{id}/home` 의 의사/코디 구분은 응답에 `patients` 가 있느냐로 한다.
2. **환자 상세 `history[]`** 는 「이 병원」 줄까지 back 이 넣는 것으로 했다(front 는 받은 줄을 그대로 그림). 「타 병원 · 상담 메모에 이력 없음」 같은 빈 줄도 back 몫.
3. **방 이름**: 직원 화면의 `room` 은 칸 id 로 받아 front 가 LAYOUT 이름으로 바꾼다. 동선(`route[].room`)은 back 이 이름으로 준다(대응표 적용 뒤).
4. 시안 렌더러에서 쓰던 `style-hover`(방 칸 · 빈 관리실 버튼 그림자/테두리)는 CSS 클래스 `cc-room` · `cc-free-room` 으로 옮겼다.
5. 직원 화면에는 시안대로 **로그아웃이 없다** — 계정을 바꾸려면 `/login` 으로 직접 가야 한다(로그인 화면은 세션이 있어도 열린다).
6. 접수 모달 정보(나이 · 주의 · 시술권)는 모달을 열 때 환자 상세 API 를 한 번 부른다 — 응답 전 잠깐 「보유 시술권이 없어요 · 상담 필요」로 보였다가 바뀔 수 있다(로컬이라 체감 거의 없음). [초기화] 하면 그 캐시를 비운다.
