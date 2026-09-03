# [planner] baseline T4 — 01-product-summary 동기 (S14 반영 마지막 조각)

너는 **sc-ax `planner` 워커**다. 역할 문서와 조사 A·T1~T3 맥락을 그대로 쓴다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax`

## 1. SSOT — 먼저 읽을 것

- `products/sc-ax/00-baseline/02-background-and-problems.md` 외 T3 에서 갱신된 본문 — **요약의 원천.** 요약은 원본을 따라간다, 새 사실을 만들지 않는다.
- `products/sc-ax/00-baseline/01-product-summary.md` — 대상 문서. 현재 43건·6개 대분류 기준으로 낡아 있다.

## 2. 무엇을 바꾸나

T3 가 본문을 다 갱신했다 (PR 43→61 · 대분류 7 · S14 반영). `01-product-summary.md` 는 「원본 아님 — 전부 요약」 문서라 마지막에 따라간다 — 지금이 그 차례다. T3 완료 보고가 지목한 잔여( 2.3 「같이 확인」 전파처 중 1절 1.2 의 PR 건수·대분류 서술 )를 포함해, 본문과 어긋난 수치·서술만 맞춘다.

## 3~5. 계약 / 핵심 파일 / allowed_paths

- 계약: 해당 없음
- allowed_paths: `products/sc-ax/` — 이번 태스크의 실제 수정 대상은 `01-product-summary.md` **1개 파일뿐**이다

## 6. 구현 단계

1. `01-product-summary.md` 전체를 T3 반영 후 본문과 대조 — 낡은 수치(43건·대분류 6)·서술을 갱신
2. 요약 문서의 기존 톤·형식·길이를 유지한다. 새 절 신설·재구성 금지 — 어긋난 곳만 맞춘다
3. `C-changelog.md` 는 **손대지 않는다** — T3 의 S14 반영 행이 이미 마감이며, 요약 동기는 그 행의 후속 정합화다. changelog 행이 규약상 반드시 필요하다고 판단되면 §9 로 물어라

## 7. 하지 말 것

- `01-product-summary.md` 밖 수정 금지
- 새 사실·해석 추가 금지 — 본문에 있는 것의 요약만
- AS-·발견지도 ID·실명 금지 (기존 규약 그대로)

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/sc-ax/ 범위 ERROR 0
grep -n "43건\|여섯 대분류\|6개 대분류" products/sc-ax/00-baseline/01-product-summary.md → 낡은 기준 잔존 0건 (본문이 실제로 그 수치를 쓰는 정당한 문맥 제외 — 있으면 사유 보고)
git status --porcelain → 신규 변경이 01-product-summary.md 뿐인지
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --text "[질문] planner: <질문>" --enter`
