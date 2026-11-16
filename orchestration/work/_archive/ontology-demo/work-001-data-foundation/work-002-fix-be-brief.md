
# [backend] WORK-002 검수 FAIL 수정 — 차단 1건 + 경고 필수 3건

너는 **ontology-demo `backend` 워커**다. 같은 워크트리, WORK-002 이어서. 리포트 먼저 (read-only):
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-002-report.md`

## 차단 (필수)

- **source_group 은 브론즈만** — allowlist.py 의 실버 6종 인자 제거, 실버·골드 null (SPEC-003 v0.0.8). 실버·골드 null 검사 회귀 1건 추가.

## 경고 중 필수 3건

- **W4** verify_session 이 password_configured 미확인 — env 미주입 시 공개 상수 키 세션 위조 경로. 검증 경로도 503(또는 401)으로 닫고 회귀 1건.
- **W5** build_meta 를 _all 채택 트랜잭션에서만 찍는 건 맞는데, 단계 단독 실행이 stale 표식을 남기는 경로 차단 — 단독 실행 시 표식 무효화(삭제) 또는 표식에 빌드 해시/시각 검증. 회귀 1건.
- **W1** 마스킹 뷰 컬럼명 유지로 '여기서 막힌다' 주석 2곳이 거짓 — 주석을 사실로 정정(막는 주체는 AC-8 게이트+뷰 SELECT 목록이며 필터 통과 편차는 테스트에 명시돼 있음). 코드 동작 변경 불요.

## 나머지 경고 5건·nit 6건 — 리포트 읽고 각각 「수정함 / 수정 안 함+사유」.

참고(수정 불요, 인지만): AC-8 게이트의 한계 2갈래(대소문자·f-string 합성)는 리뷰어 실측 — 게이트 정규식에 IGNORECASE 와 f-string 프리픽스 매치 추가가 싸게 되면 같이, 안 되면 한계를 게이트 docstring 에 명시.

## 완료 기준 — 테스트 전건 통과(신규 회귀 포함) + AC-8 재실행. 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "backend 완료: WORK-002 fix".
