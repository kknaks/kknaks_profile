# [writer] strong-hajin-attach-read 회고를 개념으로 소화한다

너는 **strong-hajin `writer` 워커**다. **맥락이 없다** — 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/orchestration/roles/strong-hajin/planner/role.md`
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/templates/areas/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/para/projects/summer-star/strong-hajin/log/2026-10-15-strong-hajin-attach-read.md` **§2 「적용한 기술·개념」**(§3 막혔던 것도 소재)
- 조사 리포트(근거) `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진/orchestration/work/_archive/strong-hajin/strong-hajin-attach-read/research-attach-read-report.md` (§2 · §5 · §7)
- 선례 커밋: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진 show --stat 6942b46` (notify 회고 소화 — 신규 일곱 · 보강 넷)

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진` (브랜치 `kknaksss/스트롱하진`)

## 할 일
회고 §2 · §3 의 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep — pdf · ocr · 텍스트 추출 · 파싱 · 문서 처리 등) 기존 노트가 있으면 **보강**(`up:` 에 출처 · 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄, 번호는 현재 마지막 다음). 후보(판단은 네가 — 근거 보고):
1. **PDF 텍스트 층 vs 윤곽선 글자** — 화면엔 글자인데 추출 0자. 쪽별 `/Font` · 텍스트 연산자(BT/Tj/TJ) · Image XObject(최상위 · Form 재귀 · 인라인)로 래스터 · 윤곽선 · 추출기 문제를 가른다. HTML → macOS Quartz PDF 가 글자를 윤곽선으로 만든 실례
2. **추출 실패 사유를 판정 근거로 가르기** — 텍스트 0자에서 이미지 유무로 `needs_ocr` / `empty` 를 가르는데 판정이 얕으면(최상위만 · 예외를 False 로 삼킴) 엉뚱한 사유가 붙는다. 사유 문구가 판정 범위보다 넓게 말하는 문제(「스캔 이미지 PDF 또는 빈 파일」) · 판정한 상태가 저장 단계에서 뭉개지는 문제(`needs_ocr` → `failed`)
3. (§3 소재) 화면 증상 조사는 원본 파일 실측이 먼저 · 실패 배지가 「업로드 실패」로 읽히는 표시 문제 — 개념감이 되는지 판단, 아니면 건너뛰고 이유 보고
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 · §3 역링크만)
- 사람 실명·메일·파일 실명(고객사명 포함) 금지(공개 레포) — 실례는 「인터뷰 PDF(3.1MB · 14쪽)」 정도로

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 역링크
- 커밋·push 금지 (pre-commit 개념↔맵 검사가 있으니 맵 줄 누락 없게)

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_0ddce177-d531-4467-b612-30e3928f8d3d --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: attach-read 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_0ddce177-d531-4467-b612-30e3928f8d3d --text "[worker_done] writer 완료 — attach-read 개념 소화." --enter
```
