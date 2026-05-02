/* global React */
const { useState: _cuS, useEffect: _cuE } = React;

/* =========================================================
   Contents — daily study log
   YouTube video + 교안 (개념 + 적용예시)
   ========================================================= */

const CONTENTS_DATA = [
  {
    id: 'C-005',
    date: '2026.04.30',
    day: 'Day 05',
    title: 'Vector DB 기본기 — HNSW가 왜 빠른가',
    youtubeId: 'dQw4w9WgXcQ',
    duration: '18:42',
    speaker: 'kknaks',
    tags: ['AI', 'VectorDB', 'HNSW'],
    summary: '벡터 검색의 기본 자료구조 HNSW를 그래프 관점에서 풀어보고, FAISS와 pgvector에서의 트레이드오프를 비교한다.',
    concept: [
      'HNSW(Hierarchical Navigable Small World)는 다층 그래프로 근사 최근접 탐색(ANN)을 수행한다.',
      '상위 레이어일수록 sparse — 멀리서 빠르게 후보를 좁히고, 하위 레이어에서 정밀하게 탐색.',
      'M(노드당 이웃 수), efSearch(탐색 폭) 두 파라미터가 recall/latency를 결정.',
      '브루트포스 대비 1000× 빠르지만 100% recall은 보장 못함 — recall@10을 측정해야 한다.',
    ],
    example: [
      '사내 RAG 파이프라인에서 pgvector(IVFFlat)에서 HNSW로 옮긴 후 p99 검색이 320ms → 38ms.',
      'efSearch를 40에서 80으로 올리면 recall@10이 0.91 → 0.97로 올라가지만 latency 1.6배.',
      '요약: 트래픽이 적은 구간에선 efSearch 높여 정확도 올리고, 피크엔 낮추는 식으로 조정.',
    ],
  },
  {
    id: 'C-004',
    date: '2026.04.29',
    day: 'Day 04',
    title: 'asyncio의 이벤트 루프 — await가 멈추는 진짜 위치',
    youtubeId: 'dQw4w9WgXcQ',
    duration: '14:08',
    speaker: 'kknaks',
    tags: ['Python', 'asyncio', 'concurrency'],
    summary: 'await 키워드가 만드는 suspension point와 이벤트 루프가 코루틴을 다시 깨우는 메커니즘을 코드 레벨에서 따라간다.',
    concept: [
      '코루틴은 generator의 일반화 — yield 대신 await로 제어를 양보.',
      '이벤트 루프는 ready 큐 + I/O selector(epoll/kqueue) 두 축으로 돌아간다.',
      'await는 awaitable.__await__()를 호출, StopIteration이 나오면 결과 확정.',
      'CPU 바운드 작업 안엔 await가 없으면 다른 코루틴이 절대 실행되지 않는다.',
    ],
    example: [
      '실제 사내 워커: httpx 30개 동시 호출 — sync면 18초, async면 1.4초.',
      'BUT pandas 대용량 정렬을 코루틴 안에서 돌리면 다른 요청이 다 멈춤. run_in_executor로 분리 필요.',
      '결론: I/O는 async, CPU는 thread/process. 섞으면 혼자 다 막힌다.',
    ],
  },
  {
    id: 'C-003',
    date: '2026.04.28',
    day: 'Day 03',
    title: 'PostgreSQL의 MVCC — 동시성과 vacuum의 함정',
    youtubeId: 'dQw4w9WgXcQ',
    duration: '21:55',
    speaker: 'kknaks',
    tags: ['Database', 'Postgres', 'MVCC'],
    summary: 'MVCC가 어떻게 락 없이 일관성을 만드는지, 그리고 vacuum이 왜 필수이고 언제 문제를 일으키는지 정리.',
    concept: [
      '모든 row는 xmin/xmax 트랜잭션 ID를 가진다 — 보이는지 여부는 트랜잭션 스냅샷이 결정.',
      'UPDATE는 in-place 수정이 아니라 새 row를 만들고 기존 row의 xmax를 채운다.',
      'dead tuple이 쌓이면 테이블이 부풀고(bloat) 인덱스 효율이 떨어진다.',
      'autovacuum이 dead tuple을 회수 — 테이블 크기에 따라 임계치를 따로 조정해야.',
    ],
    example: [
      '핫 테이블(분당 5만 UPDATE)에서 autovacuum_vacuum_scale_factor 0.2 → 0.05로 낮춤.',
      'bloat가 35% → 8%로 줄고 seq scan p99도 절반.',
      '교훈: 디폴트는 작은 테이블 기준이라, 큰 테이블엔 직접 튜닝 필수.',
    ],
  },
  {
    id: 'C-002',
    date: '2026.04.27',
    day: 'Day 02',
    title: 'Tokenizer 비교 — BPE vs WordPiece vs Unigram',
    youtubeId: 'dQw4w9WgXcQ',
    duration: '12:30',
    speaker: 'kknaks',
    tags: ['AI', 'NLP', 'Tokenizer'],
    summary: '세 토크나이저의 학습 방식과 한국어에서의 동작 차이를 직접 토크나이즈해 보면서 비교.',
    concept: [
      'BPE: 빈도 기반 merge — 가장 흔한 byte pair부터 합친다.',
      'WordPiece: BPE와 비슷하나 likelihood 최대화로 merge 결정.',
      'Unigram: 큰 vocab에서 시작해 likelihood 작은 토큰을 제거.',
      '한국어처럼 형태소가 많은 언어에선 Unigram이 일반적으로 토큰 수가 더 적게 나온다.',
    ],
    example: [
      '"오늘 점심 뭐 먹지" 문장 — BPE 8토큰, Unigram 5토큰.',
      'API 호출 비용은 토큰 수에 비례 — 한국어 서비스에선 토크나이저 선택이 곧 비용.',
      'Llama 계열은 BPE, mBERT는 WordPiece. 모델 갈아끼울 땐 비용 시뮬레이션 필수.',
    ],
  },
  {
    id: 'C-001',
    date: '2026.04.26',
    day: 'Day 01',
    title: 'Docker layer cache — 빌드를 10배 빠르게',
    youtubeId: 'dQw4w9WgXcQ',
    duration: '09:18',
    speaker: 'kknaks',
    tags: ['Infra', 'Docker', 'CI'],
    summary: 'Dockerfile 명령 순서가 캐시 히트율을 결정한다. 의존성과 소스를 분리하는 패턴 정리.',
    concept: [
      '각 RUN/COPY/ADD는 layer를 만들고, 동일하면 캐시 재사용.',
      '한 줄이라도 바뀌면 그 줄 이후 layer는 모두 무효화.',
      '의존성 설치(npm/pip)는 거의 안 변하니 위로, 소스 COPY는 아래로.',
      'BuildKit의 --mount=type=cache로 패키지 매니저 캐시도 layer 밖으로 분리 가능.',
    ],
    example: [
      '사내 CI: Dockerfile 순서 바꾸기만으로 빌드 4분 → 24초.',
      'requirements.txt가 안 변할 땐 COPY . 단계만 다시 — pip install 통째로 스킵.',
      '결론: layer 순서는 의존성 변동 빈도 역순으로.',
    ],
  },
];

