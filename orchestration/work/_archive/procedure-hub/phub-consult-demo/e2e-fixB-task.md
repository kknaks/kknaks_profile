# [app] 테스트 고침 B — 카드 용량 · 설명 / 효과 · 부작용 LLM 풀이 / 스피너 하나 (사용자 승인 11-22 「응 진행해줘」)

너는 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. 허브 18105 = gold 661335b6(GET 만) · 매핑 JSON d21903f5. 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(빈 포트로 확인 · 재기동은 코디) · 시험은 관련만. **아래 셋만.**

## 1. 진료항목 카드 — 용량 · 설명
- 카드 이름 옆(또는 아래)에 **용량** = `$J` items `kos_unit` 원문(예 「10pulse」). 같은 이름 진료항목(소프웨이브 5 등)이 용량으로 갈려 보이게.
- **진료항목 설명** = `kos_description` 원문 · 비면 그 진료항목이 매핑된 허브 케이스의 한 줄 설명(시술 이름 · 부위 · 방법 — 허브 값 이음 · 지어내기 금지). 모달 「시술 개요」 의 설명 칸도 같은 값.

## 2. 효과 · 부작용 = LLM 이 허브 값을 풀어 쓴 고객 문장(미리 만듦)
- 사용자가 본 문제: 「리프팅즉시3개월 점진2-3개월…」 · 「염증후 색소침착very_low< 1%」 · 「통증★★★★☆★★★★☆☆」 처럼 원문 값이 구분 없이 붙어 읽을 수 없음 · 빈 줄 · 묶음 머리 안 보임 · 얼굴 케이스에 바디 효과(바디 컨투어링 · 지방 감소).
- **미리 만들기:** 스크립트(예 `scripts/build_modal_text.py`)가 명동점 매핑 케이스 전부(137 안팎)에 대해 허브(facets outcome · adverse — 지금 모달이 쓰는 값 그대로 · 계열 줄 뺌 · 이름 합침 · 분류 · 경고 줄)를 모아 **LLM(앱이 쓰는 claude CLI · 모델은 앱 설정)** 에 넘겨 **JSON** 으로 받는다: 항목마다 `{name, class(위급/주의/일시적/효과), when, how_long, frequency, what_to_do, alert, sentence}` — sentence = 고객용 한두 문장(존댓말 · 쉬운 말). **허브 값에 없는 내용은 쓰지 마라**(없는 칸은 빈 값). low · very_low · 별점 같은 원문 등급은 말로(「드묾」 · 「매우 드묾」 · 「통증 정도 4/5」 꼴 — 규칙 표로 앱이 먼저 바꿔 LLM 에 넘김).
- **부위 맞춤:** 케이스 부위가 얼굴이면 몸 전용 효과(바디 컨투어링 · 지방 감소 등 — 효과 행 부위 · 원장 문장으로)는 뺀다(규칙을 리포트에).
- 결과 파일 `data/kos/modal-text-<gold 앞 8>.json`(git 무시 자리 · 두 경로: `/Users/kknaks/git/clinic_chat/data/kos/` · `$A/data/kos/`) · 키 = 케이스 코드 · meta = gold 해시 · 만든 때. 모달은 이 파일을 읽어 **같은 틀로 정렬**(항목 · 한 줄 문장 · 작은 칸(언제 · 얼마나 · 빈도)) · 묶음 머리 위급 / 주의 / 일시적 보임 · 빈 줄 0. 파일에 없는 케이스는 지금 모달(원문)로.
- 검증: 표본 10 케이스 문장 ↔ 허브 값 대조 표(지어낸 말 0) · 스크린숏 `$W/e2e-shots/fixB-modal-*.png`(입꼬리보톡스 제오민 · 얼굴필러 쥬비덤 · 소프웨이브 · 울쎄라).

## 3. 스피너 하나 · 한 줄
- 사용자가 본 것: 새 단계 스피너 + 그 아래 줄 글 + 답변 자리 기존 스피너 = 스피너 둘 · 글은 아랫줄. → **스피너 하나 + 글 한 줄(「◌ 답변을 작성하고 있어요」)** · 답변 자리 기존 대기 스피너 없앰 · 답 오면 그 줄 사라짐. 스크린숏 `$W/e2e-shots/fixB-spinner.png`.

리포트 `$W/e2e-fixB-report.md`(파일 · 시험 · 생성 케이스 수 · LLM 호출 수 · 대조 표 · 스크린숏 · 모달 텍스트 파일 sha).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 테스트 고침 B" --body "카드 / 모달 문장 / 스피너"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app 테스트 고침 B 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] app: <질문>" --enter`
