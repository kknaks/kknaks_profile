
# 재개 노트 — sts-prototype (cc-prototype)

**지금**: 배포본 https://ccc.medisolveai.xyz — back 2abe704 · **front 14e5250(통역 되먹임 반이중 fix, infra PR #18)**. 사용자 E2E 3차 중(`e2e-feedback-batch-3.md`)
**다음**: 사용자 E2E(배포본) → 피드백 → 코드 PR main 머지 · 아카이브. 재배포 = 코드 push → Actions → values-prod tag → infra PR → argocd sync. 재시드 = PVC 의 cc.db 삭제 후 back 재시작

세팅: `scripts/new-work.sh cc-prototype sts-prototype` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc` (2026-10-13 terminal list 로 확인) · 중복·고아 task `task_ef0f1595fa70` · `task_eeac9547189d` · `task_7c4984ee9e0b` 는 failed 처리(무시)

## 워크트리



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] 조사 리포트 정할 것 Q-1~Q-10 중 Q-1(연결 구조)·Q-2(번역 모드)·Q-3(언어 쌍) 사용자 결정 대기
- [ ] 조사 결과로 sts 경로 결정(STS 단독 vs STT→번역→TTS) → 프로토타입 코드 발주
- [!] 배포 대상 미정(DEC-001 OQ-001)
- [!] cc 시안 링크 전체 URL 미기록(claude.ai/design/p/dda9a931-…) — 사용자에게 받기
- [!] iOS 모바일: Soniox 자동 포맷에 mp4 없음 — 모바일 화면이면 오디오 포맷 따로 정해야 함

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-10 | sts = 한국어↔다른 언어 음성 번역, Soniox(구독 중) 중심. STS 직행이 안 되면 STT→번역→TTS 허용 | 사용자 원문 |
| 2026-10-10 | 빨리 프로토타입 — 조사부터 | 사용자 원문 |
| 2026-10-12 | sts 는 별도 기능 폴더가 아니라 cc 안의 통역 기능. Soniox 연결은 cc/back | DEC-001 D-06 · 사용자 「dec 바꾸자」 |
| 2026-10-12 | cc 시안 import·구현은 DesignSync 되는 frontend 워커로 | 메모리 규칙 · researcher 보고 |
| 2026-10-12 | 화면은 2종 — 현황판(전체) · 로그인 후 역할별 개인 화면 | 사용자 「화면이 총 2개가 나와야해」 |
| 2026-10-12 | 역할은 의사 · 상담사(카운셀러) · 코디 · 간호 · 피부 | 사용자 「의사 카운셀러 코디 이렇게 가자」→「간호도 잇고 피부도 잇어」 |
| ~~2026-10-12~~ | ~~PoC 개인 화면은 **의사만**~~ — 2026-10-13 뒤집음: 모든 직원 화면 | 사용자 「poc에서는 의사만 잇으면 될거같아」→「아니 모든 직원 화면에 넣을건데」 |
| 2026-10-13 | 페이지 3종 — **로그인 · 데스크 페이지(=현황판) · 직원 페이지**. 직원 페이지는 역할별로 조금씩 다르게 그린다(= 사용자가 말한 「디자인 수정」). 통역은 **모든 직원 페이지**에 | 사용자 원문 |
| 2026-10-13 | 직원 페이지 두 갈래 — **코디·간호**(시술실을 돌아다님): 지금 내원 환자 목록 → 환자 상세 / **상담사·의사·피부**(방에 배정): 지금 내가 맡은 환자 = 「지금 진행 중」+「오늘 내 일정」(의사 모바일 시안 그 부분) → 환자 상세. 내 일정·내 동선은 상담·의사·피부만 | 사용자 원문 · 시안 캡처 |
| 2026-10-13 | 환자 상세는 전 역할 공통 — 환자명 · 오늘 예약 내역 · [통역][진료시작] / 환자 차트[펼치기] · 환자 메모[펼치기] · 시술이력 / 오늘 고객 동선 | 사용자 원문 |
| 2026-10-13 | 로그인 · 직원 페이지 역할별 · 통역 화면 시안은 **frontend 워커(DesignSync)가 초안** → 사용자 수정 | 사용자 「응 그렇게 가자」 |
| 2026-10-13 | 통역 컨셉 = **잠깐 필요한 짧은 통역**(통역사 부르기 싫을 때). 본 상담은 전문 프로그램이 따로 있음 → 위아래 분할 없음, 직원이 폰 들고 쓰는 단순 화면 | 사용자 원문 |
| 2026-10-13 | 통역 화면 = 환자 상세 위 모달 · **메신저형**(상대 말풍선 왼쪽 · 나 오른쪽, 원문+번역) · 언어는 환자 국적 자동(변경 가능) · 화자 전환 버튼 없음(two_way) · 켜기/멈춤 하나 | 사용자 「응 근데 메신저 처럼」 |
| 2026-10-13 | PoC 직원 페이지는 **의사 · 코디 둘만**(배정형 대표 · 돌아다니는형 대표). 상담·피부·간호는 다음 | 사용자 「구현 범위가 너무 크니까 의사, 코디 이렇게 2개만」 |
| 2026-10-13 | **가짜는 고객명뿐.** 메모·시술·시술이력·직원은 실데이터. 시술이력은 KOS API 로 보강 가능 — 스크립트 `/Users/kknaks/git/ax-clinic-project/scripts` · 가이드 `ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` | 사용자 「고객명만 가짜로 하라니까」 |
| 2026-10-13 | **KOS 는 운영 DB — 읽기 전용 절대.** 쓰기·수정 호출 금지 | 사용자 「실제 운영 디비라 절대 수정하면 안돼」 |
| 2026-10-13 | 버튼 — 의사: [통역][진료 시작] · 코디: [통역]만 (코디 추천안) | 사용자 「버튼은 추천으로 해줘」 |
| 2026-10-13 | Soniox 키 등 환경설정은 사용자가 직접 — 코드 쪽은 `.env.example` 만 둔다 | 사용자 원문 |
| 2026-10-12 | PoC 데이터 = **캡처한 KOS 데이터**(reference/2026-10-12-cc-prototype)를 목데이터로. 실시간 KOS API 연동은 나중 확장 | 사용자 「poc는 지금 더미 데이터로 만들건데 나중에 … kos api 연동」→「데이터는 지금 우리 데이터 쓰자니까」 |
| 2026-10-13 | 현황판은 **시안 그대로**(33칸 = 층 안내판 도면). 데이터 방 14개(A_ 하단 구역)는 도면의 부분집합 — **임시 순서 대응표**(코디 작성)로 끼우고 나머지 방은 빈 방. 실제 대응은 지점 확인 후 | 사용자 「시안 그대로 가고 … poc 니가 시안 대로 가도 될거 같아」 |
| 2026-10-13 | 데모 데이터는 **하루치만**. 고객 이름 = 가짜 · 시술 = 실데이터 · 직원 = 실데이터 | 사용자 원문 |
| 2026-10-13 | 현황판 ↔ 의사 화면 **연결**(back 이 상태를 든다 — 한쪽 조작이 다른 쪽에 반영) | 사용자 「나 로 연결 까지 해야해」 |
| 2026-10-13 | **초기화 = 시드 상태로 복귀.** 시드는 사용자가 앱을 움직인 뒤 「이걸 시드로」라고 지정 → 그 시점 상태를 시드로 저장. 첫 시드는 하루치 데이터 적재본 | 사용자 「초기화 하면 시드 상태로 … 이걸 시드 상태로 하자고 말할거야」 |
| 2026-10-13 | 첫 시드 = **10-09** 하루치 | 사용자 「10월 9일로 하자」 |
| 2026-10-13 | 통역 용도 = 의사·상담·코디가 외국인 환자와 **시술·이동 중 대면 대화**(통역사 호출 대체). **직원 폰·태블릿 개인 화면**에 뜬다(OQ-004 답) | 사용자 원문 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| researcher | `term_ccbeb5ee-150a-49ac-ac88-da0dd51c4f01` | `task_78ab55aeed37` | `ctx_731da713fa51` | `cc-data-fit-research-brief.md` → `research-cc-data-fit-report.md` | 완료(2026-10-12) — 리포트 `research-cc-data-fit-report.md` 수령 · 코디 개인정보 패턴 재확인 0건 |
| researcher | `term_4e46377b-beeb-4892-8fb8-70517fb63683` | `task_7a6f4cd3b6d6` | `ctx_06c4830cf3b4` | `soniox-chinese-research-brief.md` → `research-soniox-chinese-report.md` | 완료(2026-10-13) — `research-soniox-chinese-report.md` 수령 |
| frontend(시안) | `term_a10169a1-7391-473c-a46f-c08315dd6775` | `task_8dc07e4d20ec` | `ctx_d96c951b8890` | `cc-staff-design-brief.md` → `design-staff-report.md` | 완료(2026-10-13) — claude design 새 파일 4개 · 리포트 수령 · 사용자 눈 확인 대기 |
| researcher | `term_4e46377b-beeb-4892-8fb8-70517fb63683` | `task_48ae9423bff9` | `ctx_cf05adca891c` | `patient-detail-data-research-brief.md` → `research-patient-detail-report.md` | 완료(2026-10-13) — `research-patient-detail-report.md` 수령 |
| frontend(시안 r2) | `term_a10169a1-7391-473c-a46f-c08315dd6775` | `task_a457b12a875b` | `ctx_e452443f5311` | `cc-staff-design-r2-brief.md` → `design-staff-r2-report.md` | 완료(2026-10-13) — 의사·코디 파일 갱신 · 사용자 눈 확인 대기 |
| frontend(시안 r3) | `term_a10169a1-7391-473c-a46f-c08315dd6775` | `task_7af2aa55c14c` | `ctx_9c6cf2700901` | `cc-staff-design-r3-brief.md` → `design-staff-r3-report.md` | 완료(2026-10-13) — 리포트 수령 |
| backend WP1 | `term_eb0f5374-235a-4757-bb3a-1b2768c7e255` | `task_e356ee5c74db` | `ctx_0e51ca7fa9a2` | `wp1-be-brief.md` → `wp1-be-report.md` | 완료(2026-10-13) — pytest 20 · ruff clean 코디 재확인 · `.env`(Soniox 키 ← `~/.config/soniox/env`) 코디가 넣음 |
| backend WP2 | `term_eb0f5374-235a-4757-bb3a-1b2768c7e255` | `task_edd69d808493` | `ctx_8a10efa14b88` | `wp2-be-brief.md` → `wp2-be-report.md` | 완료(2026-10-13) — pytest 36 · ruff 코디 재확인 · 실물 4건(간체 → s2tw 자막 변환 · 광둥어 zh 로 번역됨 · TTS 간체만 · 음색 Jiwoo 24k) → fix1 완료(pytest 45) |
| frontend WP3 | `term_1bd4c892-2253-4670-9a5f-c6412cf15a9d` | `task_77d6bd57c1dc` | `ctx_d2ade0128a6b` | `wp3-fe-brief.md` → `wp3-fe-report.md` | 완료(2026-10-13) — tsc 0 코디 재확인 · `wp1-wp3-contract-addendum.md`(types.ts 가 계약) |
| frontend WP4 | `term_1bd4c892-2253-4670-9a5f-c6412cf15a9d` | `task_dfb92dcbb737` | `ctx_1176b14774ec` | `wp4-fe-brief.md` → `wp4-fe-report.md` | 완료(2026-10-13) — 계약 대조 완료(back 수정 0 · front 6건) |
| frontend(시안 r4) WP6 | `term_a1daffd6-7d91-48d1-87fe-bac9ebe6a012` | `task_75dacb3b4227` | `ctx_d2aa638cb84a` | `wp6-design-r4-brief.md` → `design-r4-report.md` | 완료(2026-10-13) · r4b 완료(미결제 · [결제 완료] · [초기화]) — 사용자 눈 확인 대기 |
| backend WP7 | `term_eb0f5374-235a-4757-bb3a-1b2768c7e255` | `task_894aba33761d` | `ctx_4c5c7c562cf8` | `wp7-be-brief.md` → `wp7-be-report.md` | 완료(2026-10-13) — pytest 41 코디 재확인 |
| researcher 시나리오 | `term_92c69c69-0fb5-4f2c-99f6-c189d24e0955` | `task_5edabc8bc3ee` | `ctx_d484e1e40a02` | `scenario-research-brief.md` → `scenario-report.md` + `cc/back/data/scenario/` | 완료(2026-10-13) — S1~S8 · staffIds 14 |
| backend WP7b | `term_eb0f5374-235a-4757-bb3a-1b2768c7e255` | `task_ecd9746f97f3` | `ctx_47048ac349b1` | `wp7b-be-brief.md` → `wp7b-be-report.md` | 완료(2026-10-13) — pytest 43 코디 재확인 |
| frontend WP8 | `term_1bd4c892-2253-4670-9a5f-c6412cf15a9d` | `task_e7ccfcfd7b06` | `ctx_ce21927d1dbb` | `wp8-fe-brief.md` → `wp8-fe-report.md` | 완료(2026-10-13) — tsc · lint · build · 코드 커밋 9f8f712 |
| frontend(시안 r5) | `term_0b06bf42-18f0-4292-8d50-500c8bcc2cb6` | `task_c0bfd9b60a15` | `ctx_c901494a65ca` | `design-r5-brief.md` → `design-r5-report.md` | 완료(2026-10-13) |
| backend WP10 | `term_eb0f5374-235a-4757-bb3a-1b2768c7e255` | `task_a14327d8c49b` | `ctx_3a642dd0476a` | `wp10-be-brief.md` → `wp10-be-report.md` | 완료 · fix1 완료(pytest 50) |
| researcher 직원 이름 | `term_6aefc840-e29e-4b09-b06b-144dec5b0b7a` | `task_678bec09d39d` | `ctx_27bb2fb1be23` | `staff-rename-brief.md` → `staff-rename-report.md` | 완료 — 실명 65 · 이메일 88 가짜. **로컬 seed.json · 백업 · cc.db 는 아직 실명 → 로컬 스택 재기동 때 seed build** · map/orig 파일은 Secret 금지 |
| backend 배포 | `term_7993d892-b5e4-4ff8-8ee9-ade502f64924` | `task_3a960c2eb904` | `ctx_4850d0aaffa0` | `deploy-be-brief.md` → `deploy-be-report.md` | 완료 — 로컬 컨테이너 health 200 · pytest 53 |
| frontend 배포 | `term_b8c9cf80-7ebb-4df8-8d9c-db451c88c768` | `task_d466afbaa017` | `ctx_83366851d16c` | `deploy-fe-brief.md` → `deploy-fe-report.md` | 완료 — docker 200 · wss 확인 |
| infra 배포 | `term_38643bb0-bece-4c6f-abd4-eb8a801ed023` | `task_e88c71b08b70` | `ctx_f37a7adab1b6` | `deploy-infra-brief.md` → `deploy-infra-report.md` — 워크트리 `/Users/kknaks/orca/workspaces/k8s_infra_mac/sts-prototype` | 완료 — lint · template 통과, dry-run 은 medi-me 에서. 클러스터 접근 = `ssh medi-me` + `/opt/homebrew/bin/kubectl` 확인 |
| frontend WP11 | `term_b8c9cf80-7ebb-4df8-8d9c-db451c88c768` | `task_8aa50a4a2768` | `ctx_20975f3db451` | `wp11-fe-brief.md` → `wp11-fe-report.md` | 발주(2026-10-13) — 배포 전 필수(WP10 back 계약과 맞춤) |
| researcher | `term_92c69c69-0fb5-4f2c-99f6-c189d24e0955` | `task_74f8a2ea95c6` | `ctx_6cdf5007c311` | `counselor-trace-research-brief.md` → `research-counselor-trace-report.md` | 완료(2026-10-13) — `research-counselor-trace-report.md` |
| researcher | `term_92c69c69-0fb5-4f2c-99f6-c189d24e0955` | `task_b140c10eb08f` | `ctx_266d4b492e3e` | `kos-har-research-brief.md` → `research-kos-har-report.md` | 완료(2026-10-13) — 1차 `research-kos-har-report.md` · 2차 `research-kos-har2-report.md`(완료·담당자·집도의·상담사 내부 API 확인) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-10-12` cc 문서·설정 커밋 1fc792b(프로필) · 시안 사본 1d11cf2(코드). researcher 발주 — cc 시안 × 운영 데이터 적합성 조사

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
