
# 재개 노트 — day-chart-photo (day)

**지금**: 사용자 「PR 올리고 합치고 마무리(회고 · 개념 · 이슈 닫기)」 · 코드 커밋 `7e7cb368` · origin/dev `fed616a8`(#274) 위로 rebase 진행(충돌 9 · migration 0024→0025) · 스택 내림(infra 유지) (run `run_1efd9f107698`)
**다음**: rebase 보고 → 코디 게이트 → push · code PR(dev) · 스쿼시 머지(사용자 지시) → #960 머지 여부 확인 → SUMMARY(회고) · archive-work.sh · 개념 · profile PR · 로컬 env/.local 정리 · Delivery 이슈 없음(발행 안 함)

세팅: `scripts/new-work.sh day day-chart-photo` · 설정 SSOT `config/projects/day.json`
코디handle: `term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` (branch `kknaksss/day-chart-photo-spec`, base `origin/main` → PR `main`)
- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` (branch `kknaksss/day-chart-photo`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] planner fix-2(`planner-fix-2-instructions.md`) → reviewer R1~R3 확인 → spec 커밋 · PR(mediness main · 머지 X)
- [!] 새 OQ-90 ~ 92(충돌 토스트 글자 · 글자 한도 값 없음 · 사진 읽기 토큰) — 사용자 몫 글자 · 한도
- [ ] planner Delivery Issue 발행(CENTURION_DAY · baseline = spec PR 커밋) · 30-work Coverage
- [ ] 사진 탭 시안 — designer 워커(DesignSync) · 화면 글자 OQ
- [!] 헤더 표시 모양 「이름 직군」 사용자 확인 전(OQ)
- [!] 다른 DAY 코디 세션 `day-reservation2` 가 살아 있음 — mediness SPEC-002 · CENTURION_DAY dev 를 같이 건드릴 수 있음. PR 전 base 위치 확인
- 참고: 데모 지점 시드 5명(11-24 13:30 칸 · `scripts/seed_demo_board.py --count 5` · origin/dev `4bf0b4a1` 스크래치 복사본으로 실행)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-24 | 결정 C1 ~ C16 — 정본 `reference/2026-11-24-day-picture/chart-photo-decisions.md`(탭 3 · 명시적 저장 탭별 · [저장] 탭 줄 오른쪽 · 최근 저장 옆 · 미저장 경고 · 트랜잭션처럼 · 사진 올리기/삭제 즉시 KOS · 직원 토큰 · KOS 웹 필드 · 메모 「{이름} 고객 시술 전/후」 · 코드 DB 없이 이름 매칭 · 서버 경유 · Blob 없음 · 웹만 · 헤더 로그인 표시) | 사용자 대화 2026-11-24 |
| 2026-11-24 | C17 저장 충돌 = 저장 전 KOS 확인 · 하나라도 다르면 탭 전체 저장 안 함 · 걸린 줄 = KOS 글 + 줄바꿈 + 내 글 · 담당자 KOS 값 · 토스트 · 다시 저장 / 기본값: KOS 확인 실패 = DAY 사본만 · 한도 초과 = 길이 오류 · WARN 9 기본값(코디) | 사용자 · review-doc-1 |
| 2026-11-24 | 이슈(Delivery) 없이 마감 · 스펙 #960 머지 | 사용자 「이슈 없이 마감하자 스펙도 다 마감해야지」 |
| 2026-11-24 | C35 시스템 토큰 Redis 공유(API · 워커) · C36 사진 토스트 글자 2 | e2e 3회차 · 사용자 「응 그렇게 하자」 |
| 2026-11-24 | C33 사진 올리기 경로만 Caddy 100MiB · C34 C31 안전장치(매핑 실패 · 빈 목록이면 판정 안 함) | review-code-4 · 사용자 「응 올려」 |
| 2026-11-24 | C28 여러 장 · C29 토스트 글자 3 · C30 사진 탭 열린 동안 10초 동기화 · C31 KOS 삭제 → DAY 소프트 삭제 · C32 바로 시작 = 시스템 그대로 | e2e 1회차 · 사용자 |
| 2026-11-24 | C25 KOS 삭제 실패 = 다음 탭 열기 때 재삭제 · C26 삭제 확인 창 「사진을 삭제할까요?」 [취소][삭제] · C27 토스트 「KOS 반영에 실패했습니다」 | review-code-3 · 사용자 「응」 |
| 2026-11-24 | e2e 는 차트 · 사진 다 된 뒤 최종 한 번 — 중간 e2e 요청하지 않음 | 사용자 「최종 e2e 해야지」 |
| 2026-11-24 | 사진 키 접두 = `beforeAfter/`(Azure dev 컨테이너 실제 폴더 · 코드 예약 `before-after` 와 다름) · 저장소 = 채팅 첨부와 같은 계정 · 컨테이너 · 관리 ID(`DAY_CHAT_STORAGE` 설정 그대로) | 사용자 Azure 화면 · 「우리 앱도 이미 쓰는 거」 |
| 2026-11-24 | C18 바뀜 — 동기화 이력은 글만 비교(집도의 비교 안 함) | review-code-2 N1 · 코디 기본값 |
| 2026-11-24 | C23 KOS 웹 사진 = 사진 탭 열 때 중앙 작업으로 가져와 DAY 저장(10초 동기화엔 안 넣음) | 사용자 「사진 열 때 불러오자」 |
| 2026-11-24 | C22 사진 = DAY(Blob before-after/ + 새 테이블 · external_ref) + KOS 등록 · C14 뒤집힘 · 기본값 C22 ①~⑤ | 사용자 「데이에 저장하고 kos에도 저장해야지」 |
| 2026-11-24 | C21 집도의 한 명 = 매핑 뒤 DAY 직원 수(앞 판 「매핑 전」 뒤집음 · DAY 사본이 매핑된 것만 저장) | backend 질문 · 코디 |
| 2026-11-24 | C18 KOS 동기화 이력 충돌 아님 · C19 응답 유실 뒤 같은 저장 = 성공 · C20 CRLF 정규화 · C21 기본값(보내는 동안 칸 잠금 · 집도의 한 명 기준) | review-code-1 · 사용자 「응」 |
| 2026-11-24 | #960 머지 안 함 · Delivery 없이 바로 코드 구현 | 사용자 「pr 나중에 머지할거야 머지하지 말고 바로 코드 구현해」 |
| 2026-11-24 | baseline(기획안) 안 고침 — decision → SPEC-002 개정 → Delivery | 사용자 「스펙이랑 이슈까지 발행해」 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_3b019a47-8c77-4d76-ba69-466956084d6b` | `task_1b853388f09b` | `ctx_93b0dd43629b` | `day-chart-photo-spec-brief.md` | 완료 |
| reviewer_doc | `term_1c95f60f-45d5-4c05-96af-5157798267d2` | `task_8f3ef561127f` | `ctx_5de056be2223` | `day-chart-photo-review-doc-brief.md` | 완료 WARN 9 |
| planner fix-1 | `term_3b019a47-8c77-4d76-ba69-466956084d6b` | `task_23c7504399db` | `ctx_01ac389de3f3` | `planner-fix-1-instructions.md` | 완료 |
| reviewer_doc 2 | `term_1c95f60f-45d5-4c05-96af-5157798267d2` | `task_1e3ca5c9dac4` | `ctx_ec7897ee1827` | `review-doc-2-instructions.md` | 완료 WARN 3 |
| planner delivery-1 | `term_3b019a47-8c77-4d76-ba69-466956084d6b` | `task_becf63a37a61` | `ctx_9257a10f75f0` | `planner-delivery-1-instructions.md` | blocked(main baseline) |
| backend WP① | `term_cfd99c77-dafd-41c1-91a3-0ad1e4c6c1f3` | `task_95357a2ebbfb` | `ctx_91a5c41738dd` | `day-chart-photo-be-brief.md` | 완료(`be-1-report.md`) |
| frontend fix-1 | `term_f69bad17-fd69-468b-81f6-d30eca448f36` | `task_d045486cfed1` | `ctx_2bffea649cab` | `fe-fix-1-instructions.md` | 완료 |
| reviewer(code) | `term_1b967637-b488-40a4-8a36-00c3ebec0496` | `task_342d22cba522` | `ctx_ec34178b5cf5` | `review-code-2-instructions.md` | 재검수 2 PASS |
| backend fix-2 | `term_cfd99c77-dafd-41c1-91a3-0ad1e4c6c1f3` | `task_6961ef7a490f` | `ctx_2fe2a9ecf393` | `be-fix-2-instructions.md` | 진행 |
| planner fix-3 | `term_3b019a47-8c77-4d76-ba69-466956084d6b` | `task_4789c0ee2a79` | `ctx_137ccc60aa63` | `planner-fix-3-instructions.md` | 완료 `d98c5a28` |
| backend fix-1 | `term_cfd99c77-dafd-41c1-91a3-0ad1e4c6c1f3` | `task_de322def923f` | `ctx_a803aad9557f` | `be-fix-1-instructions.md` | 진행 |
| frontend fix-2 | `term_f69bad17-fd69-468b-81f6-d30eca448f36` | `task_6254c17a7f86` | `ctx_7825214d136d` | `fe-fix-2-instructions.md` | 완료 |
| frontend WP③ | `term_f69bad17-fd69-468b-81f6-d30eca448f36` | `task_04a49972124a` | `ctx_65cae49849fa` | `day-chart-photo-fe-brief.md` | 완료(`fe-1-report.md`) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/960 — **스쿼시 머지 `69ef0dcb`**(2026-11-24 · 사용자 「스펙도 다 마감」)
- code PR: <링크>
- 리포트: `planner-1-report.md` · `planner-fix-1/2-report.md` · `review-doc-1/2/3-report.md`(WARN 9 → WARN 3 → PASS)
- 커밋: `a896cda0` — SPEC-002 개정 ㉘ · SPEC-001 개정 ⑫ / `d98c5a28` C18~C21 / `b2005927` C21 / `4d9214af` C22~C24 사진 DAY 저장

## 5. 이력 (최신이 위)

- `2026-11-24` #960 스쿼시 머지 69ef0dcb · 이슈 없이 마감 결정
- `2026-11-24` C35 실물 확인(API 저장 sign-in 0) · 코드 커밋 7e7cb368 · rebase 발주
- `2026-11-24` be-loop4 · fe-loop4 완료 · 게이트 2710 · 로컬 재기동
- `2026-11-24` planner fix-12 커밋 · be-loop4 · fe-loop4 발주
- `2026-11-24` e2e 3회차 됨 · 로그인 로그 확인 · C35 · C36 · planner fix-12 발주
- `2026-11-24` be-loop3 완료 · 게이트 2701 · 로컬 재기동 · e2e 3회차 요청
- `2026-11-24` fe-loop3 완료(513 · npm 123) · 413 · 빠진 장 토스트 글자 사용자 대기
- `2026-11-24` planner fix-11 · 커밋 8ab5e2d2 · be-loop3 · fe-loop3 발주
- `2026-11-24` review-code-4 FAIL 1 · e2e 2회차 F1 · F2 · C33 · C34 · planner fix-11 발주
- `2026-11-24` fe-loop2-fix-1 · 게이트 798 · 로컬 재기동 · review-code-4 발주 · e2e 2회차 요청
- `2026-11-24` be/fe loop2 완료 · 게이트 1 failed(innerHTML) · fe-loop2-fix-1 발주
- `2026-11-24` planner fix-10 · 커밋 7c5820d5 · be-loop2 · fe-loop2 발주
- `2026-11-24` 최종 e2e 1회차 피드백 E1~E6 · C28~C32 · planner fix-10 발주
- `2026-11-24` be-photo-fix-2 · fe-photo-fix-1 완료 · 게이트 2678 · 로컬 기동 · 최종 e2e 요청
- `2026-11-24` planner fix-9 · 커밋 1179b017 · be-photo-fix-2 · fe-photo-fix-1 발주
- `2026-11-24` be-photo-fix-1 완료(462) · C25~C27 · planner fix-9 발주
- `2026-11-24` review-code-3 WARN · be-photo-fix-1 발주 · P2/P3/P6 사용자 질문
- `2026-11-24` be-photo-1 완료 · 게이트 2668 · review-code-3 발주
- `2026-11-24` fe-photo-1 완료(pytest 13 · npm 118/0) · be-photo-1 진행
- `2026-11-24` planner fix-8 · 커밋 4d9214af · WP② be/fe 발주 · 사용자 「최종 e2e · 다 되면 알려줘」
- `2026-11-24` be-fix-2 완료(게이트 422 · ruff 0) · 로컬 스택 기동(port TIME_WAIT 한 번 · 샌드박스 밖 실행) · review-doc-4 WARN 9 · planner fix-7 발주
- `2026-11-24` planner fix-6 완료 · review-doc-4 발주
- `2026-11-24` 재검수 2 PASS · be-fix-2 발주 · 사진 키 beforeAfter/
- `2026-11-24` be fix-1 완료 · 게이트 421 · review-code-2 발주 · planner fix-5 완료 · 사용자 C23 · planner fix-6 발주
- `2026-11-24` fe fix-2 완료 · planner fix-4 커밋 b2005927 · 사용자 C22 · planner fix-5 발주
- `2026-11-24` planner fix-3 → 커밋 d98c5a28 push(#960) · be-fix-1 · fe-fix-2 발주
- `2026-11-24` review-code-1 WARN 7 · 사용자 C18~C20 · planner fix-3 발주
- `2026-11-24` fe fix-1 완료(ruff 0 코디 확인) · reviewer(code) 발주
- `2026-11-24` be · fe 완료 · 코디 게이트(board 231 · npm OK · ruff 21 fe) · fe fix-1 발주
- `2026-11-24` Delivery blocked(main baseline) · 사용자 바로 구현 · be WP① · fe WP③ 발주
- `2026-11-24` 재검수 3 PASS · 커밋 a896cda0 · PR #960 · planner Delivery 발주
- `2026-11-24` 재검수 2 WARN 3 · R2 기본값(한도 정해질 때까지 길이 검사 안 함) · planner fix-2 발주
- `2026-11-24` planner fix-1 완료 · lint 0(코디) · 재검수 2 발주
- `2026-11-24` review-doc-1 WARN 9 · 사용자 C17 · planner fix-1 발주
- `2026-11-24` planner 완료 · lint strict exit 0(코디 재실행) · reviewer_doc 발주
- `2026-11-24` new-work.sh(planner · reviewer_doc · backend) · orca run 필요해짐(`run-create` → `run_1efd9f107698`) · planner 발주
- `2026-11-24` 데모 지점 시드 5명

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
