
# [planner] SPEC 0.9.5 리뷰 수정 — FAIL-1 · WARN-1 ~ 8 (D-70 ④)

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디 워크트리를 그대로 쓴다. 코디가 `10-decision/` 에 D-67 ~ D-69 · BASE-001 입력 6 을 이미 적었다 — 그 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-spec-095-report.md` ← 고칠 목록(FAIL-1 · WARN-1 ~ 8 · 줄 번호)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-70**(① 문장 고침 · **④ 리뷰 처분**) ← 처분의 근거. 여기 없는 정책 금지.
- 네가 쓴 SPEC 0.9.5 · WORK WP30 ~ 32(코디 워크트리 · 미커밋)

## 2. 처분(코디 · D-70 ④) — 이대로 고친다

- **FAIL-1**: 마이크가 닫힌(멈춤 중) 동안 끝난 재생 구간은 여유 없이 끝 = 시작. 지난 구간 30초 보관은 서버 시계. §9.1 에 「멈춤 중 재생이 끝난 뒤 `resume` — 재생 쪽 언어 첫 토큰이 남는다」 시험 한 줄.
- **WARN-1**: D-70 을 SPEC(머리 D 목록 · §5.13 제목 · OQ-037 ~ 039 닫음 · 부록 A) · WORK 에 반영. OQ-037 은 「말하던 사람의 차례 중」 으로(DEC ① 고친 문장).
- **WARN-2**: 끼어들기 멈춤 순서 = front 에 `audio_stop` **먼저** → 큐 비움 → TTS 스트림이 **아직 진행 중일 때만** `cancel` · `terminated` 기다림에 한도(상수 · 넘으면 로그 1줄 · 연결은 그대로). 이미 끝난 스트림엔 `cancel` 없음. ㉘-4 실물 조건도 그에 맞게.
- **WARN-3**: 감수 — `playback_stopped` 가 오가는 사이 back 이 이미 보낸 다음 발화는 재생될 수 있다고 그 자리에 적고 §9.6 실기기 확인 항목에.
- **WARN-4**: 「끝」 은 여유 없는 값으로 하나만 정의하고, 여유는 판정식에서 한 번만 더한다(시험 문장도).
- **WARN-5**: agent text 대상 = 재생 위치 기준 · 같은 차례의 다음 발화 글자도 0.7초 앞서 보낸다(공식 「about 500 ms to 1 second ahead of playback」). 시험 ⑫ 에 발화 경계.
- **WARN-6**: 반이중 잔재 문장(`spec:1801` · `spec:1852` · `spec:1383` 등)은 취소선 + 0.9.5 문장으로 바꾼다. WP31 이 §7.4 만 읽어도 맞게.
- **WARN-7**: 리포트 수치로 바로잡기(되울림만 8 중 7 재생 쪽 0 · 겹침 6 중 5 · 1 세션 0.30).
- **WARN-8**: 표시된 기본값은 D-70 ④ 로 받아들였다 — 「기본값」 표기 옆 근거에 D-70 을 단다.

## 3. 계약

WS 메시지 이름 · 모양은 그대로(`audio_stop` · `playback_stopped`). 바뀌는 건 순서 · 정의 · 시험뿐.

## 4. 먼저 볼 것

- 리포트의 줄 번호 자리 전부 · 「끝」 · 「여유」 · `ECHO_TAIL_MS` grep.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 할 것

위 처분만. 판은 0.9.5 그대로(변경 이력 0.9.5 줄에 「리뷰 반영」 덧붙임).

## 7. 범위 제약 — 하지 말 것

- DEC · 코드 · `orchestration/` 수정 금지. 처분 밖 정책 금지.

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
