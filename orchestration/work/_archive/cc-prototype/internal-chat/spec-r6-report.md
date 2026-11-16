# internal-chat planner r6 결과 보고 — 마감 동기

## 상태: done

## 수행 내용

- `20-spec/spec-007-internal-chat.md` **0.5.0 → 0.5.1**(draft 그대로 · updated_at 2026-10-30) · 바뀐 줄 끝 `(r6)` · 머리 변경 표 0.5.1 행 · frontmatter sources 2줄(r5-dispositions · review-code-r4 · `bf30db4`) · §0 근거 표기 `R5D:x · CR4:WARN-n` 한 줄
- `r5-dispositions.md` 동기(처분 표는 **5줄** — FAIL-1 · W-1 ~ W-4. 브리프의 「4줄」과 다름 · 다섯 줄 모두 옮김):

| 처분 | SPEC 자리 |
|---|---|
| FAIL-1 푸시 · SSE 받는 사람 = 볼 수 있는 멤버만 | §4.6 V10(「안 바꿈」 ~~취소선~~ → 거름) · §7 `chat_message` 받는 연결 · r5 줄 · §8 「받는 사람」 · §13.1 새 행 「푸시 · SSE 경합」 |
| W-1 옛 DB 채우기 전 · 뒤 `unread` 같음 | §13.1 「안 읽음 불변식」 |
| W-2 `chat_app3_test.dart:446` 옛 문구 | §13.2 r6 줄 |
| W-3 아이패드 모아보기 = 방 정보 시트 안 | §10.16 「틀」(이미 r5 그대로 · 확인 표시) · §10.11 그대로 |
| W-4 꺼진 기기 열린 대화 = 알려진 한계 · 경계 바뀐 방 처음부터 | §11 새 행 「멤버 경계가 바뀐 방」 · §13.2 r6 |

- 코드 리뷰 r4 WARN 3 → **§15 OQ-970 · 971 · 972**(각각 지금 동작 · 고칠 길 · 「남음 — 고치지 않고 마감」 · 리뷰 문장 그대로 근거) · §10.16 「나감 · 숨김」에 OQ-972 가리킴
- 부록 D → 「처분 문서 8개」 · **D.8 r5-dispositions 5 / 5** · 합 42 / 42 · 부록 A D-69 행에 r6 자리 더함
- **§12 「바뀌는 코드 자리」 표는 안 고침**(R5-B14 「안 바꿈」은 이력으로 남김 · V10 행이 `R5-B14(이력 · 안 고침)` 로 가리킴)
- `30-work/work-011-internal-chat.md`: progress **0 → 96**(WP 25 중 24 완료) · Meta 「진행 (r6)」 줄 · Covers 0.5.1 · WP 상태 25행 = `완료`(PR · 빌드 번호) / WP-E2E3 = `남음`(C1 ~ C23) · WP-REVIEW4 = 완료 + WARN 3 남음(OQ-970 ~ 972) · 병렬 그림 r5 끝 줄
- `20-spec/README.md` SPEC-007 행(0.5.1 · API 20 · 경로 71 · C1 ~ C23) · `30-work/README.md` WORK-011 행(progress 96 · 남음) · `log.md` 한 줄

## 검증

- DEC D-01 ~ D-69 → SPEC 본문 grep 0 인 것 = **0** · 부록 A 행 = **69 / 69**(`sed -n '/^## 부록 A/,/^## 부록 B/p' | grep -oE "^\| (~~)?D-[0-9]+" | sort -u | wc -l` = 69)
- 새 OQ 행 `^| OQ-97[0-2]` = 3
- public grep(키 · 토큰 · 비밀번호 꼴 · 전화번호 · 팀 id · 실명) 바뀐 5파일 = **0**

## 미결 · 주의

1. **실기기 범위**: 브리프는 「C1 ~ C21」이지만 SPEC §13.3 · WORK-011 완료 조건은 **C1 ~ C23**(r5 가 C22 초대 · C23 들어온 뒤 대화만을 더함) — SPEC 대로 C1 ~ C23 으로 적었다. 코디 확인
2. **WP-SIM3**: `_RESUME` §5 에 r5 시뮬레이터 확인 기록이 없다 — 「완료로 넘김 — 기록 없음(코디 확인)」으로 적음
3. progress 96 = WP 개수 셈(완료 조건인 실기기 E2E3 가 남아 마감 아님)
4. SPEC 머리 SSOT 줄의 「운영 `b988f21`」(§0 위 인용)은 줄 번호 기준 이력이라 그대로 둠 — 운영 `bf30db4` 는 frontmatter · 변경 표 · V10 행에 적음

## git status --short

```
 M orchestration/config/projects/cc-prototype.json
 M para/projects/summer-star/cc-prototype/00-baseline/README.md
 M para/projects/summer-star/cc-prototype/10-decision/README.md
 M para/projects/summer-star/cc-prototype/20-spec/README.md
 M para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md
 M para/projects/summer-star/cc-prototype/30-work/README.md
 M para/projects/summer-star/cc-prototype/deploy.md
 M para/projects/summer-star/cc-prototype/log.md
?? orchestration/roles/cc-prototype/designer/
?? orchestration/work/internal-chat/
?? para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md
?? para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md
?? para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md
?? para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md
```
