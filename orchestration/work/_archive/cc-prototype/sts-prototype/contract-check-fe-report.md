# WP3·WP4 ↔ 실제 back 계약 대조 결과 (frontend)

## 상태: done

목업 대신 **실제 `cc/back`**(임시 포트 18621) + front dev(임시 포트 13621)로 대조했다. 응답 모양은 `lib/types.ts` 와 **필드 단위로 모두 맞았다**(빠진 필드 0 · 타입 다름 0). 실데이터에서 드러난 표시 문제 5건은 front 에서 고쳤다. **back 수정 필요는 없음**(아래에 동작 관찰 2건만 참고로 적음).

- 환경: `CC_DB_PATH=data/contract-check/cc.db`(시드도 같은 폴더 `seed.json` — back 이 DB 폴더에 시드를 둔다). `seed build --date 2026-10-09 --at 14:45` → 일정 27 · 지금 내원 5 · 귀가 6 · 직원 17 · 완료 기록 30
- 사용자 E2E 파일 무손상: `data/seed.json` · `data/cc.db` shasum 이 작업 전후 같다(b012dad5… · 50f2499f…). 대조용 폴더 `data/contract-check/` 는 끝나고 지웠다
- 끝나고 임시 프로세스 3개(uvicorn 18621 · next dev 13621 · SSE curl)만 종료. 3600 · 8600 · 사용자 프로세스는 건드리지 않았다. `cc/back/` 파일은 읽기만 했다. 커밋 없음

## 엔드포인트별 대조

검사는 스크립트로 했다: 응답마다 `types.ts` 의 필드 이름 · 타입을 대조. 환자 상세는 27명 전부, 그중 ⚠ 주의가 있는 고객 12명 포함.

| 엔드포인트 | 결과 | 비고 |
|---|---|---|
| `GET /api/staff` | 같음 | 15계정(데스크 `desk` + 의사 4 + 코디 10). 시연 카드 3장(데스크 · 권태윤 · 곽태린)이 이름으로 잡힘 |
| `POST /api/login` | 같음 | 역할별 이동(데스크 → `/desk`, 의사 · 코디 → `/staff`) 확인 |
| `GET /api/board` | 같음 + 남는 필드 | `now`(서버 시각, 로컬과 차이 0ms) · `corridors` · `rooms[].{col,row,cs,cap,kosRooms}` · `customers[].nationality` — front 는 무시(무해). `resv[].st` 실값 booked · checked · canceled(canceled 표시는 WP3 에서 이미 처리) |
| `GET /api/staff/{권태윤}/home` | 같음 | 시드 시각에는 `current` · `next` 가 null, `done` 2건(label 「귀가」, room · state · since null). 배정 뒤 `current` 가 채워짐 |
| `GET /api/staff/{곽태린}/home` | 같음 | `patients` 5 · `summary {wait 1, consult 2, treat 2}` |
| `GET /api/patients/{id}` | 같음 | 27명 모두 빠진 필드 없음. `history` 는 27명 모두 「이 병원」 + 「타 병원」 두 줄(계약대로 back 이 채움). `order` 가 null 인 고객 3명 — front 는 칸을 숨김. 시술권 있는 고객 1명(4종) |
| `GET /api/events` (SSE) | 같음 | 변경마다 `event: state` `data: {"version": n}` 1~11 연속 |
| `assign` → 의사 home | 같음 | 데스크 화면에서 권태윤을 관리실 07 에 배정 → 의사 화면에 그 고객이 뜨기까지 **476~483ms**(SSE) |
| `start` / `finish` | 같음 | start → 그 방이 큐 앞으로(`['c07','c02']`), 의사 화면 「진행 중」. finish → 큐에서 빠지고 고객 다음 단계로, 「완료」 |
| `undo {version}` | 같음 | finish 직전으로 돌아감(라벨 · since 원복) |
| `check-in` 현장 접수 `{scheduleId:null,name,order}` | 같음 | back 이 `walkin-1` 을 만들어 고객 · 예약(`procedure: 현장 접수`, `st: checked`)에 넣음. 환자 상세도 응답함(국적 빈 값 · 시술권 []) |
| `check-in` 예약 · `place` · `remove-staff` · `complete` | 같음 | 모두 `{version}` |
| 오류 모양 | 같음 | 없는 직원 배정 → 404 `{"error":{"code":"staff_not_found","message":"…"}}` — front 토스트에 message 가 그대로 뜸 |
| `reset` | 같음 | 시드 상태로(현장 접수 고객 사라짐 · 고객 11) + SSE |

## front 에서 고친 것 (실데이터에서 드러남)

