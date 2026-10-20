
# 재개 노트 — strong-hajin-attach-read (strong-hajin)

**지금**: backend 워커 read-only 조사 발주(10-13) — 결과 자료 「내용을 읽지 못함 · 본문에 텍스트가 없습니다」 원인. 리포트 수령·근거 대조 완료. 사용자 결정 대기(고칠지·어디까지)
**다음**: 사용자 결정 — 고치면 개선 목록 SH-IMP 로 올리고 문서 파이프라인부터. 파일 형식은 운영 DB 쿼리(리포트 §6.1)로 확정 필요

세팅: `scripts/new-work.sh strong-hajin strong-hajin-attach-read` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_172d1382-eaf9-44d6-b91c-40f64680644e`

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-attach-read` (branch `kknaksss/strong-hajin-attach-read`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] <진행 중 — 누가 · 무엇을>
- [ ] <다음 할 일>
- [!] <막힌 것 · 사용자 게이트 · 주의>

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| <YYYY-MM-DD> | <무엇을 정했나> | <사용자 지시 · 조사 리포트 · 리뷰 판정> |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| backend | `term_6f585bca-a6ca-4c8e-b24f-0fd37a0881af` | `task_c50631b1dee2` | `ctx_7e81d060ecad` | `strong-hajin-attach-read-be-brief.md` | 완료(검수 OK) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-10-13` 실물 PDF(세라미크_명동_본사_인터뷰.pdf) §7 — 글자가 벡터 윤곽선(Quartz PDFContext · Creator=Claude), 14쪽 0자 직접 재확인. 판정은 계약대로, 문구가 오해. 코디handle → term_172d1382
- `2026-10-13` 리포트 수령 — empty_content 오판(PDF 이미지 판정 얕음·Office 판정 없음) + needs_ocr 저장 시 failed 로 뭉개짐. 핵심 인용 4곳 코드 대조 확인
- `2026-10-13` 사용자 스크린샷으로 조사 요청 → backend 워커 read-only 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
