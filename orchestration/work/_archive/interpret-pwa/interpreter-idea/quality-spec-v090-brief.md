# [planner] 통키 품질 개선 — SPEC 0.9.0 · WORK WP26 · WP27 (DEC D-55 ~ D-59 · WP22 · WP24 결과)

너는 **interpret-pwa `planner` 워커**다. 앞 맥락은 없다 — 0.8.0 ~ 0.8.4 는 다른 planner 터미널이 썼다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- DEC **D-55 · D-56 · D-57 · D-58 · D-59**(새 행) — `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` 끝
- SPEC 0.8.4(지금) — 특히 §4.2(시드 스키마 · 검사) · §4.5 · §4.6(언어별 한도 표) · §5.9(기록의 걸린 term 판정 — D-58 이 같은 규칙을 쓴다) · §5.11(빈 원문 막기 — 같은 `_emit` 자리) · §9.3 「6차」
- 시험 결과(수치만): `orchestration/work/interpreter-idea/wp22-be-report.md` · `wp23-be-report.md` · `wp24-be-report.md` · 사람 판정 `wp22-human.json` · `wp24-human.json` · 처분 `quality-research-dispositions.md`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` — `back/app/service/records.py`(걸린 term 판정 · `hit_terms`) · `back/app/service/interpret/session.py`(`_emit` · `_blank_filter`) · `back/app/service/glossary.py` · `back/seed/glossary.json`(`.7` · 미커밋)

## 2. 할 것

1. **§4.6 · §2.4 한도 표 = D-56 값**(v6 × 0.96) · 근거
2. **새 절 §5.12 「시술명 바로잡기」(D-58)** — backend 가 바로 짤 수 있게:
   - 걸리는 조건(원문에 term 걸림 — §5.9 판정 그대로 · 번역에 그 언어 `name` · 별칭 0) · 방향 둘(한 → 외: 대상 = 세션 언어 name / 외 → 한: 대상 = ko 대표명)
   - 바꿀 꼴 찾기 순서: ① 시드의 그 term 「틀린 꼴」 목록(새 필드 — §4.2 스키마 · 검사 규칙 · 언어별) ② 그 term 의 **다른 언어** name · 별칭(라틴 · 다른 문자) ③ ①② 와 아주 가까운 라틴 낱말(거리 기준을 숫자로 — 예: 글자 4개 이상 · 편집 거리 ≤ 2 · 대소문자 무시) — **근거 없는 기준을 짓지 말고, 숫자는 「기본값 · 시험으로 확인」 으로 표시**
   - 한 발화에 term 이 여럿이면 각각 · 바꾼 뒤 그 언어 name 이 생기면 끝 · 못 찾으면 그대로 + 로그 1줄(term id · 언어만)
   - 자리 = 확정 발화를 자막 · TTS · 기록으로 내보내기 직전(`final:true` 만 — `final:false` 는 그대로). TTS 는 바꾼 글을 읽는다. 기록에는 바꾼 글 + 바꿨다는 표시(새 키 — §5.9 「여기 없는 키 0」 을 함께 고침)
   - 틀린 꼴 첫 목록(시드 `.8`): 이번 시험에서 나온 꼴 — 번호 · term · 언어만 SPEC 에, 꼴 자체는 시드에(로컬 결과 `reference/2026-11-12-interpreter-idea/quality-run/*-local.json` 에서 backend 가 뽑는다 — SPEC 에 기록 문장 0)
3. **§9.3 「7차」 나라별 시험(D-57 · D-59)** — 언어마다 직원 쪽(한국어 음성 → 그 언어 · D-57 의 10문장 + 시술명 문장) · 손님 쪽(그 언어 문장 · 9개 시술 하나씩 — 토닝 · 울쎄라 · 써마지 · 스컬트라 · 쥬베룩 · 리투오 · 보툴렉스 · 보톡스 · 필러 · 그 언어 사전 이름으로 말함) · 조합 A · C · **D(= C + 바로잡기)** · 판정 규칙(사전에서 자동) · 결과 페이지 = 언어별 탭(로컬 전용) · 기존 33 · 21문장은 그대로 두고 7차가 넓힌다
4. **D-55 결과**: C2 는 조각 · 판정이 C 와 같음 → `max_endpoint_delay_ms` 1000 유지(OQ-027 닫힘 — 사용자 판단은 비교 페이지에서 · 지금은 결과만 기록)
5. **WORK** — WP26(back: 바로잡기 · 시드 `.8` 틀린 꼴 · 시험) · WP27(7차 나라별 시험 · 결과 페이지) 행 추가 · WP25(배포)는 WP27 뒤로 · 배포는 사용자 확인 뒤

## 3. 범위 · 검증

- allowed_paths: `20-spec/` · `30-work/` 만 · DEC · 처분 · 코드 · 시드 읽기만
- 시험 문장 · 통역 기록 문장 0 · 키 · 실명 0
- SPEC `version` 0.9.0 · 변경 이력 · 부록 A(D-55 ~ D-59)
- 보고 `orchestration/work/interpreter-idea/quality-spec-report.md` 끝 「0.9.0」 절

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_999506d9-1342-4e49-bca8-25f4cb1aa731 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
