# [planner] 통키 통역 기록 — 7일 삭제를 env 로 빼고 기본 「삭제 안 함」(DEC D-42) · SPEC 0.7.0 · WORK WP19 · WP20

너는 **interpret-pwa `planner` 워커**다. 앞 맥락은 없다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승 — 코디와 같은 트리. `reference/` · `orchestration/work/` 의 다른 파일은 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다) · ⚠ **PUBLIC 레포** — 키 · 계정값 · 실명 · 통역 기록 문장 0

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` — **D-42**(98줄, 이번 결정) · D-41(97줄). 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` (지금 0.6.1) — 고칠 문서
- `para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` — WP18 까지. WP19 · WP20 을 더한다
- 코드(읽기만): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` (main `17c26b5`) — `back/app/service/records.py`(28 `KEEP_DAYS` · 132 `sweep` · 155 `sweep_forever` · 235 기동 로그) · `back/app/main.py:70-85`(삭제 배경 작업) · `back/tests/test_records.py:320-424`(7일 삭제 시험)

**기대는 개념**: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

통키 통역 기록(D-41 · SPEC §5.9)은 날짜별 JSONL 을 back PVC 에 쓰고 **7일 뒤 지운다**(기동 1회 + 24시간마다). 7일은 코디 기본값이었고 env 로 못 바꾸게 고정했다.
지금 베타 테스트 기간이라 데이터를 모아야 해서 사용자가 「7일 보관 없애자」로 정했다(D-42). 보관 기간을 env 로 빼고 **비어 있으면 삭제하지 않는다** — 베타가 끝나면 값만 넣어 다시 켠다.
운영 서버에 지금 11-11 ~ 11-14 파일이 있고 **11-11 파일은 11-18 에 지워진다** — 그 전에 배포가 목표다.

## 3. 계약 (코디가 정함 — 이대로 SPEC 에 쓴다)

| 항목 | 값 |
|---|---|
| env | **`INTERPRET_RECORD_KEEP_DAYS`** (back · §2.4 표에 행 추가) |
| 비어 있음 / 없음 | **삭제 안 함** — 기동 때 삭제 0 · 24시간 배경 작업을 **만들지 않는다**. 기동 로그 `interpret records: on dir=<경로> keep_days=off` |
| 양의 정수 N | 지금 규칙 그대로, 7 자리에 N — 이름이 정확히 `YYYY-MM-DD.jsonl` 이고 날짜 ≤ 오늘(한국 시간) − N 인 파일 삭제 · 기동 1회 + 24시간마다 · 로그 `keep_days=N` |
| 그 밖의 값(0 · 음수 · 숫자 아님) | **경고 로그 1줄 뒤 삭제 안 함**(`keep_days=off`) — 기동은 멈추지 않는다(기록은 통역의 부속 · §5.9 기동 ③과 같은 결) |
| 기록 끔(`INTERPRET_RECORD_DIR` 비었음) | 지금처럼 파일 · 삭제 작업 없음 — KEEP_DAYS 값과 무관 |
| 운영 | ConfigMap 에 **넣지 않는다**(= 삭제 안 함). infra 는 이미지 태그만 바뀐다 |
| 그대로 | D-41 의 나머지(넣는 것 · 안 넣는 것 · 화면 · API 없음 · 꺼내기 kubectl · 허용 경로 6개) |

## 4. 먼저 읽을 핵심 파일 (SPEC 안 「7일」이 나오는 곳 — 전부 grep 으로 다시 세라)

- SPEC 머리 `version` · 개정 이력 표(62줄 위에 0.7.0 행) · §1(85줄) · 디렉토리 설명(103줄) · §2.4 env 표(149줄) · §5.9(748줄 ~ — 756 · 757 기동 · 807 ~ 815 「7일 뒤 삭제」 · 보관 기간) · §9.1 「기록」 ⑨(1045줄) · §9.3 주(1122줄) · §9.6 크기 근거(1175줄) · 배포 뒤 확인(1196 · 1202줄) · 끝의 DEC ↔ 절 대조표(D-41 행 근처에 D-42)
- `grep -n "7일\|keep_days\|KEEP_DAYS\|D-41" spec-001-interpret-pwa.md` — 이 목록이 고칠 자리 전부인지 **스스로 전수 확인**하고 보고에 줄 번호 목록을 붙여라

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 구현 단계

1. **SPEC 0.7.0** — 머리 `version` · `updated_at` · 개정 이력 행 · 근거 목록의 「D-01 ~ D-41」 → 「D-01 ~ D-42」
2. §5.9 「7일 뒤 삭제」 절을 「보관 기간 — env(D-42)」로 다시 쓴다(§3 표 그대로) · 기동 ②④ · 로그 문구 · 보관 기간 행(「7일 고정 — env 로 바꾸지 않는다」 지움)
3. §2.4 env 표에 `INTERPRET_RECORD_KEEP_DAYS` 행(설명 · 비었을 때 = 삭제 안 함 · 근거 D-42) · §1 · 디렉토리 설명의 「7일」 문구
4. §9.1 「기록」 ⑨ 시험을 계약대로: 비었음 → 삭제 0 · 배경 작업 없음 · 로그 `keep_days=off` / N=7 → 지금 ⑨ 그대로 / 잘못된 값(0 · `-1` · `abc`) → 경고 1줄 · 삭제 안 함 · 기동 성공
5. §9.6 크기 근거(보관 무기한 → 하루 수십 KB 실측 · 1Gi 여유 — 실측 수치: 11-11 ~ 11-14 4일에 44KB) · 배포 뒤 확인을 0.7.0 용으로(기동 로그 `keep_days=off` · 재시작 뒤 가장 오래된 날짜 파일이 그대로 남음 · 표면 그대로) — 0.6.x 의 확인 결과 기록은 지우지 말고 둔다
6. **WORK** — WP19(back: §5.9 0.7.0 · 시험 · `.env.example` 이름만 · 검증 명령은 WP16 형식) · WP20(배포 · 실물: main sha → infra 태그 PR → 수동 sync → §9.6 0.7.0 확인 · **11-18 전**) 행 추가 · 머리 인용 블록에 이번 fix 한 줄 · 「병렬」/「주의」에 필요한 것만
7. 문서 README · `log.md` 갱신이 규칙(role 문서)에 있으면 따른다 — 없으면 하지 마라

## 7. 범위 제약 — 하지 말 것

- DEC 문서는 고치지 마라(코디 소유 — D-42 는 이미 들어가 있다)
- 코드 · infra 레포는 읽기만
- §3 계약 밖의 정책(보관 기간 기본값 · 용량 경보 · 압축 등)을 짓지 마라 — 필요해 보이면 §10 OQ 로 올리고 보고
- 통역 기록 문장 · 운영 파일 내용을 문서에 넣지 마라(수치만)

## 8. 검증

```
SPEC 의 모든 절이 DEC · 확정 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 계정값 · 실명 0(grep)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_0965e26d-1c74-41c6-82cb-1c70ff704a68 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
