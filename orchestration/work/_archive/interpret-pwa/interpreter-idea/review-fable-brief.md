# [reviewer_fable] 요금제 설계안 — 「읽히는가」 검토

너는 문서 검토 워커다(Fable). 앞 맥락은 없다. **read-only** — 리포트 1개만 쓴다.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토`

## 무엇을 · 왜

사용자(이 요금제를 정할 사람)가 이 문서를 읽고 **「값의 단위도 모르겠고, 결론이 이해가 안 된다」**고 했다. 계산이 맞는지가 아니라 **사람이 읽고 결론까지 따라갈 수 있는지**를 본다.

대상(스냅샷 — 수정 중인 원본 말고 이것을 읽어라): `orchestration/work/interpreter-idea/snapshot-pricing/pricing-design.md` + 같은 폴더 `pd-*.png`
참고(작성 계약): `orchestration/work/interpreter-idea/interpreter-idea-research-brief.md` §0 · §2 · §3

## 볼 것

1. **단위** — 모든 숫자 · 기호에 단위가 붙어 있는가(USD / 원, 시간 / 월 / 기기, 토큰, 비율 0 ~ 1 이 무엇의 비율인지). 없는 곳 전부 `파일:줄`.
2. **기호 · 용어** — ρ · φ · ψ · c_h · p · p_f · Q · k · n · m · r · C · M · R 등 기호가 처음 나올 때 정의되는가 · 사용자가 정한 말(시간제 · 토큰제 · 정액제 · 해피/워스트 · 상담 1발화 · 간단 통역 1발화)과 워커가 만든 말이 구분되는가. 사용자가 모를 말 목록.
3. **흐름** — 1 → 8 단계를 순서대로 읽을 때 앞에서 정의 안 된 것이 뒤에 쓰이는 곳 · 표가 무엇을 보여 주려는지 한 줄 설명이 없는 곳.
4. **결론** — 7절 비교 · 안 A ~ D 를 읽고 **「그래서 각 요금제를 얼마로 받으면 되나 · 왜 그 값인가」가 한 번에 답해지는가.** 답이 안 되면 어디서 끊기는지.
5. **표 · 그래프** — 각 표 · 그래프가 무엇을 비교하는지 · 축과 열의 단위 · 읽는 법. 의미 없는 표(예: 손익분기 0.05 표)는 「빼거나 바꿀 것」으로.
6. **사용자가 정하지 않은 가정이 결론에 섞인 곳**(예: 발화마다 수동 stop, 1시간 = 스트림 1시간).

## 산출물

`orchestration/work/interpreter-idea/review-fable-readability.md` 1개:
- 판정(읽힘 / 부분 / 안 읽힘)
- 지적 목록 — `파일:줄` · 무엇이 불명확 · 사용자가 어떻게 오해할 수 있나 · 고치는 방향 한 줄
- **「이 문서가 말하려는 결론」을 네가 이해한 대로 5줄 이내로** — 이해가 안 되면 「이해 불가」와 이유
- 다시 쓴다면 목차 제안(짧게)

계산 재실행 · Soniox 호출 · 파일 수정 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_f9070431-deb4-493f-bc4a-08144f040835 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_fable 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] reviewer_fable 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] reviewer_fable: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
