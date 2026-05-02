/* global React */
const { useState: useS, useEffect: useE, useRef: useR, useMemo: useM } = React;

/* =========================================================
   Notes — Obsidian-style graph view
   - default: full-width force graph of all notes
   - click node: graph collapses to left, body slides in right
   - same outer chrome as other pages (header + max-width)
   ========================================================= */

// Sample notes — placeholder data. Replace with API later.
const NOTES = [
  // AI / LLM cluster
  { id: 'rag-basics',         title: 'RAG 기본 구조',          tags: ['ai','rag','embedding'],   group: 'ai', date: '2026.04.10', links: ['bge-m3','vector-db','prompt-eng','llm-eval'] },
  { id: 'prompt-eng',         title: 'Prompt Engineering',     tags: ['ai','llm','prompt'],     group: 'ai', date: '2026.03.22', links: ['rag-basics','llm-eval'] },
  { id: 'llm-eval',           title: 'LLM 평가 방법론',         tags: ['ai','eval'],             group: 'ai', date: '2026.02.18', links: ['rag-basics','prompt-eng'] },
  { id: 'bge-m3',             title: 'BGE-M3 multilingual',    tags: ['ai','embedding'],        group: 'ai', date: '2026.01.05', links: ['rag-basics','vector-db'] },
  { id: 'vector-db',          title: 'Vector DB 비교',          tags: ['ai','vector-db'],        group: 'ai', date: '2026.01.30', links: ['rag-basics','bge-m3','db-index'] },

  // Python cluster
  { id: 'asyncio-deep',       title: 'asyncio 동작 원리',        tags: ['python','async'],        group: 'py', date: '2025.12.20', links: ['fastapi-deps','gil'] },
  { id: 'fastapi-deps',       title: 'FastAPI Depends 패턴',     tags: ['python','fastapi'],      group: 'py', date: '2025.11.14', links: ['asyncio-deep','pydantic-v2'] },
  { id: 'pydantic-v2',        title: 'Pydantic v2 마이그',       tags: ['python','pydantic'],     group: 'py', date: '2025.10.02', links: ['fastapi-deps'] },
  { id: 'gil',                title: 'GIL · 멀티프로세싱',        tags: ['python'],                group: 'py', date: '2025.09.18', links: ['asyncio-deep'] },

  // Infra cluster
  { id: 'docker-compose',     title: 'Docker Compose 패턴',      tags: ['infra','docker'],        group: 'infra', date: '2025.08.25', links: ['multistage','tailscale','caddy'] },
  { id: 'multistage',         title: 'Multi-stage build',       tags: ['infra','docker'],        group: 'infra', date: '2025.07.11', links: ['docker-compose'] },
  { id: 'tailscale',          title: 'Tailscale + 홈서버',        tags: ['infra','homelab'],       group: 'infra', date: '2025.06.30', links: ['caddy','docker-compose'] },
  { id: 'caddy',              title: 'Caddy 리버스 프록시',       tags: ['infra','caddy'],         group: 'infra', date: '2025.05.12', links: ['tailscale','docker-compose'] },
  { id: 'k8s-vs-compose',     title: 'k8s vs compose',          tags: ['infra'],                 group: 'infra', date: '2025.04.04', links: ['docker-compose'] },

  // CS cluster
  { id: 'tcp-ip',             title: 'TCP/IP 핸드셰이크',         tags: ['cs','network'],          group: 'cs', date: '2025.03.20', links: ['consistent-hash'] },
  { id: 'db-index',           title: 'B-tree vs Hash index',    tags: ['cs','database'],         group: 'cs', date: '2025.02.14', links: ['vector-db','consistent-hash'] },
  { id: 'consistent-hash',    title: 'Consistent Hashing',      tags: ['cs','system-design'],    group: 'cs', date: '2025.01.20', links: ['tcp-ip','db-index'] },

  // Daily / loose
  { id: 'daily-2026-04',      title: '2026-04 트러블슈팅',        tags: ['daily'],                 group: 'daily', date: '2026.04.28', links: ['fastapi-deps','tailscale'] },
  { id: 'daily-2026-03',      title: '2026-03 트러블슈팅',        tags: ['daily'],                 group: 'daily', date: '2026.03.31', links: ['rag-basics','docker-compose'] },
];

