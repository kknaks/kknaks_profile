# [reviewer] WORK-007 검수 — 회의 중 · STT 중계 · 2트랙 · AI 배치

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`)

```bash
git log --oneline 618d5bb..HEAD    # b09a16a(be Phase 1~4) + 프론트 커밋
git diff 618d5bb...HEAD --stat
```

**산출물** — `orchestration/work/docs-v1/work007-review-report.md` **1개**. 코디 워크트리에 쓴다.

## 1. 네 층으로 본다 — 코드가 아니라 문서 기준

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
```

| 층 | SoT |
|---|---|
| **정책** | `10-decision/decision-003-meeting-notes.md` §1·§2·§3·§4·§6·§7·§STT |
| **아키텍처** | `40-architecture/backend/README.md` §5-1·§5-2·§8-2·§8-3·§12 · `frontend/README.md` · `system/README.md` 흐름 ③ · `database/domains/meeting.md` |
| **SPEC** | `20-spec/spec-007-meeting-live.md` §2 U-1~U-8 · §4 WS·API·**Case Matrix 15행** · §6 Acceptance 26개 |
| **WP** | `30-work/work-007-meeting-live.md` Phase 1~6 |

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. 공용 부품 — **두 번째 구현이면 FAIL**

```
프론트
  AgendaLineTree     회의록 탭 · AI 탭 · (WORK-008)통합본 탭 셋이 쓴다
                     **컴포넌트 안에 `track ===` 비교 0건.** 차이는 props 로만
                     — 여기서 분기하면 WORK-008 이 또 갈라진다
  MeetingStatusBar   WORK-006 MeetingTopBar 와 **같은 자리**(top 150 · 1640×56)다.
                     두 파일이 그 자리를 다투지 않는지 봐라
  TranscriptPanel · PromptBar · LineKindPopover   WORK-008 이 재사용한다
  lib/api/ws.ts      `new WebSocket(` 이 이 파일 밖에 0건
  WORK-006 것 재사용   첨부 탭 · 추가 팝오버 · 파일 드로어 · DrawerFrame · ItemRow · V2Gate
  lib/ 로 올라간 것    useRowFailures · useWorkSettings · inlineErrorMessage (618d5bb)
  features 사이 import 0건 — static.test 가 고정 중

백엔드
  build_detail        1개. agendas.ai·latestBatchSeq 를 **조립 변경 없이** 채웠나
  _assert_allowed     1곳
  schedule_service    두 번째 겹침·파생 구현 0
  codex 옵션 빌더      한 함수. 새 세션 호출과 resume 이 다른 옵션으로 나가지 않나
```

### 2-2. 정책이 못박은 실패 처리 — **가장 중요하다**

DEC-003 §7 이 열거한 것**만** 처리하고 그 밖은 전파해야 한다(BASE-003 L43).

```
자동 재연결 0건            setInterval/setTimeout 재접속 · WS onclose 재시도
except Exception 0건       광범위 포착이 어디서 깨졌는지를 가린다
배치 실패                  조용히 넘기고 다음 배치에 병합. 사용자에게 표시 안 함
스키마 위반                결과 **전체** 폐기. 부분 파싱 0
없는 업무 참조              화이트리스트 밖 → **그 줄만** action 강등. 내용은 살린다
파일 적재 실패              그 자리에서 끊는다 (원본 없는 녹음을 계속하지 않는다)
마이크·스트림 실패           일시정지 + 사유. 별도 「다시 연결」 버튼 0
```

**설계 밖 실패에 fallback 을 넣은 자리가 있으면 FAIL 이다.**

### 2-3. 2트랙 경계

```
AI 는 AI 요약 탭만 채운다     사람 트랙에 개입 0 · 줄 제안 0 (DEC-003 §4 L95)
AI 안건은 track='ai' 에만     회의 중 사람 회의록 탭에 안 보인다 (L96)
AI 증분 즉시 반영             버퍼링 0 · 「배치 n회 반영」 표시 (L97)
배치 입력                    사람 안건·사람 줄을 **읽기 전용 컨텍스트**로 넣는다
                            (ERD M-6 정정 — 「읽기는 한다」)
확정 토큰만 적재              잠정은 화면 표시용 (§3)
화자                        익명 라벨까지만. 이름 입력 자리 0 (§2)
```

### 2-4. 그리지 않았나 (SPEC-007 §7-B)

```
상태 바 파형 15개 막대 · 상태 바의 「자동 저장 · 09:42」 · 「회의실 A」
프롬프트 바 「+」 버튼 · AI 요약 카드(문단·카운트·펼침)
「회의 중 작성」·「· 안건 1」 캡션 · PNG/PDF 첨부 행 · 잠정 발화의 시각
```

**반대도 본다** — 정책에 있는데 없는 것: `/` 팝오버의 **「업무」 항목**(시안 3종 누락 보정) · 일시정지 3종에서도 **「회의 종료」 활성** · 안건 배지 **「대기」**(회의 중이다).

### 2-5. 수치 — DEC-003 §STT 와 같나

```
600자 · 80자 · 180초 · 120초 · 회의당 세션 1
stt-rt-v5 · language_hints ["ko"] · enable_speaker_diarization true
endpoint detection 미사용
env 로 빠져 있고 config 기본값이 .env.example 과 같나
```

### 2-6. 키

```
SONIOX_API_KEY 가 프론트로 내려가는 경로 0
.env.example 은 빈 값
커밋·로그·문서에 실제 값 0
```

### 2-7. E2E 대체

**이번 발주는 앱 창 실물 확인을 하지 않았다.** WP Phase 6 의 「Tauri 앱 창에서 실제 마이크로」 항목이
대역 WS·목 `getUserMedia` 테스트로 옮겨졌는지 보고, **못 옮긴 것이 「실물 확인 필요」로 정직하게 남았는지** 확인해라.
**통과로 처리한 게 있으면 FAIL 이다.**

백엔드가 이미 8건을 남겼다(Soniox 응답 필드 · 오디오 포맷 · codex output_schema · 웜스타트 session_id 회수 ·
**compose 에 Redis·worker 없음** · 유휴 유지 · `at_ms` 기준 · NPM WS upgrade). **프론트 목록과 합쳐 한 표로 만들어라.**

### 2-8. 코디가 이미 판정한 것 — FAIL 로 올리지 마라

```
POST …/lines 응답이 LineItem 이다 (MeetingDetail 전체 아님)
  → SPEC-007 §4 를 따른 것이 맞다. 「자식 쓰기 = Detail 전체」는 안건·첨부 같은
    저빈도 표면 규칙이고, 줄은 초 단위로 쌓이며 WS 로 증분이 따로 간다.
    코디 브리프가 그 예외를 안 적었다
```

### 2-9. 프론트 워커가 올린 불일치 1건 — **판정해라**

```
AI 「업무」 줄에 유형 배지를 못 그린다
  디자인 시스템 [09] L668~672  업무 줄 = 라벨 #5F6470 + **유형 배지** + 「업무 갱신」 버튼
  실제 응답                     LineItem.task 요약에 workType 이 없다
  프론트 판단                   배지를 뺐다. 「백엔드/SPEC 불일치」로 보고

→ SPEC-006 §4 필드 소유 표 · SPEC-007 §4 LineItem · SPEC-008 §4 를 열어
  `task` 요약이 무엇을 담기로 돼 있는지 판정해라.
  ① SPEC 이 workType 을 담기로 했는데 백엔드가 빠뜨렸나
  ② SPEC 자체가 안 담기로 했나 (그러면 디자인 시스템과의 충돌 — 문서 공백)
  어느 쪽인지 근거와 함께 적어라. WORK-008 이 「업무 갱신」 버튼을 붙일 때 같은 자리를 쓴다
```

## 3. 판정

```
FAIL   계약·정책 위반, Phase 검증 미충족  → 원 워커에게 수정 재발주
WARN   동작은 하나 규약 이탈, 범위 밖 변경
PASS

항목마다 파일:줄 + 어긋난 문서의 절 번호. 근거를 못 대면 싣지 마라
```

**「문서 공백」은 별도 절**로. **WORK-006 검수에서 남은 5건**(G-2 `field` — 이번에 백엔드가 고쳤다 ·
G-3 문서함 임시 계약 · G-5 훅이 어느 층에 사나 · G-6 `ItemRow` 규격 충돌 · G-9 enums 경로)의
**현재 상태도 함께 적어라** — 닫혔는지 남았는지.

## 4. 하지 마라

1. **코드·테스트·문서를 고치지 마라**
2. **취향으로 지적하지 마라.** 문서 근거가 있는 것만
3. **커밋·push 하지 마라**
4. 산출물은 리뷰 리포트 1개

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_e32d8809-dd52-46ae-b32c-7263e08c0274 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-007 검수 완료" \
  --body "FAIL n · WARN n · 문서 공백 n / 공용 부품 판정(AgendaLineTree track 분기 · MeetingStatusBar↔MeetingTopBar · WebSocket 생성 위치) / 실패 처리 7항목 판정 / 2트랙 경계 / 안 그린 것·있어야 하는데 없는 것 / 수치 대조 / 키 / 실물 확인 필요 통합표 / WORK-006 문서 공백 5건의 현재 상태 / 가장 심각한 3건"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-007 검수 완료. 상세는 인박스." --enter
```
