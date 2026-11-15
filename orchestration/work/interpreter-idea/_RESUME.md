# 재개 노트 — interpreter-idea (interpret-pwa)

**지금**: 품질 개선 **배포 완료**(2026-11-15 · code PR #12 → `6d57ba3` · infra PR #55 · sync · 시드 `.10` 로드 · 기록 keep_days=off) · 패치 노트 https://claude.ai/artifact/F2ZPH3NvgH2qPisfUaWGQP(배포 완료로 갱신) · **남은 것**: 사용자 폰 실물 확인 · 프로필 문서 PR(price.md 1.4 상담 문장 PUBLIC 처리 먼저 묻기) · 마감 archive-work.sh(회고 · 개념)
**다음**: 프로필 문서 PR 은 **보류**(사용자 2026-11-14 — 오역 수정 코드 업데이트와 같이 올림). 그때 price.md 1.4 상담 문장(PUBLIC) 처리 먼저 묻기. 마감은 archive-work.sh. OQ-020(베타 종료 때 값) 열림.
**요금 · 아이디어**: `price.md` 1 ~ 4절 · `idea.md` 커밋 `0bcb0ebe`(push 전). 남은 결정 = 마진율 · 포함 대화 수 · context 축소 · 무발화 종료 시간 · 상담 비율 기준(시간/건수) · price.md 1.4 상담 문장(인터뷰 출처 — PUBLIC) · 앞 판 문서(pricing-design · pricing-function · g*/pd*) 처분 · 원본(PDF · 캡처 · useage.md) 커밋 여부.
**운영 통역 기록 사본**: `reference/2026-11-12-interpreter-idea/records/` (11-11 ~ 11-14 · 세션 43 · 발화 137) — `info/exclude` 로 git 제외(PUBLIC · 문장 포함).

세팅: `scripts/new-work.sh interpret-pwa interpreter-idea` · 설정 SSOT `config/projects/interpret-pwa.json`
코디handle: `term_d181fbae-29f2-43bb-9a41-6bc888ca07de` · Run: `run_7ec81cd08e35`

## 1. 지금

- [~] researcher — `pricing-design.md` (브리프 `interpreter-idea-research-brief.md`)
- [!] `pricing-function.md` §3 이후(§5 ~ §10 · g3/g4 그래프)는 코디가 근거 없이 쓴 것 — 새 보고서 나오면 처분(사용자에게 묻기)
- [!] 아이디어 문서(0 · 1 · 2단계)는 앞 판 취소. 다시 할지 사용자 미정
- [!] PUBLIC — 원본(PDF 2 · 캡처 · useage.md) gitignore 여부 미정

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-12 | 요금제 후보 = 시간제 · 토큰제 · 정액제 비교 | 사용자 |
| 2026-11-12 | 30일 · 근무 12h · 실사용 1 ~ 12h · 동시 1 ~ 5 · 상담 비율 0 : 100 | 사용자 |
| 2026-11-12 | 무발화 1분 세션 종료(정책) · 연결 고정비 = 최대 context 언어로 통일 | 사용자 |
| 2026-11-12 | 분석 = 독립변인 1개 · 나머지 해피/워스트 고정. 가격은 범위에서 역산(결과) | 사용자 |
| 2026-11-12 | 특정 병원 · 지점 데이터 쓰지 않음. 앞 작업(아이디어 · 요금제 1 ~ 3판) 전부 취소 | 사용자 |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner (fable) | `term_bab04d70-ca05-420e-8996-9e7d2e3a953b` | `task_850059b51d60` | `ctx_9a55e9914e70` | `quality-spec-fix2-brief.md` | 완료 — SPEC 0.8.2 · WP23 · OQ-030(코디 처분 → dispositions §4) · ja · th 한도 열림(§5) |
| reviewer_doc (fable) | `term_84f40940-7d19-4ce7-b55c-2f76c48155c8` | `task_1820b701690b` | `ctx_d63083d4076f` | `review-doc-quality-6-brief.md` | 0.9.0 검수 완료 — `review-quality-doc-report-6.md` |
| researcher r1 (fable) | `term_abd0126a-6243-4b84-9616-3629e04aa7d1` | `task_cda6a9026613` | `ctx_c6c23c6620bc` | `quality-r1-zh-brief.md` | 완료 — 510칸 · 표 A 95행 · 정할 것 12 · `quality-r1-zh-report.md` · `-cells.json` |
| researcher r2 (fable) | `term_2480bb9c-aef3-4923-8c0f-2909b198366c` | `task_64d2df2acd28` | `ctx_563abe7e5e30` | `quality-r2-en-ja-th-vi-brief.md` | 완료 — 680칸 · 정할 것 17 · `quality-r2-en-ja-th-vi-report.md` · `-cells.json` |

| backend WP21 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_bbd2ba29a949` | `ctx_f9cb78328c42` | `quality-wp21-be-brief.md` | 완료 — pytest 407 · ㉒ 7개 언어 거절 0 · zh-Hant `terms` 170 + 역방향 별칭 44 빠짐 · `wp21-be-report.md` |
| reviewer WP21 (opus) | `term_023c5b4c-6d18-4fb0-a27b-ec8fa0acf608` | `task_4f1fdcc8a57f` | `ctx_d39fafe2057b` | `quality-wp21-review-brief.md` | 완료 — WARN 4(FAIL 0) · `review-wp21-code-report.md` |
| backend WP21 수정 1 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_ddd4ca654c88` | `ctx_24b865257453` | `quality-wp21-fix1-be-brief.md` | 완료 — pytest 412 · v6 거절 = 첫 메시지(374 ~ 474ms) → `_check_config` 그대로 · 코드 로컬 커밋(push 전) |
| researcher r3 대만 별칭 (fable) | `term_db3667db-6cfe-4684-aa18-85104b414f88` | `task_a4fb15528ddd` | `ctx_fc807016a318` | `quality-r3-tw-alias-brief.md` | 완료 — 유지 161 · 뺌 77 · 겹침 7 · 뺌 반영 22,095자(한도 21,689 · 406 초과) · `quality-r3-tw-alias-report.md` · `.json` |
| planner 0.8.3 (fable) | `term_abdfc414-5fdf-42c2-aca3-9c64b4cc071c` | `task_e07ccf04c278` | `ctx_1574d52b5c32` | `quality-spec-fix3-brief.md` | 0.8.4 완료 · 재검수 PASS(`review-quality-doc-report-5.md`) — 사전 문서 단계 끝 |
| backend WP22 ① (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_f37486527ab4` | `ctx_b0104473b366` | `quality-wp22-be-brief.md` | 완료 — 기계 FAIL A 15 / B 7 · 사람 오역 A 12 / B 7 · 지연 중앙값 A 1,580 / B 516ms · 3절 v6 도 조각 · `wp22-be-report.md` · `wp22-human.json` |
| backend WP23 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_cef7a343f19c` | `ctx_df891a3dd26d` | `quality-wp23-be-brief.md` | 완료 — 시드 `.7` · D-54 27 뺌 · v6 실측 → D-54 5 멈춤 → **D-56**(× 0.96) · `wp23-be-report.md` |
| backend WP24 ① (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_0755c345fe98` | `ctx_3ab444e4a44a` | `quality-wp24-be-brief.md` | 완료 — C · C2 · 손님 쪽 18/21 · 다국어 묶음 C 21/35 FAIL |
| backend WP26 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_ecfce62f41be` | `ctx_bf9187793f3b` | `quality-wp26-be-brief.md` | 완료(수정 1) — 시드 `.8` · 바로잡기 · pytest 447 · 연기 22/39 · `wp26-be-report.md` |
| reviewer WP26 (opus) | `term_15cca63d-5a2d-4753-a247-cde1162df48f` | `task_b48bf077b564` | `ctx_b3985c859892` | `quality-wp26-review-brief.md` | 완료 → 처분 §14 → backend 수정 2 완료 · 코드 커밋 `0ec772d`(push 전) |
| researcher r4a (fable) | `term_133d6a82-b91e-4f3d-97c0-dd0ef56a50c4` | `task_90df1e6296fb` | `ctx_efe234724875` | `quality-r4a-zh-brief.md` | 완료 — 38/136 현지 글자 · `r4a-zh-report.md` |
| researcher r4b (fable) | `term_d6e2a95f-064d-4137-8335-719a2638e4c9` | `task_2471f3ef30f2` | `ctx_24b5d715e80a` | `quality-r4b-th-ja-brief.md` | 완료 — 42/84 현지 글자 · `r4b-th-ja-report.md` |
| backend 시드 .9 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_57b9c8dce282` | `ctx_340729d92add` | `quality-seed-v9-be-brief.md` | 완료 — name 73 · 별칭 36 뺌 · ja · th terms 줄이기(D-62) · `seed-v9-be-report.md` |
| backend WP27 (opus) | `term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b` | `task_cf84d8c13b58` | `ctx_d7c752e3a626` | `quality-wp27-be-brief.md` | 진행 — 7차 나라별 · 문장 초안 뒤 코디 확인 |
| planner 0.9.0 (fable) | `term_999506d9-1342-4e49-bca8-25f4cb1aa731` | `task_2ca15781af05` | `ctx_e69d828e6c02` | `quality-spec-v090-brief.md` | 0.9.1 완료 · 확인 PASS(`review-quality-doc-report-7.md`) · 문서 커밋 `b37783db` |
- 배포 순서(사용자 2026-11-15 「진행하자」): backend 수정 3(D-65) → 배포 전 재검수 → planner 0.9.3(D-65 한 줄 · OQ-033 은 D-65 로 닫음) → 코드 · 문서 커밋 · PR → Actions sha → infra 태그 PR → sync → 운영 확인 → 패치 노트 「배포 완료」 로 다시 올림(https://claude.ai/artifact/F2ZPH3NvgH2qPisfUaWGQP · 파일 scratchpad tongky-patch-notes.html)
- **이번 판에서 다 고친다**(사용자 2026-11-15 「한김에 다 고치고 가자」) — D-58 바로잡기 · D-59 나라별 시험 · 결과 페이지 언어별 탭
- **배포(WP25)는 사용자가 결과를 본 뒤** — 사용자 2026-11-14 「배포 전까지만 해놓자 · 24번까지 내가 결과 볼수 잇게 정리」. WP24 뒤 산출: 전후 비교 HTML(로컬 전용 · A · B · C · C2 나란히 · 요약 숫자 · 카톡 지적 문장 표시) + 결정할 것 목록(끊김 1초/2초 등 · 추천 포함)
- 판단은 추천안으로 진행(사용자 「추천으로 가줘」) — 사용자에게만 남는 것: D-54 로 안 닫히는 한도
- WP24 발주서에 넣을 것: 조합 C2(= C + `max_endpoint_delay_ms` 2000 · D-55) · 손님 쪽 21문장(D-50) · 사람 판정은 코디(`wp22-human.json` 과 같은 등급)

다음: WP21 완료 → reviewer(코드) · 토닝 zh 사용자 확인 → planner 0.8.2(§4.2.4 값 · N-1 ~ N-3) → WP22(시험 「전」 · 12-15 전) → WP23 → WP24 → WP25

## 4. 산출물

- `quality-research-dispositions.md` — 조사 처분안 초안(사용자 판단 ① 써마지 · 중국 코디 확인 ② 토닝 zh 대기)

- `reference/2026-11-12-interpreter-idea/pricing-design.md` (작성 중)

## 5. 이력 (최신이 위)

- `2026-11-14` 문서 검수 WARN 6. 코디 처분: 참고 1 → BASE · DEC 의 기록 문장 조각을 서술로 바꿈 · 참고 2 → D-47 방향 바로잡음(sensitivity 는 낮춤). W-1 처분 = 조합은 조립 · 세션 함수의 선택 인자로만 끈다(기본 켬 · env · WS 로 못 끔) · W-2 ~ W-4 · W-6 권장대로 · W-5 는 OQ-025 답과 같이

- `2026-11-14` 베타 피드백(실장 · 중국 코디 카톡) 분석 → 품질 개선을 이 slug 안에서(새 slug 안 만듦). 로컬 전용 산출물(git 제외): `records-viewer.html` · `records-review.json`(발화 평가) · `glossary-viewer.html`(사전 점검) · `test-sentences.md`(T01 ~ T33). 만든 스크립트는 세션 scratchpad(`build_viewer.py` · `build_glossary_viewer.py`) — 다시 쓰려면 레포로 옮겨야 함

- `2026-11-14` D-42 배포 완료 — WP19(코드 #11 · 리뷰 W-1 상한 36,500) · WP20(infra #54 · sync · §9.6 0.7.0 ①②③⑤ 통과 · ④ 줄 증가 미확인)

- `2026-11-14` 사용자 「7일 보관 없애자」(베타 데이터 수집) → DEC D-42 · planner 발주. 운영 기록 4일치 로컬 사본. price.md 1 ~ 4절 다시 씀(초당 원가 · 변인별 산식 · 원가 그래프 · 요금제 × 마진 30/50/70) · 커밋 0bcb0ebe

- `2026-11-12` 요금제 추천 시간제 → 토큰제(100만 토큰당 12,800원 · 최저 마진 42.6%). WARN 3 반영 후 코디 확인으로 open 0

- `2026-11-12` idea.md WARN 6 반영 → 재확인 PASS. 요금제 보고서는 Fable 이 적정 케이스(사용자 승인) 기준으로 재작성 발주(task_7f8cbd0c5d1a)

- `2026-11-12` 수정 중인 문서에 Fable 검토를 동시 발주했다가 취소(사용자 지적). 결론 절 추가 지시(사용자: 결론이 없다)

- `2026-11-12` pricing-design 검수 FAIL(F1 · F2 · W8) → 수정 발주. 아이디어 목업 발주(사용자: 목업만 · QR = 고객 화면)

- `2026-11-12` 요금제 보고서 처음부터 재발주(8단계 플로우 · 근거 4종만)
- `2026-11-12` 앞 작업 전부 취소(명동 데이터 오용) · 산출물 scratchpad/cancelled 로
