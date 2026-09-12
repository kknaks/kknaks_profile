
# 작업 요약 — sc-meeting (sc-ax)

기간: `2026-09-08` ~ `2026-09-12`
결과: 앱 PR #5·스펙 PR #719 둘 다 main 에 squash 머지(2026-09-12). 실물 e2e 4회(실제 회의 녹음 3 + 사용자 실제 회의 1) 통과 뒤 전체 스위트(BE 847·FE 467) 녹색으로 마감.

## 1. 무엇을 했나

SCAX 의 회의 기능이 「브라우저가 STT 를 직접 부르고, 회의록은 한 층」인 옛 모델이라 기획(회의·미팅노트 v1.1.0)과 어긋나 있었다. 스펙을 0.4.1→0.4.11 로 다시 세우고(SPEC-004 + WP-001~007, 결정 D1~D51) 코드를 새로 올렸다 — 서버가 Soniox 세션을 소유하는 WS 중계, 메모 트랙·AI 중간 요약 트랙, 종료 시 원본 음원 2-pass 재전사 뒤 합성(재료로 새로 쓰기), 후속업무 승격(시스템이 보내는 업무 요청), 자료·공유, THE CONNECT 회의실 자동 대체 예약, 주제 스레드형 A4 내보내기. 디자인은 Claude Design 시안(회의록·회의실 dc.html v3)을 정본으로 두 페이지를 라운드로 맞추며 공용 부품(DateField·Select·Popover·GutterList·TimeChip 등)을 세웠다. 실물 테스트에서 드러난 결함 11건(D41~D51)을 당일 고치고, main 의 두 PR(#3·#8)을 머지해 스위트를 녹색으로 만든 뒤 두 PR 을 squash 머지했다.

## 2. 적용한 기술·개념

이 작업의 알맹이다. **새로 쓴 것 · 판단이 갈린 것 · 막혔다가 푼 것**만 적는다.

- **서버 소유 STT 중계(WS relay) + 역할 둘(upstream/subscribe)** — 브라우저 직결을 걷고 서버가 Soniox 세션을 잡는다 → [[websocket-relay]]
  - 왜 이걸 골랐나: 키가 브라우저에 나가지 않고, 참석자 여러 창이 같은 회의 소켓에 읽기 전용(subscribe)으로 붙어 확정·잠정·AI 요약·메모 줄·안건 추가를 **한 채널로** 받는다. 참석자 폴링(D41 초안)은 「업데이트를 전부 실시간으로」라는 요구와 맞지 않아 하루 만에 철회.
  - 무엇이 어려웠나: Soniox 는 20초 무음에 408 로 끊고, 종료 프레임 뒤 드레인을 기다리지 않으면 마지막 발화가 유실된다 — keepalive 10초·드레인 8초를 실물로 찾았다. 컨테이너(webm/opus)는 `audio_format=auto`, raw pcm 은 헤더가 없어 끝을 모르므로 직접 테스트는 pcm 으로.
  - 근거: `modules/meetings/stream.py`·`stream_service.py` · `report-be-wp002.md` · SPEC-004 §5.3 · D41
- **2-pass 재전사 — 실시간은 화면용, 최종 원문은 비동기 재전사** — 종료 시 음원 전체를 `stt-async-v5`(화자 분리)로 다시 전사해 원문을 갈아 끼우고 그 위에서 합성 → [[two-pass-transcription]]
  - 왜 이걸 골랐나: 실시간 STT 는 저지연 때문에 화자 분리가 부정확하다. task-management 원형이 이미 그렇게 했는데 코디가 「실시간 전사가 정본」이라는 초기 결정(D3)을 넓게 읽어 폐기했다가 사용자 지적으로 복원(D44).
  - 무엇이 어려웠나: 파일의 0초 ≠ 회의의 0초 — 녹음 시작 − 회의 시작만큼 밀어야 근거 시각이 맞는다. 재전사 결과 GET 이 175KB 본문을 urllib 단발 `read()` 로 받다 `IncompleteRead` 로 끊긴 것을 실물에서 잡았다.
  - 근거: `modules/meetings/retranscribe.py` · `platform/soniox.py` · `finalize_service.py` · D44 · 회의 d6e7b8e0 로그
- **조용한 폴백 금지 — 외부 단계 실패는 상태로 드러낸다** — 재전사 실패 시 「실시간 원문 유지」 폴백을 걷고 회의를 「실패」+[다시 시도]로 → [[no-silent-fallback]]
  - 왜 이걸 골랐나: 코디 브리프가 넣은 폴백이 실패를 삼켜 화면엔 아무 표시 없이 화자가 어긋난 원문 위의 회의록이 섰다. 「화자가 어긋난 원문으로 만든 회의록은 고치는 것이 새로 만드는 것보다 비싸다」 — 실패 여섯 갈래(녹음 없음·업로드·거절·수신·빈 결과·상한) 전부 failed, 사유는 사람 말(D43).
  - 무엇이 어려웠나: 「실패로 보내면 회의가 막힌다」는 걱정으로 폴백을 넣었지만, 재시도 경로([다시 시도] = 재전사부터)가 있으면 막히지 않는다. 멱등 단계(같은 transcription_id 의 결과 GET)만 재시도하고 업로드·전사 생성은 재시도하지 않는다.
  - 근거: `sc-meeting-be-retranscribe-nofallback-brief.md` · 커밋 e252dee · D44 정정 · 10-decision
- **strict 구조화 출력 — 강제(–output-schema)와 검증(서버 재검증)은 다른 층** — 모든 object `additionalProperties:false`·모든 키 required·선택은 nullable → [[strict-json-schema-output]]
  - 왜 이걸 골랐나: Codex 는 strict 규격 하나라도 어기면 `invalid_json_schema` 로 빈 출력을 준다(실물 400 사례). 회의 중 스키마에는 최종 전용 필드(제목 후보)를 키 자체를 두지 않는 방식으로 막았다가, D46 에서 회의 중 todos 를 required 로 열자 그것을 모르는 테스트 픽스처가 줄줄이 깨졌다 — required 추가는 호출자 전부에 닿는다.
  - 근거: `modules/meetings/schemas/ai_batch_output.json`·`ai_final_output.json` · `batch.py parse_output` · D46
- **근거(evidence) 결박의 검증 범위 = 회의 전체, 배치 창이 아니다** — 매 배치가 AI 트랙 전체를 다시 쓰므로 앞 회차 근거를 「이번 구간 밖」으로 떼면 칩이 사라진다 → [[evidence-binding]]
  - 왜 이걸 골랐나: 실물에서 AI 요약 30줄 중 25줄의 시간 칩이 없었다. 규칙은 「존재하지 않는 구간을 인용할 수 없다」이지 「이번 구간만 인용한다」가 아니다. 검증 구간을 `(0, 지금까지 적재된 마지막 end_ms)` 로.
  - 근거: `application.py batch_input covered_ms` · `batch.py demote_line` · D47 · 피드백-회의실 D5
- **합성은 두 트랙을 잇는 게 아니라 재료로 처음부터 새로 쓴다** — 사람 안건 보존 검사(「사람 안건을 정확히 한 번씩 덮어야」)를 걷음 → [[synthesis-as-rewrite]]
  - 왜 이걸 골랐나: 서기가 메모를 안 남긴 회의가 「사람 안건 0개를 못 덮었다」로 실패했다. 통합 회의록의 뜻은 「사람 + AI 가 쓴 것을 재료로 한 벌을 새로 짓는다」 — 남는 검증은 스키마·근거 실재·기존 업무 제외뿐.
  - 근거: 커밋 ada1aa9 · D42 · 실패 회의 3edd8f88 사유
- **전사 블록 경계 — 시간 상한·글자 상한·문장 끝, 토큰 경계에서만** — 300자 → 20초·150자·문장 끝 우선 → [[transcript-segmentation]]
  - 왜 이걸 골랐나: 재전사가 한 화자 51초를 한 블록으로 묶어 칩(03:42)이 블록 시작(03:29)을 켜고, 근거 구간이 블록 경계에 걸쳐 두 줄이 켜졌다. 문제는 점프 규칙이 아니라 블록 길이였다. 글자 가운데서 자르면 조각에 시각을 줄 수 없어 토큰 경계에서만 끊는다.
  - 근거: `stream.py build_blocks·ends_sentence` · D51 · 회의 8c63e19b
- **오버레이는 body 포털 + fixed — 컨테이너 overflow 에 잘리지 않게** — DatePicker·Select 팝오버가 드로어 정보 카드 안에서 잘림 → [[viewport-aware-overlay]]
  - 왜 이걸 골랐나: 원인이 앵커 계산이 아니라 렌더 위치(`.meta-grid{overflow:hidden}` 안의 absolute)였다. 포털로 빼면 바깥 클릭 판정에 패널을 더해야 하고 z-index 층(드로어 41·모달 50·팝오버 55·토스트 60)을 정해야 한다.
  - 근거: `frontend/src/Popover.tsx` · 커밋 b941846 · DS-18
- **디자인 시스템 부품은 하나의 생김새 — OS 달력 갈래 삭제** — `DateField` 의 platform/showPicker 경로를 지우고 우리 DatePicker 하나로 → [[design-system-single-source]]
  - 왜 이걸 골랐나: 같은 부품이 화면마다 다른 달력(크롬 기본/우리 것)을 내면 부품이 아니다. 타이핑 입력도 함께 사라지는 축소를 감수(사용자 결정). main 의 AX 카드가 요구한 점 표기·아이콘은 프롭(displaySeparator·pickerIcon)으로 얹었다.
  - 근거: `frontend/src/DateField.tsx` · DS-17 · 회의 목록 라운드 항목 18
- **승격 요청자는 시스템 행위자(`system:meeting`)** — 사람이 아니라 회의가 업무 요청을 보낸다 → [[system-actor]]
  - 왜 이걸 골랐나: 승격한 사람을 요청자로 두면 조직 경계·권한(팀장 work_request.create) 예외가 줄줄이 필요했다(D29·D30). 요청자를 시스템으로 두고 `promoted_by`·cc 로 사람을 남기면 경계 예외가 사라진다(D40).
  - 근거: `modules/work/requests.py` · 커밋 d939dae · D40 · SPEC-001 §12 R-48
- **회의실 예약 자동 대체 — 정원 ≥ 인원인 최소 방, 없으면 생성 거절** — THE CONNECT 실물 계정으로 예약 → [[fallback-selection]]
  - 왜 이걸 골랐나: 기획 v1.1.0 이 자동 대체를 택했고, 대체할 방이 없을 때 회의만 만들어 두면 「예약 없는 회의」가 조용히 생긴다. 409 + 가능한 방 목록으로 사용자가 고르게(D36).
  - 근거: `platform/the_connect.py` · `modules/meetings/rooms.py` · `report-be-wp007.md`

## 3. 막혔던 것 / 사고

일이 잘못됐던 지점. **다음에 같은 걸 안 밟기 위해 남긴다.**

- **코디가 결정을 넓게 읽어 세 번 틀렸다** — 「미리보기 빼자」→ 드로어 전체 제거(정정: 4종 뷰어만) · 「참여자는 웹소켓 연결 안 할거야」→ 폴링 설계(정정: 같은 WS 에 subscribe) · 「실시간 전사가 정본」→ 2-pass 폐기(정정: 재전사 복원) → 사용자가 화면·질문으로 잡아냄 → 스펙 정정 판(0.4.5/0.4.6/0.4.7)으로 되돌림. **결정은 문장 그대로 적고, 넓혀 읽은 부분은 「기본값 통보」로 드러낸다.**
- **지시 없는 발주 두 번** — 합성 검증 버그(C8)와 실패 회의 재시도를 시키지 않았는데 돌림 → 사용자 강한 질책 → 취소하고 「기록 먼저, 발주는 신호 뒤」로 고정. 이후 피드백 파일(피드백-회의실 D1~D10·DS-17/18)에 적고 「발주해」에만 움직였다.
- **폴백이 실패를 삼켰다** — 재전사 결과 수신이 `IncompleteRead` 로 끊겼는데 코디 브리프의 「실패 시 실시간 유지」가 done 으로 흘려보냄 → 화면에 실시간 원문 위 회의록이 서서 발견 → D44 정정(§2 no-silent-fallback). 브리프에 폴백을 쓸 때는 「그 실패를 사용자가 어디서 보는가」를 같이 적어야 한다.
- **orca 주입이 입력창에만 남고 실행되지 않음** — dispatch --inject 뒤 워커 터미널에 텍스트가 대기만 함(BE 두 번·FE 한 번) → `terminal read` 로 「❯ 텍스트」 상태 확인 → Enter 재전송 또는 텍스트+--enter 로 다시 보냄. 발주 뒤 10초 안에 `terminal read` 로 스피너를 확인하는 습관.
- **워커의 파이썬 파일 편집 명령이 5분 넘게 걸림** — heredoc 치환이 걸린 채 「Deliberating」 → 코디가 ESC 로 끊고 「픽스처 통째 재작성 말고 공통 헬퍼 한 곳」으로 범위를 좁혀 재지시 → 10분 안에 완료.
- **로컬 스택이 메모리 부족으로 두 번 죽음** — 백그라운드 pytest + 스택 + 워커 셋 동시 → 재기동. 스택 재기동은 백엔드 코드가 바뀔 때만, 워커가 같은 트리를 편집 중일 때는 하지 않는다(반쯤 고친 파일을 import 하다 깨짐).
- **main 머지가 조용히 메서드를 떨어뜨림** — 알림 메서드 셋이 사라져 `/api/notifications` 500 → 실물 curl 로 발견 → main 이 더한 `def/class` 이름을 병합 트리와 comm 으로 대조해 누락을 셌다(런북 STEP 7 의 blob 대조와 같은 발상). 머지 뒤엔 「main 이 더한 정의 목록 − 우리 트리」를 기계로 센다.
- **실물 e2e 우선 구간의 대가** — 사용자 지시로 D46~D51 은 스위트 없이 tsc/import 만 보고 커밋 → 머지 전 전체 스위트에서 FE 16·BE 수집 오류 5 → 워커 둘로 회수(1시간). 빠르게 화면을 보는 대신 마지막에 한 번은 전체를 돌린다는 계약으로 정리.
- **squash 잔상 판별** — 아카이브 dry-run 이 두 브랜치의 「커밋 25/54건 앞섬」을 blob 동일로 판정해 통과. squash 머지 뒤엔 커밋 수가 아니라 내용 대조가 기준.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-09 | STT 는 백엔드 중계, 회의 = 나·AI 두 트랙 + 종료 후 합성 | 사용자 지시(키 보호·기획 컨셉) |
| 2026-09-09 | ~~실시간 전사가 원문 정본, 2-pass 폐기(D3)~~ → 2026-09-11 D44 로 철회 | 코디가 넓게 읽음 — 화자 분리는 재전사가 정확 |
| 2026-09-10 | 확정 시안(dc.html)이 화면 정본, 기획 차이는 §12 통보 | 사용자 「되묻지 마라」 |
| 2026-09-11 | 회의실 예약 데모 범위 편입, 자동 대체·대체 불가 시 생성 거절(D33·D36) | 기획 v1.1.0 |
| 2026-09-11 | 승격 요청자 = 시스템(회의), promoted_by·cc, 조직 경계 없음(D40) | D29·D30 예외 연쇄 제거 |
| 2026-09-11 | ~~참여자는 폴링(D41 초안)~~ → 같은 WS subscribe 로 전부 실시간 | 사용자 정정 |
| 2026-09-11 | 합성 = 재료로 새로 쓰기, 사람 안건 보존 검사 삭제(D42) · 실패 사유 사람 말(D43) | 서기 없는 회의가 실패하던 것 |
| 2026-09-11 | 종료 시 2-pass 재전사 복원(D44) → 같은 날 정정: 폴백 없음, 실패는 「실패」 | task-management 원형 · 실물에서 폴백이 실패를 삼킴 |
| 2026-09-11 | 회의 중 안건 추가(D45) · 회의 중 다음 할 일 후보 읽기 전용(D46) | 사용자 |
| 2026-09-11 | 근거 검증 구간 회의 전체(D47) · 자리표시 안건 제목 AI 가 채움(D48) | 실물 2회차 칩 소실·「안건 1. 안건 1」 |
| 2026-09-11 | 근거 칩 전부 + 눌리는 칩(D49) · 시각 표기 회의 경과 mm:ss, 벽시계 철회(D50) | 1분 안 발화가 많아 HH:MM 은 구분 불가 |
| 2026-09-11 | 블록 경계 20초·150자·문장 끝(D51) | 51초 한 블록이 칩 매핑을 깨뜨림 |
| 2026-09-11 | DateField = 우리 DatePicker 하나(DS-17) · Popover 포털(DS-18) · 승격 드로어 「업무 요청」(D10) | 실물 드로어 결함 |
| 2026-09-12 | main 은 리베이스가 아니라 브랜치로 머지(충돌 한 번) · 머지 전 전체 스위트 → squash | PR 은 squash 라 결과 동일 |

## 5. 날짜별 로그

- `2026-09-08` 워크트리·워커 3(planner·backend·frontend) 세팅, 조사 1(AI 프로바이더=Codex CLI).
- `2026-09-09` 사용자 결정: 백엔드 STT 중계 · 두 트랙 컨셉. 기획 충돌 A~E 정리.
- `2026-09-10` SPEC-004 0.3.0→0.4.1 재작성 + WP-001~006, 검수 1·2, 시안 v2(회의록·회의실), WP-001~005 + FE P1~P5 구현·실물 e2e(Soniox·Codex·브라우저 마이크), PR #5·#719 개설.
- `2026-09-11` 디자인 라운드(회의록 20건·회의실 A1~C9), 기획 v1.1.0/v1.2.0 조사, WP-007 THE CONNECT 자동 대체, 내보내기 스레드형, D33~D40; 실물 테스트 3회(Charty 녹음)+사용자 실제 회의 → D41~D51 당일 반영, 스펙 0.4.6~0.4.11.
- `2026-09-12` main(#3·#8) 머지·충돌 24파일 해소·알림 메서드 복원, 전체 스위트 녹색(BE 847·FE 467), 앱 #5·스펙 #719 squash 머지, 아카이브.

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/719 (squash → main 8c8cae5e, 2026-09-12)
- code PR: https://github.com/MediSolveAIDev/ax-workspace/pull/5 (squash → main 0a8a04b, 2026-09-12)

- `kknaksss/sc-meeting-spec` → `main`
  - `92cb17ad` Merge origin/main into kknaksss/sc-meeting-spec
  - `f4b331f0` docs(sc-ax): SPEC-004 0.4.11 — D49 근거 칩 전부(겹치는 줄 켜기) · D50 시각 표기 회의 경과 mm:ss(벽시계 철회)
  - `3f5cada4` docs(sc-ax): SPEC-004 0.4.10 — D47 배치 근거 검증 구간은 회의 전체 · D48 빠른 시작 자리표시 안건 제목은 AI 가 채움
  - `a149b3ad` docs(sc-ax): SPEC-004 0.4.9 — D46 회의 중 AI 요약에 「다음 할 일」 후보(읽기 전용·provisional)
  - `ef0d19a1` docs(sc-ax): SPEC-004 0.4.8 — D44 정정: 재전사 폴백 없음(실패는 회의 「실패」) · 종료 뒤 원문 재조회 · 회의 중 시각 칩 점프
  - `64601f7c` docs(sc-ax): SPEC-004 0.4.7 — D45 회의 중 안건 추가(주최자, agenda.added) · WP-001/002/003/006 동기
  - `3dae89f8` docs(sc-ax): SPEC-004 0.4.7 — D44 종료 시 2-pass 재전사 복원(실시간=회의 중 화면, 최종 원문=재전사, transcript_source) · D3 취소선 · WP-002/004 동기
  - `54d588ef` docs(sc-ax): SPEC-004 0.4.6 — D41 정정(참석자 WS 구독·memo.line·OQ-310 확정·OQ-318 삭제) · WP-002/003/006 동기
  - `17a7cedd` docs(sc-ax): SPEC-004 0.4.6 — D41 참여자 폴링(WS 는 주최자만) · D42 합성=재료로 새로 쓰기(사람 안건 보존 삭제) · D43 실패 사유 사람 말 · WP-002/003/004/006/007 동기
  - `475e7e3e` docs(sc-ax): SPEC-004 0.4.5 — D37 정정(자료 드로어 유지, 4종·조작만 데모 밖) · 스크립트 탭은 전사만(메모 분리) · WP-003/005/006 동기
  - `68c2a83f` docs(sc-ax): SPEC-004 0.4.5 — D38 재정정 출처 다섯(AI 정리 종류) · D40 승격 요청자=시스템(회의), promoted_by·cc, 조직 경계 없음(D29·R-36 철회, R-48)
  - `61ea571a` docs(sc-ax): SPEC-004 0.4.4 — D38 안건 출처 넷(+AI 정리 표시 축, 데모는 직접·지난 회의) · R-19 철회·R-47 · R-36/37 소유 표기 · R-40 확정 · D39 내보내기 주제 스레드형 조판
  - `98df94f2` docs(sc-ax): SPEC-004 0.4.4 — D35 승격 요청됨 유지 · D36 회의실 자동 대체·대체 불가 시 생성 거절·시간대 조회(R-45/46 철회) · D37 자료 미리보기 데모 제외 · WP-006/007 동기
  - `7a3e49b7` docs(sc-ax): SPEC-004 0.4.3 — 기획 v1.1.0 반영(D34): 화면 상태 다섯(종료)·회의명·「회의」·목록 세 구획·공유 끝난 뒤·자료 떼기 예정만·줄 우측 발화 시각·같은 요일 다음 날짜 · §12 재통보/R-46
  - `ddda69ee` docs(sc-ax): SPEC-004 0.4.2 — 회의실 예약(THE CONNECT) 데모 범위 편입(D33, R-45) · WP-007 신설 · WP-001/006·30-work 동기
  - `aadd03d4` docs(sc-ax): SPEC-004 §12 R-39~R-44(회의록 시안 v3 이탈) · §3.1 시안 v3 정렬(삭제 갈래 하나·선택 안 함 기본·[회의 생성]) · WP-001 DELETE scope 사실 복원 · WP-006 Scope
  - `a913c84e` docs(sc-ax): SPEC-004 §0 sources — PLAN-004·SCREENDEF-005 v1.0.0 입고(313ae36) 반영, 업무 v1.2.0 동반 입고 명시
  - `6c1de4ed` docs(sc-ax): SPEC-004 D32 바로 시작 기본 안건 · 정리 중 폴링(OQ-317) · 10-decision D32
  - `51d05d87` docs(sc-ax): SPEC-004 R-38(MOD-104-T02 문구 범위) · OQ-311 FE P4 임시 문구 키 표
  - `d7ec5515` docs(sc-ax): WP-005 공유 경로 /shares(GET basis) · 자료 첨부 응답 {attached, failed} · 진행 중 409
  - `4963c6e7` docs(sc-ax): SPEC-004 내보내기 422 · D29 참석자 승격 조직 예외 · D30 팀장 work_request.create(R-36/R-37) · due 기준일 환산
  - `37923ac0` docs(sc-ax): WP-006 Phase 4 회의 뒤 배선 · WP-003 transcript/at_ms/can_write_memo 계약 · OQ-311 임시 문구 6건
  - `df4c9373` docs(sc-ax): SPEC-004 메모 API 주소·OQ-307/315 잠정값 · 줄 편집=안건 덮어쓰기 · 내보내기 HTML 하나(R-35) · todos/{todoId}/promote · title_candidate
  - `d79cb80b` docs(sc-ax): SPEC-004 WS 인증=세션 쿠키 · WP-002 계약 · WP-005 전사 자료 다리 재건
  - `a54c2e6e` docs(sc-ax): SPEC-004 회의·미팅노트 0.4.1 재작성 + WP-001~006 신설
- `kknaksss/sc-meeting` → `main`
  - `e6ab21f` test(backend): main 머지 뒤 스위트 녹색 — 옛 회의 모델 시험 정리, 제품 코드 둘 새 모델로(action_center 계보 None · actions 겹침 status!=cancelled), D46 픽스처(todos·provisional), codex_cli 인자 순서, local-stack 가드 표지
  - `dd9e2fb` test(frontend): main 머지 뒤 스위트 녹색 — DateField 달력 상호작용·포털 옵션 조회·드로어 이름(D10)으로 테스트 정렬, 채팅 CSS 의 focus-visible 규칙 제거(전역 포커스 링 없음)
  - `ec9946b` fix(merge): main 의 알림 메서드 셋 복원 — list_notifications · mark_notification_read · _authorized_notification_view
  - `4212691` Merge origin/main (#3 채팅 인터랙션 · #8 프로젝트 참여 이력) into kknaksss/sc-meeting
  - `6004fb6` fix(meetings-be): 전사 블록 경계 — 최대 20초·150자·문장 끝 우선(실시간·재전사 공통)(D51)
  - `15d0cf5` fix(work-fe): CreateWorkDrawer — 만들 수 있는 유형이 하나면 토글 없음·제목은 그 유형(회의 승격 = 「업무 요청」)(D10)
  - `469c91f` fix(meetings-fe): 칩 점프를 겹치는 줄로(D49) · 시각 표기 회의 경과 mm:ss / h:mm:ss(D50, 벽시계 철회)
  - `b941846` fix(frontend-ds): DateField 를 우리 DatePicker 하나로(OS 달력 갈래 삭제, 전 화면) · Popover 를 body 포털+fixed 로(카드·드로어 안 잘림 해소)(DS-17·18)
  - `cf60d06` feat(meetings-fe): 근거 시간 칩 전부 표시 · TimeChip 부품(눌리는 칩, 구간 점프)(D49)
  - `cee9bca` fix(meetings-be): 배치 근거 검증 구간을 회의 전체(0~마지막 end_ms)로(D47) · 빠른 시작 자리표시 안건 제목을 AI 가 채움(D48)
  - `c52f94a` feat(meetings-be): 회의 중 AI 배치에 「다음 할 일」 후보(D46) — 스키마 todos·provisional 전량 교체·push, 최종이 지우고 새로
  - `e252dee` fix(meetings-be): 재전사 폴백 폐기 — 실패 여섯 갈래는 회의 「실패」(합성 미호출) · 결과 GET 끝까지 읽기+재시도 · lease 1800
  - `d9303b2` feat(meetings-fe): 회의 중 「AI 요약」 탭에 안건별 「다음 할 일」 후보(D46) — 읽기 전용, 배치마다 통째 교체
  - `e7e0cfa` fix(meetings-fe): 상태 전이마다 스크립트 원문 재조회(종료 뒤 재전사분으로 교체) · 회의 중에도 시각 칩으로 스크립트 점프
  - `b440c6b` feat(meetings-be): 종료 시 원본 음원 2-pass 재전사(Soniox 비동기·화자 분리) 뒤 합성 · 회의 중 안건 추가(agenda.added)
  - `b6fc76d` feat(meetings-fe): 회의 중 「+ 새 안건」(메모 칸에서 안건 생성 후 메모) · agenda.added 프레임 수신
  - `57a4925` fix(meetings-fe): memo.line 프레임 키 agendaId(BE 실물)
  - `ada1aa9` feat(meetings): 종료 합성 = 재료로 새로 쓰기(사람 안건 보존 검사 삭제·안건 이어 쓰기/신설) · 실패 사유 사람 말 · memo.line 프레임 broadcast · 잠정 발화 구독자 전체 송출
  - `55a1da4` feat(meetings-fe): 참여자 = 회의 웹소켓 읽기 전용 구독(폴링 제거) · memo.line 실시간 수신 · 주최자 두 번째 창 구독 복원
  - `a462b6c` feat(meetings-fe): 참여자 진행 중 화면 = 두 탭 읽기 전용 + 4초 폴링(웹소켓은 주최자만, 구독 폴백 제거) · 스크립트 시간|화자|내용 세 칸 한 줄·간격 축소
  - `504e1d8` fix(meetings-fe): 스크립트 화자 라벨 「화자 N」
  - `bef1683` feat(meetings-fe): 업스트림 거절 시 구독 폴백(마이크·메모 없이 실시간 수신) · 진행 중 스크립트 탭 적재 블록 선로드 후 실시간 이어 붙임
  - `ab8a8ef` fix(meetings-fe): 목록 패널 [내보내기]를 실제 export 링크로(토스트 가짜 제거)
  - `b0cf1b9` feat(meetings): 내보내기 HTML 주제 스레드형 A4 조판(D39, 템플릿 조각 렌더러·서버 장 나눔·쪽 번호) · 관계 그래프 시스템 행위자 제외 · 자료 떼기는 예정에서만(D34)
  - `62be71b` feat(meetings-fe): 회의실 v3 — 상태 어휘 종료·취소(정리 중 배지 없음), 줄 오른쪽 시각 하나+스크립트 점프, [공유] 종료·실패만, 회의명, 자료 드로어 복원, 스크립트 탭 전사만
  - `b61ba47` fix(meetings-fe): 공유 조직도 부서별 인원수가 고른 부서 명단 길이로 찍히던 버그
  - `d939dae` feat(meetings): D40 승격 업무 요청의 요청자=시스템(회의) — promoted_by·cc, requester_kind·source_meeting_title, 담당 조직 경계 없음, 누른 사람 수정·거두기
  - `54a4287` fix(fe): DateField inline 변형 — 한 칸 안에 YYYY-MM-DD + 달력 아이콘(시각 칸과 같은 트리거), 칸 어디를 눌러도 열림
  - `51ec0aa` fix(meetings-fe): 회의록 페이지 뷰포트 고정(canvas.full-height 100vh · columns 행 minmax(0,1fr)) — 목록은 패널 안에서만 스크롤
  - `e297e1e` feat(meetings): 회의실 자동 대체(정원≥인원 최소 방)·대체 불가 시 409 room_unavailable+available_rooms(회의 미생성)·시간대별 rooms 조회(D36) · 자료 content inline
  - `ab1dffc` feat(meetings-fe): 안건 출처 라벨(기획 넷 + AI 정리)·목록 패널에도 출처 표시(E21)
  - `5d3eda9` feat(meetings-fe): 자료 미리보기 제외(D37) — 행 클릭은 새 탭 열기, MaterialDrawer 삭제
  - `82af0b1` feat(meetings-fe): 회의실 대체 예약 토스트 · 409 거절 시 모달 유지·입력값 유지·회의실만 재렌더 · 일시 변경 시 시간대별 회의실 재조회(D36)
  - `e740f32` feat(meetings-fe): WP-007 P3 — 실제 회의실 목록·room_id·예약 실패 안내·[예약 중] 상태
  - `d0d5e32` feat(meetings): WP-007 THE CONNECT 회의실 예약 — 실제 회의실 목록·생성 시 예약(트랜잭션 밖)·실패해도 회의 유지·사내=회사 계정/사외=표시 문자열·일시 변경/취소 동기화·계정 미노출
  - `83e3d69` fix(fe): 포커스 시 테두리 변화 없음(전역) · 회의록 패널 푸터와 AX 버튼 겹침 해소 · 이름 찾기 0건 시 「직원 정보 없음」/「사외 참석자로 추가」 두 줄
  - `61f915b` feat(meetings-fe): 회의록 페이지 v3 — 뷰포트 높이 패널·투명 스크롤·3단 패널, 예약 모달 공용 부품(DateField inline·TimeRangeField·Select)·직원 정보 없음·회의실 선택 안 함·[회의 생성] 하나·닫기/취소 모달 문구
  - `1925a76` fix(meetings): 합성 적재 순서(트랙 줄→AI 안건 줄→todos→안건) · 적재 실패도 시도 실패로 · 상한 뒤 failed+failure_reason(예외 종류만) · 메모 달린 AI 안건 보존
  - `08f6381` fix(meetings-fe): 안건 번호를 정렬 자리(1부터)로
  - `20723a7` fix(meetings): quick-start 도 웜스타트 제출 · 기본 안건 「안건 1」(D32)
  - `f463f5d` fix(meetings-fe): 정리 중 동안 5초 폴링으로 상태 재확인(OQ-317)
  - `2285277` fix(meetings-fe): vite 프록시 WebSocket 통과(ws:true) · 닫힘 코드를 끊김 사유로
  - `16d249c` fix(meetings-fe): can_detach 소비 · 공유 삭제 응답 목록 소비 · MeetingLive 테스트 소켓 대기(검수 6 W-2)
  - `cbb4799` fix(meetings): MeetingMaterial.can_detach(서버 판정) · DELETE /shares 응답을 뷰어 목록으로
  - `eda908e` feat(meetings-fe): WP-006 P5 자료 첨부(다중·부분 실패·드로어)·공유(basis·member_ids) 실계약 배선 + DropZone·FileList 범용 부품
  - `59e1102` feat(meetings): WP-005 자료 첨부(다중·20MB·PDF/MD·부분 성공)·드로어 본문·공유 목록(basis)·전사 검색 다리(meeting_transcript, 열람 축) + evidence 키 start_ms/end_ms 투영
  - `ad4da8a` fix(meetings-fe): D31 근거 칩·스크립트 눈금 벽시계(started_at+at_ms) · 근거 계약 키 가드(NaN 칩 없음)
  - `96d5312` fix(meetings): WP-002/004 후속 — 종료 시 업스트림 드레인(finish·finally flush)·Soniox keepalive·스모크 재작성 + 참석자 승격 조직 예외(D29)·합성 기준일·제목 후보 스탬프·팀장 work_request.create(D30)
  - `9644e7c` feat(meetings-fe): WP-006 P4 회의 뒤 배선 — transcript 원문·근거 칩 점프·promote/삭제/finalize/export·title_candidate·안건 저장 409·작성자 표시 이름·D26 세 필드 소비
  - `8397d8f` feat(meetings): WP-004 종료 합성(같은 세션·durable job·콜드 폴백)·다음 할 일·제목 후보·근거 + 승격(업무 요청·출처 두 열·origin_kind) + 줄 덮어쓰기 409 + HTML 내보내기 + 배치 output_schema 결속(검수 4 F-A)·지연 트리거·게이트 테스트
  - `80dd097` feat(meetings): WP-003 메모 트랙 API·at_ms·can_write_memo·transcript 열람 + AI 중간 요약 배치(웜스타트 세션·MCP 도구 레지스트리·strict 스키마·강등·전량 교체·push) + 업스트림 소유자 게이트(검수 3 F1)
  - `bfc9770` fix(meetings-fe): W9 MeetingLine.author nullable — AI·최종 줄 작성자 없음, 스크립트 메모 행 이름 자리 비움
  - `806f52c` feat(meetings): WP-002 WS 전사 중계(Soniox 서버 소유·확정 블록 적재·원본 append·fan-out) + WP-006 P3 진행 중 화면(스트림 클라이언트·마이크·메모/AI 탭·스크립트) · 브라우저 직결·2-pass 재전사 폐기
  - `5751efa` feat(meeting): WP-001 회의·안건·줄 도메인+상태 6+회의 API · WP-006 회의 목록/상세 화면 Phase 1·2
- 리포트: `review-code-03..06-report.md` · `survey-01-ai-provider-report.md` · `survey-02-plan001-v120-report.md` · `survey-03-plan004-v110-report.md` · `report-be-wp002..7*.md` · `report-fe-p3..5.md` · `design/REPORT-회의록-v2/v3.md` · `design/REPORT-회의실-v2/v3.md` · `design/REPORT-export-template.md`

## 7. 잔여

- **채팅 [확인]의 회의 만들기/공유(meeting.create/share)** — main #3 의 AX 카드가 옛 회의 모델을 부르던 것을 안내 오류로 막아 둠. 새 모델(MeetingApplication) 위에 다시 세우는 것은 별도 작업(SPEC-008 소유 판단 포함).
- **재전사 context 힌트**(회의 제목·참석자 수) 미탑재 — 무엇을 외부로 보낼지 결정 필요. 폴링 5초·상한 1200초는 상수(lease 1800).
- **회의 중 배치는 기존 업무 중복 제외(task_list)를 생략** — 최종에서만. 회의 중 후보가 최종에서 빠질 수 있음.
- **회의 공유 알림** — 우리 share 는 알림을 만들지 않는다(D10 알림 데모 밖). main #722 의 「공유 시 제품 내 알림」과 갈림 — 판단 필요.
- **스펙 미결**(planner): spec-004 §3.1 번호 9→11 건너뜀 · system.md 70·78줄이 D44·D34 이전 서술 · ESC-006→007 참조 두 곳.
- **DS 후보**: TimeChip·GutterList·Composer·StatusNote·DropZone·FileList·MaterialDrawer 는 코드에 있으나 시안 DS 등재는 `DS-backlog.md`(DS-1~18) 대기. 재전사 블록 규칙 변경으로 기존 회의 원문은 그대로(재전사 다시 돌려야 바뀜).
- **잔여 디테일** `잔여-디테일.md` A~E 섹션(2차 범위 밖 항목).
- 데이터·음원: `reference/2026-09-11-charty-meeting/`(gitignore) 로컬만. 로컬 스택은 내렸다.
