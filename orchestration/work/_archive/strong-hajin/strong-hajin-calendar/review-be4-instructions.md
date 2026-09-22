# [reviewer] Phase BE-4 코드 검수 — 회의 도메인을 연 판

너는 **strong-hajin `reviewer` 워커**다. **앞 검수를 한 워커는 죽었다 — 너는 맥락이 없다.**
먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md`·`skills.md`·`tools.md`·`workflow.md`)
- 앞 검수들이 무엇을 보았는지 — `review-be3-report.md`(281줄, **바로 앞 판**) · `review-spec-004-v2-report.md`

작업 워크트리(읽기 전용 검증용): `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

**완료 보고** — 끝나면 이 한 줄:

```bash
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac   --text "[worker_done] reviewer BE-4 검수 완료 — <판정과 한 줄>" --enter
```

본문에 판정(FAIL/WARN/PASS)·근거·지적을 담아라. 막히면 같은 방식으로 `[질문]`.


대상: 코드 워크트리의 **uncommitted diff** (수정 11 · 신규 2). BE-3 은 커밋됐다(`bc3b5d8`).
리포트: **새 파일** `review-be4-report.md`. read-only. **테스트 돌리지 마라 — 내가 돌렸다.**

기준: SPEC-004 **v0.3.1 §2.9** · DEC-003 **증보 8~10 (K22 · K25~K30)** · WORK `Phase BE-4`.

## 코디가 확인한 것

- allowed_paths 위반 **0건** (`backend/` + 허용한 `docs/` 둘만)
- **운영 대장 `git diff` 0줄** — 워커 주장(`approval` 은 `http_signature` 에 안 든다)이 맞다
- `make test-unit` **369 passed / 0 failed** — `test_operation_inventory` 포함 통과
- 워커 보고: `test-contract` 1158p/2f · `test-postgres` 102p/0f

## 코디가 이미 정한 것 — 지적하지 마라

- **K28** `MeetingInfoPatch.validate_times` 의 `astimezone(UTC)` 추가는 **내가 지시했다.**
  워커가 「밀린 값을 단언하는 테스트 없음」을 전수 확인한 뒤 고쳤다
- **K29** `meetings_visible_to` 의 SQLite tz 는 **남기기로 했다** — 손 안 댄 것이 맞다
- **K30** 참석자만 추가하는 것은 검사를 안 지난다 — **사용자가 「이번 판은 그대로」로 확인했다**

## 볼 것 아홉

1. **문이 하나인가** — 회의 쪽이 `overlapping_blocks` 를 쓰고 **규칙을 다시 쓰지 않았나**.
   반열림·자정 분할이 회의 쪽에 복사돼 있으면 FAIL.
2. **`member_ids` 가 주최자 + 활성 참석자 전원인가.** 제거된 참석자(`removed_at`)가 섞이지 않나.
   **사외 참석자가 구조적으로 빠지나.**
3. **`quick_start` 가 정말 안 걸리나** — 워커가 「`_validated_creation` 을 안 지나서 구조적으로
   제외」라고 한다. **분기가 없으니 맞는지 코드로 확인하라.** 그리고 워커가 남긴
   「그 리팩터가 오면 잡는 테스트」가 실제로 그 일을 하나.
4. **시각이 안 바뀌면 검사를 안 지나는 것이 옳은가** — 워커 판단이다. 안 걸면 이미 겹친 회의의
   제목조차 못 고친다(K22 「검증은 새 쓰기에만」). **시각과 참석자가 같이 오면 바뀐 뒤의 명부로
   묻는가.**
5. **※1 회귀 수정이 정당한가 — 이게 제일 중요하다.** 워커가 **검수 census 밖에서 실제 회귀를
   찾아 고쳤다**: 방예약 갈래에서 겹침 관문이 provider 호출 앞에 있어, **재전송이 원장 영수증에
   닿기 전에 자기가 첫 시도에 세운 회의와 겹쳐 409** 가 됐다. 고친 방법은
   `validate_creation(ignore_meeting_id=attempt.meeting_id)`.
   - **K12 를 회의로 들여온 것이 아닌가** — 워커는 「있는 원장을 안 깨는 것」이라 한다. 맞나
   - **관문을 앞에 둔 채 자기만 뺀 이유**(빼면 고아 예약이 남고 거두는 호출이 없다)가 서는가
   - `_release_orphan_reservation` 이 정말 호출자가 없나
6. **`approval`** — 목록·상세와 **같은 함수·같은 어휘**인가. `derived` 묶음 전체를 안 싣나.
   열을 안 만들었나. **한 질의인가**(N+1 아닌가).
7. **WARN-2 수정** — `meeting_id.in_()` 한 질의로 바뀌었나. **계약이 안 갈렸나**
   (BE-3 테스트 19건 그대로 통과).
8. **기존 회의 계약 회귀** — 목록 두 모양 · 기간 갈래 행 필드 · 열람 권한 · 생성 응답 모양.
   워커가 회귀 테스트를 남겼다는데 **실제로 그것들을 재나.**
9. **조용히 통과하는 자리.** 특히 ※2 — `test_meeting_core` 셋업을 갈라 둔 것이
   그 테스트가 재던 것을 약화시키지 않았나. **같은 자리가 더 있는지 세라**
   (워커는 「전수 확인, 없다」고 한다).

## 판정

FAIL 은 계약과 다른 것이 도는 자리·경계 위반·증명 없음에만.
WARN 은 **FE-3 브리프에 실을지**를 적어라.
