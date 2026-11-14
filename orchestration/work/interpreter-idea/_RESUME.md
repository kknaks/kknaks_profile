# 재개 노트 — interpreter-idea (interpret-pwa)

**지금**: **품질 개선(오역 수정) 문서 단계** — BASE-001 입력 5 · 확인한 사실(2026-11-14) · DEC D-43 ~ D-48 · OQ-021 ~ 023 작성(미커밋). 사용자 승인 대기 → 승인되면 planner(SPEC · WORK) + researcher(7개 언어 × 현지 피부과 6곳) 발주. 배포 12(D-42)는 완료
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
| planner (fable) | `term_5fb24b1c-5649-42e7-bcfe-dd33ee95ddc7` | `task_225c6fb1bf47` | `ctx_a1605c399ea7` | `quality-spec-brief.md` → `quality-spec-fix1-brief.md`(`task_5a94775e2759` · `ctx_7400d102ba80`) | 0.8.0 완료 → 0.8.1 보완 진행(WARN 6 · D-49 · D-50) |
| reviewer_doc (fable) | `term_9bf4f5be-03de-42ff-81a7-d3e96f2e238d` | `task_75333f7ff9c4` | `ctx_95efde4723c0` | `review-doc-quality-brief.md` → `review-doc-quality-2-brief.md`(`task_a87949ff27e9` · `ctx_ed082c6ef49b`) | 0.8.1 재검수 완료 — WARN 경미 3(N-1 ~ N-3 문구) · `review-quality-doc-report-2.md` → 다음 planner 판(§4.2.4 값 채움)에 같이 |
| researcher r1 (fable) | `term_abd0126a-6243-4b84-9616-3629e04aa7d1` | `task_cda6a9026613` | `ctx_c6c23c6620bc` | `quality-r1-zh-brief.md` | 완료 — 510칸 · 표 A 95행 · 정할 것 12 · `quality-r1-zh-report.md` · `-cells.json` |
| researcher r2 (fable) | `term_2480bb9c-aef3-4923-8c0f-2909b198366c` | `task_64d2df2acd28` | `ctx_563abe7e5e30` | `quality-r2-en-ja-th-vi-brief.md` | 완료 — 680칸 · 정할 것 17 · `quality-r2-en-ja-th-vi-report.md` · `-cells.json` |

다음: 세 워커 완료 → reviewer_doc(SPEC · WORK) · 조사 리포트 → 코디 처분(사용자에게 최종 판단만) → SPEC §4.2.x 값 채움 → 사용자 리뷰 → WP21 backend 발주

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
