
# [planner · 마감] SPEC-007 · 006 · 002 · 000 — 화면 확인(B1 ~ B42)으로 바뀐 계약 반영 + Delivery 마감 표시

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다. 이 spec 워크트리는 너 혼자 쓴다(브랜치 `kknaksss/day-reservation2-spec` · PR MediSolveAIDev/mediness#961 · `54bbeb14`).

## 1. 읽을 것

- **화면 확인 목록** `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/e2e-1-feedback.md` — B1 ~ B42(고침 · 철회 · 열림). **고침 행 중 계약(SPEC 문장)을 바꾼 것만** SPEC 에 반영
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D56) · 지금 SPEC-007 · 006 ⑫ · 002 ㉘ · 000 ②(이 워크트리)
- 구현(참고 · read-only): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2`(rebase 중일 수 있음 — `git log` 로 최신 커밋만 읽어라)

## 2. 반영할 것 (계약이 바뀐 행 — 빠짐없이 · B 번호 붙여 개정 이력에)

- B13 등 철회 = 초진 / 재진 = KOS `isNew` 그대로(KOS 는 귀가 처리 때 「신규 환자」를 지움) — SPEC 그대로면 「확인」만
- B14 이전 방문 = 이번 방문보다 앞선 방문 전부(오늘 앞선 귀가 포함 · 취소 · 노쇼 뺌 · 최신 순)
- B15 · B23 · B24 · B26 · B27 관리실 목록 = 접수 구역 방만 · 시술 현황 방 고르기와 같은 모양 · 순서(빈 방 먼저 · 오른쪽 「비어 있음」)
- B16 SSE 다시 그릴 때 화면에 담은 값 유지
- B18 · B19 · B31 · B32 · B33 시술 목록 통일(옵션 머리 › 구성 시술 · n = 전체 − 남음 · 오늘 작업은 시술권 id 로 자기 줄 · 구매 전 수납 필요 시술 포함 · 순서 · 상품 합계 = 구매가 + 구매 전 수납 필요 옵션가)
- B20 상담 대기 관리실 = 「방 배정」 없으면 만들고 지정 · 실패 토스트
- B22 「열」 → 「예약그룹」 · B36 상태 「시술 후」 → 「시술 종료」(문구 바뀜)
- B28 · D53 단계 바꾸기 포함 모든 쓰기 = 보낸 즉시 다시 읽어 확인
- B29 오늘 예약 [접수] 전에도 「시술만 진행」 켜면 「오늘」 체크 · B30 오더 메모 = 시술 목록 아래 · 시술 대기부터 숨김
- B37 · B38 · B39 · B40 상담 정보 칸 없앰 → 바닥 줄 `□시술만 진행 [상담사 ▴] [관리실 ▴] [접수]`(단계별 고름 / 바로 / 비활성) · [예약 취소] = [예약 변경] 옆 · 평소 회색 · 빠진 칸은 누를 때만 깜빡
- B11 · B41 SSE 신호 = 보이는 값이 바뀐 때만 · 다시 받기 합침
- **B42(열림)** = SSE 연결 한도(HTTP/1.1 같은 주소 6개 · 화면당 SSE 2개) — OQ 로 남김(운영 HTTP/2 확인 · 화면당 SSE 하나 후보)
- SPEC-000: migration 번호가 rebase 로 `0026` · `0027` · `0028` 로 바뀜(칸 · 권한 이름은 같음) — 번호를 적은 곳이 있으면 고침

## 3. 그 밖

- `30-work.md` Spec Coverage: SPEC-007 = Delivery #275 ~ #278 **구현 완료**(code PR 번호는 코디가 나중에 채움 — 자리만) · `10-decision.md` 현재 결론 · `log.md` 한 줄
- 열린 OQ 정리: 남은 것만 남기고 닫힌 것은 닫힘 표로
- lint `--strict` products/day 0 error
- **커밋 · push 해서 PR #961 에 얹어라**(머지 금지)

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day 0 error · 반영 표(B 번호 → SPEC 자리)를 보고에
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_b7fbdb1a-d331-489a-908f-f073c4bbc267 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
