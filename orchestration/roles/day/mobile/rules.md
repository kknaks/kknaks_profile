# @day-mobile — 규칙

## Flutter
- 로직은 back 이 준 값만 쓴다 — 앱에서 규칙을 다시 계산하지 않는다.
- back 주소 · 환경값은 빌드 설정(`--dart-define` 등)으로만. 하드코딩 금지.
- 시안이 정본. 폰(390px)과 아이패드 둘 다 시안대로. 시안에 없는 자리는 리포트에 기록하고 임의로 꾸미지 않는다.
- Apple 팀 id · 서명 값 · APNs 키를 코드 · 레포에 넣지 않는다.

## 안전
- 서명 · TestFlight 업로드 · 실기기 설치는 하지 않는다(코디 · 사용자 몫).
- 사용자 포트 · 프로세스 · 시뮬레이터 · 기기를 건드리지 않는다.

## 스코프
- allowed_paths 밖 수정 금지. 커밋 · push · PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일 · 화면 목록
## 검증 — 명령과 결과 (analyze · test · build ios --no-codesign)
## 계약 대조 — SPEC · 시안 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
