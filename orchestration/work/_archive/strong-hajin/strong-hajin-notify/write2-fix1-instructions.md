# [writer] 알림 2판 수정 1 — 검수 FAIL 3 · WARN 11 · 사용자 결정 넷

정본: 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-spec-work-report.md`(§11 표가 고칠 곳의 줄 번호까지 준다) · 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/_RESUME.md` §2 「검수(FAIL 3·WARN 11) 뒤 사용자 결정」 행.

## allowed_paths (이번 판)
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` · `spec-006` · `spec-008` · `spec-009` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-010-notifications.md` — **새 결정 D-36~ 를 더하고 뒤집는 줄에 취소선만**(다른 결정은 고치지 마라)

## 1. FAIL — 반드시
- **F-1 SSE 재연결**: `EventSource` 실제 동작(비-200 → 영구 닫힘 · 상태 코드 안 보임 · 새 인스턴스엔 `Last-Event-ID` 없음)에 맞춘다 — 화면이 직접 백오프 재연결(새 인스턴스) · 마지막 사건 id 는 `?last_event_id=` 쿼리 · 인증 실패와 서버 재시작을 **세션 확인 API** 로 가른다(로그인으로 튕기는 것은 세션이 진짜 없을 때만) · 「비-200 뒤 회복」 시험을 AC·WORK 에. 검수표의 줄 전부
- **F-2 Code Surface 빠짐 5**: 검수표 그대로 — 회의 `share()`·공개 전환(`apply_legacy_visibility`) · 메일 안 읽음 `IS:112-130`·`INB:503,525` · `build.rs:138-160`·`Cargo.toml` · worker-external(이미지·재시작). M12/M13 범위 정정. 공개 전환은 **알림 없음**(사용자 결정 ③)으로 행을 정한다
- **F-3 [모두 읽음] = 시안대로 전부**(테마 필터와 무관) · 비활성 기준도 전체 · OQ-1107 닫힘

## 2. 사용자 결정 넷 → DEC-010 D-36~ · SPEC 반영
- ① 알림 목록 스크롤 끝 **자동 이어 불러오기**(단추 없음) — DEC 「이번 범위 밖 · 더 불러오기」 를 취소선으로 · OQ-1106 닫힘(W-1)
- ② **메시지함에서 메시지(메일 한 통 · 방 읽음 범위)를 읽으면 그 메시지의 알림 줄도 읽음** — 점 둘이 맞게 · OQ-1110 닫힘(W-7)
- ③ 회의 **공개 전환은 「공유받음」 알림 없음**, 특정 사람에게 공유할 때만
- ④ OS 알림 줄이기 — 앱이 앞에 있고 **그 대상 화면을 보고 있으면 OS 알림 생략**(목록·점은 그대로) · 슬랙 채널 합친 줄은 **처음 생길 때만** OS 알림(OQ-1103 닫힘 · W-8) · 짧은 시간에 몰리면(재연결 직후 등) **「새 알림 N건」 한 번**으로 묶음 — 묶는 창·문턱 값은 SPEC 이 정하고 근거를 적는다(W-6)

## 3. WARN — 이렇게 닫는다
- W-2 사건 순번 ≠ 커밋 순서: 이어 받기에서 빠지지 않게 계약으로 닫는다(예: 이어 받기 때 겹침 창 + 화면이 id 로 중복 제거) — 택한 방식과 근거
- W-3 백필: 셈 확인은 「같음」 이 아니라 **적용 전 셈을 출력하고 사람이 확인 뒤 적용** · 백필 전/dmg 전 `from_me` 가 `null` 인 줄의 처리 규칙(내 것 아님으로 본다 등)을 명시
- W-4 메일 `from_me`(From == 연동 계정): DEC D-34 에 없다 → **DEC 에 도출 결정으로 한 줄**(근거: 같은 원칙 ① · 판정 재료가 이미 있다)
- W-5 검증: Phase 마다 **관련 시험만**(전체 스위트 금지) · `make verify` 는 마지막 1회 · FE 병렬 가능 여부 · cargo feature(`kakao-collector` 켠/끈 빌드 둘)
- W-9 설정 탭 「시스템 알림이 꺼져 있습니다」 줄: **확정 시안에 없다 → 빼고** 2루프 후보로 WORK Open Issues 에
- W-10 사이드바 id: 코드의 기존 id `notifications` 하나로 통일하고 시안 `alert` 와의 대응을 한 줄 · 줄 번호 `:457 → :456`
- W-11 운영 SSE 실측 시간: **1시간**으로 통일

## 4. 검증 · 끝나면
- 검수표 FAIL·WARN 각 행이 어디서 닫혔는지 대응표를 WORK 부록에 · DEC-010 새 결정이 SPEC 에 대응
- 다른 파일 금지 · 커밋 금지 · 실명 금지
- 완료 보고는 앞 브리프 §7 두 명령. subject 「writer 완료: 알림 2판 수정 1」 · text 「[worker_done] writer 알림 2판 수정 1 완료 — <한 줄>」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
