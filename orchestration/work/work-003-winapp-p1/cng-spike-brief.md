# [winapp] spike — 채팅사진 .cng 복호 가능성 실증 (핵심 리스크 선검증)

너는 **mykakao `winapp` 워커**다. 같은 워크트리. **탐색(spike) — PR·커밋 없음.** 사용자 승인 완료.

## 목표
채팅방 사진 `.cng` 가 실제 이미지(JPEG/PNG/WEBP)로 **복호 가능한지 판정**. 가능하면 방식·난이도, 불가면 대안. 억지 금지 — 못 되면 근거+필요조건이 결과.

## 근거 (직전 사진 spike)
- 채팅사진 원본 URL(talk.kakaocdn.net)=GET 410 Gone(만료) → URL 불가, **로컬 .cng 가 유일 소스**.
- .cng: 매직 없음·엔트로피~8=암호화. 앞16B=IV 추정.
- 매핑 확보(둘 다 memory harvest 키로 복호): `talkmedia.edb` tokenInfo(token→filePath,fileSize,checkSum[SHA1]) + chatMsgTokenJunction(logId→token). (url_image_v2 는 URL 200 이라 별개·쉬움.)

## 조사 스텝
1. 알려진 채팅사진 1개: logId→token→tokenInfo.filePath 로 대응 .cng 특정(mci_v2 등).
2. **AES-128/256-CBC(앞16B IV)** 시도. 키 후보 순서: (a) 이미 harvest 한 메모리 후보(계정/캐시키 우선), (b) checkSum/token 파생, (c) 안되면 KakaoTalk 미디어 복호 루틴 정적 RE(passive 덤프).
3. **성공 판정 = 복호 선두 FFD8(JPEG)/8950(PNG)/RIFF(WEBP) + SHA1==checkSum.** (정답지 = 매직 + SHA1.)
4. 되면 이미지 1장을 **다운로드 폴더 저장까지 PoC**(파일 저장 위치만 보고, 이미지 내용 비노출).

## 판정
- (A) 복호 성공 — 방식(키 출처·AES 모드·IV)·난이도·다음스텝(구현).
- (B) 부분 — 어디까지, 뭐가 막나.
- (C) 막힘 — 왜(키 못 찾음/RE 필요), 필요조건.

## 안전 (불변)
- 원본 읽기만·카톡 무변조·SAC 미변경·키 RAM only·복호 임시본 RAII.
- **이미지·URL·토큰·키·checkSum 원값을 로그·리포트·커밋·출력에 남기지 마라** — 매직바이트·SHA1 일치 여부·개수·지문만.
- 새 crate 금지(부득이하면 보고). 조사 test 는 사후 삭제(프로덕션/커밋 변경 0). **anti-debug 주의**(지속 디버거 attach 시 카톡 크래시 이력 — passive 우선, WinDbg 류 지속 BP 금지).
- `win_app/` 밖·문서 SoT 수정 금지.

## 검증
탐색이라 통상 검증 없음. 재현 명령은 리포트에, 값은 마스킹. cargo 쓰면 build 만.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject ".cng 복호 spike: <판정 A/B/C 한 줄>" --body "특정/키출처/AES모드·IV/매직+SHA1 성공여부/난이도/다음스텝"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] .cng 복호 spike <판정> — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
