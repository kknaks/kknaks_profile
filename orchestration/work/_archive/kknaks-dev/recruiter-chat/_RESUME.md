
# 재개 노트 — recruiter-chat (kknaks-dev)

**지금**: **전 라운드 종료(수정 11건: BE 7 · FE 5 · 리뷰 1) — e2e 전부 완료.**
최종: back **162** · mcp **24** · tsc 0. spec **v0.0.12**(패널 유형표까지).
e2e 5종(개인·resume·회사 제품·프롬프트 우선순위·카드 url) 실측 통과. 우측 문서 패널 가동.
(이전 기록:) **구현·검증 전부 완료.** fix1·fix2 반영, back 133·mcp 24, 로컬 compose
e2e 완주(첫 질문 ~15초 · resume · retry · 근거 · tool 단계 · Bearer 노출 0).
work-023·024 done, DEC-027 OQ-2 닫힘. 프론트 dev 가 :3000 에서 떠 있다(사용자 확인 중).
**다음**: FE fix2(스크롤)·BE fix4(회사 제품 tool) 완료 → FE fix3(admin product 토글 화면,
fix2 뒤 순차) → 회사 제품 질문 e2e 재확인 → rebase(origin/main 2d07629, 겹침 main.py) → **코드 PR**
(recruiter-chat → main) + **문서 PR**(agent → main, para·orchestration) → 머지 후
로컬 스택 down → archive-work.sh(SUMMARY → para log/ 첫 착지). 배포 전 레이트리밋 결정.

세팅: `scripts/new-work.sh kknaks-dev recruiter-chat` · 설정 SSOT `config/projects/kknaks-dev.json`
코디handle: `term_53806a6d-ced5-4948-88bd-4181b7ba4323`

## 워크트리

