# [reviewer_doc] 검수 4 — SPEC 고침 fix-3 ~ fix-6 (차트 판정 C18 ~ C21 · 사진 DAY 저장 C22 · KOS 가져오기 C23)

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 에서:
- `planner-fix-3/4/5/6-instructions.md` · 각 `-report.md`
- 네 앞 리포트 `review-doc-3-report.md`

결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`:
- **C14 취소 · C18(글만 비교로 바뀜) · C19 · C20 · C21(매핑 뒤) · C22 · C22-기본값 · C23**
- 키 접두 `beforeAfter/`

## 작업 자리
워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — read-only.
- fix-3 · fix-4 = 커밋 `d98c5a28` · `b2005927`
- fix-5 · fix-6 = 미커밋
- `git diff a896cda0` 로 본다

## 볼 것
1. 결정 하나하나가 SPEC 에 반영됐는지 표로 대조한다
2. 사진 절 전수 — 아래 문장이 취소선 없이 살아 있지 않은지(grep):
   - 「DAY 저장 없음」
   - 「Blob 없음」
   - 「서명 주소 썸네일」
   - 「DAY 행만」
   - `before-after`
3. SPEC-000 `visit_photo` 가 데이터 규칙과 맞는지:
   - 소프트 삭제
   - external_ref
   - 시각 UTC
   - 업체 칸 금지
   - migration 필요가 SPEC-002 「migration 없음」 문장과 어긋나지 않는지
4. 구현 가능성 — 코드 워커가 되묻지 않을 만큼 닫혔는지:
   - 올리기 순서 · KOS 실패 · 다시 시도 · 삭제 · 가져오기 작업(입구 · 잠금 · 토큰 · 다시 그리기) · 저장소 꺼짐 · 크기 한도
5. 발명 · 금지 · lint

## 보고
- 리포트 `review-doc-4-report.md`(같은 폴더) — 판정 · 지적 파일:줄
- 수정 · 커밋 금지
- 완료 = preamble worker_done 두 채널
