/* 「설정」 화면 — 좌 레일(GutterList 안의 설정 메뉴) + 본문(섹션 상자).
   틀·여백·상자는 프로젝트/자료 화면과 같은 어휘를 쓴다 (레일 = GutterList, 본문 = 500/600 여백 + 라운드 상자).
   연동의 목적은 흩어진 메일·대화를 우리 DB 로 적재하는 것이다. 세 연동 모두 적재 상태 3칸을 같은 자리에 둔다.
   메일·슬랙은 사용자 한 번 연결 → 실시간 수집이다: 셋째 칸이 「실시간」이고, 메일은 Google 계정 연결,
   슬랙은 워크스페이스 연결 + 방 고르기 창으로 방을 넣는다. 카카오톡은 Mac 앱 상태 카드 + 방 고르기 창(조회만).
   연동 상태 넷(연결 전 · 연결됨 · 과거 채우는 중 · 연결 끊김)과 방 고르기 창 상태는 화면 아래 DevSwitch(시안 전용)로 본다.
   공용 틀은 ../../shell/js/scax-ui.jsx, 데이터는 ./data.js. */
const { Icon, Button, IconButton, Badge, Select, SegmentedControl, GutterList, Empty, Skeleton, AppShell, SideNav, AppHeader, AppBody, StatusNote } = window;

const SET_MENU = [
  { caption: '연동', items: [
    { id: 'mail', label: '메일 연동' },
    { id: 'slack', label: '슬랙 연동' },
    { id: 'kakao', label: '카카오톡 연동' },
  ] },
  { caption: '계정', items: [
    { id: 'account', label: '프로필 설정' },
    { id: 'notify', label: '알림 설정' },
  ] },
];

