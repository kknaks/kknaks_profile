# [planner] baseline T3 — 인터뷰 본문 반영 (b 6곳 수정 · c 10건 신설 · a 8건 보강 · changelog)

너는 **sc-ax `planner` 워커**다. 역할 문서(`/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/sc-ax/planner/` 5종)와 조사 A·T1·T2 맥락을 그대로 쓴다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax` (PR 은 코디네이터가 올린다)

**이번이 baseline ① 의 마지막 조각이다** — T2 가 등재한 사실을 본문(00~10절)에 반영한다.

## 1. SSOT — 먼저 읽을 것

- `products/sc-ax/00-baseline/_working/interview-mgmt-dept-2026-08.md` ← **네가 T2 에서 만든 매핑표가 작업 목록이다.** AS 31행의 착지·구분(a/b/c)대로 반영한다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/interview1-update/survey-baseline-report.md` ← 갱신 지점 표 (b-1~b-6 · c-1~c-10 · a-1~a-8)의 상세 — 무엇을 어떻게 고칠지가 항목별로 적혀 있다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/현행업무-발견지도.md` ← 사실 확인용. **여기 없는 사실을 만들지 마라.**

**기대는 개념** — 사용자 승인이 끝난 결정 (재논의 금지):
- **돌발유입은 2.3 의 7번째 대분류(PR-7)로 승격한다.** 전파 갱신 포함 — 2.3 서두 · 2.5 공통 원인 · 3.3 US 매핑 · 4.1 전제 (00-overview 「같이 확인」 메모를 따른다).
- **M-11/M-12 차수 재배치는 하지 않는다** — 6절에 「이번 발견의 무게가 4차 배치와 어긋난다」 관찰만 기록.
- **AS-·발견지도 R- ID 는 본문에 쓰지 않는다** — 본문 인용은 전부 `(S14)`, 추적은 `_working/` 매핑표.

## 2. 배경 / 무엇을 바꾸나

S14(경영관리부 1차 인터뷰)가 등재됐고(T2), 이제 본문이 그 사실을 담는다. 낡은 서술을 고치고(b), 자리가 없던 문제를 신설하고(c), 이미 있던 항목에 근거를 보강한다(a). 끝나면 회차 대장 상태를 올리고 changelog 한 행으로 닫는다.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `products/sc-ax/00-baseline/00-overview.md` — 「여기를 고치면 같이 확인」 전파 메모 · `[결정]` 카운트 규칙
- `products/sc-ax/00-baseline/02-background-and-problems.md` — PR 번호 체계·형식 (신설 PR 은 기존 형식 그대로)
- `products/sc-ax/00-baseline/C-changelog.md` — S13 반영 행(2026-08-11)이 마무리 행의 형식 모델

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/sc-ax/`

## 6. 구현 단계

1. **(b) 낡아서 어긋남 6곳** — survey-baseline-report 「(b) 표」 그대로:
   - b-1 기준선 창 상태 갱신 (8절·10절 R-1·9절 G-2 후속): 「이관됨」→「1회차 실시·미확보」, 2차 회차 재질문(기간 좁혀)을 다음 경로로 기록. **방법론 재설계·fallback 신설은 하지 마라 — 사실 기록만**
   - b-2 2.4 「현재 방식에 생긴 변동」에 경영관리부 협업 도구 전환 행 추가
   - b-3 PR-2.3·US-4 근거줄 시점 분리 (S13 문장 유지 + S14 시점 병기)
   - b-4 근태(외근·출장·현장 인력)를 「문제로 올리지 않은 것」에서 PR 로 승격
   - b-5 HOLD-10·Q-12 보류 사유 갱신 (실제 곤란 사례 확보 — 판단 조건 충족을 기록. 보류 해제 여부 자체는 코디·사용자 몫이므로 「조건 충족」까지만)
   - b-6 2.4 자체 제작 도구 행의 한계 열 보강 (장점 서술은 유지)
2. **(c) 자리 없음 10건** — 「(c) 표」 그대로: 계약 라이프사이클 묶음(c-1) · 입퇴사 신호(c-2) · 외국인 서류(c-3, 3.1 특성표 포함) · 정산 연쇄(c-4, 7월 실측값 포함) · 전결 모호(c-5) · **돌발유입 PR-7 승격(c-6, 전파 포함)** · 일일보고 취합(c-7) · 자료 재업로드(c-8) · HOLD-8 위험 신설(c-9) · Q-1 근거 보강(c-10)
3. **(a) 근거 보강 8건** — 「(a) 표」 그대로: 해당 항목에 S14 근거 추가 (교차확인·층 승격 등). 문장 재작성이 아니라 근거줄 보강이다
4. **전파 정리** — 02절 대분류·PR 수가 바뀌므로 00-overview 상태 표·2.5·3.3·4.1 등 「같이 확인」 대상과 6절 M-11/12 관찰 기록, 03절 3.0 근거 수준표(관리자 표본 +1)를 맞춘다. `[결정]` 카운트를 재확인한다
5. **마무리** — `interview/README.md` 회차 대장 상태 「실시 — 결과 반영 대기」→「반영 완료」, `C-changelog.md` 최상단에 S14 반영 행 1건 (S13 행 형식: ①②③… 절별 요약 + `[결정]` 카운트 확인)

## 7. 범위 제약 — 하지 말 것

- `01-product-summary.md` 는 손대지 않는다 (원본이 다 정리된 뒤 마지막 — 조사 A 「건드리지 않는 것」)
- `present/` · `SCAX-BL-001-*` · `request/` 본문 · `_working/` 스킬 산출물 · `00-planning/` 이하 · `20-spec/` 는 손대지 않는다
- 발견지도에 없는 사실 발명 금지. 미래 방법론 결정(기준선 fallback, 차수 재배치, HOLD 해제) 금지 — 사실과 조건 충족 기록까지만
- AS-·발견지도 R-·미결 #·X-·V- ID 를 본문에 쓰지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/sc-ax/ 범위 ERROR 0
grep -rn "AS-0" products/sc-ax/00-baseline/*.md → 0건 (본문에 AS ID 금지 — _working/ 은 예외)
grep -rn "조상아\|권예은\|박소은\|서형석\|이건학\|전창원\|최우영" products/sc-ax/00-baseline/*.md → 0건
git status --porcelain → 변경이 00-baseline 안 + T1·T2 기존분뿐인지
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
