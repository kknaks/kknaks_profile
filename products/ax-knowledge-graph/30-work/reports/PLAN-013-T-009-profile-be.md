# PLAN-013-T-009 결과 보고

## 상태: done

WORK-010 BE 몫(C-1~C-3). Source Inbox md 파일 업로드 intake. 코드 레포
`/Users/kknaks/git/toy_pr2/ax-graph/apps/api`. T-006/T-008 워킹트리 변경분 무접촉.
**미커밋** — admin 검수 후 일괄(브랜치 생성 안 함).

## OQ 확정값 (SPEC-003 §7 OQ — 리포트 필수)

- **파일 크기 상한 = 1 MiB(1,048,576 bytes)**. 근거: md는 텍스트라 1 MiB면 장문
  노트/아티클(수백 페이지 분량)도 충분하고, 요약① 입력·서버 메모리·업로드 남용을 유계로 둔다.
  초과 시 413 `UPLOAD_TOO_LARGE`. (`MAX_UPLOAD_SIZE_BYTES`)
- **md frontmatter 처리 = strip 안 함(본문 그대로 보존)**. 근거: intake를 무손실·무파서로
  유지한다. frontmatter의 메타(제목/태그 등)도 의미가 있어 요약①(LLM)이 함께 정제하게 두는 편이
  안전하고, 파서 도입/오파싱 리스크가 없다. BOM만 제거(`utf-8-sig`)한다.
- **md 본문 저장 위치 = DB `raw_text`**(별도 파일시스템 아티팩트 없음). 근거: chat/manual과
  동일 저장 경로로 요약 파이프라인이 그대로 소비한다(별도 스토리지 도입 불필요).

## 수행 내용

### C-1 업로드 endpoint
- `POST /sources/upload` (`axkg/api/routes/sources.py`), multipart form 필드 `file`.
- **admin 전용**: sources 라우터가 `main.py`에서 `require_admin`으로 등록돼 있어
  `/sources/manual`과 동일 authz. staff 개방 없음(기존 인박스 표면 경계 무변경, AXKG-SPEC-008).
- **v1 = `.md`만**: 확장자(대소문자 무시) 미일치 또는 텍스트 디코딩 불가 → `UnsupportedUploadTypeError`
  → 422 `UNSUPPORTED_UPLOAD_TYPE`, **source row 미생성**(intake validation, 수집 실패 아님 —
  SPEC-012 adapter 경로 미진입). 빈 본문 → 422 `EMPTY_UPLOAD_TEXT`(SPEC-003 §4 upload raw_text
  필수 강제), 크기 초과 → 413 `UPLOAD_TOO_LARGE`.
- FE(PLAN-013-T-010) 계약과 정합 확인: 경로 `/sources/upload`, 필드 `file`, 반환 bare Source,
  Case `UNSUPPORTED_UPLOAD_TYPE`(FE `createUploadSource`/`isSupportedUploadFile`).

### C-2 upload source 생성
- `SourceService.create_upload` (`services/sources.py`): `source_channel=upload`,
  `source_url=null`, `normalized_url=null`, `slack_message_ts=null`, `raw_text`=디코딩한 md
  본문(필수), `original_filename`=업로드 파일명 보존, `received` 생성.
- **DB 변경**: `sources.original_filename`(nullable Text) 컬럼 추가 → 마이그레이션
  `0021_source_original_filename.py`. `source_channel`의 `upload` 값과 URL nullable은 이미
  T-008의 0020에서 커버됨(중복 마이그 없음). 모델·DTO·SourceResponse 동기(`original_filename` 노출).

### C-3 요약 직행 (adapter 미경유)
- 생성 직후 `create_manual`과 **동일 배선**으로 자동 요약 트리거: open-kknaks 구성 시
  `start_summary`(received → summarizing + `collect_source_summary` queued task) 후 background
  `execute_source_summary`. URL이 없어 SPEC-012 adapter 수집 경로를 타지 않고, 업로드 md 본문
  자체가 원문으로서 곧 요약 입력이 된다(**fallback 아님·원문 그 자체**). 이후 요약→분류 흐름·분류
  승인(admin)은 slack/manual/chat과 동일·무변경.

## 테스트/검증 결과

- 신규 `tests/test_source_upload.py` 11건:
  - 정상 업로드(admin) 201 — channel=upload·source_url/normalized_url null·slack_ts null·
    raw_text=md 본문·original_filename 보존·received / inbox 목록 노출
  - staff 403(`FORBIDDEN`) / 미인증 401
  - 비md(pdf/txt) 422(`UNSUPPORTED_UPLOAD_TYPE`) + source 미생성 / 대문자 `.MD` 허용
  - 빈 md 422(`EMPTY_UPLOAD_TEXT`) / frontmatter 보존
  - 요약 직행(received → start_summary → summarizing + collect_source_summary, source_url null)
  - 서비스 유닛 — 확장자/None/디코딩 불가/빈본문/크기상한 거부
- 전체 `cd apps/api && uv run pytest`: **425 passed**(T-008 후 414 + 신규 11), in-memory sqlite.
- `uv run alembic heads` → `0021 (head)` 단일 head, 체인 `0020 → 0021` 정상.

## 다른 팀 영향

- **@profile-fe**: 업로드 UI는 PLAN-013-T-010에서 이미 구현(work-010 C-4 done). BE 계약 정합
  확인 완료 — `POST /sources/upload`(multipart `file`), 반환 Source(`original_filename` 포함),
  Case `UNSUPPORTED_UPLOAD_TYPE`(422). FE 클라이언트(`createUploadSource`)와 경로·필드·에러코드 일치.
- **API 스키마 추가**: `Source.original_filename`(nullable) 필드가 응답에 추가됐다(upload 채널만
  값, 그 외 null). FE Source 타입에 optional로 이미 반영돼 있으면 무영향.

## 이슈/블로커

- 없음. 커밋은 하지 않았다(admin 검수 대기).
- 참고 — 스펙 미정의 보조 에러코드 2건을 **구현 기본값**으로 도입(스펙 Case Matrix 아님,
  문서 수정 없음): `EMPTY_UPLOAD_TEXT`(422, SPEC-003 §4 "upload raw_text 필수" 강제),
  `UPLOAD_TOO_LARGE`(413, §7 OQ 크기 상한 강제). 계약 승격이 필요하면 후속 spec 반영 권고.