function SetNav({ active, onSelect, counts }) {
  return (
    <div className="scax-set-nav">
      {SET_MENU.map((g) => (
        <div className="scax-set-nav__group" key={g.caption}>
          <p className="scax-set-nav__caption">{g.caption}</p>
          {g.items.map((it) => (
            <button
              key={it.id}
              type="button"
              className={`scax-set-nav__item${it.id === active ? ' scax-set-nav__item--on' : ''}`}
              aria-current={it.id === active ? 'true' : undefined}
              onClick={() => onSelect(it.id)}
            >
              <span className="scax-set-nav__label">{it.label}</span>
              {counts[it.id] != null ? <span className="scax-set-nav__tail">{counts[it.id]}</span> : null}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}

function Card({ title, legend, end, note, children }) {
  return (
    <section className="scax-set-card">
      <header className="scax-set-card__head">
        <h2 className="scax-set-card__title">{title}</h2>
        {legend ? <span className="scax-set-card__legend">{legend}</span> : null}
        {end ? <div className="scax-set-card__end">{end}</div> : null}
      </header>
      {children}
      {note ? <p className="scax-set-card__note">{note}</p> : null}
    </section>
  );
}

function Field({ label, hint, children }) {
  return (
    <label className="scax-field">
      <span className="scax-field__label">{label}</span>
      {children}
      {hint ? <span className="scax-field__hint">{hint}</span> : null}
    </label>
  );
}

function Switch({ on, onToggle, label }) {
  return (
    <button type="button" className={`scax-switch${on ? ' scax-switch--on' : ''}`} role="switch" aria-checked={on} aria-label={label} onClick={onToggle}>
      <span className="scax-switch__knob" />
    </button>
  );
}

/* ===== 섹션 ===== */

/* ===== 메일 · 슬랙 공용 — 실시간 연동 부품 =====
   두 연동은 사용자 한 번 연결로 실시간 수집한다. 수집 주기 Select 는 없고 셋째 칸이 「실시간」이다. */

const STATE_LABEL = { live: '실시간', backfill: '과거 채우는 중', broken: '연결 끊김' };

function LiveStrip({ last, total, paused, pausedLabel = '멈춤 — 연결 끊김' }) {
  return (
    <div className="scax-set-sync">
      <div className="scax-set-sync__cell">
        <span className="scax-set-sync__key">마지막 수집</span>
        <span className="scax-set-sync__val">{last}</span>
      </div>
      <div className="scax-set-sync__cell">
        <span className="scax-set-sync__key">DB 적재 건수</span>
        <span className="scax-set-sync__val">{total}</span>
      </div>
      <div className="scax-set-sync__cell">
        <span className="scax-set-sync__key">수집</span>
        <span className={`scax-set-live${paused ? ' scax-set-live--paused' : ''}`}>
          <span className="scax-set-live__dot" />{paused ? pausedLabel : '실시간'}
        </span>
      </div>
    </div>
  );
}

/* 줄 오른쪽 상태 — 실시간 / 과거 채우는 중 · N건 / 연결 끊김 — 다시 연결 */
function LiveState({ status, backfillLabel, onReconnect }) {
  if (status === 'broken') {
    return (
      <span className="scax-set-state scax-set-state--broken">
        <span className="scax-set-state__dot" />연결 끊김
        <button type="button" className="scax-set-link" onClick={onReconnect}>다시 연결</button>
      </span>
    );
  }
  if (status === 'backfill') {
    return <span className="scax-set-state scax-set-state--backfill"><span className="scax-set-state__dot" />{backfillLabel}</span>;
  }
  return <span className="scax-set-state scax-set-state--live"><span className="scax-set-state__dot" />실시간</span>;
}

/* 확인 창 — 연결 해제 · 방 빼기 */
function ConfirmBox({ confirm, onClose }) {
  if (!confirm) return null;
  return (
    <div className="scax-modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="scax-modal scax-modal--sm" role="dialog" aria-modal="true" aria-label={confirm.title}>
        <header className="scax-modal__head">
          <h2 className="scax-modal__title">{confirm.title}</h2>
          <IconButton name="close" size={24} label="닫기" onClick={onClose} />
        </header>
        <div className="scax-modal__body">
          <ul className="scax-set-confirm">
            {confirm.lines.map((l) => <li key={l}>{l}</li>)}
          </ul>
        </div>
        <footer className="scax-modal__foot">
          <Button variant="outlined" tone="neutral" label="취소" onClick={onClose} />
          <Button variant="solid" tone="danger" label={confirm.cta} onClick={() => { confirm.run(); onClose(); }} />
        </footer>
      </div>
    </div>
  );
}

/* ===== 메일 연동 — Gmail API · 계정마다 한 번 연결 ===== */

function MailSection({ list, onConnect, onReconnect, onAskRemove }) {
  if (!list.length) {
    return (
      <React.Fragment>
        <p className="scax-set-view__intro">받은편지함의 메일을 우리 DB 로 적재한다. 계정마다 한 번 연결하면 된다.</p>
        <Card title="Google 계정 연결">
          <div className="scax-set-connect">
            <p className="scax-set-connect__desc">한 번 연결하면 받은편지함이 실시간으로 쌓인다. 연결할 때 받은편지함 전체를 가져온다.</p>
            <Button variant="solid" tone="primary" label="Google로 연결" onClick={onConnect} />
          </div>
        </Card>
      </React.Fragment>
    );
  }
  const broken = list.filter((a) => a.status === 'broken').length;
  return (
    <React.Fragment>
      <p className="scax-set-view__intro">받은편지함의 메일을 우리 DB 로 적재한다. 계정마다 한 번 연결하면 된다.</p>
      <Card title="연결된 메일 계정" legend={`${list.length}개`}>
        <LiveStrip last="10-06 09:12" total="4,003" />
        <ul className="scax-set-list">
          {list.map((a) => (
            <li className={`scax-set-row${a.status === 'broken' ? ' scax-set-row--broken' : ''}`} key={a.id}>
              <span className="scax-set-row__mark scax-set-row__mark--gmail" aria-hidden="true">G</span>
              <span className="scax-set-row__who">
                <span className="scax-set-row__name">{a.addr}</span>
                <span className="scax-set-row__meta">Gmail · 적재 {a.count}건 · 마지막 {a.synced}</span>
              </span>
              <span className="scax-set-row__end">
                <LiveState status={a.status} backfillLabel={`과거 메일 채우는 중 · ${a.count}건`} onReconnect={() => onReconnect(a.id)} />
                <Button size="sm" variant="text" tone="neutral" label="연결 해제" onClick={() => onAskRemove(a)} />
              </span>
            </li>
          ))}
        </ul>
        {broken ? <p className="scax-set-card__note scax-set-card__note--danger">연결이 끊긴 계정은 새 메일을 받지 못한다. 토큰이 만료됐거나 Google 에서 권한을 거둔 경우다 — 「다시 연결」로 한 번 더 동의하면 이어 받는다.</p> : null}
        <div className="scax-set-foot scax-set-foot--start">
          <Button variant="outlined" tone="neutral" label="다른 계정 연결" iconBefore="plus" onClick={onConnect} />
        </div>
      </Card>
    </React.Fragment>
  );
}

/* ===== 슬랙 연동 — 사용자 토큰 · 워크스페이스 한 번 연결 · 방 고르기 ===== */

const ROOM_TYPE = { channel: '채널', private: '비공개', dm: 'DM', group: '그룹 DM' };

function roomMeta(r) {
  if (r.type === 'channel') return '채널 · 공개';
  if (r.type === 'private') return '채널 · 비공개';
  if (r.type === 'dm') return 'DM';
  return `그룹 DM · ${r.members}명`;
}

function RoomMark({ type }) {
  const glyph = type === 'channel' ? '#' : type === 'private' ? '#' : type === 'dm' ? '@' : '∴';
  return <span className={`scax-set-row__mark scax-set-row__mark--${type}`} aria-hidden="true">{glyph}</span>;
}

function SlackSection({ ws, rooms, onConnect, onReconnect, onAskDisconnect, onPick, onAskRemove }) {
  const intro = <p className="scax-set-view__intro">슬랙에서 보고 싶은 채널·DM·그룹 DM 을 골라 우리 DB 로 적재한다. 내 계정으로 한 번 연결하면 고른 방이 실시간으로 쌓인다.</p>;
  if (ws.state === 'none') {
    return (
      <React.Fragment>
        {intro}
        <Card title="워크스페이스">
          <div className="scax-set-connect">
            <p className="scax-set-connect__desc">내 슬랙 계정으로 연결한다. 내가 들어가 있는 채널·비공개 채널·DM·그룹 DM 중에서 고른 방만 가져온다.</p>
            <Button variant="solid" tone="primary" label="슬랙 연결" onClick={onConnect} />
          </div>
        </Card>
      </React.Fragment>
    );
  }
  const broken = ws.state === 'broken';
  return (
    <React.Fragment>
      {intro}
      <Card title="워크스페이스" legend={broken ? '연결 끊김' : '연결됨'} end={<Button size="sm" variant="outlined" tone="neutral" label="연결 해제" onClick={onAskDisconnect} />}>
        <div className={`scax-set-row${broken ? ' scax-set-row--broken' : ''}`}>
          <span className="scax-set-row__mark scax-set-row__mark--slack" aria-hidden="true">{ws.name.slice(0, 1)}</span>
          <span className="scax-set-row__who">
            <span className="scax-set-row__name">{ws.name}</span>
            <span className="scax-set-row__meta">{ws.domain}</span>
          </span>
          <span className="scax-set-row__end">
            <LiveState status={broken ? 'broken' : 'live'} onReconnect={onReconnect} />
          </span>
        </div>
        {broken ? <p className="scax-set-card__note scax-set-card__note--danger">슬랙 연결이 끊겨 모든 방의 수집이 멈췄다. 토큰이 만료됐거나 슬랙에서 앱 권한을 거둔 경우다 — 「다시 연결」하면 멈춘 뒤의 메시지부터 이어 받는다.</p> : null}
      </Card>
      <Card title="수집 방" legend={`${rooms.length}개`} end={<Button size="sm" variant="solid" tone="primary" label="방 추가" iconBefore="plus" onClick={onPick} />}>
        <LiveStrip last="10-06 09:14" total="7,257" paused={broken} />
        {rooms.length ? (
          <ul className="scax-set-list">
            {rooms.map((r) => (
              <li className="scax-set-row" key={r.id}>
                <RoomMark type={r.type} />
                <span className="scax-set-row__who">
                  <span className="scax-set-row__name">{r.name}</span>
                  <span className="scax-set-row__meta">{roomMeta(r)} · 적재 {r.count}건</span>
                </span>
                <span className="scax-set-row__end">
                  {broken ? <span className="scax-set-state scax-set-state--paused"><span className="scax-set-state__dot" />멈춤</span> : <LiveState status={r.status} backfillLabel="과거 메시지 채우는 중" />}
                  <Button size="sm" variant="text" tone="neutral" label="빼기" onClick={() => onAskRemove(r)} />
                </span>
              </li>
            ))}
          </ul>
        ) : <p className="scax-set-card__note">고른 방이 없다. 「방 추가」에서 볼 방을 고른다.</p>}
        <p className="scax-set-card__note">방을 처음 추가하면 「과거 메시지 채우는 중」이 된다 — 슬랙이 허락하는 가장 오래된 메시지까지 거슬러 가져온 뒤 실시간으로 바뀐다.</p>
      </Card>
    </React.Fragment>
  );
}

/* 방 고르기 창 — 검색 · 묶음 탭 · 체크 · 「선택한 N개 추가」. 상태: default · loading · error (결과 없음은 검색으로) */
const PICK_TABS = [
  { value: 'all', label: '전체' },
  { value: 'channel', label: '채널' },
  { value: 'private', label: '비공개' },
  { value: 'dm', label: 'DM' },
  { value: 'group', label: '그룹 DM' },
];

function RoomPicker({ open, state, query, onQuery, added, onClose, onAdd, onRetry }) {
  const [tab, setTab] = React.useState('all');
  const [picked, setPicked] = React.useState([]);
  React.useEffect(() => { if (open) { setPicked([]); setTab('all'); } }, [open]);
  if (!open) return null;
  const q = query.trim();
  const rows = SLACK_CANDIDATES.filter((c) => (tab === 'all' || c.type === tab) && (!q || c.name.includes(q)));
  const toggle = (id) => setPicked((l) => (l.includes(id) ? l.filter((x) => x !== id) : l.concat([id])));
  const groups = tab === 'all' ? ['channel', 'private', 'dm', 'group'] : [tab];

  let body;
  if (state === 'loading') {
    body = <div className="scax-skeleton-stack">{[0, 1, 2, 3, 4].map((i) => <div className="scax-set-pick__skel" key={i}><Skeleton variant="text" /></div>)}</div>;
  } else if (state === 'error') {
    body = <StatusNote title="방 목록을 불러오지 못했습니다" desc="슬랙 연결을 확인한 뒤 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" onClick={onRetry} />} />;
  } else if (!rows.length) {
    body = <Empty icon="search" title="찾는 방이 없습니다" desc={`「${q}」 와 맞는 방이 없습니다. 이름을 다르게 적어 보세요.`} />;
  } else {
    body = groups.map((g) => {
      const list = rows.filter((r) => r.type === g);
      if (!list.length) return null;
      return (
        <section className="scax-set-pick__group" key={g}>
          {tab === 'all' ? <h3 className="scax-set-pick__caption">{ROOM_TYPE[g]} <span className="scax-set-pick__count">{list.length}</span></h3> : null}
          <ul className="scax-set-pick__list">
            {list.map((r) => {
              const isAdded = added.includes(r.id);
              const on = picked.includes(r.id);
              return (
                <li key={r.id}>
                  <label className={`scax-set-pick__row${isAdded ? ' scax-set-pick__row--added' : ''}${on ? ' scax-set-pick__row--on' : ''}`}>
                    <span className="scax-checkbox">
                      <input type="checkbox" className="scax-checkbox__input" checked={isAdded || on} disabled={isAdded} onChange={() => toggle(r.id)} />
                      <span className="scax-checkbox__box"><Icon name="check" size={14} /></span>
                    </span>
                    <RoomMark type={r.type} />
                    <span className="scax-set-pick__name">{r.name}</span>
                    {r.bot ? <span className="scax-set-app">앱</span> : null}
                    <span className="scax-set-pick__meta">{r.type === 'dm' ? 'DM' : `${r.members}명`}</span>
                    {isAdded ? <span className="scax-set-pick__added">추가됨</span> : null}
                  </label>
                </li>
              );
            })}
          </ul>
        </section>
      );
    });
  }

  return (
    <div className="scax-modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="scax-modal scax-modal--md scax-set-pick" role="dialog" aria-modal="true" aria-label="방 추가">
        <header className="scax-modal__head">
          <h2 className="scax-modal__title">방 추가</h2>
          <IconButton name="close" size={24} label="닫기" onClick={onClose} />
        </header>
        <div className="scax-set-pick__tools">
          <div className="scax-textfield scax-textfield--search">
            <Icon name="search" size={20} />
            <input className="scax-textfield__input" value={query} placeholder="방 이름이나 사람 이름으로 찾기" aria-label="방 찾기" onChange={(e) => onQuery(e.target.value)} />
          </div>
          <SegmentedControl value={tab} options={PICK_TABS} onChange={setTab} ariaLabel="방 종류" />
        </div>
        <div className="scax-modal__body scax-set-pick__body">{body}</div>
        <footer className="scax-modal__foot">
          <span className="scax-set-pick__hint">이미 추가한 방은 「추가됨」으로 표시된다</span>
          <Button variant="outlined" tone="neutral" label="취소" onClick={onClose} />
          <Button variant="solid" tone="primary" label={`선택한 ${picked.length}개 추가`} disabled={!picked.length || state !== 'default'} onClick={() => { onAdd(picked); onClose(); }} />
        </footer>
      </div>
    </div>
  );
}

/* 시안 전용 상태 토글 — 연동 상태 넷 · 방 고르기 창 상태. 제품 화면이 아니다 */
function DevSwitch({ groups }) {
  return (
    <div className="scax-state-switch scax-set-dev">
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

/* ===== 카카오톡 연동 (2026-10-06) — Mac 전용 · 조회만 =====
   Strong Hajin 데스크톱 앱(Rust)이 백그라운드로 이 Mac 의 카카오톡 로컬 DB 를 읽어 올린다. 앱이 카카오톡 실행 여부를 확인한다.
   계정은 지금 카카오톡에 로그인한 계정을 따른다(고르는 목록 없음). 고른 1:1 · 단체방만 수집하고, 오픈채팅방은 고르기 목록에 없다.
   메일·슬랙과 같은 틀: 상태 카드 → 적재 상태 3칸(셋째 「실시간」) → 수집 방 목록 → 「방 추가」 = 방 고르기 창.
   kstate: 'no-app' 앱 없음 · 'app-off' 앱 꺼짐 · 'kakao-off' 앱 켜짐+카카오톡 꺼짐 · 'live' 정상 · 'backfill' 과거 채우는 중 */

const KAKAO_TYPE = { direct: '1:1', group: '단체방' };

function kakaoMeta(r) { return r.type === 'direct' ? '1:1' : `단체방 · ${r.members}명`; }

function KakaoMark({ type }) {
  return <span className={`scax-set-row__mark scax-set-row__mark--kakao-${type}`} aria-hidden="true">{type === 'direct' ? '1' : '∴'}</span>;
}

/* 상태 칸 하나 — 이름 · 값(점) · 보조 */
function KakaoCell({ label, value, tone, sub }) {
  return (
    <div className="scax-set-kstat">
      <span className="scax-set-kstat__label">{label}</span>
      <span className={`scax-set-kstat__value scax-set-kstat__value--${tone}`}><span className="scax-set-state__dot" />{value}</span>
      {sub ? <span className="scax-set-kstat__sub">{sub}</span> : null}
    </div>
  );
}

function KakaoSection({ kstate, rooms, onPick, onAskRemove }) {
  const st = KAKAO_STATUS;
  const intro = <p className="scax-set-view__intro">이 Mac 의 카카오톡에서 고른 1:1 · 단체방의 대화를 우리 DB 로 적재한다. 조회만 한다 — 메시지함에서 보내지는 않는다. Mac 에서만 된다.</p>;
  if (kstate === 'no-app') {
    return (
      <React.Fragment>
        {intro}
        <Card title="Strong Hajin 앱">
          <div className="scax-set-connect">
            <p className="scax-set-connect__desc">Mac 앱을 설치하고 켜 두면 카톡이 쌓입니다. 앱이 이 Mac 의 카카오톡을 읽어 고른 방의 대화를 올린다 — 오픈채팅방은 수집하지 않는다.</p>
            <a className="scax-set-applink" href="#download-mac-app" onClick={(e) => e.preventDefault()}><Icon name="arrow-down" size={16} />Mac 앱 받기</a>
          </div>
        </Card>
      </React.Fragment>
    );
  }
  const appOn = kstate !== 'app-off';
  const kakaoOn = appOn && kstate !== 'kakao-off';
  const paused = !kakaoOn;
  const pausedLabel = appOn ? '멈춤 — 카카오톡 꺼짐' : '멈춤 — Mac 앱 꺼짐';
  return (
    <React.Fragment>
      {intro}
      <Card title="수집 상태" legend={paused ? '멈춤' : '실시간'}>
        <div className="scax-set-kstats">
          <KakaoCell label="Strong Hajin 앱" value={appOn ? '연결됨' : '꺼짐'} tone={appOn ? 'on' : 'off'} sub={appOn ? `${st.device} · v${st.appVersion}` : `마지막 연결 ${st.lastSeen}`} />
          <KakaoCell label="카카오톡" value={!appOn ? '알 수 없음' : kakaoOn ? '실행 중' : '꺼짐'} tone={!appOn ? 'idle' : kakaoOn ? 'on' : 'off'} sub={!appOn ? '앱이 꺼져 있어 확인하지 못한다' : kakaoOn ? '이 Mac 에서 로그인됨' : '카카오톡을 켜면 이어 받는다'} />
          <KakaoCell label="로그인 계정" value={st.account} tone="plain" sub={st.kakaoId} />
          <KakaoCell label="마지막 수집" value={st.lastSync} tone="plain" sub={paused ? '멈춘 뒤의 대화는 다시 켜면 채운다' : '새 대화가 오면 바로 올라간다'} />
        </div>
        <p className="scax-set-card__note">계정은 지금 이 Mac 카카오톡에 로그인한 계정을 따른다. 다른 계정으로 바꾸려면 카카오톡에서 다시 로그인한다.</p>
      </Card>
      <Card title="수집 방" legend={`${rooms.length}개`} end={<Button size="sm" variant="solid" tone="primary" label="방 추가" iconBefore="plus" onClick={onPick} />}>
        <LiveStrip last={st.lastSync} total="6,836" paused={paused} pausedLabel={pausedLabel} />
        {rooms.length ? (
          <ul className="scax-set-list">
            {rooms.map((r) => (
              <li className="scax-set-row" key={r.id}>
                <KakaoMark type={r.type} />
                <span className="scax-set-row__who">
                  <span className="scax-set-row__name">{r.name}</span>
                  <span className="scax-set-row__meta">{kakaoMeta(r)} · 적재 {r.count}건</span>
                </span>
                <span className="scax-set-row__end">
                  {paused ? <span className="scax-set-state scax-set-state--paused"><span className="scax-set-state__dot" />멈춤</span> : <LiveState status={r.status} backfillLabel="과거 대화 채우는 중" />}
                  <Button size="sm" variant="text" tone="neutral" label="빼기" onClick={() => onAskRemove(r)} />
                </span>
              </li>
            ))}
          </ul>
        ) : <p className="scax-set-card__note">고른 방이 없다. 「방 추가」에서 볼 방을 고른다.</p>}
        <p className="scax-set-card__note">방을 처음 추가하면 「과거 대화 채우는 중」이 된다 — 이 Mac 카카오톡에 남아 있는 만큼 거슬러 가져온 뒤 실시간으로 바뀐다.</p>
      </Card>
    </React.Fragment>
  );
}

/* 카톡 방 고르기 창 — 검색 · 전체/1:1/단체방 · 체크 · 추가됨 · 「선택한 N개 추가」. 목록은 Mac 앱이 읽은 방 */
const KAKAO_PICK_TABS = [
  { value: 'all', label: '전체' },
  { value: 'direct', label: '1:1' },
  { value: 'group', label: '단체방' },
];

function KakaoPicker({ open, state, appOn, query, onQuery, added, onClose, onAdd, onRetry }) {
  const [tab, setTab] = React.useState('all');
  const [picked, setPicked] = React.useState([]);
  React.useEffect(() => { if (open) { setPicked([]); setTab('all'); } }, [open]);
  if (!open) return null;
  const q = query.trim();
  const rows = KAKAO_CANDIDATES.filter((c) => (tab === 'all' || c.type === tab) && (!q || c.name.includes(q)));
  const toggle = (id) => setPicked((l) => (l.includes(id) ? l.filter((x) => x !== id) : l.concat([id])));
  const groups = tab === 'all' ? ['direct', 'group'] : [tab];

  let body;
  if (!appOn) {
    body = <Empty icon="blank" title="Mac 앱이 켜져 있어야 방 목록을 볼 수 있습니다" desc="방 목록은 Strong Hajin 앱이 이 Mac 의 카카오톡에서 읽어 온다. 앱을 켠 뒤 다시 연다." />;
  } else if (state === 'loading') {
    body = <div className="scax-skeleton-stack">{[0, 1, 2, 3, 4].map((i) => <div className="scax-set-pick__skel" key={i}><Skeleton variant="text" /></div>)}</div>;
  } else if (state === 'error') {
    body = <StatusNote title="방 목록을 불러오지 못했습니다" desc="Mac 앱이 카카오톡을 읽지 못했습니다. 카카오톡이 켜져 있는지 확인한 뒤 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" onClick={onRetry} />} />;
  } else if (!rows.length) {
    body = <Empty icon="search" title="찾는 방이 없습니다" desc={`「${q}」 와 맞는 방이 없습니다. 이름을 다르게 적어 보세요.`} />;
  } else {
    body = groups.map((g) => {
      const list = rows.filter((r) => r.type === g);
      if (!list.length) return null;
      return (
        <section className="scax-set-pick__group" key={g}>
          {tab === 'all' ? <h3 className="scax-set-pick__caption">{KAKAO_TYPE[g]} <span className="scax-set-pick__count">{list.length}</span></h3> : null}
          <ul className="scax-set-pick__list">
            {list.map((r) => {
              const isAdded = added.includes(r.id);
              const on = picked.includes(r.id);
              return (
                <li key={r.id}>
                  <label className={`scax-set-pick__row${isAdded ? ' scax-set-pick__row--added' : ''}${on ? ' scax-set-pick__row--on' : ''}`}>
                    <span className="scax-checkbox">
                      <input type="checkbox" className="scax-checkbox__input" checked={isAdded || on} disabled={isAdded} onChange={() => toggle(r.id)} />
                      <span className="scax-checkbox__box"><Icon name="check" size={14} /></span>
                    </span>
                    <KakaoMark type={r.type} />
                    <span className="scax-set-pick__name">{r.name}</span>
                    <span className="scax-set-pick__meta">{r.type === 'direct' ? '1:1' : `참여 ${r.members}명`}</span>
                    {isAdded ? <span className="scax-set-pick__added">추가됨</span> : null}
                  </label>
                </li>
              );
            })}
          </ul>
        </section>
      );
    });
  }

  return (
    <div className="scax-modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="scax-modal scax-modal--md scax-set-pick" role="dialog" aria-modal="true" aria-label="카카오톡 방 추가">
        <header className="scax-modal__head">
          <h2 className="scax-modal__title">카카오톡 방 추가</h2>
          <IconButton name="close" size={24} label="닫기" onClick={onClose} />
        </header>
        <div className="scax-set-pick__tools">
          <div className="scax-textfield scax-textfield--search">
            <Icon name="search" size={20} />
            <input className="scax-textfield__input" value={query} placeholder="방 이름이나 사람 이름으로 찾기" aria-label="방 찾기" disabled={!appOn} onChange={(e) => onQuery(e.target.value)} />
          </div>
          <SegmentedControl value={tab} options={KAKAO_PICK_TABS} onChange={setTab} ariaLabel="방 종류" />
        </div>
        <div className="scax-modal__body scax-set-pick__body">{body}</div>
        <footer className="scax-modal__foot">
          <span className="scax-set-pick__hint">이 Mac 카카오톡의 1:1 · 단체방만 나온다 (오픈채팅방 제외)</span>
          <Button variant="outlined" tone="neutral" label="취소" onClick={onClose} />
          <Button variant="solid" tone="primary" label={`선택한 ${picked.length}개 추가`} disabled={!picked.length || state !== 'default' || !appOn} onClick={() => { onAdd(picked); onClose(); }} />
        </footer>
      </div>
    </div>
  );
}

/* ===== 프로필 설정 (2026-10-06 — 앞 판 「계정 설정」) =====
   구획 셋: 프로필 이미지 · AX 캐릭터 · 비밀번호 변경.
   이름 · 소속 · 직책 · 직무는 조직 명부에서 오는 값이라 입력칸이 없다 — 머리에 읽기 전용으로만 보인다.
   이미지는 고르면 바로 올라가 저장된다(「프로필 저장」 단추 없음). 캐릭터도 고르면 바로 저장된다(앱의 캐릭터 고르기와 같은 규칙). */

const IMAGE_LIMIT = 1024 * 1024; /* 정사각형 1MB 이하 PNG · JPG — 앞 시안 문구 그대로 */

/* AX 캐릭터 후보 — 앱 frontend/src/features/assistant/assistantCharacterAssets.ts 의 목록 그대로.
   그림(avif)은 시안 프로젝트에 없어서 앱 부품의 대체 글자(fallbackLabel)로 그린다 */
const AX_CHARACTERS = [
  { key: 'cream-cat', name: '크림 고양이', fallbackLabel: '크' },
  { key: 'silver-tabby', name: '실버 태비', fallbackLabel: '실' },
  { key: 'tuxedo-cat', name: '턱시도', fallbackLabel: '턱' },
  { key: 'calico-cat', name: '삼색 고양이', fallbackLabel: '삼' },
  { key: 'puppy', name: '강아지', fallbackLabel: '강' },
  { key: 'rabbit', name: '토끼', fallbackLabel: '토' },
  { key: 'bear', name: '곰', fallbackLabel: '곰' },
  { key: 'chick', name: '병아리', fallbackLabel: '병' },
  { key: 'red-panda', name: '레서판다', fallbackLabel: '레' },
];

function fmtMB(bytes) { return `${(bytes / 1024 / 1024).toFixed(1)}MB`; }

function ProfileImageCard({ me, demo }) {
  const { DropZone } = window.SCAX_DS || {};
  const [image, setImage] = React.useState(demo === 'none' ? null : (demo === 'uploading' ? null : me.avatar));
  const [uploading, setUploading] = React.useState(demo === 'uploading' ? { name: 'profile-new.png' } : null);
  const [error, setError] = React.useState(demo === 'too-big' ? { name: 'IMG_2041.jpg', size: 2.4 * 1024 * 1024 } : null);
  const timer = React.useRef(null);
  React.useEffect(() => () => clearTimeout(timer.current), []);
  const take = (files) => {
    const f = files[0];
    if (!f) return;
    if (f.size > IMAGE_LIMIT) { setError({ name: f.name, size: f.size }); return; }
    setError(null);
    setUploading({ name: f.name });
    /* 고르면 바로 올라가 저장된다. 시안에선 1.2초 뒤 기본 이미지로 바뀐다 */
    timer.current = setTimeout(() => { setUploading(null); setImage(me.avatar); }, 1200);
  };
  return (
    <Card title="프로필 이미지">
      <div className="scax-set-avatar">
        <span className={`scax-set-avatar__frame${uploading ? ' scax-set-avatar__frame--busy' : ''}`}>
          {image ? <img className="scax-set-avatar__img" src={image} alt="현재 프로필 이미지" /> : <span className="scax-set-avatar__initial" aria-label="프로필 이미지 없음">{me.name.slice(0, 1)}</span>}
          {uploading ? <span className="scax-set-avatar__busy">올리는 중…</span> : null}
        </span>
        <div className="scax-set-avatar__side">
          {DropZone ? (
            <DropZone
              drop="이미지를 끌어다 놓거나 고르세요"
              pickLabel="이미지 변경"
              hint="정사각형 1MB 이하 PNG · JPG"
              accept="image/png,image/jpeg"
              disabled={!!uploading}
              onFiles={take}
            />
          ) : null}
          {error ? <p className="scax-set-error" role="alert">{error.name} 은(는) {fmtMB(error.size)} 라 올릴 수 없다 — 1MB 이하로 줄여서 다시 고른다.</p> : null}
          <div className="scax-set-avatar__row">
            <span className="scax-set-row__meta">{image ? 'avatar-person.png · 240×240 · 고르면 바로 바뀐다' : '이미지가 없으면 이름 첫 글자로 보인다'}</span>
            {image ? <Button size="sm" variant="text" tone="neutral" label="이미지 삭제" disabled={!!uploading} onClick={() => setImage(null)} /> : null}
          </div>
        </div>
      </div>
    </Card>
  );
}

/* 앱의 「내 AX 캐릭터」 고르기를 이 자리로 옮겼다 — 후보 · 이름 · 「사용 가능」 · 고르면 바로 저장 · 실패하면 이전 값으로 되돌림 */
function CharacterCard({ demo }) {
  const [current, setCurrent] = React.useState('cream-cat');
  const [busy, setBusy] = React.useState(demo === 'saving');
  const [error, setError] = React.useState(demo === 'failed' ? 'AX 캐릭터 설정을 저장하지 못했습니다.' : null);
  const timer = React.useRef(null);
  React.useEffect(() => () => clearTimeout(timer.current), []);
  const choose = (key) => {
    if (busy || key === current) return;
    const previous = current;
    setError(null); setBusy(true); setCurrent(key);
    timer.current = setTimeout(() => { setBusy(false); if (demo === 'failed') { setCurrent(previous); setError('AX 캐릭터 설정을 저장하지 못했습니다.'); } }, 900);
  };
  return (
    <Card title="AX 캐릭터" legend={busy ? '저장 중…' : null} note="런처와 AX 답변에 표시할 캐릭터를 선택하세요. 고르면 바로 저장된다.">
      {error ? <p className="scax-set-error" role="alert">{error}</p> : null}
      <div className="scax-set-chars" role="radiogroup" aria-label="AX 캐릭터 목록">
        {AX_CHARACTERS.map((c) => (
          <button
            key={c.key}
            type="button"
            role="radio"
            aria-checked={current === c.key}
            aria-label={`${c.name} 선택`}
            className="scax-set-char"
            disabled={busy}
            onClick={() => choose(c.key)}
          >
            <span className="scax-set-char__face" aria-hidden="true">{c.fallbackLabel}</span>
            <b>{c.name}</b>
            <small>사용 가능</small>
          </button>
        ))}
      </div>
    </Card>
  );
}

function PasswordCard({ demo }) {
  const wrong = demo === 'wrong';
  const mismatch = demo === 'mismatch';
  return (
    <Card title="비밀번호 변경" note="8자 이상, 영문·숫자·기호를 두 종류 이상 섞는다. 변경하면 다른 기기의 로그인이 모두 해제된다.">
      <div className="scax-set-form scax-set-form--row scax-set-form--pw">
        <Field label="현재 비밀번호">
          <input className={`scax-set-input${wrong ? ' scax-set-input--error' : ''}`} type="password" placeholder="••••••••" defaultValue={wrong ? 'wrongpass' : undefined} />
          {wrong ? <span className="scax-set-error scax-set-error--field">현재 비밀번호가 맞지 않습니다.</span> : null}
        </Field>
        <Field label="새 비밀번호">
          <input className="scax-set-input" type="password" placeholder="••••••••" defaultValue={wrong || mismatch ? 'newpass2026!' : undefined} />
        </Field>
        <Field label="새 비밀번호 확인">
          <input className={`scax-set-input${mismatch ? ' scax-set-input--error' : ''}`} type="password" placeholder="••••••••" defaultValue={wrong ? 'newpass2026!' : mismatch ? 'newpass2025!' : undefined} />
          {mismatch ? <span className="scax-set-error scax-set-error--field">새 비밀번호가 서로 다릅니다.</span> : null}
        </Field>
      </div>
      <div className="scax-set-foot"><Button variant="solid" tone="primary" label="비밀번호 변경" disabled={mismatch} /></div>
    </Card>
  );
}

function ProfileSection({ me, imageDemo, charDemo, pwDemo }) {
  return (
    <React.Fragment>
      <section className="scax-set-me" aria-label="내 정보">
        {me.avatar && imageDemo !== 'none' ? <img className="scax-set-me__avatar" src={me.avatar} alt="" /> : <span className="scax-set-me__avatar scax-set-me__avatar--initial" aria-hidden="true">{me.name.slice(0, 1)}</span>}
        <dl className="scax-set-me__facts">
          <div><dt>이름</dt><dd>{me.name}</dd></div>
          <div><dt>소속</dt><dd>{me.unit}</dd></div>
          <div><dt>직책</dt><dd>{me.position}</dd></div>
          <div><dt>직무</dt><dd>{me.duty}</dd></div>
        </dl>
        <p className="scax-set-me__note">조직 명부에서 관리됩니다 — 바꿀 일이 있으면 관리자에게 요청한다.</p>
      </section>
      <ProfileImageCard key={`img-${imageDemo}`} me={me} demo={imageDemo} />
      <CharacterCard key={`char-${charDemo}`} demo={charDemo} />
      <PasswordCard key={`pw-${pwDemo}`} demo={pwDemo} />
    </React.Fragment>
  );
}

/* ===== 알림 설정 (2026-10-07) — 앱 알림만 =====
   받는 경로(앱 · 메일 · 슬랙 DM) 줄은 걷었다 — 이번엔 앱 알림만이다. 앱이 켜져 있으면 시스템 알림으로도 뜬다.
   맨 위 전체 on/off → 테마 셋(업무 · 메시지 · 회의, 알림 목록의 분류와 같다) 머리마다 on/off → 아래 항목 체크.
   전체를 끄면 아래가 전부, 테마를 끄면 그 항목들이 흐려진다(값은 그대로 남아 다시 켜면 돌아온다). */

function NotifyItem({ item, disabled, onToggle }) {
  return (
    <li>
      <label className={`scax-set-notify__item${disabled ? ' scax-set-notify__item--off' : ''}`}>
        <span className="scax-checkbox">
          <input type="checkbox" className="scax-checkbox__input" checked={item.on} disabled={disabled} onChange={onToggle} />
          <span className="scax-checkbox__box"><Icon name="check" size={14} /></span>
        </span>
        <span className="scax-set-row__who">
          <span className="scax-set-row__name">{item.label}</span>
          {item.desc ? <span className="scax-set-row__meta">{item.desc}</span> : null}
        </span>
      </label>
    </li>
  );
}

function NotifySection({ master, groups, onMaster, onTheme, onToggle }) {
  return (
    <React.Fragment>
      <p className="scax-set-view__intro">받을 알림을 고른다. 앱이 켜져 있으면 시스템 알림으로도 뜬다.</p>
      <section className="scax-set-card scax-set-notify__master">
        <div className="scax-switch-row">
          <span className="scax-switch-row__who">
            <span className="scax-set-row__name">알림 받기</span>
            <span className="scax-set-row__meta">{master ? '아래에서 고른 알림을 받는다' : '알림을 하나도 받지 않는다 — 아래 고른 값은 그대로 남는다'}</span>
          </span>
          <Switch on={master} label="알림 받기" onToggle={onMaster} />
        </div>
      </section>
      {groups.map((g) => {
        const themeOff = !master || !g.on;
        const picked = g.items.filter((i) => i.on).length;
        return (
          <section className={`scax-set-card scax-set-notify${!master ? ' scax-set-notify--off' : ''}`} key={g.id}>
            <header className="scax-set-card__head scax-set-notify__head">
              <h2 className="scax-set-card__title">{g.title}</h2>
              <span className="scax-set-card__legend">{g.on ? `${g.items.length}개 중 ${picked}개` : '꺼짐'}</span>
              <Switch on={g.on} label={`${g.title} 알림`} onToggle={() => master && onTheme(g.id)} />
            </header>
            <ul className={`scax-set-notify__list${themeOff ? ' scax-set-notify__list--off' : ''}`}>
              {g.items.map((it) => <NotifyItem key={it.id} item={it} disabled={themeOff} onToggle={() => onToggle(g.id, it.id)} />)}
            </ul>
            {g.note ? <p className={`scax-set-card__note${themeOff ? ' scax-set-notify__list--off' : ''}`}>{g.note}</p> : null}
          </section>
        );
      })}
    </React.Fragment>
  );
}

/* ===== 화면 ===== */

let addSeq = 0;

/* 연동 상태 넷 — 시안에서 DevSwitch 로 바꿔 본다 */
const LINK_STATES = [
  { value: 'none', label: '연결 전' },
  { value: 'live', label: '연결됨' },
  { value: 'backfill', label: '과거 채우는 중' },
  { value: 'broken', label: '연결 끊김' },
];
const KAKAO_STATES = [
  { value: 'no-app', label: '앱 없음' },
  { value: 'app-off', label: '앱 꺼짐' },
  { value: 'kakao-off', label: '카톡 꺼짐' },
  { value: 'live', label: '정상' },
  { value: 'backfill', label: '과거 채우는 중' },
];
function kakaoFor(state) {
  if (state === 'backfill') return KAKAO_ROOMS.concat([{ id: 'k7', type: 'group', name: '파일럿 2차 TF', members: 7, count: '486', status: 'backfill' }]);
  return KAKAO_ROOMS;
}
const IMAGE_STATES = [
  { value: 'none', label: '없음' },
  { value: 'has', label: '있음' },
  { value: 'uploading', label: '올리는 중' },
  { value: 'too-big', label: '용량 초과' },
];
const CHAR_STATES = [
  { value: 'default', label: '기본' },
  { value: 'saving', label: '저장 중' },
  { value: 'failed', label: '저장 실패' },
];
const PW_STATES = [
  { value: 'default', label: '기본' },
  { value: 'mismatch', label: '불일치' },
  { value: 'wrong', label: '현재 틀림' },
];
const PICK_STATES = [
  { value: 'default', label: '기본' },
  { value: 'loading', label: '로딩' },
  { value: 'empty', label: '결과 없음' },
  { value: 'error', label: '오류' },
];

function mailFor(state) {
  if (state === 'none') return [];
  if (state === 'backfill') return MAIL_ACCOUNTS.concat([MAIL_BACKFILL]);
  if (state === 'broken') return MAIL_ACCOUNTS.map((a) => (a.id === 'm2' ? Object.assign({}, a, { status: 'broken', synced: '10-03 22:41' }) : a));
  return MAIL_ACCOUNTS;
}

function slackFor(state) {
  const ws = Object.assign({}, SLACK_WORKSPACE, { state: state === 'none' ? 'none' : state === 'broken' ? 'broken' : 'live' });
  if (state === 'none') return { ws, rooms: [] };
  if (state === 'backfill') {
    return { ws, rooms: SLACK_ROOMS.concat([
      { id: 'C04', type: 'channel', name: '#design-review', members: 11, count: '1,962', status: 'backfill' },
      { id: 'G02', type: 'group', name: '한서윤, 오지훈, 서지안', members: 4, count: '214', status: 'backfill' },
    ]) };
  }
  return { ws, rooms: SLACK_ROOMS };
}

function SettingsPage() {
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [section, setSection] = React.useState('mail');
  const [linkState, setLinkState] = React.useState('live');
  const [mail, setMail] = React.useState(() => mailFor('live'));
  const [slack, setSlack] = React.useState(() => slackFor('live'));
  const [kstate, setKstate] = React.useState('live');
  const [kakao, setKakao] = React.useState(KAKAO_ROOMS);
  const [kpickOpen, setKpickOpen] = React.useState(false);
  const [notifyOn, setNotifyOn] = React.useState(true);
  const [groups, setGroups] = React.useState(NOTIFY_GROUPS);
  const [confirm, setConfirm] = React.useState(null);
  const [pickOpen, setPickOpen] = React.useState(false);
  const [pickState, setPickState] = React.useState('default');
  const [pickQuery, setPickQuery] = React.useState('');
  const [imageDemo, setImageDemo] = React.useState('has');
  const [charDemo, setCharDemo] = React.useState('default');
  const [pwDemo, setPwDemo] = React.useState('default');

  const changeLink = (v) => { setLinkState(v); setMail(mailFor(v)); setSlack(slackFor(v)); };
  const changePick = (v) => { setPickState(v === 'empty' ? 'default' : v); setPickQuery(v === 'empty' ? '없는 방' : ''); };


  /* 메일 */
  const connectMail = () => {
    addSeq += 1;
    setMail((l) => l.concat([{ id: `m-new-${addSeq}`, addr: l.length ? `team${addSeq}@company.example` : 'haram@company.example', count: '0', status: 'backfill', synced: '방금' }]));
  };
  const reconnectMail = (id) => setMail((l) => l.map((a) => (a.id === id ? Object.assign({}, a, { status: 'live', synced: '방금' }) : a)));
  const askRemoveMail = (a) => setConfirm({
    title: '메일 계정 연결 해제',
    lines: [`${a.addr} 에서 더 이상 메일을 받지 않는다.`, '이 계정으로 쌓인 메일은 메시지함에서 사라진다.'],
    cta: '연결 해제',
    run: () => setMail((l) => l.filter((x) => x.id !== a.id)),
  });

  /* 슬랙 */
  const connectSlack = () => setSlack({ ws: Object.assign({}, SLACK_WORKSPACE, { state: 'live' }), rooms: [] });
  const reconnectSlack = () => setSlack((s) => ({ ws: Object.assign({}, s.ws, { state: 'live' }), rooms: s.rooms }));
  const askDisconnectSlack = () => setConfirm({
    title: '슬랙 연결 해제',
    lines: [`${slack.ws.name} 워크스페이스의 모든 방에서 더 이상 메시지를 받지 않는다.`, '이 워크스페이스에서 쌓인 메시지는 메시지함에서 사라진다.'],
    cta: '연결 해제',
    run: () => setSlack({ ws: Object.assign({}, SLACK_WORKSPACE, { state: 'none' }), rooms: [] }),
  });
  const askRemoveRoom = (r) => setConfirm({
    title: '방 빼기',
    lines: [`${r.name} 에서 더 이상 메시지를 받지 않는다.`, '이 방에서 쌓인 메시지는 메시지함에서 사라진다.'],
    cta: '빼기',
    run: () => setSlack((s) => ({ ws: s.ws, rooms: s.rooms.filter((x) => x.id !== r.id) })),
  });
  const addRooms = (ids) => setSlack((s) => ({
    ws: s.ws,
    rooms: s.rooms.concat(SLACK_CANDIDATES.filter((c) => ids.includes(c.id)).map((c) => Object.assign({}, c, { count: '0', status: 'backfill' }))),
  }));
  const openPicker = () => { setPickQuery(''); setPickState('default'); setPickOpen(true); };

  /* 카톡 */
  const changeKakao = (v) => { setKstate(v); setKakao(kakaoFor(v)); };
  const openKakaoPicker = () => { setPickQuery(''); setPickState('default'); setKpickOpen(true); };
  const addKakaoRooms = (ids) => setKakao((l) => l.concat(KAKAO_CANDIDATES.filter((c) => ids.includes(c.id)).map((c) => Object.assign({}, c, { count: '0', status: 'backfill' }))));
  const askRemoveKakao = (r) => setConfirm({
    title: '방 빼기',
    lines: [`${r.name} 에서 더 이상 대화를 받지 않는다.`, '이 방에서 쌓인 대화는 메시지함에서 사라진다.'],
    cta: '빼기',
    run: () => setKakao((l) => l.filter((x) => x.id !== r.id)),
  });

  const toggleItem = (gid, iid) => setGroups((gs) => gs.map((g) => (g.id !== gid ? g : Object.assign({}, g, {
    items: g.items.map((i) => (i.id === iid ? Object.assign({}, i, { on: !i.on }) : i)),
  }))));
  const toggleTheme = (gid) => setGroups((gs) => gs.map((g) => (g.id === gid ? Object.assign({}, g, { on: !g.on }) : g)));

  const counts = { mail: mail.length, slack: slack.rooms.length, kakao: kstate === 'no-app' ? 0 : kakao.length };
  const titles = { mail: '메일 연동', slack: '슬랙 연동', kakao: '카카오톡 연동', account: '프로필 설정', notify: '알림 설정' };

  const devGroups = [];
  if (section === 'mail' || section === 'slack') devGroups.push({ label: '연동', value: linkState, options: LINK_STATES, onChange: changeLink });
  if (section === 'account') {
    devGroups.push({ label: '이미지', value: imageDemo, options: IMAGE_STATES, onChange: setImageDemo });
    devGroups.push({ label: '캐릭터', value: charDemo, options: CHAR_STATES, onChange: setCharDemo });
    devGroups.push({ label: '비밀번호', value: pwDemo, options: PW_STATES, onChange: setPwDemo });
  }
  if (section === 'kakao') devGroups.push({ label: '카톡', value: kstate, options: KAKAO_STATES, onChange: changeKakao });
  if (pickOpen || kpickOpen) devGroups.push({ label: '방 고르기', value: pickQuery === '없는 방' ? 'empty' : pickState, options: PICK_STATES, onChange: changePick });

  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="setting" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader title={titles[section]} />
        <AppBody railLeft={<GutterList title="설정 메뉴"><SetNav active={section} onSelect={setSection} counts={counts} /></GutterList>}>
          <div className="scax-set-view">
            {section === 'mail' ? <MailSection list={mail} onConnect={connectMail} onReconnect={reconnectMail} onAskRemove={askRemoveMail} /> : null}
            {section === 'slack' ? <SlackSection ws={slack.ws} rooms={slack.rooms} onConnect={connectSlack} onReconnect={reconnectSlack} onAskDisconnect={askDisconnectSlack} onPick={openPicker} onAskRemove={askRemoveRoom} /> : null}
            {section === 'kakao' ? <KakaoSection kstate={kstate} rooms={kstate === 'no-app' ? [] : kakao} onPick={openKakaoPicker} onAskRemove={askRemoveKakao} /> : null}
            {section === 'account' ? <ProfileSection me={MY_PROFILE} imageDemo={imageDemo} charDemo={charDemo} pwDemo={pwDemo} /> : null}
            {section === 'notify' ? <NotifySection master={notifyOn} groups={groups} onMaster={() => setNotifyOn((v) => !v)} onTheme={toggleTheme} onToggle={toggleItem} /> : null}
          </div>
        </AppBody>
      </AppShell>
      <RoomPicker
        open={pickOpen}
        state={pickState}
        query={pickQuery}
        onQuery={setPickQuery}
        added={slack.rooms.map((r) => r.id)}
        onClose={() => setPickOpen(false)}
        onAdd={addRooms}
        onRetry={() => setPickState('default')}
      />
      <KakaoPicker
        open={kpickOpen}
        state={pickState}
        appOn={kstate !== 'app-off'}
        query={pickQuery}
        onQuery={setPickQuery}
        added={kakao.map((r) => r.id)}
        onClose={() => setKpickOpen(false)}
        onAdd={addKakaoRooms}
        onRetry={() => setPickState('default')}
      />
      <ConfirmBox confirm={confirm} onClose={() => setConfirm(null)} />
      {devGroups.length ? <DevSwitch groups={devGroups} /> : null}
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<SettingsPage />);
