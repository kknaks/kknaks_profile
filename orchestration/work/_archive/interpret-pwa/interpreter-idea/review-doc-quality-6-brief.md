# [reviewer_doc] 통키 품질 개선 — SPEC 0.9.0 · WORK WP26 · WP27 검수 (D-55 ~ D-59)

너는 **interpret-pwa `reviewer_doc` 워커**다. 앞 맥락은 없다 — 0.8.x 는 다른 리뷰어 터미널이 검수했다. **read-only** — 리포트 1개만.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 변경: `git diff -- para/projects/summer-star/interpret-pwa/20-spec para/projects/summer-star/interpret-pwa/30-work`(커밋 `ee23d056` = 0.8.4 이후)
- 기준: DEC D-55 ~ D-59 · 발주 `orchestration/work/interpreter-idea/quality-spec-v090-brief.md` · 추가 지시 `quality-spec-v090-add-1.md`(7차 = 최종 버전만) · planner 보고 `quality-spec-report.md` 「0.9.0」(planner 기본값 12건 · 미결 ① ~ ⑤) · 처분 §10
- 코드(읽기만): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` — `records.py` 걸린 term 판정 · `session.py` `_emit`

## 2. 볼 것

1. **§5.12 바로잡기**가 D-58 과 맞고 backend 가 바로 짤 수 있나 — 걸리는 조건 · 찾기 ① ② ③ 순서 · 바꾸는 자리(`final:true` · 자막 · TTS · 기록 같은 글) · 못 찾음 · 한 발화 여러 term · **잘못 바꿀 위험**(예: 다른 term 의 이름을 바꿈 · 일반 낱말이 가까운 라틴 낱말로 걸림 · 방향 반대)이 막혔나
2. 시드 `.8` 새 필드(`wrong` · `ko_wrong`) · 검사 8 · §5.9 새 키 `fixed` — 기존 시드 검사 · 기록 「여기 없는 키 0」 과 어긋남 없나
3. **§9.3 7차** — 7개 언어 × 직원 19 · 손님 9 = 196행 · 최종 버전 하나만 · 판정 규칙(사전에서 자동) · 결과 페이지 언어별 탭 · ㉖ · ㉗ 이 D-57 · D-59 와 맞나
4. planner 기본값 12건 중 DEC 근거 없이 정책을 지은 것이 있나(있으면 FAIL 이 아니라 「코디 처분 필요」 로 목록)
5. WORK WP26 · WP27 · WP25 순서 · 「코드와 시드 같은 PR」
6. public — 시험 · 기록 문장 0 · 키 · 실명 0

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-6.md` — PASS / WARN / FAIL

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_84f40940-7d19-4ce7-b55c-2f76c48155c8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
