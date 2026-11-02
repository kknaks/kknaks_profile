# 검수 반영 fix-map — SPEC-008·009 v0.3.0 · SPEC-006 v0.4.0 (2026-10-06)

리포트 `review-spec-008-009.md` 의 FAIL 4 · WARN 17 과 SPEC-006 개정을 어디에 어떻게 반영했는지.
약칭 S8=spec-008 · S9=spec-009 · S6=spec-006 · DEC=decision-008 · RM=20-spec/README.md.

## FAIL

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| F-1 | 카톡 방 목록·선택은 **Mac 이 정본** — 서버는 웹 고르기 창용 **중계만**(저장 안 함) · 서버에 남는 방 = 메시지 올라온 방뿐 · 업로드 검사 근거 = 앱이 각 업로드에 보내는 **선택 매니페스트**(`selected_room_ids`), 매니페스트 밖 방은 **403** · 근거(Mac 로컬 정본이라 서버가 못 듦)를 적음 | S8 §4.3(F-1 단락)·§4.6 messages 행·§2.5 · 대응표 D-15 |
| F-2 | 연결 시작 = **`POST …/connect` 가 `{authorize_url, state}` JSON** · 웹은 location·데스크톱은 `open_external` · 콜백은 **쿠키 아니라 `state` 로 회원** · reconnect 같은 모양 · 콜백 뒤 `AX_WEB_ORIGIN` 302 | S8 §4.2 전체 · AC-01·01b · S6 「외부 채널 수집기 수용」 연결 절 |
| F-3 | HTML 메일 **소독(script/on*/form/iframe 제거) + 샌드박스 iframe(allow-scripts 없음)+CSP · 원격 이미지 기본 차단·서버 프록시 · cid: 중계 · 링크 새 탭/open_external · 중계 응답 허용목록만 inline** | S8 §2.1 메일 본문 단락 · §4.4 · AC-08b·09 |
| F-4 | §4.3·4.4·4.6 에 **요청→응답→오류** 세 칸 전수 · 방 메시지 **페이지네이션**(cursor)·**스레드 경로**(thread_ts)·**WS 실시간**·읽음 `up_to_ts`·**`aid` 서버 발급**·카톡 연동 **첫 handshake 생성**·방 상태 `backfill_done`·묶음 500건·`Idempotency-Key`·상류 429/5xx=502 | S8 §4.2~§4.6 표 · Case Matrix |

## WARN

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| W-1 | 방별 상태 = 메시지 묶음의 **`backfill_done` 표지**로 `backfilling`→`live` | S8 §4.6 messages·불릿 · S9 §2.2 · AC-17b |
| W-2 | `unreadable` 에 **`reason: permission\|version\|unknown`** + 사유별 문구 한 곳 | S8 §2.5·§4.6 · S9 §2.2 · OQ-905 |
| W-3 | status **주기 보고 30초** · 서버 **90초 무보고=off** 판정 | S8 §4.6 status 행·AC-17 · S9 §2.2 |
| W-4 | 계정 바뀜 → **`reset-account`** · 옛 방은 소프트 딜리트 유지 · 상태 줄 추가 | S8 §2.5·§4.6 reset-account 행 · S9 §2.2 |
| W-5 | 세션 12h 만료 → **`login_required`**·트레이·재로그인 뒤 handshake 로 메움 · 장수명 토큰 **OQ-906** | S9 §4 인증 수명·AC-06b · S8 §4.6 머리 |
| W-6 | SPEC-006 개정 범위를 **I-2 + 창하나·트레이·백그라운드·AC-T23/T33/T47·trayIcon 시험·전체 디스크 접근** 전부로 — **S6 v0.4.0 신설 절** | S6 「외부 채널 수집기 수용」·인라인 포인터 · S9 §1 관계 표 |
| W-7 | 수집은 **회사판 medi-ax** 에(개인판은 주소 정해질 때) | S9 머리·§1·§5·OQ-901 · S8 §5 데스크톱 경계 · RM |
| W-8 | 슬랙 이벤트 **팬아웃** — (team,channel) 고른 모든 연동에 복제 · 키 `(연동,channel,ts)` | S8 §5 동기화 |
| W-9 | 로컬 redirect = **Google 만 `:8001`**(local-stack 포트) · **슬랙은 운영에서만**(https) | S8 §4.2 redirect_uri · §5 로컬 스택 |
| W-10 | 한도 = 메일 합계 25MB · 그 밖 파일당 50MB · **ingress `proxyBodySize` 올리기** 운영 할 일 | S8 §4.4·Validation·§5 운영 배치 |
| W-11 | 메일 = **첨부 합계(인코딩 전) 25MB** 기준(파일당 아님) | S8 §4.4·Validation·AC-13·OQ-806 |
| W-12 | **pod×(env·Secret 파일·hostPath) 표** — back 도 hostPath 마운트 · SA 키는 Secret 볼륨 · replicas kind별 1 · 암호화키/OAuth는 back·워커 둘 다 | S8 §5 운영 배치 |
| W-13 | 연동 워커 **Make 타겟 + local-stack 감독 + 두 env 파일 적재** | S8 §5 로컬 스택 |
| W-14 | AX 캐릭터 진입점 **둘(설정·신원 줄 `onUserClick`) 다** 제거 | S8 §5 프론트·AC-19 |
| W-15 | `GET /api/profile` 신설 대신 **`/api/organization/me`+`profile_image_url`** 재사용 · **`GET /api/profile/image` 신설**(아바타 내려받기) | S8 §4.7·AC-18b |
| W-16 | DEC-008 에 **D-49 대체 행**(보존 없음·계속 보관) 추가 — 본문 D-49 는 안 고침 | DEC §뒤집힌 결정 2 표 |
| W-17 | 취소선 약속 문장을 **「이 판으로 덮음」**으로 정리 · §4.5 OQ 초안문 제거(§4.2 로 이동) · `DEC-007` → `links.decisions` · `migrations/manual/` → `backend/migrations/manual/` · S9 폴링 2초 중복 한 줄 삭제 | S8 머리·frontmatter·§4.5·§5 스키마 · S9 §5 |

## SPEC-006 개정 (v0.4.0)

- 버전 0.3.1→0.4.0 · 머리에 변경 이력 · **「외부 채널 수집기 수용 — 회사판 medi-ax 개정」 절 신설**: 바뀌는
  불변식 표(I-2·창 하나·백그라운드·전체 디스크 접근) · 바뀌는 AC·셸 시험 표(AC-T23/T47·AC-T33·`trayIcon`) ·
  연결 OAuth 외부 열기(F-2) · 그대로인 것 · **개인판 strong-hajin 은 적용 안 됨**
- 본문 §2 Placement·§2.5·AC-T23·T33·T47 에 **(v0.4.0 … 「외부 채널 수집기 수용」 절) 포인터** — 옛 문장은 판별로 덮음

## 범위 밖(코디·다른 문서 몫으로 남김)

- 인프라 레포 `MediSolveAIDev/k8s_infra_mac` 차트·Secret·ingress·worker.kinds — `30-work/`·운영 (S8 §5 에 할 일로)
- SPEC-009 DB 여는 **절차**(키·userId·복호) — 구현 몫, 참조만(그대로)
- OQ-811(「Mac 앱 받기」 목적지) · OQ-906(장수명 기기 토큰) — 사용자 결정 대기
