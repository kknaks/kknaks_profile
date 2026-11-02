/* 「알림」 화면 (2026-10-07) — 사이드바 「알림」을 누르면 서는 알림 목록.
   알림은 나와 관련된 것만 온다: 업무 상태 변경 · 메일·슬랙·카톡 수신 · 회의(초대·변경·취소·회의록 완료/실패·공유) · 연동 끊김.
   같은 사건이라도 받는 사람의 관계(담당·요청자·배정자·참조 / 받는 사람·참조·그 밖의 메일 / DM·멘션·채널 / 소유자·참석자·공유받음)가 다르므로
   줄마다 그 관계를 작은 꼬리표로 단다. 줄 = 테마 표식 · 문장(누가 · 무엇을 · 어디에) · 관계 · 시각 · 안 읽음 점.
   줄을 누르면 읽음이 되고 그 업무·메시지·회의로 간다(시안은 링크 모양만 — 도착 화면은 기존 화면 그대로).
   틀은 메시지함과 같다(머리 · 「모두 읽음」 · 분류 SegmentedControl). 상세 본문이 따로 없어 레일 없이 한 단으로 선다.
   그리지 않는 것: OS 시스템 알림 모양 · 알림 지우기/보관 · 알림 설정으로 가는 지름길 · 실시간 도착 애니메이션.
   공용 틀은 ../../shell/js/scax-ui.jsx, 데이터는 ./data.js. 화면 네 상태는 화면 아래 DevSwitch(시안 전용)로 본다. */
const { Icon, Button, Badge, SegmentedControl, Empty, StatusNote, Skeleton, AppShell, SideNav, AppHeader, AppBody } = window;

const THEMES = {
  work: { label: '업무', icon: 'square-check' },
  message: { label: '메시지', icon: 'inbox' },
  meeting: { label: '회의', icon: 'persons' },
};

const FILTERS = [
  { value: 'all', label: '전체' },
  { value: 'work', label: '업무' },
  { value: 'message', label: '메시지' },
  { value: 'meeting', label: '회의' },
];

/* 나와의 관계 꼬리표 — 메시지 테마는 출처를 앞에 붙여 「메일 · 참조」처럼 읽힌다 */
const RELATIONS = {
  assignee: '담당',
  requester: '요청자',
  assigner: '배정자',
  cc: '참조(CC)',
  to: '메일 · 받는 사람',
  'mail-cc': '메일 · 참조',
  'mail-other': '메일',
  dm: '슬랙 · DM',
  mention: '슬랙 · 멘션',
  channel: '슬랙 · 채널',
  'kakao-direct': '카톡 · 1:1',
  'kakao-group': '카톡 · 단체방',
  integration: '내 연동',
  owner: '소유자',
  attendee: '참석자',
  shared: '공유받음',
};

const DAYS = [
  { key: 'today', label: '오늘' },
  { key: 'yesterday', label: '어제' },
  { key: 'week', label: '이번 주' },
  { key: 'earlier', label: '이전' },
];

/* 문장 조각 — { b } 누가 · { q } 무엇을 · 문자열 */
function Sentence({ parts }) {
  return (
    <p className="scax-alert__text">
      {parts.map((p, i) => {
        if (typeof p === 'string') return <React.Fragment key={i}>{p}</React.Fragment>;
        if (p.b) return <strong key={i} className="scax-alert__who">{p.b}</strong>;
        return <strong key={i} className="scax-alert__what">‘{p.q}’</strong>;
      })}
    </p>
  );
}

function AlertRow({ item, onOpen }) {
  const theme = THEMES[item.theme];
  return (
    <li>
      <a
        className={`scax-alert${item.unread ? ' scax-alert--unread' : ''}`}
        href={item.to.href}
        onClick={(e) => { e.preventDefault(); onOpen(item.id); }}
      >
        <span className={`scax-alert__mark scax-alert__mark--${item.fail ? 'fail' : item.theme}`} aria-hidden="true">
          <Icon name={item.fail ? 'circle-exclamation' : theme.icon} size={20} />
        </span>
        <span className="scax-alert__body">
          <Sentence parts={item.text} />
          {item.sub ? <span className="scax-alert__sub">{item.sub}</span> : null}
          <span className="scax-alert__meta">
            <span className="scax-alert__theme">{theme.label}</span>
            <span className="scax-alert__rel">{RELATIONS[item.rel]}</span>
            <span className="scax-alert__sep" />
            <span className="scax-alert__at">{item.at}</span>
            <span className="scax-alert__sep" />
            <span className="scax-alert__to">{item.to.label}<Icon name="chevron-right" size={16} /></span>
          </span>
        </span>
        <span className="scax-alert__end">
          {item.unread ? <span className="scax-alert__dot" aria-label="안 읽음" /> : null}
        </span>
      </a>
    </li>
  );
}

