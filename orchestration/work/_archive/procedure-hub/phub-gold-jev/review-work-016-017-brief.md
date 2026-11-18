# [reviewer] WORK-016 · WORK-017 검수 (+ SPEC-008 0.2.0 · SPEC-001 0.8.1 고친 곳)

너는 **procedure-hub 문서 검수 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/` 아래 reviewer(없으면 researcher) `role.md` · `rules.md`.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(d97a9ad) · 앱(읽기만) `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(be1c622).

검수 대상: `$W/WORK-016-hub-resolve-v081.md` · `$W/WORK-017-consult-v04.md`. 함께: `$W/SPEC-008-consult-entry.md` 0.2.0 · `$W/SPEC-001-hub-gold-mcp.md` 0.8.1 의 **변경 기록에 적힌 F-1~F-16 처분**이 앞 검수 `$W/review-spec-008.md` 의 고칠 방향 · `$W/_RESUME.md` §2 맨 위 11-18 코디 답과 맞는지. 작성 브리프 `$W/work-016-017-brief.md` · `$W/spec-008-fix1-brief.md`.

## 볼 것

1. **SPEC 고친 곳**: F-1~F-16 이 코디 답대로 닫혔나(특히 F-1 ⓒ · F-5 · F-8 · F-10) — 새 구멍이 생겼나.
2. **WORK ↔ SPEC**: SPEC 계약 줄(LD · UC · VF · OU · QS · QM · DT · BQ · FL · 장부 · 프롬프트 · E8) 하나씩 WORK 의 어느 WP 가 맡나 — 빠진 줄 · WP 둘이 같은 줄을 다르게 맡는 곳.
3. **표면 전수**: WORK 의 grep 표(허브 abbr 7 파일 · 앱 켠 가지 부름 6 자리 · 27 행)를 네가 다시 grep 해서 빠진 자리. 허브 시험 「지움 20 · 고침 13 · 표 밖 ★6」 도 다시 셈.
4. **시험 범위**: WP 마다 그 WP 시험 파일만 돈다는 규칙이 지켜지는 목록인가 · 바뀌는 기존 시험의 까닭이 계약에서 오나(시험이 낸 수를 그대로 기대값으로 옮기는 지시 없음).
5. **완료 조건**: E8 이 D-14 · U8-2 · U8-4 문턱 · ref.to=answer 5 대화 답 LLM 실제 호출 · score.py 를 덮어쓰지 않는 길(B-6) 로 닫혔나 · 포트(18224 · 18107) · 18105 · 18222 · 18432 금지 · 커밋 금지.
6. 화면 문구를 지어 넣은 곳 · 비밀값 노출 길.

## 산출

`$W/review-work-016-017.md` 1개: 머리 PASS / WARN / FAIL + 한 줄 · 결함 표(번호 · 심각도 · 자리 · 근거 · 고칠 방향) · 「구현 발주 전에 꼭 고칠 것」(없으면 「없음」).

## 하지 마라

쓰기는 그 1개만. 문서 · 코드 수정 · 서버 · LLM 호출 금지. 결정하지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer(WORK-016 · 017) 완료: <PASS|WARN|FAIL> <한 줄>" \
  --body "결함 수(심각도별) / 구현 전 꼭 고칠 것 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] reviewer(WORK-016 · 017) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
