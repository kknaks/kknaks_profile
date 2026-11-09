# 리뷰 리포트 — day-data-architecture / doc · DAY-SPEC-001 재검수 (WARN 반영 + SPEC-000 token_hash) (2026-11-05)

대상: 워크트리 `mediness-mediness/day-data-architecture-spec` 의 미커밋 변경. HEAD 는 `60fae27b` 이다.
- 새 파일: `spec-001-login-session.md`(untracked)
- 수정: `spec-000-data-model.md` · `40-architecture/erd.md` · `log.md` · `20-spec.md` · `30-work.md`

정답지: 바뀐 원천 `erd/04-staff.md`.
- `login_session.token_hash` 행(`:95`)
- 「정할 것」 1 닫힘(`:117`)
- 새 절 「로그인 · 세션 계약 (2026-11-05 사용자 결정 — DAY-SPEC-001)」(`:120-131`)

1판 리포트: `review-spec001-report.md`(W1 ~ W4).

## 판정: WARN

W1 ~ W4 는 원천 새 절대로 모두 풀렸다. SPEC-000 은 지정한 세 자리만 바뀌었다. planner 가 해석으로 둔 둘 중 임시 토큰 만료 코드는 바르게 「아직 열린 것」에 있다. 다른 하나인 **KOS 조기 401 → `session_expired`** 는 결정에 없는 매핑이다. 같은 SPEC 안의 「`session_expired` 는 만료만」과도 긴장 관계라 사용자 확인이 필요하다(W1).

## FAIL

없음.

## WARN

### W1. KOS 가 만료 전에 401 을 줄 때 `session_expired` 로 둔 것 — 결정 밖 해석 · 문서 안 긴장

- 위치: `spec-001-login-session.md:168` (매트릭스 「세션 만료(= KOS 토큰 만료) · **KOS 가 만료 전 401** → 401 `session_expired`」), `:208` (상태도 「사용중 → 만료: … / KOS 가 401」)
- 근거(원천 `erd/04-staff.md`):
  - `:128` 오류 행 — 「401 `session_expired`(**만료만**) · 401 `unauthorized`(세션 없음 · 로그아웃된 세션)」
  - `:129` 재로그인 행 — 「KOS 401 → 세션 끝 · 다시 로그인」. **코드는 정하지 않았다.**
- 문제:
  1. 결정은 KOS 조기 401 의 코드를 주지 않았다. `session_expired` 매핑은 planner 해석이다(planner 미결 2 가 스스로 밝힘). 그런데 SPEC 본문에는 해석이라는 표시가 없고, `:172` 는 「사용자 2026-11-05 결정」 문장 바로 위 행에 이 매핑을 둔다.
  2. 같은 문서의 `:267` 「`session_expired` 범위 — 만료만」(원천 `:128` 그대로)과 글자 그대로 부딪친다.
  3. 구현 빈칸도 생긴다. 「세션을 끝낸다」(`:107` · `:229` Rule 8)를 `revoked_at` 으로 하면, 다음 요청은 `:169` 규칙상 「로그아웃된 세션 → `unauthorized`」가 된다. `expires_at` 을 당기면 `session_expired` 가 된다. 어느 칸을 채우는지 정해지지 않아 BE 워커가 고르게 된다.
- 방향: 사용자가 둘 중 하나를 고른다. (a) `session_expired`(현재 SPEC · planner 권장 — 「KOS 토큰이 끝남 = 만료」로 본다). (b) `unauthorized`. 고른 뒤 원천 `:128` 의 「만료만」 문구와 「세션을 끝낸다」의 칸(`expires_at` / `revoked_at`)을 같이 맞춘다. 정하기 전까지는 `:278` 「아직 열린 것」에 함께 올리는 것이 정직하다.

---

## 1판 W1 ~ W4 해소 확인

| 1판 | 원천 새 절 | SPEC-001 지금 | 결과 |
|---|---|---|---|
| W1 a · b 경로 `/api/auth/hospital` · `/logout` | `:124` 4개 경로 · 메서드 | `:130-133` API 표 · `:262` | **해소** — 원천과 같다 |
| W1 c · d · e `staff_inactive` · `unauthorized` · `forbidden` | `:128` | 매트릭스 `:163-170` · `:263` | **해소** — 코드 · HTTP 같다 |
| W1 f KOS 403 → `kos_unavailable` | `:128` 「KOS 장애 · KOS 403 `Unsupported client.` 포함」 | `:159` · `:264` | **해소**. 「시간 제한 15초 넘김」도 `:131` 「KOS 호출 시간 제한 15초」와 「KOS 장애」에서 나온다 |
| W1 g 로그아웃된 세션 → `unauthorized` | `:128` | `:106` · `:169` · `:266` | **해소** |
| W2 형식 검사 | `:131` 「형식 검사는 KOS 에 맡긴다」 | `:152` Validation | **해소** — 이제 결정 근거가 있다 |
| W2 안내 문구 | `:131` 「안내 문구는 화면 SPEC(예시만)」 | `:166` 「문구 예시 — 확정 문구는 화면 SPEC」 | **해소** — `:58` 과의 모순이 풀렸다 |
| W3 SPEC-000 OQ-04-1 | `:117` 정함 | `spec-000:1293` 취소선 + 「→ 정함: DAY-SPEC-001 OQ-6」 | **해소** |
| W4-1 세션 토큰 | `:95` `token_hash` · `:125` 「토큰은 무작위 값, DB 에는 token_hash」 | `:146` · Rule 7 `:228` · Flow `:197-198` · SPEC-000 `:595` | **해소** — SPEC-000 `id` 의 「쿠키가 가리킨다」도 원천대로 빠졌다 |
| W4-2 새 `account.is_active` | `:131` 「처음 만든 `account.is_active` = true」 | S-1 3 `:85` · Rule 2 · `:269` | **해소** |
| (1판 열린 것) 비활성 직원을 아는 방법 | `:131` `get-accounts.activate` → `staff.is_active` | S-1 5 · Rule 12 · `:271` | 닫힘 — 원천에 근거가 있다 |
| (1판 열린 것) 시간 제한 값 | `:131` 15초(cc 값) | Rule 10 · `:270` | 닫힘 — 원천에 근거가 있다 |
| (1판 열린 것) 1단계 → 병원 고르기 | `:127` 「여럿이면 짧은 임시 토큰(5분) → 병원을 고르면 진짜 세션」 | S-3 2 · API 표 · Validation · Rule 6 · `:272` | 닫힘 — 원천에 근거가 있다 |