const GROUP_COLOR = {
  ai:    'var(--accent)',
  py:    '#7aa2f7',
  infra: '#e0af68',
  cs:    '#bb9af7',
  daily: 'var(--fg-3)',
};

const BODIES = {
  'rag-basics': `# RAG 기본 구조

> Retrieval-Augmented Generation. LLM 한계를 외부 지식으로 보완.

## 파이프라인

\`\`\`python
docs = load_docs("./vault")
chunks = split(docs, size=500)
embeddings = embed(chunks)
vector_db.upsert(chunks, embeddings)

q_emb = embed(query)
top_k = vector_db.search(q_emb, k=5)
answer = llm.generate(query, context=top_k)
\`\`\`

## 핵심 고려 사항

- **chunk 크기** — 너무 크면 노이즈, 너무 작으면 문맥 손실
- **하이브리드 검색** — 벡터 + BM25 거의 항상 좋음
- **rerank** — cross-encoder로 재정렬

연결: [[bge-m3]], [[vector-db]], [[prompt-eng]]`,

  'prompt-eng': `# Prompt Engineering

자주 쓰는 프롬프트 패턴 정리.

## 1. Few-shot
예시 2~3개를 먼저 보여주고 답하게 한다. 분류·추출에 강함.

## 2. Chain-of-thought
"단계별로 생각하라"는 지시. 추론 문제에 유효.

## 3. Self-consistency
여러 번 sampling 후 다수결. 비용 ↑ 정확도 ↑.

연결: [[rag-basics]], [[llm-eval]]`,

  'llm-eval': `# LLM 평가 방법론

> 정답이 하나가 아닌 생성 모델을 어떻게 평가할 것인가.

## 자동 평가
- BLEU / ROUGE — 표면 유사도. 한계 명확.
- BERTScore — 임베딩 기반.
- LLM-as-a-judge — GPT-4를 채점관으로. **편향 주의**.

## 수동 평가
- 룬릿(rubric) 기반 5점 척도
- A/B pair-wise (Elo)

연결: [[rag-basics]], [[prompt-eng]]`,

  'bge-m3': `# BGE-M3

다국어 임베딩 모델. 한국어 RAG에서 특히 좋음.

## 특징
- **multi-functionality** — dense / sparse / multi-vector 동시 지원
- **multi-linguality** — 100+ 언어
- 8192 토큰까지 입력 가능

\`\`\`python
from FlagEmbedding import BGEM3FlagModel
model = BGEM3FlagModel('BAAI/bge-m3')
emb = model.encode(["문장"])['dense_vecs']
\`\`\`

연결: [[rag-basics]], [[vector-db]]`,

  'vector-db': `# Vector DB 비교

| | pgvector | Qdrant | Weaviate |
|---|---|---|---|
| 운영 | Postgres에 그냥 얹음 | 단독 서버 | 단독 서버 |
| 필터링 | SQL과 함께 | payload | hybrid |
| 규모 | ~수백만 | ~수억 | ~수억 |

## 결론
- 작게 시작 → **pgvector**
- 본격 RAG 운영 → **Qdrant**

연결: [[rag-basics]], [[bge-m3]], [[db-index]]`,

  'asyncio-deep': `# asyncio 동작 원리

> 이벤트 루프 한 줄 요약 — *진짜* 멀티스레드가 아니라 협력적 멀티태스킹.

## 핵심
- \`async def\` → 코루틴 객체를 반환하는 함수
- \`await\` → 이 지점에서 *제어를 양보한다*는 표시
- 이벤트 루프는 양보된 코루틴들을 적당히 돌림

\`\`\`python
async def main():
    async with httpx.AsyncClient() as c:
        r1, r2 = await asyncio.gather(c.get(u1), c.get(u2))
\`\`\`

## 흔한 함정
- 동기 함수 안에서 \`await\` 못 씀
- CPU-bound 작업은 \`asyncio.to_thread\` 또는 별도 프로세스로

연결: [[fastapi-deps]], [[gil]]`,

  'fastapi-deps': `# FastAPI Depends 패턴

DI(의존성 주입)가 라우트·미들웨어·인증을 전부 깔끔하게 정리해준다.

## 기본
\`\`\`python
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/users/{id}")
def read_user(id: int, db = Depends(get_db)):
    return db.get(User, id)
\`\`\`

## 응용
- **인증**: \`Depends(current_user)\` 한 줄로 보호
- **테스트**: \`app.dependency_overrides[get_db] = fake_db\`

연결: [[asyncio-deep]], [[pydantic-v2]]`,

  'pydantic-v2': `# Pydantic v2 마이그레이션

> v1 → v2는 거의 모든 회사에서 한 번은 겪는 작업.

## 바뀐 것
- \`@validator\` → \`@field_validator\`
- \`Config\` 클래스 → \`model_config = ConfigDict(...)\`
- \`.dict()\` → \`.model_dump()\`
- 성능 5~50배 빨라짐 (Rust 코어)

## 함정
- \`Optional[str] = None\`이 v1에선 nullable, v2에선 *반드시 None을 명시* 해야 nullable

연결: [[fastapi-deps]]`,

  'gil': `# GIL · 멀티프로세싱

GIL = 한 시점에 *하나의* 파이썬 바이트코드만 실행됨.

## 그래서 뭘 써야 하나
- **I/O bound** → asyncio / threading
- **CPU bound** → multiprocessing / 외부 워커 (celery, RQ)

\`\`\`python
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as ex:
    results = list(ex.map(heavy_fn, items))
\`\`\`

연결: [[asyncio-deep]]`,

  'docker-compose': `# Docker Compose 패턴 모음

홈서버 운영하면서 자주 쓴 패턴.

## 1. depends_on + healthcheck
\`\`\`yaml
api:
  depends_on:
    db:
      condition: service_healthy
db:
  healthcheck:
    test: ["CMD", "pg_isready"]
    interval: 5s
\`\`\`

## 2. .env 분리
- \`.env\` (커밋 X) + \`.env.example\` (커밋 O)

## 3. profiles
\`docker compose --profile dev up\` — 환경별 컨테이너 토글

연결: [[multistage]], [[tailscale]], [[caddy]]`,

  'multistage': `# Multi-stage build 최적화

빌드 산출물만 가져와서 최종 이미지 줄이기.

\`\`\`dockerfile
FROM python:3.12 AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --target=/deps .

FROM python:3.12-slim
COPY --from=builder /deps /usr/local/lib/python3.12/site-packages
COPY . /app
CMD ["python", "-m", "app"]
\`\`\`

이미지 1.2GB → 230MB.

연결: [[docker-compose]]`,

  'tailscale': `# Tailscale + 홈서버

> 포트포워딩 없이, 외부 노출 없이, 어디서든 홈서버 접근.

## 셋업
1. 모든 기기에 \`tailscaled\` 설치
2. \`tailscale up\` → magic DNS 활성
3. 홈서버에서 \`tailscale serve\` 또는 \`funnel\`

## 이유
- 공인 IP 노출 X
- ACL을 코드로 관리 (\`tailnet policy\`)
- HTTPS 자동

연결: [[caddy]], [[docker-compose]]`,

  'caddy': `# Caddy 리버스 프록시

> nginx 대신 Caddy 쓰는 이유 = **자동 HTTPS** + 짧은 설정.

\`\`\`Caddyfile
api.kknaks.dev {
  reverse_proxy localhost:8000
}
notes.kknaks.dev {
  root * /srv/notes
  file_server
}
\`\`\`

이게 끝. Let's Encrypt 자동.

연결: [[tailscale]], [[docker-compose]]`,

  'k8s-vs-compose': `# k8s vs docker-compose

> 결론: 1인 운영하면 **compose**. 팀 + 다중 노드면 k8s.

## 기준
- 노드 1대 → compose
- 노드 N대 + 자가복구 + 롤링업데이트 → k8s
- 그 사이 → Docker Swarm 또는 Nomad 검토 가능

홈서버는 영원히 compose가 답.

연결: [[docker-compose]]`,

  'tcp-ip': `# TCP/IP 핸드셰이크 정리

## 3-way handshake
1. C → S : SYN
2. S → C : SYN+ACK
3. C → S : ACK

## 4-way close
- 닫을 때 양쪽이 FIN을 따로 보냄
- TIME_WAIT가 왜 필요한지 자주 까먹음 → 잔여 패킷 처리 + 재전송 안전 보장

연결: [[consistent-hash]]`,

  'db-index': `# B-tree vs Hash index

## B-tree
- **범위 검색** O(log n)
- 정렬·prefix 쿼리에 강함
- Postgres 기본

## Hash
- **동등 비교**만 O(1)
- 범위·정렬 불가
- pgvector의 ivfflat은 사실 hash 계열 아이디어

## 결론
RDB 거의 다 B-tree. 특수 목적에서만 hash.

연결: [[vector-db]], [[consistent-hash]]`,

  'consistent-hash': `# Consistent Hashing

> 노드 추가/삭제 시 *재분배 비용*을 최소화하는 해시 링.

## 아이디어
- 키와 노드 모두 같은 해시 공간 (예: 0~2^32) 위에 매핑
- 키는 시계방향으로 가장 가까운 노드에 할당
- 노드 추가 시 평균 K/N 만큼만 이동 (vs 일반 모듈로 → 거의 전부 이동)

## 어디 쓰이나
- 분산 캐시 (memcached, redis cluster)
- CDN 라우팅
- 분산 DB의 샤딩

연결: [[tcp-ip]], [[db-index]]`,

  'daily-2026-04': `# 2026-04 트러블슈팅 모음

## 04-12 · FastAPI Depends가 매번 새 세션을 열고 안 닫음
- 원인: \`yield\` 뒤에 raise 발생 시 \`finally\` 누락
- 해결: \`try/finally\`로 감쌈

## 04-22 · Tailscale ACL 적용 안 됨
- 원인: tailnet policy json 검증 단계에서 silent 실패
- 해결: \`tailscale netcheck\` + admin console에서 정책 diff 확인

연결: [[fastapi-deps]], [[tailscale]]`,

  'daily-2026-03': `# 2026-03 트러블슈팅 모음

## 03-04 · pgvector 임베딩 검색이 느림
- chunk 5만개부터 seq scan 됨
- \`CREATE INDEX ON docs USING ivfflat (emb vector_cosine_ops) WITH (lists=100)\` 추가 → 200ms → 12ms

## 03-19 · Docker compose에서 healthcheck로 무한 루프
- depends_on의 condition을 \`service_healthy\`로 바꾸지 않아서 발생
- 위 패턴 노트에 정리

연결: [[rag-basics]], [[docker-compose]]`,
};

