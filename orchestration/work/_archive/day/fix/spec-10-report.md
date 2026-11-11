# fix-spec-10 결과 보고 — 저장소 정정 4(컨테이너 `dev` · `prod` · 있음)

## 상태: done

근거 = `fix/correction-storage-4.md`(사용자 「env 없는데? 컨테이너 안 받은 거 아니야?」 · 코디 실물 확인). 계정 이름 · 주소 0 · 커밋 · push 0.

## 고친 자리

| 문서:줄 | 내용 |
|---|---|
| `40-architecture/deployment.md:19` | 머리 — 적는 컨테이너 이름 = 인프라 담당이 만든 `dev` · `prod`(정정 4) |
| `deployment.md:20` | 정정 3 줄 — 이름 정정 표시 · 「아직 없다 · 요청」 취소선 → **정정 4**: `dev` · `prod` 있음 · 사용자 계정 세 컨테이너 파일 쓰기 · VM 관리 ID 로 `dev` · `prod` · `files` 목록 읽기 200 · 올리기 · 읽기 · 지우기는 배포 뒤 · `files` 쓰지 않음 |
| `deployment.md:171` | env 표 — dev = `dev`(있음 · `dev.env` 에 이미) · prod = `prod`(있음 · `prod.env` 지금 값 없음) |
| `deployment.md:184` | 「저장소 · 환경」 지금 실제 상태(정정 4) |
| `deployment.md:190` | 「dev ↔ prod」 — 두 컨테이너 있음 · 관리 ID 둘 다 목록 읽기(사실) |
| `deployment.md:196` | 「prod」 — `prod` 있음 |
| `deployment.md:223` | Blob 준비 행 — `dev` · `prod` 있음 · `files` 쓰지 않음 |
| `deployment.md:239` | 미결 「컨테이너 요청」 **닫음** · `files` 는 쓰지 않음(지울지는 사용자 · 인프라 — 판단 문장 없음) |
| `40-architecture/mobile-deployment.md:53` | §1-1 「채팅 첨부 Blob 은 아직 없다」(7판부터 남아 있던 옛 말) 취소선 → 컨테이너 `dev` 있음 · 코드 연결 = WP-BE-4 · 배포 전까지 409 |
| `20-spec/spec-004-internal-chat.md:614` | C-A27 ⓑ — `dev` 있음(정정 4) |
| `spec-004:32` · `spec-000-data-model.md:31` | 정정 3 줄의 컨테이너 이름 `dev` · `prod` |
| `wp-plan.md:21` · `:177` · `:182` · `:199` | WP-BE-4 — 컨테이너 이름 `dev` · `prod` · 실물 ⓑ 「`dev` 있음 · 관리 ID 목록 읽기는 코디 확인」 |
| `log.md` | 10판 1줄 |

그 밖 계약(환경 = 컨테이너 · 키 `{용도}/{병원 id}/…` · 관리 ID · 실패 동작)은 9판 그대로.

**주의 — 바로잡은 실수**: 일괄 바꾸기(`daydev`→`dev`)가 사용자 인용 「daydev / dayprod 이렇게 컨테이너 만들고」 까지 바꿨다 → 인용 원문으로 되돌렸다(`deployment.md:20` · `spec-004:32` — grep 으로 확인). 사용자 말은 원문 그대로 둔다.

## 옛 이름 grep

`daydev` · `dayprod` · 「아직 없」 · 「인프라에 요청」 · 「생긴 뒤 / 생기기 전」 · 「사용자가 정한 이름」 → `products/day/20-spec` · `40-architecture` · `wp-plan.md` 에서 남은 것 = **취소선 · 사용자 인용 원문 · 「정정 3 의 `daydev` · `dayprod` 라는 컨테이너는 없다」 설명뿐**(살아 있는 계약 문장 0). 저장소와 무관한 「아직 없음」(정식 「DAY」 record · 서버 통역 · 기획안의 KOS)은 손대지 않음. `log.md` 의 이전 판 이력 줄은 이력이라 그대로.

## Delivery #241

v4 결과 계약 · 수용 항목에 `daydev` 가 있었다(이슈 본문 12줄) → **사실 정정으로 version 을 올렸다.**

| 항목 | 값 |
|---|---|
| contract_version | **5**(scope delta 기록 — 더해진 범위 없음) |
| risk | L3 그대로 |
| contract_digest | `sha256:97de14caa4771e857ce1eff781b04a5e6180fe6c4c0c083bcecad642d0f4568b` |
| plan_digest | `sha256:3fb28dfcc23cf85cf8e6804faf752d47e34fa951119b4ed18a32f50eb7d78288`(v4 승인 stale) |
| 승인 | **적용함**(`human` · `kknaksss` · 근거 = 사용자가 컨테이너를 받아 알려 준 것 「컨테이너 안 받은 거 아니야?」) |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| next_action | `prepare-spec-baseline` |
| 이슈 본문의 `daydev` | 0줄 |

바꾼 것: Target Delta 파일 저장소 줄(이름 · 있음) · A13(「`daydev` 생긴 뒤」 뺌 · `dev` 안 경로) · Review Surface(환경 = 컨테이너 `dev` · `prod` · 있음 · `files` 안 씀) · Execution(predeploy `DAY_BLOB_CONTAINER=dev` · dependencies · open questions). request = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v5.request.json`.

## 검증

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0.
