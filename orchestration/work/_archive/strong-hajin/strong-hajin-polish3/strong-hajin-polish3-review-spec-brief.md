# [reviewer] 고도화 3차 SPEC 반영 검수 — planner 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. **너는 이 작업의 맥락이 없다** — 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` 등)

이번 모드: **planner 리뷰**(문서). **read-only** — 문서·코드를 한 글자도 고치지 않는다. 산출물은 리포트 한 장.

## 1. 대상

문서 레포(코디 워크트리) `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화` 의 미커밋 diff:

```bash
git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화 diff -- para/projects/summer-star/strong-hajin/20-spec/
```

(`30-work/`·`orchestration/` 의 변경은 코디 것 — 대상 아님)

## 2. 기준 (SoT)

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/_RESUME.md` §1·§2 — 사용자와 닫은 결정(2026-10-04 행 전부: a~g · R3 · R4 · R5 · 완료 확인창)과 원문
- writer 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/strong-hajin-polish3-write-brief.md` §2 — 반영 지시
- 사실 근거(지금 코드): 같은 폴더 `be-survey-report.md` · `fe-survey-report.md`

## 3. 볼 것

1. **충실도** — 결정이 **빠짐없이, 더하지 않고** 반영됐나. 결정별 반영 위치와 일치 여부. 결정에 없는 계약을 SPEC 이 새로 세웠으면 FAIL. 특히:
   - 헤더 = 제목 + `⋯`(요청자 제안 두 개만) + `×` · 머리글·상태 칩·버전 배지·편집·AX 단추가 헤더에 **남아 있지 않은지**
   - 메타 정보 행(진행 상태·버전·담당·실제 시작일·시작 예정일·마감일·출처)과 읽기 전용/편집 가능 구분
   - 인라인 즉시 저장: 안 바뀌면 요청 없음 · 실패 시 복원 · **직렬 저장과 version 이어받기 · 422 처리** · 「변경 저장」 없음
   - 상태 셀렉트: 허용 전이만 · 사유 필수/선택이 서버 규칙(be-survey §4-5)과 일치 · 작은 모달 · 요청 업무 완료 = 완료 보고 모달 · 미완 체크리스트 확인창 유지
   - 담당 = `/reassign` 제안(수락 전 기존 담당 유지) · 「변경 제안 중」 · `task.assign` 없으면 읽기 전용
   - 「진행과 판단」 구역 삭제 + 걸린 일 상자(fe-survey §4-3 의 구획이 **하나도 빠지지 않고** 갈 곳이 있나 — 담당자 변경 단추 제외)
   - AX 묻기 삭제(대체 입구 없음) · 출처 「AX 제안 · 판단 보기」 · 홈·캘린더는 글자만
   - 선행 막힘 배너·푸터 문구 삭제 + 409 토스트 + 셀렉트 원복
   - 읽기 전용 입구에서 편집 요소 전부 꺼짐
   - 여백은 업무 상세만
   - R3 회의 제목(참석자·예정/완료만 · 후보 [적용]) · R2b 데스크톱 첨부 저장(앱 화면 유지 · macOS 실기 · Windows pending) · R1 로그인
2. **삭제되는 계약의 잔재** — 기존 SPEC(007 외 001·003·002·004 포함)에 상세 「편집」·「변경 저장」·푸터 단추(시작·막힘·완료 처리·재개·업무 취소·취소 제안·조건 변경 제안·완료 보고)·「진행과 판단」·AX 단추·「시작할 수 없습니다」를 말하는 문장이 **고쳐지지 않고 남아 있나** — grep 으로 전부 센다
3. **충돌** — 고친 문장과 고치지 않은 다른 절이 서로 다른 말을 하지 않나(같은 SPEC 안, SPEC 사이)
4. **서버 계약 발명** — 이번 판은 서버 변경이 없다. SPEC 이 없는 API·필드(예: 허용 전이 목록 응답, 선행 막힘 플래그)를 새로 요구하면 FAIL
5. **인수조건** — 바뀐 계약마다 AC 줄이 있고 검증 가능한가. 삭제된 것도 「없다」 AC 가 있나
6. **형식** — 버전·변경 이력·결정 근거 열·frontmatter. 실명·메일 0건
7. **조용히 통과하는 자리** — 취소선 옛 문장이 유효한 것처럼 읽히는 곳, 참조 절 번호가 틀린 곳
8. **writer 가 연 Open Questions — 코디가 기본값으로 닫았다(2026-10-04).** 재수정 판에서 SPEC 에 반영한다. 아직 OQ 로 남아 있는 것은 FAIL 이 아니다. 대신 이 답과 **어긋나는 문장**이 있으면 지적한다:
   - OQ-711 → 「마감일 초과」 배지는 메타 정보 **마감일 행 값 옆**(danger 배지) · 겹친 상세의 「뒤로」 단추는 헤더 **제목 왼쪽** 그대로(내비게이션이라 남긴다)
   - OQ-712 → 날짜 행 순서 = E2E-5(시작 예정일 → 실제 시작일 → 실제 종료일 → 마감일)
   - OQ-709 → 맞다. 화면은 미리 막지 않고 서버 409 문장 토스트가 유일한 안내
   - OQ-T12 → 첨부는 **OS 다운로드 폴더에 대화상자 없이 저장**, 성공·실패를 앱 토스트(또는 셸 알림)로 알린다. 같은 이름이면 덮지 않고 번호를 붙인다
   - OQ-T13 → 이번 범위 밖(결정 g 는 첨부만). 다만 macOS 실기 확인 때 인라인 `_blank` 링크가 앱 화면을 덮는지 함께 보고, 덮으면 사용자에게 다시 묻는다(SPEC 에는 pending 으로)
   - 회의 제목·내보내기 단추 크기·로그인 문구는 SPEC 없이 WP 에만 둔다(코디 판단)
9. writer 의 그 밖 판단(실제 종료일·결재·참조 읽기 전용 행 유지 · 빈 날짜 행 표시 · 서버 허용표를 따르면서 생기는 차이 — 완료 업무에 취소 없음, 요청자에게 시작·막힘·완료 없음 · 담당 셀렉트는 내 업무에서 연 상세만) — 결정과 어긋나지 않는지 의견

## 4. 판정

FAIL(결정과 다른 것이 적혔다 · 충돌 · 발명) · WARN(모호) · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-spec-report.md` ← 이 파일 하나만

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

```bash
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: 고도화 3차 SPEC 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / OQ 의견 / 리포트 경로"

orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] reviewer 완료 — SPEC 검수 <판정>. 리포트 review-spec-report.md" --enter
```