const EMPTY_BY_FILTER = {
  work: { title: '업무 알림이 없습니다', desc: '업무 요청·배정·완료 보고처럼 나와 관련된 업무 소식이 여기에 쌓입니다.' },
  message: { title: '메시지 알림이 없습니다', desc: '나에게 온 메일·슬랙·카톡과 연동 끊김 소식이 여기에 쌓입니다.' },
  meeting: { title: '회의 알림이 없습니다', desc: '회의 초대·변경·회의록 소식이 여기에 쌓입니다.' },
};

function AlertList({ state, shown, onOpen, onRetry, filter }) {
  if (state === 'loading') {
    return (
      <div className="scax-alerts__skel">
        <Skeleton variant="title" width="40" />
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <div className="scax-alerts__skel-row" key={i}>
            <span className="scax-alerts__skel-mark" />
            <div className="scax-skeleton-stack"><Skeleton variant="text" width={i % 2 ? '80' : 'full'} /><Skeleton variant="text" width="40" /></div>
          </div>
        ))}
      </div>
    );
  }
  if (state === 'error') {
    return <div className="scax-alerts__state"><StatusNote title="알림을 불러오지 못했습니다" desc="잠시 후 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" onClick={onRetry} />} /></div>;
  }
  if (state === 'empty' && filter === 'all') {
    return <div className="scax-alerts__state"><Empty icon="inbox" title="받은 알림이 없습니다" desc="나에게 온 업무·메시지·회의 소식이 생기면 여기에 쌓입니다." /></div>;
  }
  /* 분류를 고른 채 비면 그 분류의 빈 문구 — 시안에선 「빈」 상태에서 분류를 바꿔 본다 */
  if (state === 'empty' || !shown.length) {
    const e = EMPTY_BY_FILTER[filter];
    return <div className="scax-alerts__state"><Empty icon="tune" title={e.title} desc={e.desc} /></div>;
  }
  return DAYS.map((d) => {
    const list = shown.filter((i) => i.day === d.key);
    if (!list.length) return null;
    return (
      <section className="scax-alerts__day" key={d.key} aria-label={d.label}>
        <h2 className="scax-alerts__day-title">{d.label}</h2>
        <ul className="scax-alerts__list">
          {list.map((i) => <AlertRow key={i.id} item={i} onOpen={onOpen} />)}
        </ul>
      </section>
    );
  });
}

/* 시안 전용 상태 토글 — 제품 화면이 아니다 (DS .scax-state-switch 모양) */
const SCREEN_STATES = [
  { value: 'default', label: '기본' },
  { value: 'empty', label: '빈' },
  { value: 'loading', label: '로딩' },
  { value: 'error', label: '오류' },
];

function DevSwitch({ groups }) {
  return (
    <div className="scax-state-switch">
      {groups.map((g) => (
        <React.Fragment key={g.label}>
          <span className="scax-state-switch__label">{g.label}</span>
          {g.options.map((o) => (
            <button key={o.value} type="button" className={`scax-state-switch__btn${o.value === g.value ? ' scax-state-switch__btn--on' : ''}`} onClick={() => g.onChange(o.value)}>
              {o.label}
            </button>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
}

function AlertsPage() {
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [screenState, setScreenState] = React.useState('default');
  const [filter, setFilter] = React.useState('all');
  const [items, setItems] = React.useState(ALERT_ITEMS);

  /* 줄을 누르면 읽음 — 실제로는 그 자리로 이동한다 */
  const open = (id) => setItems((l) => l.map((x) => (x.id === id ? Object.assign({}, x, { unread: false }) : x)));
  const readAll = () => setItems((l) => l.map((x) => Object.assign({}, x, { unread: false })));
  const retry = () => setScreenState('default');

  const ready = screenState === 'default';
  const shown = items.filter((i) => filter === 'all' || i.theme === filter);
  const unread = items.filter((i) => i.unread).length;
  const unreadOf = (t) => items.filter((i) => i.unread && i.theme === t).length;
  const options = FILTERS.map((f) => {
    const n = f.value === 'all' ? 0 : unreadOf(f.value);
    return n && ready ? Object.assign({}, f, { label: `${f.label} ${n}` }) : f;
  });

  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="alert" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader
          title="알림"
          titleEnd={ready && unread ? <span className="scax-alerts__unread">안 읽음 <Badge variant="count">{unread}</Badge></span> : null}
          actions={ready ? <Button size="sm" label="모두 읽음" disabled={!unread} onClick={readAll} /> : null}
        />
        <AppBody>
          <div className="scax-alerts">
            <div className="scax-alerts__inner">
              <div className="scax-alerts__tools">
                <SegmentedControl value={filter} options={options} onChange={setFilter} ariaLabel="알림 분류" />
              </div>
              <AlertList state={screenState} shown={shown} onOpen={open} onRetry={retry} filter={filter} />
            </div>
          </div>
        </AppBody>
      </AppShell>
      <DevSwitch groups={[{ label: '화면', value: screenState, options: SCREEN_STATES, onChange: setScreenState }]} />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<AlertsPage />);
