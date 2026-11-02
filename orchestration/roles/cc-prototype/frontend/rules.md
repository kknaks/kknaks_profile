# @cc-prototype-frontend — 규칙

## 기능 독립 (DEC-001 D-03)
- 기능 폴더 밖의 코드를 import 하지 않는다. 의존성(`package.json`·lock)은 `<기능>/front/` 안에 둔다.

## Next.js
- TypeScript strict. back 호출은 한 모듈(`lib/api.ts`)에서만 — 컴포넌트에서 직접 `fetch` 금지.
- back 주소는 env(`NEXT_PUBLIC_API_BASE_URL` 등)로만. 하드코딩 금지.
- 시안이 있으면 시안이 정본. 없는 자리는 리포트에 기록하고 임의로 꾸미지 않는다.

## 안전
- 사용자 포트·프로세스를 건드리지 않는다. 기능의 SPEC 이 정한 포트만 쓴다.

## 스코프
- allowed_paths 밖 수정 금지. 커밋·push·PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일·화면 목록
## 검증 — 명령과 결과 (tsc · lint · build)
## 계약 대조 — SPEC 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
