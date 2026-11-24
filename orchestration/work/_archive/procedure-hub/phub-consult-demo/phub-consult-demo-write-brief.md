# [writer] SPEC-009 — 허브 보강(명동점 KOS 레인): 근거 원천 확장 · 부위 3단 · 적용 부위 범위 · 제품 · 시술 추가 · 반복 절차

너는 **procedure-hub `writer` 워커**다. **앞 판 맥락이 없다** — 아래만으로 일한다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/roles/procedure-hub/writer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` (코디와 공유 · 문서 1 개만 쓴다)

## 1. SSOT — 먼저 읽을 것

- **결정**: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/_RESUME.md` §2 — 11-19 행 전부(매핑 단위 = KOS 진료항목 · 허브 보강한다 · 부위 3단 · 부위 범위 · 원장 근거 없는 추가 부위 15 넣음 · 거미스마일 = 잇몸 · 세라핏 = PRC-123 + PRD-729 · 「바디/페이스」 = 메뉴 말 등). **여기 없는 정책은 만들지 마라 — 열린 것으로 둔다.**
- **명동점 기준 표**: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/reference/2026-11-19-myeongdong-kos/myeongdong-kos-medical-services-20261119.csv`(324 · 58 칸 · KOS 원문 + 부위 3단 · 부위 범위 · 구성 약물+용량) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/research-kos-item-decompose.md` · `research-site-tree.md` · `research-kos-site-3tier.md` · `research-site-evidence.md` · `research-kos-item-map.md`(진료항목 → 허브 매핑 초안 · 허브 없음 목록) · 부위 3단 배치안 `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/reference/2026-11-19-myeongdong-kos/hub-site-tree-draft.csv`.
- **허브 데이터 계약 · 형식 본보기**: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-003-hub-gold-db.md`(DB 76 표 · 적재 · 해시 · integrity · §11 stg) · `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-007-image-data.md`(silver 표를 더한 판의 쓰는 법 — 이 꼴을 따라라) · `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-001-hub-gold-mcp.md`(도구 · `concern_candidates` 부위 묶음) · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/data/medallion/README.md`(「값을 손으로 고치지 않는다 — 원천에서 다시 지어 통째로」 · 해시).
- **silver 원천 작업 공간(읽기만)**: `/Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/` — `silver/`(59 CSV) · `gold/gold-build.py` · `gold-check.py` · `silver-supplement.py` · `README.md` · **`notes/external-fill-notes.md`(외부 출처를 silver 에 넣은 앞 사례 — 근거 꼴 `drafts/external-research/external-research.csv:L<줄>`)** · `notes/glossary.md`. 허브 기준: 시술 = 재료 · 에너지 + 대상 조직 + 원리(부위는 시술 아님 — phub-ledger-redesign `_RESUME.md` 11-10).
- 허브 코드(읽기만): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/` 적재기 `scripts/load_medallion.py` · silver 표 계약 목록 · integrity 검사(gold 행마다 근거 · `source_ref` 의 ref).

## 2. 배경

목표 = 명동점 전용 상담 실장 봇. 명동점 KOS 진료항목 324 를 허브와 잇는 과정에서 허브에 없는 것이 드러났다 — 부위 체계가 평평함(89 중 68 최상위) · 시술 · 제품의 **적용 부위 범위**(얼굴 전체 / 얼굴 · 몸 가능 …)가 허브에 없음 · 명동점 약물 · 기기 46 종 · 시술 17 이 허브에 없음. 사용자: 「허브를 보강해야 한다 · 스펙부터 실버 수정 · 골드 빌드까지 · **앞으로도 명동점 매핑하면서 제품이 추가될 것**」 → 이번 한 번이 아니라 **반복되는 보강 레인**이어야 한다.

## 3. 계약

이 SPEC 이 정할 범위(이번 작업은 **gold 빌드까지** · stg 반입은 이 SPEC 에 절차만 · 실행은 다음 단계):
- **S1 근거 원천 확장** — 원장 외 근거 꼴(KOS 명동점 진료항목 · 사용자 확인 · 외부 출처)을 `source_ref` 에 어떻게 적나. 앞 사례(external-fill)를 출발점으로. 원장 근거와 구분되는 칸(근거 종류) · integrity 「근거 없는 gold 행 0」 이 그대로 지켜지는 꼴. **공개 레포**(허브 레포 · 프로필) — 가격 · KOS id · 개인정보는 근거에 넣지 않는다(진료항목 코드 · 이름은 사용자 확인 필요 → 열린 것).
- **S2 부위 3단** — `site.csv` 의 `parent_code` 재배치(1단 얼굴 / 몸 · 2단 · 3단) · 새 부위 · 다른 이름(`alias.csv`) · 묶음 부위 · 몸 > 기타. 입력 = `hub-site-tree-draft.csv` + `_RESUME` 11-19 확정 변경. **허브 동작 영향**(위 부위를 따라 묶는 도구 — `concern_candidates` · 고민 부위 물려받기 · `concern_site`)을 절로 — 무엇이 바뀌나 · 전후 비교 시험.
- **S3 시술 · 제품 적용 부위 범위** — 담을 자리가 지금 없다. 새 silver 표(또는 칸) 꼴 · 값 7 종(특정 부위 / 얼굴 전체 / 얼굴 일부 / 몸 / 얼굴 · 몸 가능 / 어디든 / 부위 개념 없음) · 대상(시술 · 제품 · 케이스 중 어디) · gold · DB · 도구로 어디까지 가나(이번 = silver + gold 까지 · DB 표 추가가 필요하면 마이그레이션은 열린 것으로 표시). silver 표 계약 59 → n 이 적재기에 주는 영향.
- **S4 제품 · 시술 추가** — 명동점 대조에서 나온 허브 없음(제품 46 종 · 시술 17 · `research-kos-item-map.md`) 을 silver 행으로 넣는 꼴: 필수 칸 · 연결 표(제품 ↔ 시술 · 계열 · 케이스 · 재료) · 시술 기준(재료 + 조직 + 원리)에 안 맞는 것(마취 · 수액 · 팩 · 회원권 · 희석액 하프셀라인)은 넣지 않거나 따로 · 「확인 필요」 처리. **어느 항목을 넣을지 확정은 보강 목록 검수(사용자) 몫** — SPEC 은 꼴과 판정 규칙.
- **S5 반복 절차(레인)** — 새 KOS 스냅샷 → 진료항목 표 → 허브 대조 → 보강 목록(사람 검수) → silver patch → silver 검사 → gold-build → gold-check → 허브 레포 `data/medallion/` 통째 교체 · 해시 → 로컬 적재 · 시험 → (stg 반입). 각 단계의 입력 · 산출 · 스크립트 자리 · 사람 게이트. 앞으로 다른 병원이 붙을 자리(병원 무관 원칙과의 관계 — 10-30 「허브는 병원 데이터로 안 바뀐다」 를 이번에 넘어선 범위를 정확히).
- **S6 영향 · 되돌리기** — 해시가 바뀌면 상담 앱 열린 대화 종료(`build_changed`) · stg 반입은 다음 단계 · 되돌리기.
- 열린 것은 열린 것으로(번호 매겨 「정할 것」).

## 4. 먼저 볼 자리
- `/Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/gold/gold-build.py` · `gold-check.py` · `silver-supplement.py` 의 입출력 · 검사 목록(파일:줄).
- `/Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/silver/site.csv` · `alias.csv` · `source_ref.csv` · `product.csv` · `procedure.csv` · `product_procedure.csv` · `case_product.csv` 머리 칸.
- `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/scripts/load_medallion.py` · gold 모듈의 silver 표 목록 · integrity.

## 5. allowed_paths — 이 밖은 건드리지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/SPEC-009-hub-clinic-supplement.md` 1 개만 생성. 그 외 생성 · 수정 0.

## 6. 할 일
SPEC-007 꼴로 SPEC-009 0.1.0 을 쓴다: 머리(판 · 근거 결정 목록) → §0 범위 · 범위 밖 → §1 현재 사실(파일:줄 · 수) → S1 ~ S6 각 절(규칙 · 꼴 · 예 · 시험 기준) → 정할 것(번호) → 다음 단계(WORK 로 넘길 것). 모든 요구는 _RESUME 결정 · 리포트 · 코드(파일:줄) 중 하나를 가리킨다.

## 7. 범위 제약 — 하지 말 것
- silver · gold · 허브 레포 · 진료항목 CSV 수정 0. 커밋 0. 서브에이전트 0.
- 결정하지 않은 정책 만들지 마라(열린 것으로). 회사 원장 본문 길게 옮기지 마라. 가격 · KOS id · 키 0.

## 8. 검증

```
모든 결정·요구가 _RESUME §2 결정 · 조사 리포트 · 코드(파일:줄) 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. public — 키 · 토큰 · 실명 0(grep)
```

- `git -C /Users/kknaks/orca/workspaces/kknaks_profile/상담봇 status --short` 로 변경이 SPEC-009 하나뿐인지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_103f2021-ea90-40f7-bdcc-d1ab5545bfb8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
