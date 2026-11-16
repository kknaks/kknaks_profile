
# [planner] SPEC 0.9.4 · WORK — 끊김 값 바꿈(D-67)

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디 워크트리를 그대로 쓴다. 코디가 `10-decision/` 에 D-67 을 이미 적었다 — 그 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-67**(이번 결정 · 줄 123) · D-47 · D-55 ← 근거. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` §5.10(줄 1344 ~) · §9.1 「통역」 · §9.6 「배포 뒤 확인」 · §10 OQ-027 · 부록 A · 변경 이력
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP25(배포 행 — 모양 참고)
- 공식 문서(이미 확인됨 · 인용은 이 문장만): `https://docs.soniox.com/stt/rt/endpoint-detection.mdx` — `max_endpoint_delay_ms` 500 ~ 3000 · 기본 2000 · 상한(「maximum time Soniox can wait before returning an endpoint after speech has ended」) / `endpoint_sensitivity` -1.0 ~ 1.0 · 기본 0.0 · 「Lower values make endpoints less likely. This can help Soniox wait longer before finalizing, which is useful when users pause frequently or speak slowly.」

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

운영(back main `6d57ba3` · 시드 `.10`)은 `max_endpoint_delay_ms: 1000` 만 보내고 `endpoint_sensitivity` 는 안 보낸다. 2026-11-16 실기기 zh 세션에서 손님 쪽 발화가 문장 중간에서 잘렸다(6건). 반이중 때문에 잘린 뒤의 말은 버려졌다. D-67 로 운영 값을 **`max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3** 으로 바꾼다(`endpoint_latency_adjustment_level` 은 그대로 안 보냄). 끼어들기(재생 중 받아쓰기)는 이번 범위가 아니다.

## 3. 계약

해당 없음(WS 메시지 · env · 허용 경로 · front 그대로).

## 4. 먼저 읽을 핵심 파일

- SPEC §5.10 「끊김」 표 · 「공식 문서의 끊김 값」 표의 「지금」 칸
- SPEC §9.1 「통역」 의 STT 설정 시험 줄(기본 설정에 `endpoint_sensitivity` 가 없다고 고정한 시험이 있으면 그 줄)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 할 것

1. SPEC **0.9.4**(front matter `version` · `updated_at` 2026-11-16 · 변경 이력 맨 위 한 줄).
2. §5.10 제목 · 끊김 표: 운영 값 = 2000 · -0.3(D-67) 행을 더하고, D-55 「1000 유지」 행은 「D-67 로 뒤집힘」 이 보이게 남긴다(지우지 말 것). 「공식 문서의 끊김 값」 표 「지금」 칸 갱신 · 확인 날짜 2026-11-16. 「다른 끊김 값은 보내지 않는다」 류 문장 전부 grep 해서 D-67 에 맞게.
3. §5.10 「그 밖의 STT 설정」 행의 키 목록에 `endpoint_sensitivity` 가 더해짐을 반영.
4. §9.1 시험 줄: 기본 `stt_config` 가 `max_endpoint_delay_ms: 2000` · `endpoint_sensitivity: -0.3` 을 보내고 `endpoint_latency_adjustment_level` 은 안 보냄을 고정.
5. §9.6 에 「배포 뒤 확인 0.9.4」 줄: 새 pod 기동 · 시드 `.10` 로그 · **사용자 실기기 zh 대화 1회**(손님 쪽 문장 중간 잘림이 줄었는지 · 말 끝 → 자막 지연 체감) · 기록은 수치만(문장 0).
6. §5 · §9 제목의 D 목록 · 부록 A 에 D-67. OQ-027 행에 D-67 로 다시 열고 닫았음을 한 줄.
7. WORK: `work-001` 에 **WP28**(back — 끊김 기본값 2000 · -0.3 · 시험 고침 · 주석 「= Soniox 기본」 오기 바로잡기) · **WP29**(배포 · 실기기 확인 — WP25 와 같은 절차: Actions sha → infra `values-prod` back 이미지 태그 PR만 → ArgoCD 수동 sync → §9.6 0.9.4) 두 행. `updated_at` · 「열린 것」 필요하면.

## 7. 범위 제약 — 하지 말 것

- DEC · 코드 · 시드 · `orchestration/` 은 건드리지 않는다.
- 끼어들기 · 반이중 변경 · 다른 끊김 값은 쓰지 않는다(D-67 에 없음).
- 실기기 기록 문장을 어디에도 옮기지 않는다(PUBLIC 레포).

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
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