const DEFAULT_BODY = (n) => `# ${n.title}

> ${n.tags.map(t=>'#'+t).join(' ')} · ${n.date}

이 노트의 본문은 곧 백엔드 API에서 가져옵니다.

\`\`\`
GET /api/notes/${n.id}
\`\`\`

연결된 노트: ${n.links.map(l => `[[${l}]]`).join(', ')}`;

// ---- markdown render (mini) ----
function renderMd(md) {
  const lines = md.split('\n');
  const out = []; let inCode = false; let codeBuf = [];
  lines.forEach((ln, i) => {
    if (ln.startsWith('```')) {
      if (inCode) {
        out.push(<pre key={i} style={{ background: 'var(--bg-2)', border: '1px solid var(--line-1)', borderRadius: 6, padding: 14, fontSize: 12.5, color: 'var(--fg-1)', overflowX: 'auto', fontFamily: 'var(--font-mono)' }}>{codeBuf.join('\n')}</pre>);
        codeBuf = []; inCode = false;
      } else inCode = true;
      return;
    }
    if (inCode) { codeBuf.push(ln); return; }
    if (ln.startsWith('# '))  return out.push(<h1 key={i} style={{ fontSize: 28, letterSpacing: '-0.02em', margin: '20px 0 10px', fontWeight: 600 }}>{ln.slice(2)}</h1>);
    if (ln.startsWith('## ')) return out.push(<h2 key={i} style={{ fontSize: 18, margin: '20px 0 8px', fontWeight: 600 }}>{ln.slice(3)}</h2>);
    if (ln.startsWith('> '))  return out.push(<blockquote key={i} style={{ margin: '12px 0', padding: '8px 14px', borderLeft: '2px solid var(--accent)', color: 'var(--fg-2)', fontSize: 13 }}>{ln.slice(2)}</blockquote>);
    if (ln.startsWith('- '))  return out.push(<li key={i} style={{ marginLeft: 18, color: 'var(--fg-1)', fontSize: 13.5, lineHeight: 1.7 }}>{parseInline(ln.slice(2))}</li>);
    if (ln.trim() === '')     return out.push(<div key={i} style={{ height: 6 }} />);
    return out.push(<p key={i} style={{ margin: '6px 0', color: 'var(--fg-1)', fontSize: 13.5, lineHeight: 1.75 }}>{parseInline(ln)}</p>);
  });
  return out;
}
function parseInline(s) {
  const parts = []; let buf = ''; let i = 0;
  const flush = () => { if (buf) { parts.push(buf); buf = ''; } };
  while (i < s.length) {
    if (s[i] === '[' && s[i+1] === '[') {
      flush();
      const end = s.indexOf(']]', i+2);
      if (end === -1) { buf += s[i]; i++; continue; }
      const link = s.slice(i+2, end);
      parts.push(<a key={parts.length} href="#" data-link={link} style={{ color: 'var(--accent)', borderBottom: '1px dashed var(--accent-line)' }}>{link}</a>);
      i = end + 2; continue;
    }
    if (s[i] === '`') {
      flush();
      const end = s.indexOf('`', i+1);
      if (end === -1) { buf += s[i]; i++; continue; }
      parts.push(<code key={parts.length} style={{ fontFamily: 'var(--font-mono)', fontSize: 12, padding: '1px 6px', background: 'var(--bg-2)', borderRadius: 3, color: 'var(--fg-0)' }}>{s.slice(i+1, end)}</code>);
      i = end + 1; continue;
    }
    buf += s[i]; i++;
  }
  flush();
  return parts;
}

