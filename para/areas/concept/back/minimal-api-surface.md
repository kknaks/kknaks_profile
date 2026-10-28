---
type: concept
id: minimal-api-surface
title: 최소 노출 API — 허용 경로 고정 시험 · 일반 오류 문구 · 산출물 grep (Minimal API Surface)
aliases:
  - 최소 노출
  - 밖으로는 통역만
  - 허용 경로 고정
  - 경로 목록 고정 시험
  - 일반 오류 문구
  - 빌드 산출물 grep
  - docs/openapi 끄기
  - 내부 기록
  - 서버만 기록
  - 새 입구 0
up:
  - 2026-10-27-interpret-pwa-poc
  - 2026-10-28-interpret-pwa-v2
tags:
  - 보안
  - api
  - 정보 노출
  - 시험
---

# 최소 노출 API — 허용 경로 고정 시험 · 일반 오류 문구 · 산출물 grep

공개 주소로 나가는 서비스는 **제품이 하는 일에 필요한 경로 · 필드만** 밖으로 내고, 그 목록을 시험으로 고정한다. 응답 본문 · 오류 문구 · 문서 화면 · 프론트 빌드 산출물이 모두 「밖」 이다. 우리 자산(사전 데이터)이 엔진 입력으로만 쓰이면 그 경로 외에는 어디에도 나오지 않게 한다.

## 정의

1. **허용 경로를 시험으로 고정** — 앱 경로가 정확히 이 목록(통키 6개: 로그인 · me · config · 데모 로그인 · health · WS)이어야 통과. 새 경로가 생기면 **시험이 실패**하고, 결정 문서와 함께 목록에 더해야 한다
2. **응답은 판단에 필요한 만큼** — health = `{ok}`(사전 판 · 개수는 서버 로그에만), me = `{ok}`(아이디 없음 · 토큰이 틀리면 401). 클라이언트가 실제로 쓰는 값을 세고 나머지를 뺀다
3. **오류 문구는 일반 문구 몇 개로** — 코드는 그대로 두고 문구만 「요청을 처리할 수 없어요」 등 4종. 받은 값을 되돌려 보내지 않는다(옛 「지원하지 않는 언어예요: 'xx' (가능: …)」). env 이름 · 벤더 이름 · 검증기 필드 경로 · 예외 문구 0. 원인은 로그에만. 처리기 밖 예외도 JSON 500
4. **자동 문서를 끈다** — `/docs` · `/redoc` · `/openapi.json` 404
5. **산출물을 grep 한다** — 프론트 빌드(`.next/static` · 서버 소스맵 포함)에 사전 낱말 · `SONIOX` · `INTERPRET_` 0. 소스 주석도 소스맵에 실리므로 지운다. 백엔드는 응답 · WS 로 시드가 가는 길이 0 임을 「밖으로 쓰는 곳 전부」 grep 으로 확인

### 표면을 안 넓히고 기능 더하기 — 화면 · API 없는 내부 기록

내부 사람만 볼 데이터(「어떤 통역을 했는지」 검토용)를 남겨야 할 때, 읽는 길을 서비스 밖에 내지 않는다.

1. **쓰기만 서버 안에서** — 날짜별 JSONL 파일을 서버 볼륨에(세션 시작 · 발화 · 끝 · 원문 · 번역 · 걸린 term id). 읽기 경로 · 관리 화면은 만들지 않는다
2. **꺼내기는 운영 도구로** — `kubectl cp` · `exec cat`. 접근 통제를 클러스터 권한에 맡긴다
3. **담는 것을 줄인다** — 음성 · 토큰 · IP · 계정값 없음. 보관 7일(기동 때 + 하루 한 번 삭제)
4. **본 기능을 끊지 않는다** — 쓰기 실패는 경고만 남기고 통역은 계속. 기록은 부가 기능이다
5. **「새 입구 0」 은 기존 시험으로 확인한다** — 허용 경로 고정 시험을 **고치지 않고** 그대로 통과하면 기능을 더하면서 경로가 늘지 않았다는 증거다. 고정 시험이 여기서 값을 한다