- `app`: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat` (branch `recruiter-chat`, base `origin/main` → PR `main`)

## 1. 지금

- [~] backend 워커 — WORK-023 (스키마·세션·API → MCP → 제출 → 소비자·compose)
- [~] frontend 워커 — WORK-024 (홈 재구성 → /chat+폴링 → tool 단계·근거·어드민 토글)
- [ ] 완료 후: 실물 검증 → reviewer_code 검수 → 통합 확인(FE mock→실 API 전환) → PR
- [!] **문서(para/·orchestration/)는 코디 agent 브랜치에 미커밋 상태** — 워커 완료와 별개로
  spec/결정/work 문서 커밋 + PR(코드와 분리) 필요
- [!] 레이트리밋은 범위 밖이지만 **공개 배포 전 필수** (DEC-026 OQ-1)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-08-28 | 설계 SoT 는 KDEV-SPEC-017 v0.0.3 (+DEC-025/026/027) | 사용자와 문답으로 OQ 전부 닫음 |
| 2026-08-28 | 실행 계약은 mediness-app landing-chat 레퍼런스 채택(소비자 폴딩·HTTP MCP·shell off) | 사내 검증 구현 실측 |
| 2026-08-28 | 프론트 수신 채널은 2초 폴링 (WS 이식 안 함) | 사용자 확정 |
| 2026-08-28 | BE·FE 병렬 발주 (같은 워크트리, allowed_paths 분리) | 같은 작업 단위의 분담 |
| 2026-08-28 | career·problem 은 **합성 slug**(`<company.slug>-<id>` / `problem-<id>`) — slug 컬럼 신설 안 함. 파싱 실패=미존재=미노출=404 동일, 근거 url 은 공개 표면 경로 | BE 워커 질문 → 코디 승인, spec §4 반영 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_73d0b8541843` | `ctx_1bfa4d9aa6db` | `recruiter-chat-be-brief.md` | **완료** — 코디 검증 통과(105+19 재현) |
| frontend | `term_21382c78-614d-479f-a39e-18a6ce3b47ca` | `task_ad2c23b53722` | `ctx_46df0ce3992b` | `recruiter-chat-fe-brief.md` | **완료** — 코디 스팟 검증 통과 |
| reviewer_code | `term_b90554e5-21e2-4adf-94d4-8b46d6948509` | `task_47fc06db06e0` | `ctx_f172daafbff2` | `recruiter-chat-review-code-brief.md` | **완료** — WARN(FAIL 0), 리포트 `review-code-report.md` |
| backend fix1 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_defc940beda2` | `ctx_11b43cb69eba` | `recruiter-chat-be-fix1-brief.md` | **완료** — 코디 검증(125+24 재현). BE의 「FE가 retry 안 씀」 경고는 stale(FE fix1 이 이미 전환) |
| backend fix2 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_15aaed881f78` | `ctx_8bed8250c6c7` | `recruiter-chat-be-fix2-brief.md` | **완료** — 명시 커밋 후 큐잉(3경로), 133 passed(코디 재현), e2e 로 실동작 확인 |
| frontend fix1 | `term_21382c78-614d-479f-a39e-18a6ce3b47ca` | `task_b0eff501c2fa` | `ctx_cc97fb4cb3af` | `recruiter-chat-fe-fix1-brief.md` | **완료** — 코디 검증(tsc 0 · retry 경로 · hex 제거 확인) |
| frontend fix2 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` (구 FE 터미널 agent 종료 → 신규) | `task_20ae3b42def0` | `ctx_7490e31e9d72` | `recruiter-chat-fe-fix2-brief.md` | **완료** — 앱 레이아웃+bottom-stick, tsc 0, Playwright 실측 3종 PASS(코디 스팟 확인) |
| frontend fix3 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` | `task_dbd73d3cfa51` | `ctx_96d7604a998b` | `recruiter-chat-fe-fix3-brief.md` | **완료** — 토글+types 계약, tsc 0(코디 재현). 화면 확인은 BE fix4 도착 후 |
| backend fix3 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_895efb69080d` | `ctx_35aba7be5f46` | `recruiter-chat-be-fix3-brief.md` | **완료(141)** — 경로는 열렸으나 **조사로 진짜 원인 발견**: 회사 제품은 `product` 표에 살아 tool 표면에 아예 없음(4/5는 archive 경로) |
| backend fix4 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_4dc0066b669f` | `ctx_cca8cfa17fcf` | `recruiter-chat-be-fix4-brief.md` | **완료(155+24)** — 회사 제품 tool 2종·마이그레이션 c2e91a7b40d5(로컬 적용됨)·archive 루트. **e2e 성공**: list_company_products→showcase 5개→구체 답변. product 표 전체가 회사 제품(career_id NOT NULL)이라 소속 필터 불요 |
| backend fix5 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_225b0830b9bf` | `ctx_159e4d7e5646` | `recruiter-chat-be-fix5-brief.md` | **완료(158+24)** — 문서유형/토글kind 축 분리, url 명시적 None. e2e 카드 확인 |
| backend fix6 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_c8b07c1e68bd` | `ctx_543526cffe5b` | `recruiter-chat-be-fix6-brief.md` | **완료(162)** — 프롬프트 ③ 미공개로 축소 + stale 세션 우선 지침. 새 대화 e2e 로 확인 |
| backend fix7 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_5049a0736a7e` | `ctx_46a92c3814a4` | `recruiter-chat-be-fix7-brief.md` | **완료(162)** — company_product url → /career(패널 보조링크). e2e url 확인 |
| frontend fix5 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` | `task_580f4cc6be33` | `ctx_0365299b5d61` | `recruiter-chat-fe-fix5-brief.md` | **완료** — 근거 카드 → 우측 문서 패널 3열(owner 확정 B: product·career·problem 패널 / project·note 이동). 렌더러 공용 추출, page-fade fixed 버그 발견·수정, Playwright 실측 PASS, tsc 0(코디 재현) |
| frontend fix6 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` | `task_185a803364d8` | `ctx_6890abd77051` | `recruiter-chat-fe-fix6-brief.md` | **완료** — 패널 타이포 스코프 축소(career 모달 무변경) · 컴포저 14px(mono/sans 시각차가 원인) · 모바일 좌 햄버거+우 문서 드로어(spec v0.0.13, DEC-025 OQ-3 닫힘). 375px 실측 PASS, tsc 0(코디 재현) |
| backend fix8 | `term_c671fcce-b458-4f70-a527-346229b9b7b7` | `task_99435290b0e1` | `ctx_f61c0376a041` | `recruiter-chat-be-fix8-brief.md` | **완료(167)** — 재현 실패(구멍 없음: project 는 원래 visible∧chat_exposed). 유형별 공개조건 표 문서화 + 회귀 5건 잠금. 404 의 진짜 원인은 **mock 화면 오인**(픽스처 문구·카드 일치, 실DB 에 해당 질문·카드 없음). 스냅샷 링크 위험은 spec OQ-5 로 v1 수용 |
| frontend fix7 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` | (terminal 직접 지시) | — | — | **완료** — mock project 카드 kknaks-dev → wine-log(죽은 링크 제거, :3000 실측 200) |
| frontend fix4 | `term_367b104a-5e3b-4d1c-98fe-94b8e46b79f4` | `task_a750c8cdcad6` | `ctx_c31d53d6324e` | `recruiter-chat-fe-fix4-brief.md` | **완료** — ChatSourceType+라벨 'product'+mock, tsc 0(코디 재현) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.**

## 4. 산출물

- code PR: https://github.com/kknaks/kknaks_profile/pull/23 (recruiter-chat → main, rebase 완료·169 passed)
- docs PR: https://github.com/kknaks/kknaks_profile/pull/24 (docs/recruiter-chat — agent 의 이번 세션 범위만 추출. agent 브랜치의 이전 세션 드리프트 14파일은 범위 밖으로 제외)
- 리포트: `review-code-report.md`
- 머지 후: 홈서버 pull → compose up --build back mcp chat-worker → alembic upgrade head(2건) → 어드민 노출 ON → 실질문 확인. **공개 전 레이트리밋 필수**

- [!] **로컬 검증 스택이 워크트리에서 떠 있다**(kknaks-postgres/redis/back/mcp/chat-worker,
  워크트리 compose) — archive 전에 `docker compose down` 필수. `.env` 는 canonical 에서
  복사(미추적). `docker-compose.local.yml` 의 chat-worker node 마운트 타깃 덮기 1줄은
  **코디가 수정**(검증 배선 — prod 마운트가 맥에서 mounts denied).
- [~] 프론트 dev :3000 떠 있음(백그라운드 b2s0s6skz) — 사용자 화면 확인 중.
  구 리뉴얼 dev(:3000 점유, 3일 방치)는 죽였다

## 5. 이력 (최신이 위)

- `2026-08-28` kknaks-dev 프로젝트 config·roles 신설 → new-work.sh 세팅 → BE·FE 브리프 작성 → 병렬 발주