// ---- Force-directed graph (lightweight, no D3) ----
function useForceLayout(nodes, edges, width, height, activeId) {
  const [positions, setPositions] = useS(() => {
    const cx = width / 2, cy = height / 2;
    const map = {};
    nodes.forEach((n, i) => {
      const a = (i / nodes.length) * Math.PI * 2;
      map[n.id] = { x: cx + Math.cos(a) * 160, y: cy + Math.sin(a) * 140, vx: 0, vy: 0 };
    });
    return map;
  });
  const rafRef = useR();
  const tickRef = useR(0);

  useE(() => {
    const cx = width / 2, cy = height / 2;
    const idIndex = {}; nodes.forEach(n => idIndex[n.id] = true);
    const linkSet = edges.filter(e => idIndex[e.s] && idIndex[e.t]);

    const tick = () => {
      tickRef.current++;
      setPositions(prev => {
        const next = {};
        nodes.forEach(n => next[n.id] = { ...prev[n.id] });
        // repulsion
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i+1; j < nodes.length; j++) {
            const a = next[nodes[i].id], b = next[nodes[j].id];
            const dx = a.x - b.x, dy = a.y - b.y;
            const d2 = dx*dx + dy*dy + 0.01;
            const f = 1800 / d2;
            const fx = (dx / Math.sqrt(d2)) * f;
            const fy = (dy / Math.sqrt(d2)) * f;
            a.vx += fx; a.vy += fy;
            b.vx -= fx; b.vy -= fy;
          }
        }
        // attraction along edges
        linkSet.forEach(e => {
          const a = next[e.s], b = next[e.t];
          const dx = b.x - a.x, dy = b.y - a.y;
          const d = Math.sqrt(dx*dx + dy*dy) + 0.01;
          const target = 90;
          const f = (d - target) * 0.012;
          const fx = (dx/d) * f, fy = (dy/d) * f;
          a.vx += fx; a.vy += fy;
          b.vx -= fx; b.vy -= fy;
        });
        // gravity to center
        nodes.forEach(n => {
          const p = next[n.id];
          p.vx += (cx - p.x) * 0.005;
          p.vy += (cy - p.y) * 0.005;
          p.vx *= 0.85; p.vy *= 0.85;
          p.x += p.vx; p.y += p.vy;
          // bounds
          const m = 24;
          p.x = Math.max(m, Math.min(width - m, p.x));
          p.y = Math.max(m, Math.min(height - m, p.y));
        });
        return next;
      });
      if (tickRef.current < 220) rafRef.current = requestAnimationFrame(tick);
    };
    tickRef.current = 0;
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  // re-run when canvas size changes (not on every position update)
  // eslint-disable-next-line
  }, [width, height]);

  return positions;
}

