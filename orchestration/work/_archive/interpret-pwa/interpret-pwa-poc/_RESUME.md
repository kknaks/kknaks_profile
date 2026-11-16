
# 재개 노트 — interpret-pwa-poc (interpret-pwa)

**지금**: 8차 배포 완료 — D-37 최소 노출(코드 PR #8 · back/front fe8475e 같은 sha · infra PR #33 · 개별 imageTag 오버라이드 정리됨). 확인: health/me {ok} · /api/glossary 404 · docs 404 · wss ready. 문서 PR profile #106 — D-35~D-37 · 장애 갱신 필요
**다음**: 사용자 시드 PR 또는 폰 피드백 → 문서 PR(profile: DEC · SPEC 0.4.0 · WORK · 이 work/) → archive-work.sh

세팅: `scripts/new-work.sh interpret-pwa interpret-pwa-poc` · 설정 SSOT `config/projects/interpret-pwa.json`
코디handle: `term_ce3ec37d-8f58-4bca-9420-d55b08c591e2`

## 워크트리

- app(문서): 이 코디 워크트리 — planner 가 탄다
- code: 아직 없음 — backend/frontend 추가 때 `new-work.sh interpret-pwa interpret-pwa-poc --workers backend,frontend`

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] 사용자 폰 테스트(WP8 §9.5)
- [ ] planner SPEC 0.4.0 동기(D-22~D-26 · 18832) · 문서 PR
- 재배포: 코드 main push → Actions → infra values-prod image.tag → PR 머지 → `ssh medi-me` kubectl patch application interpret-pwa-prod sync
- 시안: https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd (확정 · r2 통키)
- [ ] WP6 묶음 수정 — `e2e-feedback-batch-1.md`
- [!] 코디 dev 서버는 WP6 발주 전에 내림
- [ ] 사용자 확인 필요(WP7): SPEC OQ-001(yue = 만다린 TTS) · OQ-005(시작 오버레이 · 원=멈춤) · OQ-007(로컬은 맥 브라우저, 폰은 배포 뒤)
- [!] 이 레포는 public — 계정 비밀번호를 문서에 적지 않는다(env 로만)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-26 | 새 레포 `kknaksss/interpret-pwa`(private) · 프로젝트 `interpret-pwa` · 결정 내용은 DEC-001 D-01~D-12 | 사용자 대화 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_e1c2b1d0-e8e2-4404-81b0-8e782528ed37` | `task_d0a13a982617` | `ctx_5326656f5390` | `interpret-pwa-poc-spec-fix1-brief.md` | 완료(SPEC 0.2.0) |
| backend | `term_1bd12d37-5983-42a7-92b3-a39f7344659d` | `task_44888dbc3321` | `ctx_98414db3bd8c` | `interpret-pwa-poc-be-brief.md` | 완료(WP1·2) |
| frontend | `term_88b66637-40dd-4600-a461-5ef4f1dcd811` | `task_0636c9292f03` | `ctx_963318557861` | `interpret-pwa-poc-fe-brief.md` | 완료(WP3·4) |
| reviewer | `term_fa6245a8-e7ee-4932-8825-9d32d8e15030` | `task_7eaea892be43` | `ctx_9ffec7313a5f` | `interpret-pwa-poc-review-brief.md` | 완료(FAIL 1 · WARN 6) |
| designer | `term_c6b8d5fa-0ac4-433d-a526-e893ca6c097e` | `task_909473d5232f` | `ctx_0bba3a8b6b89` | `interpret-pwa-poc-design-brief.md` | 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-10-26` 착수 — 레포 생성 · orca repo 등록 · config/roles · para 제품 폴더 · BASE-001 · DEC-001

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
