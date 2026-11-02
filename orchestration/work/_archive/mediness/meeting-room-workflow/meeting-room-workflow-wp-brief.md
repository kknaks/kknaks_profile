
# [planner] WP 작성 — 예약 승인 → 회의 자동 등록 체인 착지 작업서 (+ 경미 2건 정리)

너는 **mediness `planner` 워커**다. 네가 쓴 SPEC-151 §7.9(R2)가 검수 PASS + 사용자 승인을 받았다. 이번 발주는 **구현 WP 작성**과 **검수 잔여 경미 2건 정리**다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (네 미커밋 변경 위에서 계속)

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §7.9 ← 계약. **WP 는 이 계약을 착지시키는 작업서다 — 계약을 다시 정하지 마라.**
- `products/mediness/20-spec/spec-031-meeting-v2-diarization.md` §3 역방향 가산
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report-r2.md` — 경미 3건과 「WP 몫」으로 넘긴 항목들
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/research-meeting-create-flow.md` — 현행 코드 좌표(파일:줄)
- 기존 WP 표준형: `products/mediness/30-work/` 의 최근 WP 1~2개 (예: work-099)를 형식 표본으로

## 2. 만들 것

**① 구현 WP 1건** — `products/mediness/30-work/work-NNN-<slug>.md` (NNN 은 레포의 다음 빈 번호, slug 는 관례대로). 담을 것:

- 착지 범위: BE 중심 — (a) 승인 실행 성공 훅에서 체인 발동(source 판정 포함), (b) participants 이메일 → organization_member 역해소(정방향 술어 재사용), (c) meeting_v2 + attendee + 연결을 한 DB 트랜잭션으로 저장, (d) 실패 시 보상(THE CONNECT 예약 취소) + 카드 표기, (e) 수정·취소 파급(예정 일시 갱신 · 대기 회의 soft delete · live/ended 연결 끊기), (f) 카드 facts·채팅 완료 안내 표면(FE 몫 있으면 분리 표기)
- 스펙이 WP 몫으로 넘긴 확인·결정 항목들을 태스크로: 「예약 건당 회의 최대 1」 보증 수단(유니크 제약 vs 생성 직전 조회) · participants 실제 필드 형태 실측(W-4) · §7.2 참석자 해소 컬럼 서술과 코드 실측 대조(R1 주의점 ①)
- 수정 파일 후보는 조사 리포트의 좌표를 근거로 적되, 줄번호 단정 대신 심볼 위주로
- 테스트 계획: 조합표 A~D 각 행 + 동기화 상태 분기 + 멱등 재진입
- 30-work.md 3자 동기: WP List · Status Board · Spec Coverage 에 이 WP 를 등재 (상태는 착지 전 값 — 레포 관례대로)

**② 경미 2건 정리** (검수 R2 리포트 잔여):

- SPEC-151 변경 노트 ⑭·log 첫 문장의 「가산 4줄」 라벨을 실제 수치로 갱신
- SPEC-031 변경 파급 bullet 에 「진행 중·종료 회의 제외 — §7.9.5」 구절 추가 (형제 취소 파급 bullet 과 대칭)

log.md 에 wp-add 행 1건 추가 (PR 칸은 «—» 유지 — 코디가 PR 후 채운다).

## 3. 하지 말 것

- §7.9 계약 본문 재개정 금지 (경미 2건 문면 정리 제외). 코드 작성 금지. 커밋·push 금지.
- WP 에서 계약을 확장하지 마라 — 스펙에 없는 동작을 작업 항목으로 만들지 않는다.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0 + WP List·Status Board·Spec Coverage 3자 일치 통과. 1회만
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
  --body "WP 파일명·구성 / 경미 2건 처리 / 3자 동기 / lint 결과 / 미결"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] planner: <질문>" --enter`