// ---- Graph component ----
function Graph({ width, height, activeId, hoverId, setHover, onPick, query }) {
  const nodes = useM(() => {
    if (!query) return NOTES;
    const q = query.toLowerCase();
    return NOTES.filter(n => n.title.toLowerCase().includes(q) || n.tags.some(t => t.includes(q)));
  }, [query]);

  const edges = useM(() => {
    const ids = new Set(nodes.map(n => n.id));
    const out = [];
    nodes.forEach(n => n.links.forEach(l => {
      if (ids.has(l)) out.push({ s: n.id, t: l });
    }));
    return out;
  }, [nodes]);

  const pos = useForceLayout(nodes, edges, width, height, activeId);

  // neighbors of active for highlight
  const neighbors = useM(() => {
    if (!activeId) return new Set();
    const s = new Set([activeId]);
    edges.forEach(e => {
      if (e.s === activeId) s.add(e.t);
      if (e.t === activeId) s.add(e.s);
    });
    return s;
  }, [activeId, edges]);

  return (
    <svg width={width} height={height} style={{ display: 'block' }}>
      {/* edges */}
      <g>
        {edges.map((e, i) => {
          const a = pos[e.s], b = pos[e.t];
          if (!a || !b) return null;
          const dim = activeId && !(neighbors.has(e.s) && neighbors.has(e.t));
          return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y}
            stroke={dim ? 'var(--line-1)' : 'var(--line-3)'} strokeWidth={1} />;
        })}
      </g>
      {/* nodes */}
      <g>
        {nodes.map(n => {
          const p = pos[n.id]; if (!p) return null;
          const isActive = activeId === n.id;
          const isNeighbor = activeId && neighbors.has(n.id) && !isActive;
          const isHover = hoverId === n.id;
          const dim = activeId && !neighbors.has(n.id);
          const color = GROUP_COLOR[n.group] || 'var(--fg-2)';
          const r = isActive ? 8 : isNeighbor || isHover ? 6 : 4.5;
          return (
            <g key={n.id} style={{ cursor: 'pointer', opacity: dim ? 0.25 : 1, transition: 'opacity 200ms' }}
               onMouseEnter={() => setHover(n.id)} onMouseLeave={() => setHover(null)}
               onClick={() => onPick(n.id)}>
              {isActive && <circle cx={p.x} cy={p.y} r={r + 6} fill="none" stroke={color} strokeWidth={1} opacity={0.4} />}
              <circle cx={p.x} cy={p.y} r={r} fill={color}
                stroke={isActive ? 'var(--bg-0)' : 'transparent'} strokeWidth={2} />
              <text x={p.x + r + 6} y={p.y + 3.5} fontSize={isActive || isHover ? 11 : 10}
                fontFamily="var(--font-mono)"
                fill={isActive ? 'var(--fg-0)' : isNeighbor || isHover ? 'var(--fg-1)' : 'var(--fg-2)'}
                style={{ pointerEvents: 'none', userSelect: 'none' }}>
                {n.title}
              </text>
            </g>
          );
        })}
      </g>
    </svg>
  );
}

