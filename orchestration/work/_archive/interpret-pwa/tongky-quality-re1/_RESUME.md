
# 재개 노트 — tongky-quality-re1 (interpret-pwa)

**지금**: WP33 배포 끝(코드 #15 `56e43a0` · infra #59 back 태그 · 시드 `.11` 로드 · health 200) — 사용자 실기기 기다림. 되돌리기 = back 태그 `c7a582f`
**다음**: 실기기 기록 받아 사전 이름 확인 · 열린 것: zh-Hant `雷射`→클라리티2(리뷰 W-1 · 사용자 결정) · 제모→제목 · 여섯 언어 n=3 · 문서(D-71 SPEC §4.2 · §4.5 · §4.6 · 리뷰 D-1~10)

세팅: `scripts/new-work.sh interpret-pwa tongky-quality-re1` · 설정 SSOT `config/projects/interpret-pwa.json`
코디handle: `term_0cdc063d-4b42-4e5f-bc41-65528f81e60f`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `app`(코디): `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
- `code`: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1` (branch `kknaksss/tongky-quality-re1`, base `origin/main` → PR `main`)

## 1. 지금

- [ ] **사용자 실기기 zh 대화 기다림** — 배포 끝(2026-11-16 · 코드 #14 `c7a582f` · infra #57 back → #58 front · pod 둘 Running · 시드 `.10` · 운영 front 번들에 `playback_stopped` 확인). 끝나면 기록 받아 SPEC §9.6 0.9.5 ③ⓐ ~ ⓕ · OQ-035 로 본다. 되돌리기 = infra 태그 back `fe375ad` · front `fe8475e`
- [ ] SPEC 문장 맞출 자리(코드 리뷰 r2 참고): §9.1 에 FAIL-1 시험 줄 · WARN-3 로그 줄 · WARN-4 세션 끝 줄 · WARN-1 「가짜 시계」 대신 상수 덮어쓰기
- [ ] 문서 PR 아직(DEC D-67 ~ D-70 · BASE 입력 6 · SPEC 0.9.4 → 0.9.5 · WORK WP28 ~ 32) — 코디 브랜치 미커밋
- [ ] 처음 할 일 남음: 09:33 zh 7문장 세션(`c40e…`) 분석
- [!] 11:00 세션 별건(처분 없음): 玻尿酸 오역 · 내 쪽 「써마지」 → `Surmag` · 바로잡기 조사 「는」 남김 · side 섞임
- [!] 기록 문장은 레포 금지(PUBLIC) — 로컬 `reference/2026-11-12-interpreter-idea/records/`
- [!] 개념 `half-duplex-echo-suppression` 은 D-68 로 대체됨 — 마감 때 개념 갱신(코디)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-16 | D-69 차례 끝 = 서버 시계 1초(실제 무음 약 2초) · 끼어들기 = 반대 언어 토큰 2개 · **agent text 사용** · D-70 OQ-037 ~ 039 기본값 + SPEC 리뷰 처분(멈춤 중 여유 0 · audio_stop 먼저 · cancel 한도 3초 · 좁은 창 감수 · agent text 다음 발화도 0.7초 앞) | 조사 리포트 · 사용자 「실제 무음 약 2초」 「agent text 쓴다」 · 나머지 코디 |
| 2026-11-16 | **D-68 세 참여자**(고객 – 통키 – 직원 · 순차 통역사 행동 ① 차례 끝에 음성 ② 늘 듣기 ③ 재생 언어 버림 ④ 끼어들면 물러남 · 기본값 1초 · 바로 멈춤 · 자막만) · BASE-001 입력 6 · OQ-034 ~ 036 | 사용자 「이 개념이야!!」 · 「코드 구현까지 가자」 |
| 2026-11-16 | ~~손님 말 번역은 자막만(A안)~~ — 같은 날 사용자 「설계를 다시」 로 폐기 → D-68 | 사용자 |
| 2026-11-16 | D-67 끊김 `max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3 · 설정만(끼어들기 안 함) | 실기기 11:00 zh 세션 잘림 6 · 공식 endpoint-detection · 사용자 「일단 설정만 바꿔서 배포」 |

## 3. 발주 (살아 있는 것만)

- researcher 요금 갱신 `task_410451653817` · `ctx_c04fc36e3a4b` · 터미널 `term_94b27364-252e-42f2-a4e6-a53e63e29109` · 브리프 `tongky-quality-re1-research4-brief.md` · 대상 `reference/2026-11-12-interpreter-idea/price-v2.md`(새 파일 · 로컬 · price.md 원본 유지) · 리포트 `research-price-update-report.md`

- (끝) reviewer WP33 WARN(FAIL 0) `task_fb311693e3aa` · `ctx_96239b5fca31` · 터미널 `term_b55c12e8-165c-4c8a-96c1-870dec4ec2a6` · 리포트 `review-wp33-code-report.md`
- (끝) backend WP33 `task_b48643878a02` · `ctx_3ff0775b2df9` · 터미널 `term_b4173bbe-8254-47fb-bbcd-7b7d07dfbdf3` · 브랜치 `kknaksss/tongky-quality-re1-dict` · 브리프 `tongky-quality-re1-be5-brief.md`

앞 발주 없음(planner · backend · reviewer 완료 — run `run_b6888e30d5a3`).

## 4. 산출물

- 문서: 코디 브랜치 미커밋(DEC D-67 · SPEC 0.9.4 · WORK WP28 · WP29) — PR 아직
- code PR: kknaksss/interpret-pwa #13 머지 `fe375ad`
- infra PR: MediSolveAIDev/k8s_infra_mac #56 머지(back 태그만) · 워크트리 `/Users/kknaks/orca/workspaces/k8s_infra_mac/tongky-quality-re1`
- 리포트: `review-wp28-code-report.md`(PASS · WARN 1 권고 — quality_check 결과 기록이 기본값을 상수로 복제)

## 5. 이력 (최신이 위)

- `2026-11-16` 실기기 19:20 ~ 19:37(zh-Hant · zh · en · ja 세션 7) — 울쎄라 zh/en/ja 맞음 · zh 써마지 → `超声刀` 4/4 · ja 「서마지」(AI 음성 · 사용자 「어쩔 수 없지」) · 제모 실기기 정상 · 손님 `超声刀` = 넓은 말(고칠 것 아님) → 요금 실측 발주

- `2026-11-16` WP33 배포: #15 `56e43a0` → back 이미지 → infra #59 → Argo sync → back pod Running · 시드 `.11` · health 200 (front 그대로 `c7a582f`)

- `2026-11-16` D-71 실물(고유명사 ① 만 → 울쎄라 18/18) 뒤 사용자: 별칭 빼고 정방향 + 역방향 · terms 도 74 만 · 「코드 수정해서 재보고 괜찮으면 바로 배포」 → WP33 발주

- `2026-11-16` 배포: #14 머지 `c7a582f` → 이미지 둘 → infra #57(back) sync 확인 → #58(front) sync · health 200

- `2026-11-16` 계정 바꿈(사용량) 뒤 재개 → SPEC 재검수 WARN 3(처분 → back 에 바로 전달 · SPEC 맞춤) · frontend WP31 · backend WP30(pytest 518 · 실물 ㉘ 6/6) → 코드 리뷰 FAIL 1 · WARN 4 → 수정(525) → 재검수 PASS → PR #14

- `2026-11-16` SPEC 0.9.5(§5.13 세 참여자 · `audio_stop` · `playback_stopped` · agent text) → 문서 리뷰 FAIL 1 · WARN 8(`review-spec-095-report.md`) → 처분 D-70 ④ → planner 수정 끝 · 재검수 전
- `2026-11-16` researcher OQ-034 ~ 036 → `research-turn-taking-report.md`(합성 63 세션)

- `2026-11-16` 배포: Argo sync → back pod `fe375ad` Running(lima-worker-1) · 시드 `.10` 로드 · 기록 on · health 200
- `2026-11-16` Soniox 실물 1회(운영 키 · 로컬 스크립트): 2000 · -0.3 오류 없음 · 대조 범위 밖 값(5) 거절
- `2026-11-16` D-67 → planner(SPEC 0.9.4) → backend(WP28 · pytest 489) → reviewer PASS
- `2026-11-16` 서버 기록 11-15 · 11-16 로컬로 · 11:00 zh 세션에서 손님 쪽 문장 중간 잘림 6 확인(원인: 끊김 상한 1000 + 반이중으로 재생 중 소리 버림)

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
