
# [planner] 수정 R2 — 리뷰 FAIL 2건 해소 (SPEC-031 모순) + WARN 2건

너는 **mediness `planner` 워커**다. 직전에 네가 만든 SPEC-151 §7.9 신설분이 reviewer_spec 검수에서 **FAIL** 났다. 원 브리프의 계약·범위는 그대로이고, 이번 발주는 **리뷰 지적 해소만** 한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (네 미커밋 변경 위에서 계속)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report.md` ← **이번 발주의 SoT.** V-1·V-2 의 「자리」·「권장 수정」이 구체적으로 적혀 있다.

## 2. 고칠 것

**V-1 (FAIL)** — 30분 슬롯의 소유 자리 정합:
- SPEC-031 §Validation 의 `scheduled_start`/`scheduled_end` 행과 §케이스 매트릭스 시간 행에 **경로 단서**를 박아라 — 슬롯은 `POST /meetings-v2` 요청 스키마 규칙이며 예약 발 자동 등록 경로에는 적용하지 않는다(§3 가산 참조).
- SPEC-151 §7.9.2 의 「모달 입력 폼의 검증」 문면을 「모달 경로 **요청 스키마**의 검증(도메인 CHECK 는 `HH:MM`·`종료 > 시작` 둘)」로 정정. SPEC-031 §3 가산 bullet 의 같은 표현도 맞춘다.

**V-2 (FAIL)** — 회의 쪽 처분 2종의 자리를 SPEC-031 에 세운다:
- SPEC-031 §3 가산에 (a) 예약 변경 파급으로 **예정 일시가 서버에 의해 갱신된다**(사용자 수정 표면은 여전히 `PATCH visibility` 하나), (b) 대기 회의의 「닫는다」가 **정확히 어떤 처분인지** 를 못박아라. 회의 도메인엔 이미 soft delete(`deleted_at`)가 있다(조사 리포트 §3-a) — state enum 에 값을 새로 만들지 말고 기존 도메인 어휘 안에서 정하라. 기존 어휘로 표현이 안 되면 만들지 말고 §9 방식으로 물어라.
- `:1387`(예정 시간 변경 기능 없음)·`:1388`(회의 취소 계약 없음) 두 기존 bullet 에 「예약 발 자동 등록 경로는 예외 — §3 가산」 단서를 달아라.
- OPEN-031-Y 인용을 실제 범위(회의 취소 3표면)에 맞춰 정정 — 「채팅 표면 중 예약 → 회의 방향만 이번에 정한다」.

**W-1 (WARN)** — §7.9.1 「예약 건당 회의 최대 1」 인용 정정: SPEC-031 인용은 「회의당 최대 1」로 줄이고, 「예약 건당 회의 최대 1」은 **이 절이 새로 세우는 불변식**임을 명시(유니크 제약 필요 여부는 WP 몫으로 표기).

**W-2 (WARN)** — §7.9.4 조합표에 「체인이 끝날 때까지 실행 축은 «진행 중» 에 머문다(외부 예약 성공 시점에 «성공» 을 적지 않는다)」 한 줄을 못박아라.

W-3(log PR 칸)은 PR 생성 후 코디가 채운다 — 손대지 마라. W-4(participants 필드 형태 실측)는 WP 몫 — 스펙에 확인 항목으로 한 줄만 남겨라.

## 3. 하지 말 것

- V·W 해소 외의 개정 금지. §7.9 의 계약 본문(확정 6건 반영분)을 재구성하지 마라.
- 코드·WP 작성 금지. 커밋·push 금지.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0 (타 제품 기존 WARN 무관 분리). 1회만
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "V-1·V-2·W-1·W-2 각각 어디를 어떻게 고쳤나 / lint 결과 / 미결"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] planner: <질문>" --enter`
