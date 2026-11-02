
# [researcher] Soniox 로 STS(한국어 ↔ 다른 언어 음성 번역) 만들 수 있는지 조사

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디 워크트리에 직접 탄다 — 리포트 파일 1개 말고는 아무것도 만들지도 고치지도 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/00-baseline/baseline-001-feature-lab.md` — 제품이 무엇인지(고객 데모용 기능별 실험)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-001-feature-lab.md` — 스택(back FastAPI · front Next.js), 기능 독립
- **Soniox 공식 문서 — llms.txt 부터 읽어라** ← 조사의 정본. 비공식 출처는 「비공식」 표시
  - `https://soniox.com/llms.txt` — 제품 개요 (STT · TTS · 번역이 STT API 에 내장, 2026-10-10 코디 확인)
  - `https://soniox.com/docs/llms.txt` — 문서 전체 목차(약 26KB). 여기서 필요한 페이지를 골라 읽는다
  - `https://soniox.com/docs/llms-full.txt` — 문서 전문(약 2MB). 통째로 읽지 말고 필요한 절만 찾아 읽는다
  - Soniox GitHub `https://github.com/soniox` — SDK·예제

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

`sts` 기능 = **한국어 ↔ 다른 언어 음성 번역**(말하면 상대 언어 음성으로 나온다). 사용자는 Soniox 를
구독 중이고 이걸 중심으로 만든다. 바로 speech-to-speech 가 안 되면 **STT → 번역 → TTS** 3단으로 가도 된다(사용자 원문).
빨리 프로토타입을 만들어 고객에게 보여주는 것이 목적이라, 이 조사의 답으로 **어떤 경로로 만들지 바로 정할 수 있어야 한다.**
코드는 아직 없다.

## 3. 계약

해당 없음.

## 4. 조사할 질문 — 전부 답한다(답이 없으면 「문서에 없음」)

**A. Soniox 가 어디까지 해 주나**
1. 제품·모델 목록(실시간 STT · 파일 STT · 번역 · TTS/음성 합성 · speech-to-speech 여부). 현재 모델명·버전
2. **실시간 번역**: 단방향/양방향(두 언어 대화) 모드, 설정 방법, 원문·번역 토큰이 어떻게 나오나(같은 스트림? 최종/중간 구분?)
3. **한국어**: STT 지원 수준, 번역 대상 언어 쌍(ko↔en·ja·zh·vi·th 등 — 전체 목록 링크)
4. 언어 자동 판별 · 화자 분리 · 엔드포인트(발화 끝) 감지 — 대화형 통역에 필요한 것
5. **Soniox TTS**(llms.txt 에 있음): 지원 언어(한국어·대상 언어 포함?)·음색·스트리밍(텍스트 조각 입력→오디오 조각 출력) 여부·지연. 실시간 번역 결과를 TTS 로 바로 흘릴 수 있나(한 연결? 두 연결?)

**B. API 를 실제로 어떻게 붙이나**
6. 실시간 API: WebSocket 엔드포인트, 인증, 설정 메시지 형식, 오디오 포맷(샘플레이트·코덱), 응답 메시지 형식 — 최소 예시 그대로 인용
7. **브라우저 마이크에서 바로** 붙일 수 있나: 임시 키(temporary API key) 발급 방식, 공식 Web/JS SDK 유무. 아니면 back 이 중계해야 하나
8. 공식 SDK(Python · JS)와 예제 레포 — 특히 실시간 번역·Next.js/React 예제가 있으면 링크
9. 문서에 적힌 지연(latency) 수치

**C. Soniox TTS 가 모자랄 때의 대안** (A-5 에서 한국어·대상 언어·스트리밍 중 빠지는 게 있을 때만. 다 되면 「해당 없음」)
10. 스트리밍 TTS 후보 3~5개(예: OpenAI · ElevenLabs · Google · Azure · 네이버 클로바 · 기타) — 한국어 품질 평판, 스트리밍(텍스트 조각 입력→오디오 조각 출력) 지원, 첫 오디오까지 지연, 가격. 각 출처
11. 번역 단계를 Soniox 가 이미 하면 LLM 번역은 필요 없는지, 필요한 경우가 있으면 무엇인지

**D. 비용·한도**
12. Soniox 요금(실시간 STT · 번역 · TTS 각각 분/시간당), 동시 연결 한도, 구독 플랜별 차이

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-soniox-report.md`

```markdown
# Soniox STS 조사 리포트 (<조사일>)
## 결론 한 장 — 경로 후보 (Soniox 단독 STS / Soniox STT+번역 → TTS X / 기타), 각각 무엇이 되고 안 되나
## A. Soniox 기능 (질문 1~5)
## B. 붙이는 법 (질문 6~9) — 최소 코드 예시 인용
## C. TTS 후보 비교표 (질문 10~11)
## D. 비용·한도 (질문 12)
## 프로토타입 구성 후보 — 브라우저 ↔ back(FastAPI) ↔ Soniox(·TTS) 흐름을 경로별로 한 줄 다이어그램
## 정할 것 — 코디·사용자가 결정할 항목 목록 (결정하지 말 것)
## 출처 목록
```

## 7. 범위 제약 — 하지 말 것

- 코드 작성·실행, API 호출, 패키지 설치 금지 — 문서 조사만.
- 리포트 외 파일 생성·수정 금지. 커밋·push·PR 금지.
- 경로를 고르지 마라 — 비교와 근거까지. 결정은 「정할 것」에.

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e3856191-5a19-4d0a-bc54-a8b016bc829b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e3856191-5a19-4d0a-bc54-a8b016bc829b \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e3856191-5a19-4d0a-bc54-a8b016bc829b --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
