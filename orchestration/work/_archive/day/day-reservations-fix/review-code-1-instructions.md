# [reviewer] 코드 검수 1회 — #300 BE · #301 웹 · #302 앱 전체 diff

너는 **day `reviewer` 워커(코드)**다. 먼저 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/reviewer/role.md`(+ 같은 폴더).

대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` 미커밋 변경 전체(base `origin/dev` `65506f35`). **파일을 고치지 마라**(stash · checkout · reset 금지). 이 검수가 **이번 작업의 유일한 코드 검수**다(사용자 결정) — 세 WP 를 묶어 본다.

## SSOT
- Issue 계약: `gh issue view 300 301 302 -R MediSolveAIDev/CENTURION_DAY`(v2 · 공통 ① ~ ⑤)
- SPEC(계약 원천 · mediness#971): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec/products/day/20-spec/` spec-006(Rule 15 ⓐ ~ ⓙ) · spec-007(고침 8 · 규칙 2 · 7 · 9 · §3) · spec-000 ④ · spec-003
- 결정 표: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §2
- 워커 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/be-1-report.md` · 인박스 frontend · mobile 완료 본문은 아래 요약 대신 diff 로 직접 확인

## 볼 것
1. **계약 맞물림**: BE 가 내는 이름 · 모양(`rows` · `cards` · `bands.end_min`/`endMin` · `questionnaire.expired` · `display-targets` · `display-requests` form `kind` · `device_id` · `[data-day-res-dp-link]` · `qrUrl`)을 웹 `day.js`/템플릿 · 앱 dart 가 **한 글자씩 같게** 읽나. 화면이 배치를 다시 계산하는 곳 = FAIL(Rule 15 ⓕ)
2. **Rule 15 정확성**: ⓐ ~ ⓙ · R71 30분 분리 · R73 순서 · ⓖ 행 넘는 카드 · 5 자리 줄 접기 — BE 테스트가 경우를 다 덮나 · 웹 · 앱 그리기가 같은 그림인가. 특히 **회색 면 · 현재 시각 선 y 매핑이 웹 · 앱 같은가**(lines ≥ 2 행에서 카드 분 위치와 어긋나는지 — 앱 워커가 짚음)
3. **F6**: 상세를 그리는 모든 경로가 `public_origin` 하나를 쓰나(grep 전수) · `qrUrl` 을 opened 요청에도 싣는 변경(BE 주의 3)이 고객 토큰 · 만료 판정을 깨지 않나
4. **KOS 문진 읽기**: 내부 legacy 경로만 · 공개 새 호출 0(grep) · 400 = 없음 · 실패 격리 · 중복(`external_ref`) · 제출 id 읽기 위치 가정(BE 주의 2) · 별도 태스크가 일정 태스크에 영향 없음 · 잠금 TTL · migration `0032` downgrade
5. **6개월**: KST 달력 · 말일 · env · 웹 · 앱 같은 값 · 다시 보내기 대상 = 제출 행만
6. **팝오버**: D44 링크 다시 씀 · 기기 줄 취소 → 새 · GET 은 요청 0 · D45 다시 그리기가 팝오버 안 닫음 · 링크 복사 클립보드 사용자 활성화 시한(frontend 주의 ⑤) 실제 위험도
7. 화면 문구: 새 글자 = 「링크 복사하기」 「링크 열기」 「연결」 「미연결」 「6개월 경과」만 · 그 밖 지은 글자 = FAIL · 인라인 스크립트 · 손 CSS 0
8. 범위 밖 변경 · 죽은 코드 · 옛 30분 전제 잔재(`RES_SLOT_MIN` · `ROW_MINUTES` · 66 · 70) grep
9. 검증 다시 돌리기(각 1회): `cd backend && ./scripts/test.sh --pure -q`(또는 관련 파일) · 웹 `node --test scripts/frontend/tests` · `cd app && flutter analyze && flutter test`. 기존 실패(mypy `test_reservation_request_rules.py:191` · 앱 `board_messages_contract_test` copy.dart)는 「무관 · 기존」으로 분리 — 정말 base 에서도 깨지는지 확인
10. 추적 안 할 파일: `scripts/frontend/node_modules` 등 커밋에 들어가면 안 되는 것

## allowed_paths
- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-code-1-report.md`

## 하지 말 것
파일 수정 · 커밋 · push · KOS 호출 · dev / prod 접속 · 사용자 포트/프로세스.

## 리포트 모양
맨 위 판정(PASS / WARN / FAIL) · 지적(파일:줄 · 근거 · 고칠 방향 · 담당 BE/웹/앱) → 계약 대조 표 → 검증 수치.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
