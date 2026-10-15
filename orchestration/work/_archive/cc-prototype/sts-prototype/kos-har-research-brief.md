# [researcher] KOS 웹앱 HAR 분석 — 화면 동작별 내부 API (DEMO 지점)

너는 **cc-prototype `researcher` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype` — 리포트 1개 말고 아무것도 만들지 · 고치지 마라.

## 1. SSOT

- **HAR**: `/Users/kknaks/Downloads/app.kos-solution.com.har` (390KB, 사용자가 KOS **DEMO 지점**(세라미크의원 명동점 DEMO)에서 Chrome 개발자 도구로 저장)
- 흐름 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` — 「KOS 반영 표」 · KOS 화면 동작 대응표(집도의 · 담당자 · 방 · 우선순위 · 시술 완료하기 · 시술 취소하기 · 귀가 대기 일괄 취소)
- 공개 OpenAPI(비교용): 스펙 `https://developers.kos-solution.com/openapi.yaml`(75개) · 문서 색인 `https://developers.kos-solution.com/llms.txt`. `changeFlowStep` 요청은 `scheduleId` · `step` 두 칸뿐

## 2. 배경

관제(현황판)는 동선 조작(시술별 담당 · 방 · 순서 · 완료/취소 · 귀가)을 나중에 KOS 에 반영해야 한다. 공개 OpenAPI 에는 그 쓰기 작업이 없다. KOS 웹앱은 이 동작을 하고 있으니 **웹앱이 부르는 내부 API 를 HAR 로 확인**해 KOS 에 「이걸 OpenAPI 로 열어 달라」고 요청할 근거를 만든다.

## 3. 조사할 것

1. HAR 의 모든 XHR/fetch 요청 목록 — 메서드 · 호스트 · 경로 · 시각(정렬) · 상태 코드. 정적 파일 · 분석 스크립트 요청은 빼고 개수만
2. **쓰기 요청 전부**(POST/PUT/PATCH/DELETE 또는 `/commands/` 류)를 **화면 동작에 짝지어** 표로: 추정 동작(담당자 · 집도의 · 방 · 우선순위 · 시술 완료 · 시술 취소 · 단계 변경 · 일괄 취소 · 시술 추가 · 상담사 지정 등 — 경로 이름 · 요청 본문으로 판단, 판단 근거 한 줄) · 경로 · 요청 본문 필드(이름 · 예시 값 모양) · 응답 모양
3. **「귀가 대기로 변경 + 일괄 취소」** 가 요청 하나인지(본문에 시술 목록이 담기나) 여러 개인지 — 순서대로
4. 각 쓰기 요청이 공개 OpenAPI 에 **같은 작업이 있나**(경로 · operationId 대조) — 없으면 「공개 없음」
5. 인증 방식 — 헤더 **이름만**(Authorization · Cookie 등), 값은 쓰지 마라. 내부 API 호스트가 공개 OpenAPI 호스트(`open-api.kos-solution.com`)와 같은가
6. 조회 요청 중 관제에 쓸 만한 것(공개 OpenAPI 에 없는 조회) — 경로 · 무엇을 주나

## 4. 범위 제약 — 반드시

- **토큰 · 쿠키 · 세션 · API 키 · 비밀번호 값은 한 글자도 리포트 · 출력 · 로그에 쓰지 마라.** 헤더는 이름만, 값 자리는 `<redacted>`. 요청 본문에 토큰류가 있으면 같은 처리
- **HAR 로 어떤 요청도 다시 보내지 마라**(재전송 · curl · 토큰 사용 금지). 파일 읽기만
- HAR 를 복사 · 가공 저장하지 마라(분석은 `python3 -c` 실행만). Downloads 의 원본을 지우거나 고치지 마라
- 고객 이름(데모라도)은 `<고객>` 으로. 직원 이름 · 시술명 · id 모양은 써도 된다
- 커밋 금지

## 5. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-kos-har-report.md`

```markdown
# KOS 웹앱 내부 API — HAR 분석 (DEMO, <날짜>)
## 결론 한 장 — 화면 동작 ↔ 내부 API 대응표(공개 OpenAPI 유무 열 포함) · 귀가 대기 일괄 취소의 정체
## 1. 요청 목록 요약
## 2. 쓰기 요청 상세(동작별)
## 3. 귀가 대기 + 일괄 취소
## 4. 공개 OpenAPI 대조
## 5. 인증(헤더 이름만) · 호스트
## 6. 쓸 만한 조회
## KOS 요청서 초안 — 「이 동작들을 OpenAPI 로 열어 달라」 목록(결정은 코디 · 사용자)
## 검증 — 토큰 · 쿠키 값 0건(리포트를 HAR 의 Authorization · Cookie 값과 대조한 결과)
```

## 6. 검증

```
쓰기 요청 전부가 표에 있다(HAR 쓰기 요청 수 = 표 행 수, 수 둘 다 적기). 리포트에 토큰 · 쿠키 값 0건(HAR 에서 뽑은 Authorization · Cookie · set-cookie 값 전부와 리포트를 대조). HAR 로 재전송 0
```

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_92c69c69-0fb5-4f2c-99f6-c189d24e0955 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
