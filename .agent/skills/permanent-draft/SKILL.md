---
name: permanent-draft
description: YouTube 링크(또는 문서/텍스트)를 받아 자막·핵심을 추출하고, 기존 지식그래프에서 진짜 연결 후보를 찾아 **풍부한 permanent 영구노트 초안**을 만든다. 초안 + `[[]]`/`up:` 연결을 제시하고, 사용자가 승인하면 `permanent/`에 저장하고 그래프(노드+lineage)를 검증한다. 사용자가 직접 쓰지 않고 AI가 초안을 잡되, "내 결론" 자리는 작성자 TODO로 남긴다(C 모드). 트리거: "이 유튜브 영구노트 초안 만들어", "permanent 정제", "이거 기반으로 초안", "지식노트 만들어줘".
allowed_tools: [Read, Write, Bash, Grep, Glob]
---

# Permanent Draft — 유튜브/자료 → 영구노트 초안 + 그래프 연결

YouTube 링크나 자료를 받아 **풍부한** permanent 영구노트 초안을 만들고, 기존 그래프에서 실제 연결을 찾아 `[[]]`/`up:`까지 잡아 제시한다. **승인 전엔 저장·커밋하지 않는다.**

> 핵심 철학(C 모드): AI가 초안을 80% 잡되, **"내 결론/판단" 자리는 작성자 TODO로 남긴다.** 그 자리를 사람이 채워야 죽은 지식이 안 된다. 그리고 **얇게 쓰지 마라** — 영상/자료의 알맹이를 충분히 캐고 연결을 충분히 찾아라.

## When to use

- 사용자가 YouTube 링크(또는 문서/긴 텍스트)를 주며 "영구노트 초안 만들어", "이거 기반으로 정제해줘", "permanent로 만들어줘"라고 할 때
- 떠오른 아이디어(inbox)를 자료와 엮어 permanent로 발전시킬 때

## Input

- 필수: YouTube 링크/ID **또는** 문서 경로/텍스트
- 선택: 이 자료를 엮을 **씨앗 명제/맥락** 한 줄 (사용자의 기존 생각 — 있으면 1순위 컨텍스트). 예: "AX 전환엔 정보 정합성이 필요"

## Flow

### 1. 자막·메타 추출 (YouTube인 경우)

서버 의존성(`youtube-transcript-api`, `yt-dlp`)이 `app/back/.venv`에 있다. **비동기 contents 파이프라인(youtube-content 스킬)을 쓰지 마라** — 그건 블로그 /contents 요약용이고 비동기·main 푸쉬다. 여기선 직접 즉석 추출한다:

```bash
cd app/back && .venv/bin/python -c "
vid='VIDEO_ID'
import yt_dlp
with yt_dlp.YoutubeDL({'quiet':True,'skip_download':True,'noplaylist':True}) as ydl:
    info=ydl.extract_info(f'https://www.youtube.com/watch?v={vid}', download=False)
print('TITLE:', info.get('title')); print('CHANNEL:', info.get('uploader'))
print('DESC:', (info.get('description') or '')[:600])
from youtube_transcript_api import YouTubeTranscriptApi
f=YouTubeTranscriptApi().fetch(vid, languages=['ko','en'])
print('TRANSCRIPT:', ' '.join(s.text for s in f))
"
```

문서/텍스트면 Read로 읽는다.

### 2. 알맹이 추출 (얇게 쓰지 마라)

- 자료에서 **substantive 주장 3~5개**를 뽑는다. 홍보/과장 톤은 걸러내고 **개념·메커니즘·반례**만.
- 사용자 언어로 재서술할 준비. 베끼지 않는다.

### 3. 연결 후보 검색 (진짜 이웃 vs 노이즈)

기존 그래프에서 실제로 닿는 노드를 찾는다. **키워드 노이즈와 진짜 개념 이웃을 구분**해서 보고:

```bash
# 개념 키워드로 reference/permanent/products 검색
grep -rilE "키워드1|키워드2|개념" reference/ permanent/ products/ | grep -vE "/_|README"
# 유력 후보는 Read 로 실제 내용 확인 (제목만 걸린 노이즈 거르기)
```

- **강한 이웃**(개념적으로 진짜 닿음) vs **노이즈**(키워드만 걸림)를 나눠 제시.
- 후보 stem이 실존하는지 확인(`[[]]`/`up:` 타겟은 enforcement L1 대상).

### 4. 풍부한 초안 작성

`permanent/{id}.md` 형태로 (저장은 5단계 승인 후). frontmatter: `type: permanent`, `id`(=파일 stem), `title`, `source`(자료 URL), `up:`(있으면).

본문 구조 가이드(얇게 X — 각 섹션 실질 채움):
- **핵심 명제** — 한 생각. 사용자 씨앗 명제가 있으면 그것을 자료로 날카롭게.
- **메커니즘/근거** — 자료의 substantive 주장들을 사용자 언어로. "왜 그런가/맥락" 포함.
- **기존 노트와의 대조** — 본문에 `[[연결-stem]]` 인용. 내 그래프/노트와 같은점·다른점.
- **풀리지 않은 긴장 (← 작성자 TODO)** — 자료가 던지는 질문 + "여기 내 결론"을 **빈 자리로 명시**. AI가 채우지 마라.

### 5. 승인 게이트 (★ 저장·커밋 안 함)

초안 + 연결 + **사용자가 정할 것**을 제시하고 멈춘다:
- 핵심 명제가 맞나
- `up:` 방향(이 생각이 그 노트를 *기반으로* 했나 = 화살표, 아니면 단순 `[[]]`)
- "긴장/결론" 단락(작성자만 채울 수 있음)

사용자가 "저장해/올려" 라고 해야 다음.

### 6. 저장 + 그래프 검증

```bash
# permanent/{id}.md 작성 (id == 파일 stem 필수 — validate_persona 강제)
# enforce ON 으로 로드해 노드+엣지 검증 (dead link/방향 위반이면 raise)
cd app/back && RUN_SCHEDULER=0 GRAPH_ENFORCE=1 .venv/bin/python -c "
from pathlib import Path; import sys; sys.path.insert(0,'.')
from service.persona_loader import load_persona
d=load_persona(Path('../../persona'))
nid='NOTE_ID'
print('노드:', [n for n in d['_graph']['nodes'] if n['id']==nid])
print('엣지:', [e for e in d['_graph']['edges'] if nid in (e['source'],e['target'])])
"
```

- 노드 생성 + `up:`→lineage 화살표 + 백링크 자동 도출 확인 후 사용자에게 보고.
- inbox에 원본 씨앗이 있었으면 "분류 완료 → 원본 폐기" 단계 안내(삭제는 사용자 확인 후).
- 커밋은 사용자 지시 시에만. push는 별도 지시.

## Rules

- **얇게 쓰지 마라.** 빈약한 초안 = 실패. 자료 알맹이 3~5개 + 진짜 연결 2개 이상.
- **"내 결론" 자리는 비워둔다.** 작성자 판단을 AI가 발명하지 않는다.
- **연결은 실존 stem만.** `[[]]`/`up:` 타겟이 없으면 enforcement에서 막힌다 — 검색으로 실존 확인.
- **승인 전 저장·커밋 금지.**
- **로컬 보기는 dev(`npm run dev`).** prod 빌드(`npm run build`/`next start`)는 `.env.production`(배포 백엔드)를 박으니 로컬 확인용으로 건드리지 마라.
- youtube-content 스킬(비동기 /contents)과 혼동 금지 — 이건 동기·즉석·permanent용.
