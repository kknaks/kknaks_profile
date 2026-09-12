선행 1건(evidence 키)과 WP-005 셋(자료·공유 목록·전사 검색 다리)을 모두 세웠다. 검증 216 passed / 0 failed (자료·공유 16 + 검색·자료 회귀 111 + 회의 89, -m 'not integration', tests/architecture 포함), make reset-demo 성공. 검색 다리를 세우다 「공유받은 사람이 검색에서 빠지는」 축 불일치를 하나 더 찾아 같이 막았고, 남은 것은 FE 소비 확인뿐이다.

## 선행 — evidence 키 투영
- `_line_view` 가 `_evidence_span()` 을 지나 **`{start_ms, end_ms}`** 로 낸다. AI 출력 스키마의 `from_ms`·`to_ms` 는 안에 그대로 두고 **나가는 자리에서 한 번** 옮긴다(저장 형식 불변). MeetingDetail·transcript·export 가 모두 이 한 자리를 지난다.
- 테스트 2: 합성 뒤 detail 의 evidence 키가 `{start_ms,end_ms}` · 구간 밖 강등 테스트도 새 이름으로.

## 변경 파일 (신규 2 · 수정 12)
신규: modules/meetings/materials.py · tests/contract/test_meeting_materials.py(16건)
수정: modules/meetings/application.py · platform/{meetings,native_materials,materials}.py · bootstrap/{application,material_sources}.py · entrypoints/http.py · tests/contract/{test_meeting_core,test_meeting_stream,test_meeting_memo_batch,test_meeting_finalize,test_answer_resources}.py

## 자료 (4 라우트)
- `GET /api/meetings/{id}/materials` → `[{material_id,name,content_type,size,uploaded_by,uploaded_at}]`(저장 위치 없음) · `POST` multipart `files` **여러 개** → 201 `{attached:[…], failed:[{name,reason}]}` · `DELETE …/{mid}` 204 · `GET …/{mid}/content`.
- 게이트: 붙이기·떼기는 **참석자**, 떼기는 **올린 사람만**(만든 사람도 남의 것은 못 뗀다), **in_progress 409**, 읽기는 참석·공유.
- 한도 20MB · `application/pdf`·`text/markdown`(확장자 `.md`/`.markdown`/`.pdf` 도 인정 — 브라우저가 형식을 비워 보내는 일이 흔하다). 전부 실패면 422 `{"code":"meeting_materials_rejected","failed":[…]}`.
- 저장은 업무 자료와 같은 Attachment 원장·같은 저장소. **떼기는 binding 만 끊는다**(원본·다른 자리 그대로, 테스트로 고정). `platform/materials.py` 의 안전 key 패턴에 `meetings/<id>/<file>` 을 더했다.

## 공유
- `GET /api/meetings/{id}/shares` → `[{member_id,name,basis:"attendee"|"share"}]`. 참석자(만든 사람 포함)가 먼저, 공유가 뒤.
- `POST /shares` body `{member_ids:[…]}` **여러 명** → 갱신된 같은 목록. 이미 참석·이미 열람은 **조용히 건너뛴다**. 알림 없음.
- `DELETE /shares/{member_id}` — **참석자는 409**(참석을 빼는 자리는 회의 정보 편집이다). 공유 근거인 사람만 거둔다.
- 공유받은 사람이 「지난」에 열람 배지로 담기고 캘린더에 서지 않는 것은 이미 그러함을 테스트로 확인만 했다.
- ⚠ **FE 영향**: `POST /shares` 의 body 가 `{member_id}` → `{member_ids:[…]}` 로 바뀌었고 응답이 MeetingRow 대신 **뷰어 목록**이다.

## 전사 검색 다리
- `native_materials.py` 에 `meeting_transcript` 갈래 신설 — **회의당 자료 하나**(material id = `uuid5(meeting_id)`), 본문은 확정 블록을 「화자 N [mm:ss] 텍스트」 줄로 이어붙인 것. 한 블록이 한 조각이라 근거 칩과 검색이 같은 단위를 센다.
- `material_sources.py` 의 `meeting` 갈래: ① 회의에 붙인 파일 ② 그 회의의 원문. 제목은 `title|title_candidate|「제목 없는 회의」`. origin 은 각각 `…/materials/{mid}/content` 와 `…/transcript`.
- **회의는 말하는 동안 원문이 자란다** — `ensure` 가 digest 가 바뀌면 그 자리를 갱신하고(판을 만들지 않는다) 검색이 그때 읽기를 다시 건다. 같은 내용이면 아무 잡도 쌓지 않는다. 테스트가 「자라도 material_id 는 하나」를 고정.
- **덤으로 찾은 것**: 검색의 회의 소유자 판정이 캘린더 투영(`list`, 조직 범위 축)을 쓰고 있어 **공유받은 사람이 교차 조직 회의를 검색에서 못 찾았다.** 열람 축(참석 ∪ 공유)을 그대로 쓰는 `readable_rows()` 를 회의 모듈에 두고 그것을 읽게 했다 — WP-002 가 상세에서 고친 것과 같은 축 불일치가 검색에 남아 있었다.

## 검증 수치
- 신규 `test_meeting_materials.py` 16
- 검색·자료 회귀: material_search_public · material_search · material_search_owners · material_persistence · material_integrity_lifecycle · link_materials · answer_resources · meeting_core · architecture = **127 passed(신규 16 포함), 실패 0**
- 회의: stream 27 · memo_batch 27 · finalize 35 = 89
- 합계 216 passed / 0 failed. `make reset-demo` 성공.

## FE 인계
- 자료 4 경로와 응답 모양은 위 그대로. 다중 업로드 필드 이름은 **`files`**.
- 부분 실패는 **201 + `failed[]`** 다 — 전부 실패일 때만 422이고 그때도 `detail.failed` 에 같은 모양이 온다.
- `POST /shares` body·응답 변경(위 ⚠). `GET /shares` 는 새 경로다.
- Line.evidence 가 이제 `{start_ms,end_ms}` — 타임칩이 그대로 읽는다.

## 미결
- 「같은 자료를 두 번 올렸을 때」의 병합은 두지 않았다 — 같은 파일이 두 줄로 선다(업무 자료와 같은 결).
- 자료 보관·계보(SPEC-006)·이미지·압축은 범위 밖 그대로.
- 원문 자료의 재읽기는 검색이 불릴 때 걸린다 — 아무도 검색하지 않는 회의는 색인되지 않는다(의도).
- 커밋·push 하지 않았다. `frontend/` 는 손대지 않았다.