/* ---------- List view ---------- */

function ContentsList({ lang, setRoute }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const [latest, ...rest] = CONTENTS_DATA;

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          05 / Contents · {T('매일 업로드', 'daily uploads')}
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, flexWrap: 'wrap' }}>
          <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Contents</h1>
          <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>// study log · video + 교안</span>
        </div>
        <p style={{ margin: '20px 0 0', fontSize: 15, color: 'var(--fg-1)', maxWidth: 640, lineHeight: 1.6 }}>
          {T(
            '매일 한 편씩 — 유튜브 영상을 보고 그 위에 개념과 적용 예시로 교안을 만들어 공유합니다.',
            'One per day — a YouTube video paired with a study sheet of concept + applied example.'
          )}
        </p>
      </header>

      {/* Latest — large card */}
      <section className="pad-x" style={{ padding: '48px 80px 24px' }}>
        <div className="caps" style={{ marginBottom: 16 }}>{T('최신', 'latest')}</div>
        <article
          className="card m-stack"
          style={{ overflow: 'hidden', cursor: 'pointer', display: 'grid', gridTemplateColumns: '1.15fr 1fr' }}
          onClick={() => setRoute('contents/' + latest.id)}
        >
          <YouTubeFrame id={latest.youtubeId} title={latest.title} />
          <div style={{ padding: '28px 32px', borderLeft: '1px solid var(--line-1)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{latest.id}</span>
              <span className="tag" style={{ color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' }}>
                <span className="tag-dot" style={{ background: 'var(--accent)' }} />{latest.day}
              </span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>{latest.date}</span>
            </div>
            <h2 style={{ margin: '0 0 12px', fontSize: 26, lineHeight: 1.25, letterSpacing: '-0.015em', fontWeight: 600 }}>{latest.title}</h2>
            <p style={{ margin: '0 0 18px', color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.65 }}>{latest.summary}</p>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 18 }}>
              {latest.tags.map(t => <span key={t} className="tag">#{t}</span>)}
            </div>
            <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', gap: 12 }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>▶ {latest.duration}</span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginLeft: 'auto' }}>{T('교안 보기', 'open sheet')} →</span>
            </div>
          </div>
        </article>
      </section>

      {/* Rest — list */}
      <section className="pad-x" style={{ padding: '24px 80px 64px' }}>
        <div className="caps" style={{ marginBottom: 16 }}>{T('이전 회차', 'previous')}</div>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {rest.map(c => (
            <li
              key={c.id}
              onClick={() => setRoute('contents/' + c.id)}
              className="contents-row"
              style={{
                display: 'grid',
                gridTemplateColumns: '76px 88px 1fr 200px 80px',
                gap: 20,
                padding: '18px 12px',
                borderTop: '1px solid var(--line-1)',
                alignItems: 'center',
                cursor: 'pointer',
                transition: 'background 120ms',
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-1)'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{c.id}</span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-2)' }}>{c.day}</span>
              <div>
                <div style={{ fontSize: 15, color: 'var(--fg-0)', marginBottom: 4 }}>{c.title}</div>
                <div style={{ fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.5 }}>{c.summary}</div>
              </div>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {c.tags.slice(0, 3).map(t => <span key={t} className="tag" style={{ fontSize: 10 }}>#{t}</span>)}
              </div>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}>{c.date}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

/* ---------- Detail view ---------- */

function ContentsDetail({ lang, id, setRoute }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const item = CONTENTS_DATA.find(c => c.id === id);
  if (!item) {
    return (
      <div style={{ padding: '80px', textAlign: 'center' }}>
        <p style={{ color: 'var(--fg-2)' }}>not found.</p>
        <button className="btn" onClick={() => setRoute('contents')}>← back</button>
      </div>
    );
  }

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '40px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <button
          className="mono"
          onClick={() => setRoute('contents')}
          style={{ background: 'transparent', border: 'none', color: 'var(--fg-3)', fontSize: 12, cursor: 'pointer', padding: 0, marginBottom: 20 }}
        >
          ← {T('전체 회차', 'all contents')}
        </button>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12, display: 'flex', gap: 12 }}>
          <span>{item.id}</span>
          <span style={{ color: 'var(--accent)' }}>● {item.day}</span>
          <span>{item.date}</span>
        </div>
        <h1 className="m-h1" style={{ fontSize: 40, lineHeight: 1.15, letterSpacing: '-0.02em', margin: 0, fontWeight: 600, maxWidth: 900 }}>{item.title}</h1>
        <p style={{ margin: '16px 0 0', color: 'var(--fg-1)', fontSize: 15, lineHeight: 1.65, maxWidth: 760 }}>{item.summary}</p>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 20 }}>
          {item.tags.map(t => <span key={t} className="tag">#{t}</span>)}
        </div>
      </header>

      <div className="pad-x m-stack" style={{ padding: '48px 80px 24px', display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 56, alignItems: 'start' }}>
        {/* Left — video only */}
        <div>
          <SectionHeader idx="01" label="video" title={T('영상', 'Video')} />
          <YouTubeFrame id={item.youtubeId} title={item.title} />
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginTop: 10, display: 'flex', justifyContent: 'space-between' }}>
            <span>▶ {item.duration}</span>
            <span>youtu.be/{item.youtubeId}</span>
          </div>
        </div>

        {/* Right — 개념설명 */}
        <aside>
          <SectionHeader idx="02" label="concept" title={T('개념 설명', 'Concept')} />
          <div className="card" style={{ padding: 24 }}>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {item.concept.map((line, i) => (
                <li key={i} style={{ display: 'grid', gridTemplateColumns: '24px 1fr', gap: 8, padding: '10px 0', borderTop: i === 0 ? 'none' : '1px solid var(--line-1)' }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', paddingTop: 3 }}>{String(i+1).padStart(2,'0')}</span>
                  <span style={{ fontSize: 14, lineHeight: 1.6, color: 'var(--fg-1)' }}>{line}</span>
                </li>
              ))}
            </ul>
          </div>
          <div style={{ marginTop: 16, padding: '16px 20px', border: '1px solid var(--line-1)', borderRadius: 6, background: 'var(--bg-1)' }}>
            <div className="caps" style={{ marginBottom: 8 }}>{T('발표', 'speaker')}</div>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-0)' }}>{item.speaker}</div>
          </div>
        </aside>
      </div>

      {/* 적용예시 — full width 별도 섹션 */}
      <section className="pad-x" style={{ padding: '32px 80px 32px' }}>
        <SectionHeader idx="03" label="applied" title={T('적용 예시', 'Applied example')} />
        <ol style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {item.example.map((line, i) => (
            <li key={i} style={{ display: 'grid', gridTemplateColumns: '60px 1fr', gap: 20, padding: '18px 0', borderTop: '1px solid var(--line-1)', borderBottom: i === item.example.length - 1 ? '1px solid var(--line-1)' : 'none' }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--accent)', paddingTop: 4 }}>03.{String(i+1).padStart(2,'0')}</span>
              <span style={{ fontSize: 16, lineHeight: 1.65, color: 'var(--fg-0)', maxWidth: 880 }}>{line}</span>
            </li>
          ))}
        </ol>
      </section>

      {/* Prev / Next nav */}
      <ContentsPrevNext id={id} setRoute={setRoute} lang={lang} />
    </div>
  );
}

function SectionHeader({ idx, label, title }) {
  return (
    <div style={{ marginBottom: 18, display: 'flex', alignItems: 'baseline', gap: 12 }}>
      <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{idx}</span>
      <h2 style={{ margin: 0, fontSize: 22, letterSpacing: '-0.015em', fontWeight: 600 }}>{title}</h2>
      <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>· {label}</span>
    </div>
  );
}

function ContentsPrevNext({ id, setRoute, lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const idx = CONTENTS_DATA.findIndex(c => c.id === id);
  const newer = idx > 0 ? CONTENTS_DATA[idx - 1] : null;
  const older = idx < CONTENTS_DATA.length - 1 ? CONTENTS_DATA[idx + 1] : null;
  return (
    <nav className="pad-x m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, padding: '32px 80px 64px', borderTop: '1px solid var(--line-1)' }}>
      {newer ? (
        <button className="card" onClick={() => setRoute('contents/' + newer.id)} style={{ padding: '20px 24px', textAlign: 'left', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)' }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>← {T('다음 회차', 'newer')}</div>
          <div style={{ fontSize: 14, color: 'var(--fg-0)' }}>{newer.title}</div>
        </button>
      ) : <div />}
      {older ? (
        <button className="card" onClick={() => setRoute('contents/' + older.id)} style={{ padding: '20px 24px', textAlign: 'right', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)' }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>{T('이전 회차', 'older')} →</div>
          <div style={{ fontSize: 14, color: 'var(--fg-0)' }}>{older.title}</div>
        </button>
      ) : <div />}
    </nav>
  );
}

/* ---------- Reusable YouTube frame placeholder ---------- */

function YouTubeFrame({ id, title }) {
  // Use a placeholder hatch with a play button — keeps the design clean offline,
  // and avoids embedding random youtube videos in mock state.
  return (
    <div style={{ position: 'relative', aspectRatio: '16/9', background: '#000', overflow: 'hidden' }}>
      <div className="placeholder-hatch" style={{ position: 'absolute', inset: 0 }}>
        [ youtube · {id} · 16:9 ]
      </div>
      <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none' }}>
        <div style={{
          width: 64, height: 64, borderRadius: '50%',
          background: 'var(--accent)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 0 0 6px rgba(0,0,0,0.4)',
        }}>
          <div style={{
            width: 0, height: 0,
            borderLeft: '18px solid var(--accent-ink)',
            borderTop: '12px solid transparent',
            borderBottom: '12px solid transparent',
            marginLeft: 5,
          }} />
        </div>
      </div>
      <div className="mono" style={{ position: 'absolute', bottom: 10, right: 12, fontSize: 11, color: 'var(--fg-2)', background: 'rgba(0,0,0,0.5)', padding: '3px 8px', borderRadius: 3 }}>
        ▶ {title.length > 40 ? title.slice(0, 40) + '…' : title}
      </div>
    </div>
  );
}

/* ---------- Top-level export ---------- */

window.ProtoContents = function ProtoContents({ lang, subRoute, setRoute }) {
  if (subRoute && subRoute.startsWith('C-')) {
    return <ContentsDetail lang={lang} id={subRoute} setRoute={setRoute} />;
  }
  return <ContentsList lang={lang} setRoute={setRoute} />;
};