| # | 증상 | 고친 곳 |
|---|---|---|
| 1 | **[진료 시작] 뒤 다른 환자로 화면이 넘어감** — 넓은 화면 `/staff`(경로에 환자 없음)에서는 상세가 기본 선택(「다음」)을 따르는데, start 로 큐가 바뀌면 「다음」이 다른 환자가 되어 방금 시작한 환자 대신 새 「다음」 환자가 보였다(back 은 정상). [진료 완료] 버튼을 못 누르는 상태가 됨 | `PatientView` 가 진료 시작/완료 때 그 환자를 경로(`/staff/patient/<id>`)에 고정(`StaffShell` 의 `onPin`). 시안 `advance()` 가 방금 진행한 환자를 선택해 두는 것과 같은 동작 |
| 2 | 현황판 도면 칸에서 **긴 로마자 이름**(FENG FANG YING · WEI YING YUN)이 칸 밖으로 나가고 점이 따로 줄바꿈 | `FloorGrid` 사람 이름에 줄임표(전체 이름은 title) — 시안 샘플은 짧은 한글 이름이라 드러나지 않던 것 |
| 3 | 시술권 만료일이 빈 값(`expires: ""`) → 접수 모달에 「잔여 1/1회 · ~」 | 만료일이 있을 때만 「· ~만료일」 |
| 4 | 동선 첫 줄(상담)의 `room: ""` → 「 · 상담」 | 방이 없으면 작업 이름만 |
| 5 | `order.anesthesia` 가 「(마취크림)」처럼 괄호째 와서 접힘 줄이 「마취 · (마취크림)」 | 바깥 괄호를 떼고 「마취 · 마취크림」(시안과 같게) |
| 6 | 현장 접수 고객의 `nationality: ""` → 빈 국적 칩 · 외국인 수에 포함 | `isForeign`(국적 있고 KR 아님)으로 칩 · 외국인 수 · 코디 기본 선택을 판단. [통역] 은 KR 만 숨기므로 국적 모르는 현장 고객에게는 보임(기본 언어 en). 통역 모달 머리 줄에서도 빈 국적은 뺌 |

## 화면 캡처 확인 (headless 크롬 · 실데이터)

| 화면 | 결과 |
|---|---|
| `/login` → 데스크 카드 → `/desk` | 이동 정상 |
| `/desk` 도면 · 진행 목록(현황) | 고객 5 · 대기 1 / 상담 2 / 시술 2 · 데스크 칸에 대기 직원 · 경과 타이머 — 깨짐 없음(2번 수정 뒤) |
| 방 패널(관리실 09) | 고객 줄 정보(여 · 48세 · 첫 방문) · 단계 4개 · 방에 있는 직원 2(원장 · 코디) · 배정 목록 |
| 예약 탭 | 예정 15 · 접수 11 · 노쇼 0 · 「n분 지연」 표시 |
| 의사 넓은 화면(권태윤) | 일정 완료 2 → 배정 뒤 진행 중 · 다음 · 「지금 진행 중」 카드 · 환자 상세 전체(메모 · 차트 · 시술 이력 · 동선 9단계) |
| 의사 [진료 시작] → [진료 완료] | 진행 중 → 완료(「완료한 환자」 · 동선 4/5) · 데스크 도면이 SSE 로 따라 바뀜 |
| 코디 폰(곽태린) | 지금 내원 5명 · 외국인 4명 · 국적 칩 · 경과 긴 순 |
| 코디 환자 상세(⚠ 주의 있는 KR 고객) | ① 고객 메모 「*영주권*」 맨 위 + 「특이사항 — 조원장님 지인」(오더 · 상담 사본) · ④ 접수 메모 펼침(코디 기본) · ② 접힘 줄 「마취 · 마취크림」 · 취소 작업 회색 · [통역] 없음(KR) |
| 콘솔 오류 | 0 |

## back 수정 필요

**없음.** 아래는 계약 위반이 아니라 동작 관찰 — 코디 판단용.

1. **start 뒤 현황판 상태가 늘 「상담」은 아니다** — SPEC §5.3 은 [진료 시작] → 「상담(원장 진료)」인데, back 은 시안 `statusOf` 그대로(고객의 현재 단계가 원장 진료면 상담, 시술 단계면 시술)라서, 이미 시술 단계에 있는 고객(예: FENG FANG YING · 울쎄라피)은 「시술」로 보인다. 원장 진료 단계 고객(LUO JIA)은 「상담 · 원장 진료」로 맞게 보였다. §9-2 시연은 원장 진료 단계 고객으로 하면 문서대로 보인다.
2. **finish 뒤 「마무리 대기」가 아닐 수 있다** — 다음 단계 담당(코디)이 이미 그 방 큐 맨 앞에 있으면 바로 「시술 · 시트팩」 처럼 보인다(ZHANG ZHI 사례). 다음 담당이 없을 때만 「○○ 대기」. 역시 시안 로직 그대로.
3. **통역 WS 는 이번 대조에서 못 봤다(pending)** — back 의 `/api/interpret` 은 12:28 에 추가됐고, 대조용 back 은 12:25 에 띄워서 그 경로가 없었다(403). WP2 가 진행 중이고 실제 Soniox 를 부르게 되므로 다시 띄워 찔러 보지 않았다. 코드상 Origin 이 `CC_FRONT_ORIGIN` 과 다르면 1008 로 닫는다 — WP5 에서 front 를 그 주소(기본 `http://localhost:3600`)로 열어야 한다.

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(오류 0 · 경고 0) |
| `npm run build` | 통과 |

바꾼 파일: `cc/front/components/staff/{PatientView,StaffShell,InterpretModal,common}.tsx/ts` · `cc/front/components/desk/{FloorGrid,CheckInModal}.tsx`
