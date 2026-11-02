# [researcher] Soniox 중국어권 — 광둥어 · 번체 · 국적별 언어 대응 확인

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype` (코디 워크트리에 직접 탄다)
리포트 파일 1개 말고는 아무것도 만들지도 고치지도 마라.

## 1. SSOT — 먼저 읽을 것

- 앞 판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-soniox-report.md` — 이미 확인된 것(STT stt-rt-v5 번역 내장 · TTS tts-rt-v2 · 「TTS zh 는 간체만」). 이걸 다시 조사하지 말고 **빈 곳만** 메운다
- **Soniox 공식 문서가 정본** — `https://soniox.com/docs/llms.txt` 목차에서 고른다. 특히
  - `https://soniox.com/docs/translation/supported-languages`
  - `https://soniox.com/docs/tts/concepts/supported-languages`
  - STT 지원 언어 · language hints · 언어 식별 페이지
  - 비공식 출처는 「비공식」 표시

**기대는 개념** — 해당 없음.

## 2. 배경

cc 의 통역은 의사·상담·코디가 외국인 환자와 시술·이동 중 **폰으로 대면 대화**하는 데 쓴다(양방향).
언어는 **담당 환자의 국적**(`visitor.nationality`)으로 자동으로 고른다. 시연 데이터(10-09) 국적은
TW 17 · KR 6 · CN 2 · HK 1 · JP 1 이고, 열흘 전체로는 TW 97 · KR 25 · CN 24 · US 8 · HK 7 · JP 6 · TH 5 · FR 2 · PH 2 · IN 1.
중국어권 셋(대만 만다린+번체 · 중국 만다린+간체 · 홍콩 광둥어+번체)이 Soniox 로 어디까지 되는지 알아야 국적→언어 표를 정한다.

## 3. 계약

해당 없음.

## 4. 조사할 질문 — 전부 답한다(답이 없으면 「문서에 없음」)

1. **광둥어(Cantonese)** — STT(인식) · 번역(원문/대상) · TTS(음성) 각각 지원하나. 언어 코드. 안 되면 문서에 그렇다고 적혀 있나
2. **번체** — STT 결과 · 번역 결과 · TTS 입력 각각 번체를 낼 수 있나/받을 수 있나. 간체만이면 번체로 바꾸는 표준 방법(예: OpenCC — 비공식 표시)과 그 한계(용어 차이) 한 줄
3. **대만 만다린** — `zh` 로 인식·TTS 할 때 대만 억양·어휘에 대한 문서 언급이 있나. TTS 에 대만식 음색이 있나
4. **two_way 번역에서 언어 지정** — 상대 언어를 `zh` 로 고정할 때 상대가 광둥어로 말하면 어떻게 되나(문서 근거가 있는 만큼만). language hints · 언어 식별로 만다린/광둥어를 가를 수 있나
5. **국적 → 언어 표 재료**: 위 10개 국적(TW · KR · CN · US · HK · JP · TH · FR · PH · IN) 각각 대표 언어 후보와 그 언어의 STT · 번역 · TTS 지원 여부 표. 후보가 둘 이상인 나라(HK · PH · IN 등)는 후보 전부
6. **TTS 음색** — 위 언어들(ko 포함)에서 쓸 수 있는 음색 이름과 수. 언어마다 다른가, 공용인가

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-soniox-chinese-report.md`

```markdown
# Soniox 중국어권 · 국적별 언어 조사 (<조사일>)
## 결론 한 장 — 광둥어 되나/안 되나 · 번체 되나/안 되나 · 대만/홍콩 고객에게 무엇이 나가나
## 질문 1~6 답 (각 답에 공식 문서 URL)
## 국적 → 언어 후보 표 (STT · 번역 · TTS 지원 열)
## 정할 것 — 코디·사용자가 결정할 항목 (결정하지 말 것)
## 출처 목록
```

## 7. 범위 제약 — 하지 말 것

- 코드 작성·실행, API 호출, 패키지 설치 금지 — 문서 조사만
- 리포트 외 파일 생성·수정 금지. 커밋·push·PR 금지
- 국적→언어 표를 확정하지 마라 — 후보와 근거까지. 결정은 「정할 것」에

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령의 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_4e46377b-beeb-4892-8fb8-70517fb63683 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과 / 미결·주의점"

# (2) 직접 주입 — 코디네이터를 깨운다
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
