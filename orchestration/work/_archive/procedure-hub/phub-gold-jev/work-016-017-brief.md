# [writer] WORK-016 허브 resolve 0.8.1 · WORK-017 앱 상담 0.4 — 구현 계획

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`(+ 같은 폴더 문서). `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`. 허브 `HUB=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD d97a9ad · 읽기만) · 앱 `APP=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(HEAD be1c622 · 읽기만).

## 정본

- 계약: `$W/SPEC-008-consult-entry.md` **0.2.0** · `$W/SPEC-001-hub-gold-mcp.md` **0.8.1**. 검수 `$W/review-spec-008.md`(F 처분은 SPEC 변경 기록).
- 결정: `$W/_RESUME.md` §2 맨 위 11-18 행 전부. 아래 코디 답도 결정이다.
- 꼴 참고: `$W/WORK-014-consult-v03.md`(앱 WORK 꼴 · WP · 시험 목록 · B 표) · `$W/WORK-013-hub-v07.md`(허브 WORK 꼴).
- 시험 · 채점: `$W/research-input-space/scripts/README.md` · `score.py` · `slim.py` · `run_now.py` · `conversations.jsonl`(78 대화 · 356 턴).

## 코디 답(SPEC 남은 정할 것)

- U8-3 옛 끈 대화를 막는 화면 문구 = **빈칸으로 둔다**(문구 짓지 않음 · 자리만 · 사용자 확인 대상 목록에).
- U8-4 E8-6b 문턱 = 추천 ⓐ 90% · ⓑⓒ 100%.
- C8-8 막는 자리 = `rev_changed` 꼴 그대로 · C8-9 `columns/col_b.py` 의 `_labels` · `_end_check` 는 그대로 import 하되, 필요하면 `columns/` 에도 얇은 공개 감쌈(동작 변경 0)을 더해도 된다(F-10 예외를 `columns/` 까지 넓힘).

## 쓸 것

### `$W/WORK-016-hub-resolve-v081.md`
SPEC-001 0.8.1 만: WP(맞춤 꼴 = 정확 일치 · 부분/줄임/덮임 지움 · `abbr` 입력 처분 · MCP 도구 설명 글 · REST/MCP 같음) · **고칠/지울 시험 표(SPEC-001 F-11 표 8 파일 — 파일 · 함수 · 고침/지움 · 새 시험)** · 확인 = 그 시험 파일들 + 실물 18107(띄우고 내림 · 정확 이름 → 코드 · 문장 → 후보 0 · 목록 꼴 820 항목 그대로) · 18105 재시작은 코디 몫(앱 0.4 와 같이). 허브 브랜치 커밋은 코디.

### `$W/WORK-017-consult-v04.md`
SPEC-008 0.2.0 전부: WP 순서(예: WP-0 E8-0 실측(CLI thinking 끄는 법 · 지연) → 목록 적재 · 이해 호출 · 검증 · 객체 · 조회 · 화면 · 장부 · 프롬프트 · 끈 상태 막기 → **E8-pre 채점 스크립트를 0.4 장부 칸에 맞춤**(`research-input-space/scripts/score.py` · `slim.py` · `run_now.py` — 답 LLM 실제 호출 길 포함 · ref.to=answer 5 대화) → 단위 시험 → E8 표 실행). WP 마다 고칠 파일 · 함수 서명(SPEC §3-4 표) · 지울 것(Jev · resolve 맞춤 꼴을 켠 경로에서 부르는 곳 전부 — **grep 으로 다 세어 표**로) · 그 WP 의 시험 파일 목록(전체 pytest 금지 — 그 WP 시험만) · 기존 시험 가운데 바뀌는 것(까닭).
- 완료 조건 = SPEC §8 E8(D-14: 앱 전체 8 검사 90%↑ · 입구 3 검사 95%↑ · 정보 종류 90% · E8-6b ⓐ 90% ⓑⓒ 100%) — **표 실행은 구현 워커가 18224(앱) · 18107(허브 0.8.1)에 띄워 돌리고 수를 보고**, 18105 · 18222 는 건드리지 않는다. 사람 표본 검수(E8-5)는 코디 · 사용자 몫으로 표만 낸다.
- 포트 · 서버 · 커밋 규칙: 구현 워커 커밋 금지(코디) · 18105 · 18222 · 18432 건드리지 마라 · 쓰는 포트는 띄우기 전 `lsof` · 끝나면 내림.
- B 표(SPEC 과 달리 받는 곳 · 열린 것).

## allowed_paths

쓰기: `$W/WORK-016-hub-resolve-v081.md` · `$W/WORK-017-consult-v04.md` 둘만. 코드 · 데이터 · 서버 · LLM 호출 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(WORK-016 · 017) 완료: <한 줄>" \
  --body "변경 파일 / WP 수 / grep 으로 센 지울 곳 수 / 바뀌는 기존 시험 수 / B 표 · 열린 것" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(WORK-016 · 017) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
