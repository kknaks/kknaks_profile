# [reviewer] WP-REVIEW — back/ · front/ 를 SPEC-001 0.2.1 에 대조

너는 **agency-settlement `reviewer` 워커**다. **맥락이 하나도 없다고 가정하고** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**read-only.** 같은 워크트리에 커밋 안 된 `back/` · `front/` 가 있다 — 고치지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` (0.2.1) — 계약 · 부록 A
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` — WP-REVIEW 행(볼 것 목록)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md`
- 워커 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/wp-fe-report.md` · backend 보고는 아래 §2
- KOS 공식 스펙 `https://developers.kos-solution.com/openapi.yaml`

기대는 개념:
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/areas/concept/cs/no-inference-from-free-text.md` — 자유 텍스트 필드를 읽는 코드가 있으면 FAIL

## 2. 배경

WP-BE(ruff OK · pytest 63 · 코디 재확인) · WP-FE(tsc · lint · build 0 · 코디 tsc 재확인)가 끝났다. 다음은 코디가 운영 KOS 로 10월을 한 번 조회하는 WP-LIVE 다. **그 전에** 계약과 코드가 맞는지, 운영 데이터에서 돈이 틀리거나 개인정보가 새는 길이 없는지 본다.

backend 가 스스로 적은 판단(코디가 볼 것): counts.transactions = 받은 ① 행 수 · ⑤ 시각이 비면 at 만 null · ⑤ 에 수납 없으면 firstApprovedUnknown · ⑤ 에 APPROVED 0 이면 itemsHere=false(SPEC 언급 없음) · 수납 currency 판정 · 취소 금액 -abs · back/.gitignore 추가 · FastAPI include_router 지연 포장. **이것들이 SPEC 과 맞는지 판정해라.**

## 3. 계약

SPEC §4.2 · §4.3 — back `schemas/sales.py` ↔ front `lib/types.ts` 필드 하나하나 대조.

## 4. 볼 것

WORK-001 WP-REVIEW 행 전부. 특히: 가드(허용 경로 5 · `/queries/` · 내부 API 0 · 토큰 잠금) · 「없음」= 400 NotFound 만 · ③④⑤ 응답에서 지정 필드 외 변수 · 캐시 · 로그 0 · 분할 결제 품목 줄 첫 승인 달만(s1~s5) · 결제일 · 정렬 = ⑤ 시각 · 자유 텍스트 0 · 로그에 이름 · 금액 · id · 키 0 · `127.0.0.1` · `.env` 미추적 · cc-prototype import 0. 그리고 **시험이 초록인데 운영에서 터질 자리**(가짜 transport 가 실제 응답 모양과 다른 곳)를 따로 모은다. 마지막에 「사용자가 실물에서 만날 자리」.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 단계

1. SSOT · 코드를 읽는다. `cd back && uv run pytest -q` · `cd front && npx tsc --noEmit` 는 돌려 봐도 된다(파일 안 바꿈)
2. 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r1-report.md` 하나 — 판정 PASS/WARN/FAIL · 지적마다 `파일:줄` + 근거(SPEC 절 · DEC D-번호)

## 7. 범위 제약

- 파일 수정 금지(리포트 1개만) · 운영 · 데모 KOS 호출 금지 · 서버를 띄우면 다른 포트로 · 끝나면 내린다 · 커밋 · push 금지

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. /commands/ 로 가는 길 · 개인정보 로그는 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --from term_c40823c2-59cf-42d8-8c37-0351f93b7267 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
