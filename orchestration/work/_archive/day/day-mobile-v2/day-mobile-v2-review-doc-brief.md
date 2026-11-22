
# [reviewer_doc] DAY 직원 앱 0.2.0 스펙 검수 1차

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner 가 쓴 미커밋 변경이 있는 워크트리다 — **읽기만.** 파일 수정 · stash · checkout 금지.

## 1. SSOT — 먼저 읽을 것

- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-spec-brief.md` §1 결정 표 M-1 ~ M-9 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/_RESUME.md` §2(같은 결정 · 날짜 · 근거)
- 리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec` 미커밋 diff(`git diff` · `products/day/` — spec-000 · 001 ⑩ · 002 ㉕ · 003 ⑲ · 005 · 40-architecture/mobile-deployment · 20-spec · log)
- planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-report.md` · Delivery `gh issue view 262 -R MediSolveAIDev/CENTURION_DAY` · `gh issue view 263 -R MediSolveAIDev/CENTURION_DAY`
- 현황 조사(코드 사실 · 파일:줄) `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`(origin/dev `844eace4`) · 통키 `/Users/kknaks/git/toy_pr2/interpret-pwa`(`git show origin/main:<path>` · `56e43a0`) · 통키 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/projects/summer-star/interpret-pwa/`

기대는 개념: 해당 없음.

## 2. 배경

DAY 직원 앱 0.2.0(기기 선택 · 시술 현황 5동작 · 호출 취소 알림 · Android FCM · 통역 = 통키 최신). 다음은 코드(backend · mobile · designer)다 — 이 스펙만 보고 짓는다. 옛 앱 호환은 안 챙긴다(M-2).

## 3. 계약

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md`

## 6. 검토 항목

1. M-1 ~ M-9 빠짐 · 넘침 — 결정 표에 없는 정책이 규칙으로 박혔나(제안 · OQ 로 둔 건 OK). 화면 · 토스트 글자가 원천(결정 표 · 웹 · KOS 글자) 밖에서 지어졌나(M-9).
2. M-2 — 옛 앱 호환 장치(버전 가르기 등)가 남았나 · 반대로 「옛 앱 고려 안 함」 때문에 새 앱이 깨질 자리가 생겼나.
3. API 계약이 지을 수 있을 만큼 닫혔나 — `/api/auth/device` · quick-start JSON(일부 · 전부 거절) · `can*` 3칸 판정 · 알림 kind · 원래 알림 닫기 · FCM 토큰 등록 · 통역 WS 메시지(`audio_stop` · `playback_stopped`) — 이름 · 모양 · 오류 코드 · 코드 사실(파일:줄)과 어긋남.
4. 통역(M-8) — 통키 `56e43a0` 의 DEC D-43 ~ D-71 · 코드와 대조: 빠진 것 · DAY 에 안 맞는데 들어온 것(records 계열 등) · 시드 `.11` 로더 · v6 마감(2026-12-15).
5. 알림(M-6) — 받는 사람 · 글자 · {N} 뜻 · 웹 쪽 처리(planner 는 OQ-N19 에서 「웹에 목록 · 종이 없어 웹 OS 알림으로 읽음」 — 코드 사실 확인) · enum migration.
6. WP 표(spec-report) — 순서 · 의존 · 빠진 일(예: 방 복귀 OQ-A55 · 시안 5자리) · FCM 분리.
7. 착수 막는 OQ 표가 정확한가 — 빠진 막는 OQ · 막지 않는데 막는다고 한 것.
8. 비밀값 · 이메일 · IP · Firebase 값 없음 · `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만) · 커밋 · Issue 수정 · 승인 금지.
- 결정 표를 뒤집자는 지적은 「사용자 확인」으로 따로 모아라(FAIL 로 섞지 마라).

## 8. 검증

```
SPEC·WORK 를 결정 표 · 코드 사실에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **완료 보고는 dispatch preamble 의 worker_done 명령을 그대로 따른다**(아래 옛 형식과 다르면 preamble 이 맞다).
- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
