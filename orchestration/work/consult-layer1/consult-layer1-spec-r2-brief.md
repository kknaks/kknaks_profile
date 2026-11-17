
# [planner] SPEC-001 0.2.0 · WORK-001 개정 — 페이스북 메신저 포함 · 채널 칸 · reaction · 폴더 밖 JSON

너는 **consult-analysis `planner` 워커**다. 앞 태스크(SPEC-001 0.1.0 · WORK-001)를 쓴 그 워커다. 역할 문서는 그대로:
`/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석/orchestration/roles/consult-analysis/planner/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석` (코디 워크트리 · allowed_paths 밖 금지)

## 1. SSOT

- `para/projects/summer-star/consult-analysis/10-decision/decision-001-two-layers.md` — **D-12 ~ D-15 새로 추가됨**(코디). 네 OQ 답이 여기 있다
- `para/projects/summer-star/consult-analysis/00-baseline/baseline-001-consult-data.md` — 페이스북 「대화 없음」 정정됨
- 네가 쓴 `20-spec/spec-001-layer1-schema.md` 0.1.0 · `30-work/work-001-layer1-load.md`
- 원본 `reference/2026-11-16-linky-data/` (read-only) — 이번엔 `this_profile's_activity_across_facebook/messages/` 까지

## 2. 무엇을 바꾸나 — 결정 요약

| OQ | 답 | DEC |
|---|---|---|
| OQ-101 | **A** — `reaction` 다섯 번째 테이블 채택 | D-12 |
| OQ-102 | **A** — 폴더 밖 대화 JSON 1개 싣는다 | D-13 |
| OQ-103 | **B** — 페이스북 메신저도 같은 1층에 | D-14 |
| (새) | **채널 칸** — 방마다 어느 메신저로 들어왔는지(인스타그램 / 페이스북 메신저). 원본 폴더 위치로 정해지는 사실 = 1층 | D-15 |

## 3. 계약 — SPEC 0.2.0 에 들어가야 할 것

1. **범위 §1** — 인스타그램(방 폴더 510 + 폴더 밖 1) + 페이스북 메신저(`inbox` · `filtered_threads` · 그 밖에 있으면 전부). 페이스북 쪽 비대화 파일(설정 3 · `stickers_used/`) 처분도 Out 표에
2. **채널 칸** — `conversation.channel`(이름 · 값은 네가 정하되 CHECK · 원본 경로에서 정하는 규칙 명시). 보관함 값(`box`)에 `filtered_threads` 추가
3. **원본 키 대응표 §3 을 두 채널 합쳐 다시 센다** — 페이스북 쪽 키 전부(`sticker` 포함 · 안쪽 키까지). 기준 그대로 「담을 칸 없는 원본 키 0」. 채널마다 건수를 따로 적는다
4. **우리 계정 판별 §4.3 을 채널별로** — 채널마다 「그 채널 모든 방에 공통인 이름 1개」. 계정명은 여전히 어디에도 쓰지 않는다
5. **방 키** — 두 채널 `thread_path` 가 겹치지 않는지 실측. 겹칠 수 있으면 (channel, thread_path) UNIQUE. 대체 키 순서 §4.5 에 channel 을 반영(다시 돌려도 같은 id)
6. **폴더 밖 JSON 규칙**(D-13) — 방 찾기 · `source_file` · G-4 대조 방식
7. 페이스북 쪽 이중 인코딩 · 시각 · 방당 파일 수(`message_2.json` 이상 있는지) · 내림차순 · 같은 이름 다수 방 — 인스타그램과 같은 실측을 채널별로
8. **건수 기준 §7 다시** — 채널별 줄 + 합계 줄. `reaction` 은 이제 정식(R-*). 「OQ-101 승인 전제」 표기 제거
9. §9 — OQ-101 ~ 103 은 닫힘으로(D 번호). 새로 열린 것이 있으면 옵션 + 권장
10. 변경 이력에 0.2.0 행

WORK-001: 범위 밖에서 페이스북 제거 · 선행 OQ 제거(이제 발주 가능 상태) · 수용 기준에 채널별 건수 일치 · 테이블 다섯 개.

## 5. allowed_paths

- `para/projects/summer-star/consult-analysis/20-spec/`
- `para/projects/summer-star/consult-analysis/30-work/`

## 7. 하지 말 것

- DEC · BASE · README 수정 금지(이상하면 보고)
- 2층 설계 금지 · 스크립트 작성 금지
- 고객 이름 · 계정명 · 본문 · 폴더명을 문서에 쓰지 않는다. 원본을 읽는 Python 은 `python3 -I` · 레포에 임시 파일 남기지 않는다

## 8. 검증

- 두 채널 합친 원본 키 경로 수 = 대응표 처분 수(누락 0) — 수치 보고
- §7 의 모든 수가 네가 원본에서 직접 센 값
- 고객 이름 grep 0 — 두 채널 `participants[].name` 전체 + 두 채널 우리 계정명을 메모리에 올려 SPEC · WORK 에 나오는지 검사, 0
- 인덱스(`20-spec/README.md` 버전 칸) 갱신

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] planner: <질문>" --enter`
