---
id: adr-02
type: adr
title: i18n A안 — 슬롯 단일 키 + frontmatter `{ko, en}` + 백엔드 lang 분기
status: accepted
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
tags: [adr, i18n, api]
---

# i18n A안 — 슬롯 단일 키 + frontmatter `{ko, en}` + 백엔드 lang 분기

## Summary

다국어(한/영)를 다음과 같이 표현: (1) 페르소나 md frontmatter는 `{ko, en}` 객체로 양쪽 보관, (2) 프론트 슬롯은 단일 키(`{{user.intro}}`, 접미사 X), (3) 백엔드가 `?lang=ko|en` 쿼리에 따라 한쪽만 추출해 응답.

---

## 1. Context

- 기본 한국어 + 영어 토글 지원 결정 (planning-01 §1)
- 디자인 시안의 mock 슬롯 명명 컨벤션 결정 필요 (`claude_design/SLOTS.md`)
- 페르소나 md SoT 결정 (ADR-01) + spec-01 frontmatter 스키마 와 정합되어야 함
- 부분 번역(예: 한국어만 작성, 영어 미작성) 케이스 핸들링 정책 필요

---

## 2. Decision

### 2.1 슬롯 명명
프론트 슬롯은 **단일 키**. `.ko` / `.en` 접미사 박지 않음.
```
{{user.intro}}        # 슬롯
{{career[].title}}    # 배열 원소 필드
```

### 2.2 데이터 표현 (페르소나 md)
다국어 필드는 `{ko, en}` 객체 (spec-01 §2.1):
```yaml
title:    { ko: "Backend Engineer", en: "Backend Engineer" }
summary:  { ko: "...요약 ko...",     en: "...summary en..." }
period:   "2025.06 — present"        # 단일 언어 X (객체 X)
stack:    ["Python", "FastAPI"]      # 태그 다국어 X
```

### 2.3 API 분기
백엔드는 `?lang=ko|en` 쿼리로 분기. 응답엔 한쪽 언어만 포함.
```python
@app.get("/api/career")
def get_career(lang: str = "ko"):
    return {
        "career[]": [{
            "period": item["period"],
            "title":  i18n(item["title"], lang),  # {ko, en} → str
            "org":    i18n(item["org"], lang),
            ...
        } for item in _data["career"]]
    }
```

### 2.4 부분 번역 fallback (policy choice)
한쪽 언어 누락 시:
- **fallback to ko** (한국어가 마스터 언어 — 본 사이트의 정책 선택. 영어-마스터 사이트라면 반대)
- 부팅 검증에서 경고 로그만 남김 (spec-01 §6.2). 부팅 fail은 안 시킴
- 프론트는 fallback 결과를 표시 (사용자에게 "번역 누락" 알림 X — 자연스럽게 노출)
- 향후 운영자 변경 또는 영어-우선 전환 시 i18n helper의 fallback 우선순위만 바꾸면 됨 (다른 코드 무영향)

---

## 3. Alternatives Considered

### 3.1 B안 — 슬롯에 접미사 (`{{user.intro.ko}}`)
- **장점**: 프론트가 lang 상태 안 들고 슬롯 키만 바꿔 렌더 가능. 정적 HTML로 미리 컴파일하기 쉬움
- **단점**:
  - 슬롯 명세 2배 (모든 다국어 필드마다 `.ko` `.en` 두 키)
  - 프론트가 lang 토글 시 모든 슬롯 키를 일괄 변환해야 함
  - 단일 언어 필드(`period`, `stack`)와 다국어 필드 명명이 비대칭
- **기각 이유**: 슬롯 명세 비대칭 + 백엔드가 어차피 분기 처리 가능

### 3.2 C안 — 페이지별 별도 라우트 (`/ko/about`, `/en/about`)
- **장점**: SEO 친화 (lang별 정적 HTML 생성 가능). Next.js i18n routing 표준
- **단점**:
  - 빌드 산출물 2배
  - lang 토글 시 페이지 이동 (라우트 변경) — UX 약간 끊김
  - 본 프로젝트는 SSG가 아니라 백엔드 서빙이라 라우트 분리 이득 적음
- **기각 이유**: 백엔드 서빙 컨텍스트에선 ?lang= 쿼리가 더 단순. 향후 SEO가 중요해지면 prerender로 양 페이지 정적 빌드 옵션 가능 (incremental)

### 3.3 (현 결정) A안 — 단일 키 + 백엔드 분기
- **장점**: 슬롯 명세 최소, 데이터 모델 깔끔, 프론트 lang 상태만 들면 됨
- **단점**: 부분 번역 시 fallback 정책 필요 (위 §2.4로 해결)

---

## 4. Consequences

### 4.1 즉시 효과
- 슬롯 명세 (`SLOTS.md`)는 단일 키로 박힘
- 페르소나 md 스키마 (spec-01)는 `{ko, en}` 객체 일관 사용
- 백엔드는 `i18n(node, lang)` helper 한 줄로 모든 분기 처리

### 4.2 코드 영향

```python
def i18n(node, lang: str):
    """ {ko: "a", en: "b"} → "a" 또는 "b". scalar/list는 그대로 반환 """
    if isinstance(node, dict) and lang in node:
        return node[lang]
    if isinstance(node, dict) and "ko" in node:
        return node["ko"]  # fallback
    return node            # 다국어 X 필드는 통과
```

API 핸들러 한 곳 한 곳에 분기 박을 필요 없이, 응답 dict를 재귀적으로 i18n 적용하는 wrapper도 가능 (spec-02에서 명세).

### 4.3 위험 + 완화

| 위험 | 완화 |
|---|---|
| 영어 번역 미작성 시 사이트에 한국어 그대로 노출 | fallback 명시 + 부팅 경고 로그로 누락 트래킹 |
| `{ko, en}` 객체 형식 실수 (예: ko만 string, en 누락) | 부팅 검증 (spec-01 §6.1) — 다국어 필드는 둘 다 있거나 fallback |
| 향후 일본어 등 언어 추가 시 객체 키 늘어남 | `{ko, en, ja}` 추가만으로 됨 — i18n helper는 lang 파라미터 그대로 동작 |

### 4.4 향후 확장 여지
- 언어 추가 (ja, en-US 등) — frontmatter 객체에 키 추가 + 백엔드 i18n helper는 무영향
- SEO 강화 시 빌드 시 lang별 정적 prerender 추가 옵션 (현 구조 유지)
