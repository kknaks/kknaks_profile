# @agency-settlement-frontend — 도구 및 구조

## 작업 위치
- 워크트리·base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → 기능의 SPEC·WORK(브리프 §1 절대경로) 통독.

## 명령
- `cd front && npm install && npx tsc --noEmit && npm run lint && npm run build`
- 로컬 기동은 기능의 SPEC 이 정한 포트로.

## 금지
- allowed_paths 밖 수정 · 커밋·push·PR · 사용자 포트/프로세스 종료.
