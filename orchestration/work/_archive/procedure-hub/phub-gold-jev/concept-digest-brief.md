# [writer] 회고 → 개념 소화 (phub-gold-jev 마감)

너는 문서 작성 워커다. 앞 판 맥락이 없다. 레포 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/CLAUDE.md` · `para/areas/area.md`(§3 — 먼저 찾는다 · 기존 노트 보강 · 없을 때만 새로 · 다 쓰면 §3.4 맵에 한 줄) · `orchestration/runbook.md` STEP 8 「아카이브 직후 — 회고를 개념으로 소화한다」.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · 회고 `$P/orchestration/work/phub-gold-jev/SUMMARY.md` §2(항목 6) · 근거 리포트는 같은 폴더(§6 목록).

## 할 일

1. §2 항목마다 `para/areas/concept/` 에서 맞는 노트를 찾는다(파일명 · 내용). 후보(확인 후 판단 — 맞지 않으면 다른 것): `ai/entity-resolution.md` · `ai/golden-set-regression.md` · `ai/strict-json-schema-output.md` · `ai/model-routing.md` · `db/medallion-architecture.md` · `db/seed-data.md` · `infra/reverse-proxy.md` · `infra/staging-area.md` 등. 「선택적 하위 시스템은 꺼져도 본체는 뜬다(graceful degradation)」 처럼 맞는 노트가 없으면 새로 쓴다(같은 폴더의 기존 노트 꼴 그대로 · §3.4 맵에 한 줄).
2. 기존 노트는 **보강**만(새 절 「사례 — phub-gold-jev(2026-11-18)」 꼴로 · 이번 작업에서 그 개념이 어떻게 쓰였고 무엇이 어려웠나 · 수 · 근거 경로). 기존 본문을 갈아엎지 마라.
3. 회고 §2 각 항목 끝에 `[[개념]]` 역링크를 단다(그 노트 경로 꼴은 레포의 다른 회고가 쓰는 꼴을 따른다 — `para/projects/company/procedure-hub/log/*.md` 에서 확인).
4. 회사 내부 IP · VM 이름 · 접속 값 · 키 쓰지 마라.

## allowed_paths

쓰기: `para/areas/concept/**` · `para/areas/area.md`(§3.4 맵 줄 추가만) · `orchestration/work/phub-gold-jev/SUMMARY.md`(§2 역링크만).

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(concept-digest) 완료: <한 줄>" \
  --body "보강한 노트 / 새 노트 / 역링크 수" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(concept-digest) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