## 사용 예시

```python
# back/tests/test_api_surface.py — 모양만
ALLOWED = {("POST", "/api/auth/login"), ("GET", "/api/auth/me"),
           ("GET", "/api/auth/config"), ("POST", "/api/auth/demo"),
           ("GET", "/api/health"), ("WS", "/api/interpret")}

def test_route_list_is_fixed():
    assert app_routes() == ALLOWED   # 새 경로 = 실패 → DEC 와 함께 목록 갱신

def test_no_seed_words_in_any_response(client):
    for method, path in ALLOWED - {("WS", "/api/interpret")}:
        body = client.request(method, path).text
        assert not any(w in body for w in seed_words())
```

## 왜 중요한가

- 데모 원탭 로그인을 켜 두니 **버튼 하나면** 용어집 API 로 사전 전체를 가져갈 수 있었다. health 는 사전 버전을, me 는 아이디를, 오류 문구는 env 이름을 흘렸다. 하나씩은 사소해도 합치면 내부 구조 지도다
- 「삭제했다」 는 지금만 참이다. 경로 목록을 시험으로 박아야 다음 기능이 몰래 표면을 넓히지 못한다

## 경계와 오해

- **[[field-level-visibility]] 와 다르다** — 그쪽은 자격에 따라 같은 응답의 필드를 비우는 것(로그인한 사람 사이의 차이), 여기는 **누구에게도** 필요 없는 것을 응답 · 경로에서 아예 없애는 것
- **인증이 있어도 필요하다** — 인증은 「누가」 를 막고, 최소 노출은 「들어온 사람이 무엇을 보나」 를 줄인다. 공개 데모처럼 인증 문턱이 낮으면 이쪽이 실질 방어다
- **사용자 문구는 남긴다** — 로그인 401 · 429 처럼 화면에 그대로 보이는 문구에는 내부 정보가 없으니 둔다. 일반화 대상은 내부 원인을 말하는 문구다
- **「안 보인다」 ≠ 「안 남긴다」** — 최소 노출은 밖으로 내는 것을 줄일 뿐 서버 안에 기록하지 말라는 뜻이 아니다. 내부 기록은 밖에 입구가 없으면 표면이 아니다. 다만 담긴 것(대화 문장)은 그 자체로 민감하므로 보관 기간 · 담는 칸을 같이 줄인다
- 표면을 세는 일 자체는 [[contract-surface-enumeration]] — 바꿀 때 닿는 자리를 세는 것과 같은 grep 이다

## 함께 보는 개념

- [[password-login-hardening]] — 로그인 전 계정 목록 표면을 없앤 같은 방향
- [[resource-scoped-token]] — allowlist 로 표면을 정하는 다른 예
- [[runtime-profile-gating]] — 데모 지름길이 표면을 여는 자리
- [[contract-surface-enumeration]] — 밖으로 쓰는 곳 전부를 세는 방법

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — 「외부 api에 json이 노출 되면 안돼」: 용어집 API · 메뉴 삭제 · health/me `{ok}` · 오류 일반 문구 4종 · docs/openapi 끔 · 허용 경로 6개 고정 시험 · 빌드 산출물 grep(`back/tests/test_api_surface.py` · `front/tests/minimal-exposure.test.ts` · `d37-be-report.md` · `d37-fe-report.md` · DEC-001 D-37 · 코드 #8)
- [[2026-10-28-interpret-pwa-v2]] §2 — 내부 검토용 통역 기록을 화면 · API 없이 서버 PVC 의 날짜별 JSONL 로 · 꺼내기는 kubectl · 음성 · 토큰 · IP · 계정값 없음 · 7일 삭제 · 쓰기 실패는 통역을 안 끊음 · 허용 경로 고정 시험이 수정 없이 통과(`back/app/service/records.py` · `back/tests/test_records.py` · `test_api_surface.py` · DEC-001 D-41 · SPEC-001 §5.9)
