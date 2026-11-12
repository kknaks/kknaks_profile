# [planner] 검수 WARN 3건 문구만 수정

대상 = 같은 spec 워크트리 products/day/60-release/app-store-preparation.md + profile work/prod-deploy-re1/mobile-description-final.txt + mobile-paperwork-report.md만. 상세 지적은 같은 profile work/prod-deploy-re1/mobile-paperwork-review.md. 다른 코드/문서/API/커밋/push/배포 변경 금지. 새 조사 금지.

정확히 세 가지:
1. 공개 privacy의 'DAY는 비밀번호를 저장하지 않습니다'를 '로그인할 때 입력한 직원 비밀번호는 DAY에 저장하지 않습니다'로 좁힘. 근거 표와 결과 보고의 같은 문구도 일치시킴.
2. 앱설명(§5-2와 별도txt)에서 'DAY는 새 진료기록을 만드는 앱이나 환자용 앱이 아닙니다. ' 한 문장만 제거, 뒤 직원 계정/권한 문장 유지. length/sha256 앞8자를 두 곳과 보고서에 갱신. 개인정보처리안내의 새진료기록작성없다는 사실문장은 유지.
3. §5-3 심사노트는 지금복사할 문안과 '데모 자격 입력·실물검증 뒤에만 붙일 문단'을 각각별도블록으로 분리. 현재 복사할 블록에는 '데모계정입력했습니다/성공합니다' 같은 미확인 완료형을 넣지 않음. 두번째 조건부블록은 이름에 조건을명확히달기. 데모자격칸은 사용자직접입력 그대로.

완료 검증: 새 설명 원천블록=txt 동일, 새로운length/hash, 개인심사연락처/데모값혼입0 유지, lint본파일오류0. 기존 reviewer WARN3를 반영했다고 원래리포트에 짧게추가. 3문구수정 이상 확장하지 말고 바로완료보고. 현재dispatch worker_done --outcome succeeded 및 코디terminal알림2채널. 코디 term_2b709186-d9f1-4811-8538-95544d6d21b8.
