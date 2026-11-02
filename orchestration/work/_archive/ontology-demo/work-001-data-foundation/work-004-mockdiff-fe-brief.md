
# [frontend] mock 픽스처 실 API 동기 (WORK-005 §1.5)

너는 **ontology-demo `frontend` 워커**다. app/front/ 만, git 조작 금지. WORK-005 백엔드 리포트의
mock↔실 API 필드 diff 를 해소하라 — 목록(read-only):
`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-work-001-data-foundation/bdd21223-455a-4b6e-803b-14b8ddf420b3/scratchpad/WORK-005-backend-report.md` §1.5 (+같은 폴더 mockdiff.txt 있으면 참조)

1. envelope 누락 필드 추가: graph(as_of·nodes[].grain) · tables(view·masked_fields) · rows(source_note).
2. **ontology 계층 픽스처 신설**: tables 2종 + ontology_nodes·ontology_edges rows(값은 design data/*.json 정본에서).
3. rows 표본 컬럼명을 실 API 이름으로(reviewDate·resv_date·body_masked 등 §1.5 나열분) — 표본 수준 유지, 전 컬럼 복제 불요(단 표시 컬럼 부분 표기 규칙 유지).
검증: tsc + build 1회. 보고 2채널(코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "frontend 완료: mock 동기".
