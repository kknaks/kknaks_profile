---
type: project
id: P-14
org: studio
title:
  ko: "mykakao"
  en: "mykakao"
summary:
  ko: "카카오톡 대화를 내보내기 없이 로컬에서 자동 추출(SQLCipher DB 복호화). 추출 확인용 웹 데모(실시간 SSE) 완성. 향후 일정 파싱 → 캘린더 출력 단계 예정."
  en: "Extract KakaoTalk conversations locally without manual export (SQLCipher DB decryption). Web demo with live SSE done. Next: parse schedules → calendar output."
category: backend
status: wip
date: "2026.06"
stack: []
visible: false
links:
  repo: "github.com/kknaksss/mykakao"
# 포트폴리오 PDF 케이스 스터디 (planning-02 §3.3) — 비면 PDF 에 미표시.
problem:
  ko: ""
  en: ""
approach:
  ko: []
  en: []
impact:
  ko: []
  en: []
learnings:
  ko: []
  en: []
troubles: []
---

# 개요

카카오톡 대화를 수동 내보내기 없이 로컬 PC에서 자동 추출하는 도구. 로컬 SQLCipher DB를 키 유도로 복호화해 메시지를 읽는다 (라이브 검증: 631k 메시지 / 741 방). 현재 범위는 **메시지 추출까지** — 추출 확인용 웹 데모(백+프론트)와 실시간 SSE를 포함한다. 일정 파싱 → 캘린더 출력은 다음 단계에서 별도로 결정·구현한다.

제품 문서 SoT: `products/mykakao/`.

# 기술스택
(TBD)

# 주요기능
(TBD)

# 아키텍처
(TBD)

# 핵심 구현
(TBD)

# 마주친 문제
(TBD)

# 회고
(TBD)
