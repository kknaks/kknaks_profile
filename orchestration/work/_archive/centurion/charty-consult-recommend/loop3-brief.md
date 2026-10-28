# frontend 3루프 브리프 — 카드 다듬기 (사용자 실물 피드백 3건)

범위·금지 사항은 `fe-brief.md` §3 그대로(커밋 금지 · **3417 서버 끄기/재시작 금지** · 얼굴 크롭 파일 저장 금지). 배치·2루프 결과는 그대로 두고 아래만 고친다. 근거: `_RESUME.md` §3 「3루프」 V-1~V-3.

## 고칠 것
1. **V-1** 카드 설명 아래 「Hub 원문」(`area-summary-source`) 문구 삭제. 출처는 모달 아래 출처 줄에만 남긴다. 금지어 검사 제외(area-summary)는 그대로
2. **V-2** [자세히] 버튼을 선택 시술 제목(예: 「보톡스」) **같은 줄 오른쪽**으로 옮긴다. 아래 출처/버튼 줄은 없애고 그 공간만큼 설명 줄 수를 늘려도 된다(카드 안에서 잘리지 않게)
3. **V-3** 부위 확대 사진이 피부색 판으로만 보인다(64px · 반경 120 텍스처px)
   - 잘라 오는 범위를 넓혀 **어느 부위인지 알아보이게**(눈가면 눈·눈썹, 팔자면 코 옆~입가, 이마/미간이면 눈썹 사이~이마 윤곽이 들어오게). 반경은 부위별로 달라도 된다 — 값과 이유를 리포트에
   - 썸네일 크기도 키운다(카드 머리 안에서 이름·등급·점수와 같이 들어가는 한 최대로, 대략 88~100px). 카드 안 다른 요소 잘림 없음 유지
   - **흐린(dim) 카드에서도 사진은 덜 흐리게**(예: 사진만 opacity 0.7 이상)
   - 스크린샷 `screens/loop3-crops.png` 로 6개가 각각 알아볼 만한지 확인

## 시험 · 보고
- 바뀐 testid·단언만 고친다. 관련 시험(`e2e/areas.spec.ts`) + `npm run lint` · `npm run test`. 전체 e2e 는 끝에 1회(3417 재사용). build 금지
- 스크린샷: `loop3-natural.png` · `loop3-crops.png`
- `fe-report.md` 에 「3루프」 절
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[frontend 3루프 완료] orchestration/work/charty-consult-recommend/fe-report.md" --enter
```
