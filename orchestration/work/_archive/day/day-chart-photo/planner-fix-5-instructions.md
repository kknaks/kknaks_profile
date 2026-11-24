# [planner] fix-5 — 사진을 DAY 에도 저장 (결정 C22 · C14 뒤집힘)

## 읽을 것
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - **C14 취소선 · C22 · C22-기본값** — 사용자 결정이다. 다시 열지 않는다
- 저장소 · 테이블 선례(read-only · `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>`)
  - `backend/day/adapters/storage/blob.py` · `contracts.py` — 키 규칙 · `before-after` 예약 · 관리 ID · disk/blob
  - `backend/day/models/chat.py` `ChatAttachment` · `models/reception.py` `IdPhoto` — `file_key` · `bytes` · `sha256` · `created_by_staff_id`
  - `models/customer.py` `ExternalRef`
  - SPEC-000 데이터 규칙 · SPEC-004 첨부 저장 절
- cc 의 KOS 재시도 선례: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/_archive/cc-prototype/overall-board/app-backend-report.md` 「WP-BE5」(`id_photo` · kos-retry)

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — 커밋 `b2005927` 위에서
- allowed_paths `products/day/`
- 커밋하지 마라

## 할 것
1. **SPEC-000** — 새 테이블(이름은 제안 · 예 `visit_photo`)
   - 칸 · 인덱스 · 소프트 삭제 · `external_ref` entity_type
   - 데이터 규칙과 맞춘다
   - **migration 필요**로 적는다
2. **SPEC-002 사진 절** — U-16 · 규칙 39 · KOS 사진 표 · API · 매트릭스를 C22 로 고친다
   - 올리기 순서 = Blob 저장 → DAY 행 커밋 → transaction 밖에서 KOS 등록 → external_ref
   - KOS 실패 = 「KOS 미반영」 표시 + [다시 시도] — 다시 시도 API 이름 제안
   - 썸네일 · 원본 = DAY 저장소에서 · KOS 서명 주소는 안 쓴다
   - 목록 = DAY 행만 · KOS 웹에서 직접 올린 사진은 OQ
   - 삭제 = DAY 소프트 삭제 + KOS 삭제 · 실패 처리는 OQ + 기본값
   - 크기 한도 = 채팅 첨부와 같은 값
   - 저장소가 꺼졌을 때 = 채팅의 `photo_disabled` 처리 선례를 따른다
3. 앞 판의 「DAY 저장 없음 · Blob 없음 · 서명 주소 썸네일」 문장은 취소선 + 날짜 · 사유
4. §4 차이 표 · 10-decision · log 갱신
5. 「서버에서만 쓰기 · 앱 범위 밖」은 그대로 둔다

## 검증 · 보고
- lint `--strict` → `products/day` ERROR 0
- 보고 `planner-fix-5-report.md`(같은 work 폴더) + preamble worker_done 두 채널
