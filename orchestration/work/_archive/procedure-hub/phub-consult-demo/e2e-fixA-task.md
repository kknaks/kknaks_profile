# [app] 로컬 테스트 고침 A — 얼굴 점 · 진료항목 목록 (사용자 승인 11-22 「a 만 하자」)

너는 WP-0 ~ WP-6 을 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 스펙 `$W/SPEC-010-consult-myeongdong.md` 0.2.8(이 문서가 앞선다 — 다른 곳은 스펙 워커가 따로 옮김). 커밋 0 · 서브에이전트 0 · **18222 손대지 마라**(사용자가 쓰는 중 · 코디가 재기동) · 빈 포트로 확인 · 시험은 관련만. **아래 A 1 ~ 7 만** — 효과 · 부작용 · 침샘 계층 · 장바구니 문구 · 묶음 가격은 하지 마라(다음 단계).

## 사용자가 본 문제(18222 실물 · 「팔자주름 개선하고 싶어」)
목록 23 = 써마지 · 울쎄라 · 슈링크 · 소프웨이브 · 볼뉴머 · 리쥬란(필러 · 보톡스 없음) · 얼굴 점 = 가운데 「얼굴」 대표점 하나 + 「• 전신」 · 팔자주름 자리 점 없음 · 점 누르면 다른 점이 사라짐.

## 정한 동작(사용자 11-22)
1. **점 = 대화에서 나온 부위.** 턴마다 이해 결과의 부위(말한 부위)와 고민의 부위(concern_site — 팔자주름 고민 → SITE-046)를 지금 주제의 점으로 **쌓는다**(주제 저장 · 되살림 때 같이). 얼굴 부위는 얼굴 점 · 몸 부위는 그림 아래 목록. **진료항목 부위를 모아 점을 찍던 방식은 없앤다.**
2. **진료항목 ↔ 점은 계산한다(하드코딩 금지).** 진료항목의 매핑 부위(`hub.site_codes`) = 「할 수 있는 범위」. 범위가 점 부위를 **품으면**(같음 · 조상 — 얼굴 ⊃ 팔자주름 · 전신 ⊃ 몸 부위) 그 진료항목은 그 점에 속한다. 얼굴 전체 시술은 말한 얼굴 점 모두에 속한다(「그 부위 집중」). 같은 진료항목이 대화에 따라 다른 점에 붙는다.
3. **점 클릭:** 그 점에 속하는 진료항목만 목록에 남긴다 · **다른 점은 그대로**(누른 점만 강조) · 다른 점 누르면 그 부위로 · 같은 점 다시 누르면 전체 목록. 화면 동작만(대화 조건 · 주제 · 장부 턴 안 바뀜).
4. **고민 → 목록:** 고민이 붙은 케이스(「케이스 직접」)에 더해, **그 케이스와 같은 시술이고 매핑 부위가 그 케이스 부위를 품는** 진료항목도 넣는다 — 팔자주름 → HA 필러 × 팔자주름(CAS-1008) → 명동점 얼굴필러(CAS-1046 · 얼굴) 6 · 보톡스 × 팔자주름(CAS-093) → 보톡스 얼굴 범위 진료항목 등. 실물로 팔자주름 · 미간 · 턱 셋 셈을 리포트에(전 → 후 · 엉뚱 0 확인).
5. **카드 「시술설명」:** 그 진료항목이 속한 점(2 의 계산)에 강조 링(시안 drawDots 꼴).
6. **다음 턴:** 새 부위 · 고민 점을 더하고 점 선택은 푼다.
7. **좌표 데이터:** 매핑 JSON v3 `sites` 에 팔자주름(SITE-046) 등이 없다(진료항목 부위 + 조상만 담음). `$P/reference/2026-11-19-myeongdong-kos/build_mapping_json_v3.py`(P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇) 를 고쳐 **얼굴 좌표표 부위 전부(앱 face_coords.py · 대표점 7 포함 · 기존 좌표 그대로) + silver concern_site 의 얼굴 부위**를 sites 에 넣어 두 경로(`/Users/kknaks/git/clinic_chat/data/kos/` · `$A/data/kos/`) 다시 만듦 · items · products 바이트 같음 · 새 sha 리포트(코디가 18222 재기동 때 씀).

## 완료
시험(점 = 대화 부위 · 품음 계산 · 클릭 거르기에 다른 점 남음 · 고민 → 같은 시술 범위 진료항목 · 다음 턴 쌓임) · 실물 빈 포트 대화 「팔자주름 개선하고 싶어」 → 「미간도 신경 쓰여」 → 「턱은?」 스크린숏 `$W/e2e-shots/fixA-*.png`(점 셋 · 팔자주름 클릭 · 미간 클릭) · 리포트 `$W/e2e-fixA-report.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 테스트 고침 A" --body "점 / 목록 / sha / 스크린숏"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app 테스트 고침 A 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] app: <질문>" --enter`