// ---- Note panel ----
function NotePanel({ note, onClose, onPick }) {
  const body = BODIES[note.id] || DEFAULT_BODY(note);
  const backlinks = NOTES.filter(n => n.id !== note.id && n.links.includes(note.id));

  // intercept wikilink clicks
  const ref = useR();
  useE(() => {
    if (!ref.current) return;
    const el = ref.current;
    const handler = (e) => {
      const a = e.target.closest('a[data-link]');
      if (a) { e.preventDefault(); onPick(a.dataset.link); }
    };
    el.addEventListener('click', handler);
    return () => el.removeEventListener('click', handler);
  }, [note.id, onPick]);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg-1)', borderLeft: '1px solid var(--line-1)' }}>
      <div style={{ padding: '14px 24px', borderBottom: '1px solid var(--line-1)', display: 'flex', alignItems: 'center', gap: 12 }}>
        <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{note.id}.md</span>
        <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>{note.date}</span>
        <button onClick={onClose} className="mono" style={{
          background: 'transparent', border: '1px solid var(--line-2)', color: 'var(--fg-2)',
          padding: '3px 8px', borderRadius: 3, fontSize: 11, cursor: 'pointer',
        }}>esc ✕</button>
      </div>
      <div ref={ref} style={{ padding: '20px 28px 30px', overflowY: 'auto', flex: 1 }}>
        {renderMd(body)}
        <div style={{ marginTop: 24, paddingTop: 14, borderTop: '1px solid var(--line-1)', display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {note.tags.map(t => <span key={t} className="tag">#{t}</span>)}
        </div>
        {backlinks.length > 0 && (
          <div style={{ marginTop: 24 }}>
            <div className="caps" style={{ marginBottom: 8 }}>backlinks ({backlinks.length})</div>
            {backlinks.map(b => (
              <button key={b.id} onClick={() => onPick(b.id)} style={{
                display: 'block', width: '100%', textAlign: 'left', padding: '8px 0',
                background: 'transparent', border: 'none', borderTop: '1px solid var(--line-1)',
                cursor: 'pointer', color: 'var(--fg-1)', fontFamily: 'var(--font-mono)', fontSize: 12,
              }}>← {b.title}</button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ---- Page ----
window.ProtoNotes = function ProtoNotes({ lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const [activeId, setActive] = useS(null);
  const [hoverId, setHover]   = useS(null);
  const [query, setQuery]     = useS('');

  const wrapRef = useR();
  const [size, setSize] = useS({ w: 900, h: 620 });

  useE(() => {
    const measure = () => {
      if (!wrapRef.current) return;
      const r = wrapRef.current.getBoundingClientRect();
      setSize({ w: Math.max(360, Math.floor(r.width)), h: Math.max(420, Math.floor(r.height)) });
    };
    measure();
    const ro = new ResizeObserver(measure);
    if (wrapRef.current) ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, [activeId]);

  // esc to close
  useE(() => {
    const h = (e) => { if (e.key === 'Escape') setActive(null); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, []);

  const note = activeId ? NOTES.find(n => n.id === activeId) : null;

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          04 / Notes · {T('옵시디언 vault 미러', 'obsidian vault mirror')}
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, flexWrap: 'wrap' }}>
          <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>
            Notes
          </h1>
          <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>
            {NOTES.length} {T('노트 · 자동 동기화', 'notes · auto-synced')}
          </span>
          <span className="tag accent" style={{ marginLeft: 'auto' }}>
            <span className="tag-dot" style={{ background: 'var(--accent)' }} />vault → live
          </span>
        </div>

        {/* search + legend bar */}
        <div style={{ marginTop: 24, display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
          <input value={query} onChange={e => setQuery(e.target.value)}
            placeholder={T('검색 — 제목 또는 #태그', 'search — title or #tag')}
            style={{
              padding: '8px 12px', fontFamily: 'var(--font-mono)', fontSize: 12,
              background: 'var(--bg-1)', border: '1px solid var(--line-2)', color: 'var(--fg-0)',
              borderRadius: 4, outline: 'none', minWidth: 280,
            }} />
          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
            {[
              ['ai', 'AI'], ['py', 'Python'], ['infra', 'Infra'], ['cs', 'CS'], ['daily', 'Daily'],
            ].map(([g, l]) => (
              <span key={g} className="mono" style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--fg-3)' }}>
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: GROUP_COLOR[g] }} />
                {l}
              </span>
            ))}
          </div>
          <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>
            {T('노드 클릭 → 본문 보기', 'click node → open note')}
          </span>
        </div>
      </header>

      {/* graph + (optional) panel — desktop only */}
      <div className="pad-x m-hide" style={{ padding: '24px 80px 0' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: activeId ? '1.2fr 1fr' : '1fr',
          gap: 0,
          height: 640,
          border: '1px solid var(--line-1)',
          borderRadius: 6,
          background: 'var(--bg-0)',
          overflow: 'hidden',
          transition: 'grid-template-columns 320ms cubic-bezier(.2,.8,.2,1)',
        }}>
          <div ref={wrapRef} style={{ position: 'relative', overflow: 'hidden' }}>
            <Graph width={size.w} height={size.h}
              activeId={activeId} hoverId={hoverId}
              setHover={setHover} onPick={setActive} query={query} />
            {/* corner hint */}
            <div className="mono" style={{
              position: 'absolute', bottom: 10, left: 12, fontSize: 10, color: 'var(--fg-3)',
              pointerEvents: 'none',
            }}>
              {NOTES.length} nodes · {NOTES.reduce((a,n)=>a+n.links.length,0)} edges
            </div>
          </div>
          {activeId && note && (
            <NotePanel note={note} onClose={() => setActive(null)} onPick={setActive} />
          )}
        </div>
      </div>

      {/* Mobile list view */}
      <div className="m-only pad-x" style={{ padding: '24px 20px 48px' }}>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {NOTES.filter(n => {
            if (!query.trim()) return true;
            const q = query.trim().toLowerCase();
            return n.title.toLowerCase().includes(q) ||
              (n.tags || []).some(t => t.toLowerCase().includes(q));
          }).slice(0, 40).map(n => (
            <li key={n.id}
                onClick={() => setActive(n.id)}
                style={{ padding: '14px 4px', borderTop: '1px solid var(--line-1)', cursor: 'pointer' }}>
              <div style={{ fontSize: 15, color: 'var(--fg-0)', marginBottom: 4 }}>{n.title}</div>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <span>{n.path || n.group}</span>
                {n.date && <span>· {n.date}</span>}
              </div>
            </li>
          ))}
        </ul>
        {activeId && note && (
          <div style={{ marginTop: 24 }}>
            <NotePanel note={note} onClose={() => setActive(null)} onPick={setActive} />
          </div>
        )}
      </div>
    </div>
  );
};
