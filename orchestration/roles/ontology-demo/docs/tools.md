# @ontology-docs — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: 워크트리에서 `git branch --show-current` 확인 →
  `para/projects/project.md` → `templates/projects/` → 담당 제품 디렉토리 파악

## 탐색 경로 (레포 루트 기준)
```
para/projects/summer-star/ontology-demo/   # 담당 — 여기만 쓴다
para/projects/project.md                   # 문서 규칙 SoT
templates/projects/                        # 단계별 양식
para/resources/note/ontology/              # 기록 01~09 — 사실의 SoT (read-only)
para/projects/summer-star/kknaks-dev/      # 모범 문서 (read-only)
```

## 참조 전용 (수정 금지)
```
app/ontology-agent/                        # 백엔드 스캐폴드 — 현황 파악용
app/front/                                 # 프론트 — 현황 파악용
<브리프 §1 의 원천 절대경로>                 # reference/ontology_demo — read-only, 복사 금지
```

## 금지 사항
- `para/projects/summer-star/ontology-demo/` 밖 수정 금지 (다른 제품 문서·note·app·orchestration)
- 원천 데이터·PII 복사 금지
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다
