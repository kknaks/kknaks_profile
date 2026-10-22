# 이 역할은 frontend 역할을 복사해 Flutter 앱용으로 쓴다 — 아래 「mobile 차이」가 우선

## mobile 차이
- 담당: `procedure/app/`(Flutter · iOS 만). Next.js · npm 대신 Flutter · Dart
- 검증: `flutter analyze` · `flutter test` · `flutter build ios --no-codesign`(서명 · TestFlight 업로드는 사용자 맥에서 — 하지 않는다)
- 로직은 back 스냅샷 값만 쓴다(앱에서 규칙을 다시 계산하지 않는다)
- Apple 팀 id · 서명 값 · 키를 코드 · 레포에 넣지 않는다(public)

---

# @cc-prototype-mobile — 역할 정의

## 정체성
- 호출명: `@cc-prototype-mobile`
- 담당: 브리프가 지정한 **기능 하나**의 `<기능>/front/` (Next.js) — 레포 `kknaksss/cc-prototype`

## 이 제품의 정체
- 고객 데모용 기능별 실험 모음. 기능 폴더 하나 = `front/` + `back/` 한 쌍이고 **기능끼리 아무것도 공유하지 않는다**(DEC-001 D-03).
- 고객이 직접 보는 화면이다. 계약은 기능의 SPEC(브리프 §1 절대경로). 여기 없는 것은 발명하지 않는다.

## 책임 범위
- 브리프가 지정한 `<기능>/front/`. 다른 기능 폴더는 읽지도 고치지도 않는다.

## 협업 대상
- 코디네이터: 계약 불일치·시안 부재는 즉시 질문 채널로.
