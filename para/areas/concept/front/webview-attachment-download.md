---
type: concept
id: webview-attachment-download
title: 데스크톱 웹뷰의 첨부 응답 받기
aliases:
  - 웹뷰 다운로드
  - Tauri 다운로드
  - wry 다운로드
  - Content-Disposition 첨부
  - 셸 가로채기
  - 하위 프레임 이동
  - srcdoc
  - 이동 훅
up:
  - 2026-10-05-strong-hajin-polish3
  - 2026-10-07-strong-hajin-inbox
tags:
  - frontend
  - tauri
  - webview
  - download
---

# 데스크톱 웹뷰의 첨부 응답 받기

브라우저는 `Content-Disposition: attachment` 를 보고 파일로 저장한다. 데스크톱 앱의 웹뷰(Tauri/wry)는 **그 헤더를 안 볼 수 있다** — 그러면 「내보내기」가 파일이 아니라 앱 창에 그려지고 사용자는 그 화면에 갇힌다. 앱 셸이 **요청 단계에서 가로채 직접 받아** 저장해야 한다.

## 정의

1. **웹뷰는 MIME 만 본다** — wry 0.55.1(macOS)의 응답 정책은 `canShowMIMEType` 만 묻고 `Content-Disposition` 은 읽지 않는다. `text/html` 첨부는 「표시 가능」이라 **Allow → 창에 그려지고** download handler 는 불리지 않는다(소스로 확인). 응답 단계에서는 이미 늦다
2. **요청 단계에서 가른다** — 셸이 이동 훅에서 같은 origin 의 `/api/` 접두 링크를 가로채 막고, 셸(Rust)이 같은 요청을 **웹뷰의 쿠키를 실어** 직접 보낸다. 응답이 첨부면 다운로드 폴더에 저장한다
3. **inline 응답이면 아무것도 안 한다** — macOS 에선 `_blank` 링크도 opener 의 이동 훅을 먼저 지나 셸이 「같은 탭인가 새 창인가」를 못 가른다. inline 을 「다시 navigate」 하면 새 창이었어야 할 링크가 앱 창을 덮는다
4. **쿠키 읽기는 스레드를 고른다** — `cookies_for_url` 은 메인 스레드 콜백이라 이동 훅(메인)에서 기다리면 막힌다. 별도 스레드에서 받는다
5. **웹에 알리기는 권한 0 으로** — 저장 결과는 셸이 `eval` 로 `CustomEvent` 를 쏘아 웹이 듣는다. 새 IPC 명령이 아니라 capabilities 변경이 없다

## 경계와 오해

- **가로챌 경로를 셸이 얼마나 아는가가 선택의 축이다** — 웹을 fetch+blob 으로 바꾸면(링크 자리 전부 + 기존 화면 파일 수정) 표면이 넓고, 엔드포인트 패턴을 셸이 들면 새 파일 엔드포인트마다 셸을 고친다. **접두 하나(`/api/`)만 아는 쪽**이 새 엔드포인트를 자동으로 덮는다
- **가로채기는 미리보기도 삼킨다** — `/api/` 로 여는 PDF 미리보기 같은 inline 표시가 같은 훅을 지나면 빈칸이 될 수 있다. 실기로 확인해야 하는 자리다
- **이동 훅은 하위 프레임 이동도 받는다** — wry 는 iframe 안의 이동도 같은 이동 훅으로 보낸다. 메일 본문을 `srcdoc` 으로 넣은 iframe 은 `about:srcdoc` 으로 이동하는데, 훅이 「앱 밖 주소」로 보고 **취소**해 메일 본문이 웹에선 보이고 앱에서만 비었다. 훅에 예외를 늘리는 대신 **이동 없이** iframe 의 첫 문서에 본문을 직접 써 넣어 닫았다 — 훅을 지날 일 자체를 없앴다
- 서버를 고칠 일이 아니다 — 헤더는 맞다. 웹뷰 쪽 동작 차이다
- jsdom·브라우저 테스트로는 안 잡힌다 — 웹뷰 정책은 실기에서만 보인다

## 함께 보는 개념

- [[http-message]] — `Content-Disposition`·`Content-Type` 이 사는 헤더
- [[cookie]] — 셸이 직접 보낼 때 웹뷰의 세션을 실어야 하는 이유
- [[build-flavor]] — 같은 Tauri 셸의 판별 설정
- [[output-escaping]] — 메일 본문을 샌드박스 iframe 에 그리는 이유
- [[oauth-state-parameter]] — 같은 훅이 302 를 안 따라가 동의 URL 을 JSON 으로 받은 자리

## 출처

- [[2026-10-05-strong-hajin-polish3]] §2 — Strong Hajin WORK-010 Phase 3 데스크톱 셸(`fe-p3-decision.md` §0·§5 · `review-fe-p3-report.md` · SPEC-006 U-5 · 커밋 `9c15934`)
- [[2026-10-07-strong-hajin-inbox]] §2 — Strong Hajin WORK-011 메일 본문이 앱에서만 빈 결함(PR #15 · SH-IMP-011)
