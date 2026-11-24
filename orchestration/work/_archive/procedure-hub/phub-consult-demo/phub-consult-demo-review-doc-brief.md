# [reviewer_doc] SPEC-009 0.1.0 검수 — 허브 보강(명동점 레인)

너는 **procedure-hub 리뷰어(문서)** 다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/roles/procedure-hub/reviewer/role.md`(+ 같은 폴더 `rules.md` · `workflow.md`). **read-only** — 리포트 1 개만 쓴다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇`

## 1. 검수 대상 · 대조 원천
- 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/SPEC-009-hub-clinic-supplement.md`(0.1.0)
- 결정 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/_RESUME.md` §2 의 2026-11-19 행 전부 · 작성 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/phub-consult-demo-write-brief.md`(S1 ~ S6 범위)
- 사실 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/research-*.md`(kos · kos-fields · kos-item-map · kos-item-decompose · site-evidence · site-tree · kos-site-3tier) · `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/reference/2026-11-19-myeongdong-kos/`(진료항목 CSV · hub-site-tree-draft.csv) · silver 원천 `/Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/`(silver · gold-build.py · gold-check.py · silver-supplement.py · notes/external-fill-notes.md) · 허브 레포 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/data/medallion/README.md` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/scripts/load_medallion.py` · 앞 SPEC `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-003-hub-gold-db.md` · `SPEC-007-image-data.md` · `SPEC-001-hub-gold-mcp.md`
- 로컬 PG(SELECT 만 · `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 값 출력 금지)로 수 · 칸 대조 가능.

## 2. 볼 것
1. **근거 없는 정책 0** — 모든 규칙이 _RESUME 결정 · 리포트 · 코드(파일:줄) 중 하나를 가리키나. 사용자가 정하지 않은 것을 정한 문장(특히 S1 근거 꼴 · S3 새 표 꼴 · S4 판정 규칙 · S5 사람 게이트)을 찾아라 — 「정할 것」 으로 가야 할 것.
2. **사실 대조** — §1 현재 사실 · 부록 B 재셈의 수(부위 89 · 최상위 68 · 이동 48 · 추가 24 · 진료항목 324 · 부위 범위 분포 · 허브 없음 제품 46 · 시술 17 · silver 표 59 등)를 실물로 다시 센다. 파일:줄 인용이 실제와 맞나.
3. **결정 반영 누락** — 11-19 결정(부위 3단 세부 · 머리 · 귀 = 얼굴 2단 · 팔자 → 볼 · 마리오네트 → 입 · 관절 → 몸 > 기타 · 원장 근거 없는 추가 15 인정 · 거미스마일 = 잇몸 · 부위 범위 7 값 · 다한증 = 손 · 혈액 줄기세포 = 얼굴 전체 · 세라핏 = PRC-123 + PRD-729 · 하프셀라인 = 희석액 · 「보톡스」 = 국산 톡신 이름표 · 「앨러간」 = 회사 · 「수입」 = 원산지 · 반복 레인 · 이번 범위 = gold 빌드까지)이 빠지거나 바뀐 곳.
4. **구현 가능성** — S1 근거 꼴이 integrity(근거 없는 gold 행 0) · gold-build · 적재기 silver 계약(59 표 · 계약 밖 CSV 거부)과 실제로 맞물리나(코드 파일:줄). S3 새 표가 적재기 · DB 마이그레이션에 주는 영향이 빠짐없이 적혔나. S2 의 허브 동작 영향(`concern_candidates` · 부위 물려받기 · `concern_site`)과 전후 비교 시험이 충분한가.
5. **공개 레포** — 키 · 토큰 · 실명 · 가격 · KOS id 0(grep). 진료항목 코드 · 이름의 공개 여부가 「정할 것」 에 있나.
6. 「사용자가 실물에서 만날 자리」 — 상담 앱 · 허브 응답에서 사람이 보게 될 변화.

## 5. allowed_paths
- 리포트 1 개: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/review-spec-009.md` — 판정 FAIL / WARN / PASS + 지적마다 SPEC 절:줄 · 근거(파일:줄 · 실측 수). 그 외 생성 · 수정 0.

## 7. 하지 말 것
SPEC 수정 0 · 커밋 0 · 서브에이전트 0 · 허브 · silver 수정 0.

## 8. 검증

```
DEC · SPEC · WORK 를 _RESUME 결정 · 조사 리포트 · 코드에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_bfbdb948-25d8-4ab3-81af-8c0505638f4c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
