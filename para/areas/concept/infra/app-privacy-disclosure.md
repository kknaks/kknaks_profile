---
type: concept
id: app-privacy-disclosure
title: 앱 개인정보 신고 — 「수집」은 기기에서 보내 보관하는 것 (App Privacy · Privacy Nutrition Label)
aliases:
  - App Privacy
  - 앱이 수집하는 개인정보
  - 개인정보 영양 성분표
  - privacy nutrition label
up:
  - 2026-11-12-prod-deploy-re1
tags:
  - 모바일
  - 앱스토어
  - 개인정보
---

# 앱 개인정보 신고

App Store 는 앱마다 「무엇을 수집하고, 사용자와 연결하고, 추적에 쓰는지」를 제품 페이지에 표로 보여 준다. 개발자가 직접 신고한다.

## 정의

Apple 정의: 「Collect」 = 데이터를 **기기 밖으로 보내, 요청을 실시간으로 처리하는 데 필요한 시간보다 오래** 개발자나 협력사가 접근할 수 있게 하는 것.

- 기기 안에서만 처리 → 수집 아님.
- 실시간 처리 뒤 보관하지 않음 → 수집 아님(예: 실시간 음성 인식 스트림).
- 서버가 **다른 곳에서 받아 온** 데이터 → 앱이 수집한 것 아님(예: 병원 EMR 사본).
- 종류마다 목적 · 사용자 연결 여부 · 추적 여부를 답한다.

## 왜 중요한가

「우리 앱은 조회만 한다」 는 직관이 틀리기 쉽다. DAY 는 「채팅만 수집」이라고 생각했지만, 로그인 때 저장하는 이메일 · 이름 · 계정 id, 푸시용 설치 id · 토큰, 업무 조작 이력도 서버에 남아 신고 대상이었다. 반대로 EMR 사본과 Soniox 통역 음성은 정의상 빠진다. **코드에서 「앱이 보내고 서버가 보관하는 것」을 세는 것**이 답을 정한다.

## 경계와 오해

- **공개 API 가 없다** — App Store Connect API 에 이 표가 없어(`dataUsages` 404) 웹에서 손으로 넣는다.
- **「연결됨」을 하나만 빠뜨리기 쉽다** — 계정 id 를 「연결 안 됨」으로 두면 미리보기에 「연결되지 않은 데이터」가 생긴다. 게시 뒤 미리보기로 확인한다.
- **추적은 광고 · 광고 측정 목적의 타사 데이터 결합이다** — 업무용 앱의 기능 목적 보관은 추적이 아니다.

## 함께 보는 개념

- [[code-signing]] — 같은 제출 과정의 서명 쪽
- [[unlisted-app-distribution]]

## 출처

- [[2026-11-12-prod-deploy-re1]] §2 「App Store 「수집」 정의로 App Privacy 답하기」 — DAY 7종 신고 · EMR · 통역 · 접속 IP 제외(`mobile-asc-answers.md` · `mobile-asc-apply-report.md` · https://developer.apple.com/app-store/app-privacy-details/)
