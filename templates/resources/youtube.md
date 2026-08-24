# 교안 양식 — `para/resources/youtube/C-NNN-<slug>.md`

**외부 사람이 영상을 안 보고도 이 문서만으로 이해·학습할 수 있어야 한다.**
영상 요약이 아니라 교안이다. 짧게 압축하지 말고 학습 가능한 수준으로 쓴다.

DB `content` 표가 이 파일의 frontmatter 를 씨드로 읽고, `detail_path` 로 본문을 가리킨다.
**본문의 원장은 이 파일이다** — DB 에 복사하지 않는다.

## frontmatter

```yaml
---
type: content
id: C-NNN                # 기존 최대값 + 1. 결번을 재사용하지 않는다
date: YYYY.MM.DD         # → DB published_on
duration: "M:SS"
speaker: 출처 채널
kind: study              # tutorial · study · talk · review
youtubeId: xxxxxxxxxxx   # → DB youtube_id
title:
  ko: "60자 이내. 원본 제목보다 간결·구체적으로"
  en: "same"
summary:
  ko: "핵심 한 줄. 80자 이내"
  en: "same"
tags:
  - "#소문자-키워드"     # 3~7개
---
```

`kind` 판정 — 모호하면 `study`.

| 값 | 무엇 |
| --- | --- |
| `tutorial` | 따라하면 무언가 만들어지는 hands-on 가이드 |
| `study` | 개념 · 이론 학습. 코드는 보조 |
| `talk` | 발표 · 강연 · 인터뷰 |
| `review` | 도구 · 라이브러리 평가 |

**파이프라인 상태를 frontmatter 에 두지 않는다.** 옛 구조의 `status` · `enriched_at` ·
`transcript` · `day` 는 전부 걷어냈다 — 처리 상태는 DB `queue` 가 갖고, 문서는 내용만 갖는다.

## 본문 — 순서대로

```text
## 요지            핵심 문장 4~6개. 사이트 카드에 실린다
## 개요            주제와 왜 중요한지 1~2문단
## 배경 / 사전 지식  모르는 사람도 따라올 수 있게
## 핵심 개념        개념별 H3 분리 권장
## 작동 원리        단계별 설명
## 코드 예시        실행 가능한 블록 최소 1개 + 의미 설명
## 함정·실수        흔한 실수 + 회피법
## 베스트 프랙티스   권장 패턴 · 대안 · 팁
## 참고            영상이 언급한 자료. 없으면 "(영상 내 명시 없음)"
```

영상에 명시되지 않은 항목은 자막에서 합리적으로 추론하거나 일반적으로 알려진
베스트 프랙티스로 채운다. **섹션을 비워 두지 않는다.**

## 개념과의 연결

**이 파일이 유튜브 개념의 출처층이다.** 이 교안에서 자란 개념은
`para/areas/concept/<영역>/` 에 만들고, 그 개념의 `up:` 이 이 파일 stem(`C-NNN-<slug>`)을
가리킨다. 만드는 절차는 `para/areas/area.md` 3.3.
