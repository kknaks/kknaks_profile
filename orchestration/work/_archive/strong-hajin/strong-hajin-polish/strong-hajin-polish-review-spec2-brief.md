# [reviewer] WORK-008 SPEC 재검수 (fix1 후) — planner 리뷰 모드

너는 앞서 이 SPEC 반영을 검수한 **strong-hajin `reviewer` 워커**다. 역할·규칙은 앞 브리프(`orchestration/work/strong-hajin-polish/strong-hajin-polish-review-spec-brief.md`)와 같다. **read-only**.

## 1. 대상
문서 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화` 의 미커밋 diff 전체 —
`20-spec/`(SPEC-001·002·003·005·007·README) + `00-baseline/`·`10-decision/`(포인터만 바뀌었다고 보고됨). `30-work/README.md` 는 대상 아님.

## 2. 볼 것
1. 앞 리포트 `review-spec-report.md` 의 **FAIL 4 · WARN 8 이 각각 닫혔나** — 항목별 닫힘/미닫힘 + 파일:줄
2. 코디가 닫은 OQ 넷(writer fix1 브리프 §2: `strong-hajin-polish-write-fix1-brief.md`)과 OQ-O 보충 답 「(a) AX 초안 줄은 그 칩을 켰을 때만, 전체·다른 칩엔 안 섞임」이 **그대로** 반영됐나. 더하거나 바꾼 것이 있으면 FAIL
3. fix1 이 **새로 만든 충돌** — 같은 개념의 다른 서술을 다시 grep 으로 전부(칩·간트 축·참조자·담당자 변경 사유·confirm draft·기한)
4. `00-baseline/`·`10-decision/` diff 가 **포인터 숫자만** 바뀌었나. 본문 의미 변경이 있으면 FAIL. 바뀐 포인터 몇 개를 표본으로 대상 줄이 맞는지 확인
5. 실명·메일 0

## 3. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-spec2-report.md` 하나만

## 4. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 SPEC 재검수 <PASS|WARN|FAIL>" \
  --body "판정 / 앞 FAIL·WARN 닫힘표 / 새 지적(파일:줄) / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — SPEC 재검수 <판정>. 리포트 review-spec2-report.md" --enter
```