원천 새 절 8행(`:124-131`)의 모든 항목이 SPEC-001 에 있다(줄 단위로 대조함). 원천에 없는 새 값 · 이름은 W1 하나뿐이다.

## planner 해석 2건 판정

| 해석 | 판정 | 이유 |
|---|---|---|
| 임시 토큰(5분)이 지난 병원 고르기 요청의 오류 코드 | **정상(열린 것)** | 원천 `:127` 은 5분까지만 정했다. SPEC 은 `:278` 「아직 열린 것」에 두었고 본문에서 코드를 정하지 않았다. S-3 2 「5분이 지나면 로그인부터 다시」는 원천 「임시 토큰(5분)」에서 바로 나오는 뜻이라 발명이 아니다 |
| KOS 조기 401 → `session_expired` | **WARN(W1)** | 결정에 코드가 없고, 표시 없이 본문 계약에 들어갔으며, 「만료만」과 긴장한다 |

참고: 임시 토큰을 어디에 어떻게 두는지(서버 저장 / 서명 토큰 · KOS 토큰 보관)는 SPEC-000 에 칸이 없지만, 외부 계약이 아니라 구현 선택이다. 문서 규칙상 WP 몫이라 SPEC 의 빈칸으로 보지 않는다.

## SPEC-000 diff 확인 (다른 표가 바뀌지 않았나)

`git diff products/day/20-spec/spec-000-data-model.md` 결과 바뀐 덩어리는 **3개뿐**이다.
1. `:594-595` `login_session` — `id` 설명에서 「쿠키가 가리킨다」 삭제, `token_hash` 행 추가(원천 `:94-95` 그대로)
2. `:615-618` `#### 로그인 · 세션 계약` — 링크 한 줄
3. `:1293` OQ-04-1 취소선 + 정함

그 밖의 표는 바뀌지 않았다. 원천 9개 파일과 다시 줄 순서로 diff 했다. 04 절의 차이는 머리말 변환 · 「정할 것」 → §6 · 새 절 → 링크뿐이다. 01 ~ 03 · 05 ~ 07 · 04-1 · 공통은 지난 PASS 때와 같다.

- 새 절을 링크로만 둔 것: 원천을 그대로 옮긴다는 1판 계약과 한 곳 원칙이 부딪친다. 원천 새 절의 모든 항목이 SPEC-001 에 있으므로 내용 손실은 없다. 한 곳 원칙(`rules/document-pipeline.md` 「한 곳 원칙」)에 맞으니 **수용**한다.
- planner 리포트의 「SPEC-000 `last_updated` 2026-11-05」는 이미 HEAD 에 있던 값이라 이번 diff 에는 없다(무해).

## 그 밖

- `40-architecture/erd.md:134` 인벤토리 `login_session` 핵심 키에 `token_hash` UNIQUE — 원천 `:95` 「varchar UNIQUE」와 같다.
- `log.md`: 2026-11-05 `spec-change` · `DAY-SPEC-001, DAY-SPEC-000` · `#909` 행이 맨 위에 있고 형식에 맞는다. 요약 문구 「`session_expired` 는 만료만」은 원천 그대로지만 W1 과 같은 긴장이 있다.
- 인덱스(`20-spec.md` · `30-work.md`)는 1판 그대로다. 미러가 맞다.
- lint `python3 scripts/lint-pipeline.py --strict` 1회 → **exit 0 · 0 error · 263 warning**. `products/day/` 범위는 ERROR 0 · WARN 0이다. 263 WARN 은 타 제품의 기존 경고라 **무관**하다.
- 링크 전수 검사: 깨진 링크 0. 보안 grep(이메일 · 토큰 · URL): 0건.

## 직원이 실물에서 만날 자리

- W1: KOS 가 직원 토큰을 일찍 끊으면 직원은 「세션이 만료됐습니다」나 「로그인이 필요합니다」 중 하나를 본다. 구현이 `revoked_at` 으로 끝내면 SPEC 매트릭스(`session_expired`)와 다른 코드가 나간다. 앱 · 웹 문구 분기가 어긋날 수 있다.

## 참고(원천 쪽)

- SPEC-000 「주제와 상태」 표(`spec-000:64`)와 원천 `erd/README.md` 주제 표가 04 를 아직 「열린 것 2」로 적는다. OQ-04-1 이 닫혀 이제 1개다. 원천 README 를 고치면 SPEC-000 도 따라 고친다.
- `mfaMethods` 의 ③ 응답 위치는 1판에서 검증하지 못한 그대로다(원천 04 에는 이름만 있음).
