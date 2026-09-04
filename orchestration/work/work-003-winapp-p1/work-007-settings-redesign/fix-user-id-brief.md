# [winapp] 빠른 수정 — 본인 유저 식별자 표시 (닉네임 없으면 계정 이메일)

너는 **mykakao `winapp` 워커**다. 같은 워크트리 `work-003-winapp-p1`. 커밋 금지(코디).

## 배경
사용자 지적: "닉네임 말고 **유저가 누구인지 식별은 되잖아**, 그걸 넣어라." 맞다 — Profile.nickname 이 비어 me=null 이지만, **UserAccounts 레지스트리에 로그인 계정(이메일)이 있다.** 지금은 "-"/"(이름 없음)" 만 떠서 누군지 안 보인다.

## 고칠 것
- 본인 식별자 해석 우선순위: **① TalkUserDB 닉네임(있으면) → ② 계정 이메일 → ③ "(이름 없음)"**.
- **계정 이메일 소스**: `HKCU\Software\Kakao\KakaoTalk\UserAccounts\<이메일>` — 서브키 이름이 로그인 이메일이다. (또는 로그인 계정 폴더와 연결된 UserAccounts 항목.) 이 이메일을 읽어 반환.
- `/api/state.me` 와 **트레이 "로그인 유저 :"** 에 이 식별자를 표시. state.rs 의 my_profile/me 해석부에 fallback 추가.
- 로그아웃 시엔 "-" (해당 없음).

## 안전 (불변)
- 이메일은 **본인 기기·본인 화면 표시용** — 로그·리포트·커밋에는 남기지 마라(값 마스킹/비노출). UI/트레이 표시에만.
- 레지스트리 **읽기만**. 카톡 무변조. SAC 미변경. 새 crate 금지. `win_app/` 밖 금지.

## 검증
```
cargo build --release(SAC 통과) + cargo test. 실기동: /api/state.me 가 null 대신 계정 이메일/식별자 반환하는지(값은 마스킹 로그 말고, 존재/형태만 확인). 트레이 "로그인 유저"에 뜨는지 육안(사용자). 검증 1회.
```

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "유저 식별자 fallback 완료: <한 줄>" --body "소스/우선순위/me 반환 형태/트레이 반영/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 유저 식별자 fallback 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
