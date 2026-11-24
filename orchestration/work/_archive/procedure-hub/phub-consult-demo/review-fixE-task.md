# [reviewer · 읽기만] 테스트 고침 E 검수 (자동 검수 · 11-23)

너는 검수 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **리포트 1 개만 쓴다** · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라**(허브 18105 GET 만) · 실물은 빈 포트에 앱을 따로 띄워서(끝나면 끈다).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 18222 기동 env(같은 값으로 빈 포트): `CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images uv run python -m clinic_chat.consult --port <빈 포트>`

## 대상
발주 `$W/e2e-fixE-task.md`(사용자 결정 넷) · 리포트 `$W/e2e-fixE-report.md` · 스크린숏 `$W/e2e-shots/fixE-*.png` · 바뀐 코드(`git -C $A diff` · 이번 변경 위주).

## 볼 것
1. 넷이 사용자 결정대로인가 — 머리(말한 값만 · 겹침 0 · 제품 풀이 시술 숨김 · 지어낸 문구 0) / 주제 하나 머리 / 부위별 시술 찢기(고민은 그 부위 것만 · 「입꼬리에는 필러」 뒤 눈가 볼뉴머 주제 남음) / 큰 재료(원인 잰 값이 맞나 · 줄인 재료로 답 · 중단 0 · 줄여서 빠진 정보가 답을 틀리게 하지 않나).
2. **실물 직접:** 세 대화를 빈 포트에서 실제 이해 · 답 호출로 다시 돌려 리포트 표와 대조 — conv 03b8(「팔자주름에 대해서 고민이돼」 → 「미간에 주름도 고민이야」 → 「얼굴에 탄력이 좀 떨어지는거 같은데」 → 「그중에서 소프웨이브, 써마지, 울쎄라만 관심이 잇어」 → 「고주파 원리가 머야 ?」 → 「응 고주파에 대해서 전반적으로 설명해줘」) · ecc6(「요즘 피부 탄력이 저하 되서 고민이야」 → 「얼굴에」 → 「얼굴에」) · 73bd(「얼굴에 피부 탄력이 없어져서 걱정이야」 → 「아 주름이 눈가 입꼬리에 잇어」 → 「아 눈가는 볼뉴머 이ㅃ고리는 필러를 맞고 싶어」 → 「입꼬리에는 필러를 맞고 싶다니까」). 턴마다 주제 · 머리 글 · 목록 수 · 답 앞 2 줄.
3. **화면을 직접 본다:** 새 브라우저 프로필(캐시 없이)로 위 세 대화 마지막 화면 스크린숏 — 머리 · 점 · 목록 · 답 · 스피너 한 줄. 사람 눈으로 이상한 것(겹침 · 긴 머리 · 빈 칸 · 원문 값 노출 · 이상한 문장)을 적는다.
4. 앞 고침(넓히기 · 되돌리기 · 점 늘 다 · 점 필터 · 모달 한 줄 문장) 이 깨지지 않았나 — 관련 시험만.

## 산출
`$W/review-fixE.md`: 판정 PASS / FAIL · 지적(P0 / P1 / P2 · 근거 = 파일:줄 · 실측 · 스크린숏 경로 · 고칠 방향) · 실물 표 · 스크린숏 `$W/e2e-shots/review-fixE-*.png`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: 테스트 고침 E" --body "판정 / P0 · P1 · P2 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review 고침 E 완료 — <한 줄>. 상세는 인박스." --enter
```
