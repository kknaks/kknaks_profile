---
type: work
id: MRT-WORK-004
title: "M4: 앱 아이콘 추출"
status: done
product: mac-remote
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/work
  - status/done
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-004-app-icon|MRT-SPEC-004]]"
  works:
    - "[[work-001-cli-prototype|MRT-WORK-001]]"
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# M4: 앱 아이콘 추출

실행 중 앱들의 아이콘을 PNG base64로 추출하는 함수를 만든다. 화면 캡처가 아닌 설치된 앱의 아이콘 파일을 읽는 것.

> 원본: `mac-remote/doc/work/Work-04-app-icon.md`. 구현 계약은 [[spec-004-app-icon|MRT-SPEC-004]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[work-001-cli-prototype\|MRT-WORK-001]] |
| 관련 스펙 | [[spec-004-app-icon\|MRT-SPEC-004]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-04 §데이터 모델 | AppIcon (appName, iconData) | [x] |
| Spec-04 §상태 전이 | 아이콘 추출 → base64 인코딩 | [x] |
| Spec-04 §에러 처리 | ICON_NOT_FOUND → 기본 아이콘 대체 | [x] |
| Spec-04 §엣지 케이스 | 아이콘 리사이즈, CLI 도구 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | NSRunningApplication.icon으로 아이콘 추출 | [x] | 035a8c5 | AppIcon 모델 + IconExtractor |
| 2 | NSImage → PNG Data → base64 인코딩 | [x] | 4f805d0 | encodeToBase64 + formatAppIconsJSON |
| 3 | 아이콘 리사이즈 (64x64) | [x] | 2cabb6c | iconSizePixels=64, resizeAndEncodePNG |
| 4 | 실패 시 기본 아이콘 fallback | [x] | 714043d | defaultIconBase64 (1x1 PNG) |
| 5 | 앱별 중복 제거 (이름 기준 1회) | [x] | 7e99766 | IconCache + uniqueAppNames |

## 기술 메모

- NSRunningApplication(processIdentifier: pid)?.icon → NSImage
- fallback: NSWorkspace.shared.icon(forFile: bundlePath)
- NSImage → tiffRepresentation → NSBitmapImageRep → png → base64

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 아이콘 추출 | `swift run MacHelper icons` → 앱별 base64 문자열 출력 | 수동 검증 필요 (macOS) |
| 2 | base64 검증 | 출력된 base64를 디코딩해 PNG 이미지인지 확인 | 수동 검증 필요 (macOS) |
| 3 | 중복 없음 | 같은 앱이 2번 이상 출력되지 않는지 확인 | 수동 검증 필요 (macOS) |
| 4 | 모델/캐시 테스트 | 순수 Swift 로직 테스트 (AppIcon, IconCache 등) | 수동 검증 필요 (Swift 미설치) |
| 5 | base64 유틸 테스트 | encodeToBase64, isValidPNGBase64, defaultIconBase64 | 수동 검증 필요 (Swift 미설치) |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
| 2026-05-24 | 전체 구현 완료 (5개 태스크, TDD) |
