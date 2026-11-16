# [reviewer_doc] 요금제 설계 보고서 `pricing-design.md` 검수

너는 **interpret-pwa `reviewer_doc` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/` (`role.md` 외 4개)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (read-only) · ⚠ PUBLIC — 리포트에도 키 · 실명 금지.

## 1. 대상 · 계약

- 대상: `reference/2026-11-12-interpreter-idea/pricing-design.md` + 같은 폴더 `pd-*.png` + `orchestration/work/interpreter-idea/pricing-calc/`
- **계약 = 작성 브리프** `orchestration/work/interpreter-idea/interpreter-idea-research-brief.md` §0 ~ §3 · §8. 특히 §0 규칙(근거 4종 · 가격은 결과 · 병원 데이터 금지 · 사용자 용어 그대로) · §2 사용자 지정 값 · §3 8단계 순서.
- 코디 추가 지시: 환율은 USD 계산 + 변수 r(정할 것) · 원 열은 r=1,400 「비교용」.

## 3. 볼 것

1. **근거 없는 숫자** — 숫자 있는 줄을 전수로 보고 근거 태그가 실제로 맞는지(태그만 붙고 근거가 틀린 것 포함). 〔정의〕 · 〔코드〕 보조 태그가 §0 의 4종을 벗어나 근거 없는 가정을 숨기고 있지 않은지.
2. **사용자 지정과 다른 값 · 해석** — §2 표와 다른 값, 사용자가 말하지 않은 해석(예: 상담 비율 ρ 를 「시간 비율」로 읽은 것 · 「1시간 = STT 스트림 1시간」 · 세션 최대 = 발화마다 수동 stop · 300분 한도 사용)이 「정할 것」으로 드러나 있는지.
3. **가격이 결과인가** — §5 가 §3 범위에서 역산했는지, 앞에서 가격 · 마진 · 포함량을 정해 두지 않았는지.
4. **8단계 순서 · 절 제목** 그대로인지.
5. **재계산** — `calc.py` 를 스크래치 복사본에서 `python3 -I` 로 재실행해 보고서 · `results.json` 과 diff. 실측 2건은 `pricing-calc/usage-logs-cost-probe-2026-11-12.json` 에서 토큰 × 단가 = cost_usd 확인. **Soniox 호출 금지.**
6. **그래프** — 범례 · 축 제목 · 단위 · 숫자가 results.json 과 같은지.
7. **사람이 읽을 때 오해할 자리** — 결정처럼 읽히는 추천 · 워스트 세트가 실제 최대가 아니라는 점(ρ=0 이 ×4.28)이 요약에서 드러나는지.
8. PUBLIC 위생 · 병원/지점 데이터 0.

## 4. allowed_paths

- 리포트 1개: `orchestration/work/interpreter-idea/review-pricing-design-report.md`. 그 외 수정 금지.

## 8. 검증

```
계약(작성 브리프)에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_a9c98cf8-16b5-4a44-852d-251a83c05b85 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
