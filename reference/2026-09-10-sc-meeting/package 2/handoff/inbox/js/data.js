/* 「메시지함」 목데이터 — 사람·회사·사이트·파일은 전부 가상이다.
   메일은 단건(kind: 'mail'), 슬랙·카톡은 대화방 단위(kind: 'room' — 슬랙 채널 · DM · 그룹 DM / 카톡 1:1 · 단체방)로 쌓인다.
   메일·슬랙은 읽고 답장한다(design-change-3). 카톡은 조회만 한다.

   슬랙 메시지 body 는 블록 배열이다.
     { p: [세그먼트…] } · { ul: [항목…] } · { ol: [항목…] }
     항목 = [세그먼트…] 또는 { segs: [세그먼트…], sub: [[세그먼트…], …] } (들여쓴 하위 목록)
     세그먼트 = '글자' | { b } 굵게 | { code } 인라인 코드 | { mention } @멘션 | { link, href } 링크 | { emoji }
   첨부: images[{ name, size, caption }] · files[{ name, type, size }] · pdf{ name, size, pages, preview } · unfurl{ site, title, desc, domain, thumb }
   reactions[{ emoji, count }] · thread{ count, last, replies[메시지…] } */

const SLACK_USERS = {
  me: { name: '유하람', initial: '유', tone: 'a' },
  seoyoon: { name: '한서윤', initial: '한', tone: 'b' },
  jihoon: { name: '오지훈', initial: '오', tone: 'c' },
  daeun: { name: '문다은', initial: '문', tone: 'd' },
  sungmin: { name: '배성민', initial: '배', tone: 'e' },
  deploybot: { name: '배포 알리미', initial: '배', tone: 'bot', bot: true },
};

const MAIL_ITEMS = [
  {
    id: 'm1', kind: 'mail', source: 'mail', sourceLabel: '메일', unread: true,
    title: '[노을랩] 2차 파일럿 일정표 공유드립니다',
    from: { name: '서지안', addr: 'jian.seo@noeul-lab.example' },
    to: [{ name: '유하람', addr: 'haram@company.example' }],
    cc: [{ name: '한서윤', addr: 'seoyoon@company.example' }, { name: '노을랩 운영팀', addr: 'ops@noeul-lab.example' }],
    date: '2026년 10월 6일 (화) 오전 9:04', dateShort: '09:04', account: 'haram@company.example',
    excerpt: '2차 파일럿 일정표를 공유드립니다. 표의 3주차 일정이 바뀌었으니 확인 부탁드립니다.',
    html: [
      '<p>유하람님, 안녕하세요. 노을랩 서지안입니다.</p>',
      '<p>지난주 회의에서 말씀 나눈 <b>2차 파일럿 일정표</b>를 공유드립니다. 표의 <b>3주차</b> 일정이 하루 당겨졌습니다.</p>',
      '<table><thead><tr><th>주차</th><th>기간</th><th>내용</th><th>담당</th></tr></thead><tbody>',
      '<tr><td>1주차</td><td>10/13 – 10/17</td><td>환경 구성 · 계정 발급</td><td>노을랩</td></tr>',
      '<tr><td>2주차</td><td>10/20 – 10/24</td><td>사용자 교육 2회</td><td>공동</td></tr>',
      '<tr><td>3주차</td><td><b>10/26</b> – 10/31</td><td>현장 적용 · 중간 점검</td><td>공동</td></tr>',
      '</tbody></table>',
      '<p>첨부한 일정표와 범위 문서도 함께 봐 주세요.</p>',
      '<div class="sig"><b>서지안</b> | 노을랩 사업운영팀<br>02-000-0000 · jian.seo@noeul-lab.example</div>',
    ].join(''),
    quoted: [
      '<p class="quote-head">2026년 10월 2일 (금) 오후 4:10, 유하람 &lt;haram@company.example&gt; 작성:</p>',
      '<blockquote><p>지안님, 2차 일정표 정리되면 공유 부탁드립니다. 3주차는 현장 사정에 맞춰 조정 가능합니다.</p></blockquote>',
    ].join(''),
    attachments: [
      { name: '2차_파일럿_일정표.xlsx', type: 'xlsx', size: '48 KB' },
      { name: '파일럿_범위_v2.pdf', type: 'pdf', size: '1.2 MB' },
    ],
  },
  {
    id: 'm2', kind: 'mail', source: 'mail', sourceLabel: '메일', unread: true,
    title: '현장 사진 보내드립니다 (설치 완료)',
    from: { name: '배성민', addr: 'sungmin@company.example' },
    to: [{ name: '유하람', addr: 'haram@company.example' }, { name: '문다은', addr: 'daeun@company.example' }],
    cc: [],
    date: '2026년 10월 5일 (월) 오후 5:42', dateShort: '어제', account: 'haram@company.example',
    excerpt: '오늘 설치 끝난 현장 사진 보내드립니다. 2번 사진의 배선은 내일 정리 예정입니다.',
    html: [
      '<p>하람님, 다은님</p>',
      '<p>오늘 설치 끝난 현장 사진 보내드립니다.</p>',
      '<ul><li>1번 — 입구 쪽 단말 2대</li><li>2번 — 배선 (내일 정리 예정)</li></ul>',
      '<p>추가로 필요한 각도 있으면 말씀 주세요.</p>',
      '<div class="sig">배성민 드림</div>',
    ].join(''),
    quoted: null,
    attachments: [
      { name: '현장_입구.jpg', type: 'jpg', size: '2.4 MB', image: true, caption: '입구 단말' },
      { name: '현장_배선.jpg', type: 'jpg', size: '2.1 MB', image: true, caption: '배선' },
    ],
  },
  {
    id: 'm3', kind: 'mail', source: 'mail', sourceLabel: '메일', unread: false,
    title: '[주간] 10월 1주차 운영 리포트',
    from: { name: '운영 리포트', addr: 'report@company.example' },
    to: [{ name: '유하람', addr: 'haram@company.example' }],
    cc: [],
    date: '2026년 10월 3일 (토) 오전 8:00', dateShort: '10-03', account: 'haram@company.example',
    excerpt: '주간 처리 412건, 지연 7건. 지연 건은 담당자에게 개별 통보되었습니다.',
    html: '<p>주간 처리 <b>412건</b>, 지연 <b>7건</b>.</p><p>지연 건은 담당자에게 개별 통보되었습니다.</p>',
    quoted: null,
    attachments: [],
  },
];

const ROOM_ITEMS = [
  {
    id: 'r1', kind: 'room', source: 'slack', sourceLabel: '슬랙', roomType: 'channel',
    title: '#pilot-launch', members: 14, unread: true, unreadCount: 9, newCount: 2,
    openUrl: 'https://example.slack.com/archives/C0PILOT',
    days: [
      { key: 'd1', label: '10월 2일 금요일' },
      { key: 'd2', label: '어제' },
      { key: 'd3', label: '오늘' },
    ],
    messages: [
      {
        id: 'r1-1', user: 'seoyoon', day: 'd1', at: '16:02',
        body: [
          { p: [{ b: '2차 파일럿 준비 체크' }, ' 정리했습니다 ', { emoji: '📝' }] },
          { ol: [
            ['계정 발급 — ', { mention: '오지훈' }, ' 님 담당'],
            { segs: ['교육 자료'], sub: [['기본편 — 완료'], ['심화편 — ', { b: '10/10까지' }]] },
            ['현장 일정 확정 (노을랩 회신 대기)'],
          ] },
        ],
        reactions: [{ emoji: '👍', count: 4 }, { emoji: '🙏', count: 2 }],
      },
      {
        id: 'r1-2', user: 'seoyoon', day: 'd1', at: '16:03',
        body: [{ p: ['범위 문서도 같이 올려 둘게요'] }],
        pdf: {
          name: '파일럿_범위_v2.pdf', size: '1.2 MB', pages: 6,
          preview: {
            title: '2차 파일럿 범위',
            lines: ['1. 목적 — 현장 단말 2종의 운영 적합성 확인', '2. 기간 — 2026.10.13 ~ 10.31 (3주)', '3. 범위 — 입구 단말 · 접수 화면 · 주간 리포트', '4. 제외 — 결제 연동 · 외부 알림', '5. 성공 기준 — 하루 처리 200건 · 지연 1% 이하'],
          },
        },
      },
      {
        id: 'r1-3', user: 'jihoon', day: 'd1', at: '16:20',
        body: [{ p: ['계정 발급 스크립트는 ', { code: 'issue-accounts --dry-run' }, ' 으로 먼저 돌려 볼게요. 가이드는 여기 있습니다 ', { link: '사내 위키 · 계정 발급', href: 'https://wiki.company.example/accounts' }] }],
        unfurl: { site: '사내 위키', title: '계정 발급 절차 (2차 파일럿)', desc: '파일럿 현장 계정을 한 번에 발급하는 절차와 점검 목록. 발급 전 dry-run 결과를 확인하고, 중복 계정은 자동으로 건너뛴다.', domain: 'wiki.company.example', thumb: null },
        thread: {
          count: 3, last: '어제 오전 10:41',
          replies: [
            { id: 'r1-3a', user: 'seoyoon', day: 'd2', at: '10:02', body: [{ p: ['dry-run 결과 중복 3건 나왔어요'] }] },
            { id: 'r1-3b', user: 'jihoon', day: 'd2', at: '10:30', body: [{ p: ['확인했습니다. 셋 다 기존 계정이라 건너뛰면 됩니다 ', { emoji: '✅' }] }] },
            { id: 'r1-3c', user: 'seoyoon', day: 'd2', at: '10:41', body: [{ p: ['감사합니다!'] }] },
          ],
        },
      },
      {
        id: 'r1-4', user: 'daeun', day: 'd2', at: '14:15',
        body: [{ p: ['참고할 만한 글 공유합니다 ', { link: 'paperwind.example/blog/field-pilot', href: 'https://paperwind.example/blog/field-pilot' }] }],
        unfurl: { site: 'Paperwind 블로그', title: '현장 파일럿, 3주 안에 끝내는 법', desc: '현장 파일럿을 짧게 끝내려면 성공 기준을 하나로 좁히고, 매일 같은 시각에 숫자를 본다. 우리가 다섯 번의 파일럿에서 배운 것.', domain: 'paperwind.example', thumb: { caption: '블로그 대표 이미지' } },
        reactions: [{ emoji: '👀', count: 3 }],
      },
      {
        id: 'r1-5', user: 'deploybot', day: 'd2', at: '18:00',
        body: [{ p: [{ b: '배포 완료' }, ' — 파일럿 접수 화면 ', { code: 'v0.9.3' }, ' 이 스테이징에 올라갔습니다.'] }],
      },
      {
        id: 'r1-6', user: 'seoyoon', day: 'd3', at: '09:12',
        body: [{ p: [{ mention: '유하람' }, ' 님 교육 자료 최종본입니다. 확인 부탁드려요'] }],
        files: [
          { name: '교육자료_기본편_최종.md', type: 'md', size: '18 KB' },
          { name: '교육자료_심화편_초안.md', type: 'md', size: '24 KB' },
          { name: '교육_일정표.pdf', type: 'pdf', size: '320 KB' },
        ],
      },
      {
        id: 'r1-7', user: 'seoyoon', day: 'd3', at: '09:13',
        body: [{ p: ['심화편은 아직 초안이라 3장만 봐 주시면 됩니다'] }],
      },
      {
        id: 'r1-8', user: 'jihoon', day: 'd3', at: '09:40',
        body: [{ p: ['어제 현장 화면 캡처예요'] }],
        images: [{ name: '접수화면_현장.png', size: '840 KB', caption: '접수 화면 — 현장 단말' }],
        reactions: [{ emoji: '🎉', count: 5 }, { emoji: '😮', count: 1 }],
      },
    ],
  },
  {
    id: 'r2', kind: 'room', source: 'slack', sourceLabel: '슬랙', roomType: 'dm',
    title: '오지훈', members: 2, unread: true, unreadCount: 2, newCount: 0,
    openUrl: 'https://example.slack.com/archives/D0JIHOON',
    days: [{ key: 'd2', label: '어제' }, { key: 'd3', label: '오늘' }],
    messages: [
      { id: 'r2-1', user: 'me', day: 'd2', at: '17:05', body: [{ p: ['지훈님, 계정 발급 끝나면 목록만 보내 주세요'] }] },
      { id: 'r2-2', user: 'jihoon', day: 'd3', at: '08:51', body: [{ p: ['발급 끝났습니다. 목록은 내부 드라이브에 올려 뒀어요 ', { link: '계정 목록', href: 'https://drive.company.example/accounts' }] }] },
      { id: 'r2-3', user: 'jihoon', day: 'd3', at: '08:52', body: [{ p: ['중복 3건은 기존 계정 그대로 씁니다'] }] },
    ],
  },
  {
    id: 'r3', kind: 'room', source: 'slack', sourceLabel: '슬랙', roomType: 'group',
    title: '문다은, 배성민', members: 3, unread: false, unreadCount: 0, newCount: 0,
    openUrl: 'https://example.slack.com/archives/G0FIELD',
    days: [{ key: 'd2', label: '어제' }],
    messages: [
      { id: 'r3-1', user: 'sungmin', day: 'd2', at: '17:40', body: [{ p: ['현장 사진은 메일로도 보냈어요. 원본은 여기 둡니다'] }],
        images: [{ name: '현장_입구_원본.jpg', size: '4.8 MB', caption: '입구 단말 — 원본' }] },
      { id: 'r3-2', user: 'daeun', day: 'd2', at: '17:52', body: [{ p: ['고마워요 ', { emoji: '🙌' }, ' 배선 정리 끝나면 한 장만 더 부탁해요'] }],
        reactions: [{ emoji: '👌', count: 1 }] },
    ],
  },
];

/* 카카오톡 — Mac 앱이 이 Mac 카톡에서 읽어 올린 것. 조회 전용(입력창·스레드 없음).
   첨부: photo(사진 — 수집 때 받아 저장) · album(앨범 — 여러 장) · files(파일 — 받기) · video/voice(표시만, 받지 않음)
   · emoticon(「(이모티콘)」 글자) · expired(이미 만료된 옛 첨부 — 「만료됨」). 사람은 전부 가상 */
const KAKAO_USERS = {
  jiyun: { name: '박지윤', initial: '박', tone: 'c' },
  taeo: { name: '김태오', initial: '김', tone: 'b' },
  sua: { name: '이수아', initial: '이', tone: 'd' },
  minjae: { name: '정민재', initial: '정', tone: 'e' },
};

const KAKAO_ITEMS = [
  {
    id: 'k1', kind: 'room', source: 'kakao', sourceLabel: '카카오톡', roomType: 'direct',
    title: '박지윤', members: 2, unread: true, unreadCount: 4, newCount: 0,
    days: [
      { key: 'd0', label: '9월 20일 토요일' },
      { key: 'd2', label: '어제' },
      { key: 'd3', label: '오늘' },
    ],
    messages: [
      { id: 'k1-1', user: 'jiyun', day: 'd0', at: '14:02', body: [{ p: ['지난번 현장 사진이에요'] }], expired: { kind: '사진', name: '현장_0920.jpg' } },
      { id: 'k1-2', user: 'me', day: 'd0', at: '14:10', body: [{ p: ['고마워요! 확인했어요'] }] },
      { id: 'k1-3', user: 'jiyun', day: 'd2', at: '18:31', body: [{ p: ['내일 오전 미팅 장소 바뀌었어요. 2층 회의실이요'] }] },
      { id: 'k1-4', user: 'jiyun', day: 'd2', at: '18:32', body: [], emoticon: true },
      { id: 'k1-5', user: 'me', day: 'd2', at: '18:40', body: [{ p: ['넵 알겠습니다'] }] },
      { id: 'k1-6', user: 'jiyun', day: 'd3', at: '08:12', body: [{ p: ['회의실 화이트보드 정리한 거 찍어 뒀어요'] }], photo: { name: 'KakaoTalk_20261006_081201.jpg', size: '1.8 MB', caption: '화이트보드 — 회의 정리' } },
      { id: 'k1-7', user: 'jiyun', day: 'd3', at: '08:14', body: [], voice: { length: '0:24' } },
      { id: 'k1-8', user: 'jiyun', day: 'd3', at: '08:15', body: [{ p: ['회의록 초안도 같이 보내요'] }], files: [{ name: '회의록_초안_1006.docx', type: 'docx', size: '86 KB' }] },
    ],
  },
  {
    id: 'k2', kind: 'room', source: 'kakao', sourceLabel: '카카오톡', roomType: 'group',
    title: '김태오, 이수아, 정민재', members: 4, unread: true, unreadCount: 6, newCount: 0,
    days: [
      { key: 'd1', label: '10월 2일 금요일' },
      { key: 'd3', label: '오늘' },
    ],
    messages: [
      { id: 'k2-1', user: 'taeo', day: 'd1', at: '10:05', body: [{ p: ['지난주 견적서 다시 올립니다'] }], expired: { kind: '파일', name: '견적서_v1.pdf' } },
      { id: 'k2-2', user: 'sua', day: 'd1', at: '10:20', body: [{ p: ['링크 만료됐네요 ㅠ 새로 부탁드려요'] }] },
      { id: 'k2-3', user: 'taeo', day: 'd3', at: '09:01', body: [{ p: ['오늘 현장 사진 모음이에요'] }], album: { count: 5, captions: ['입구', '접수대', '단말 1', '단말 2', '배선'] } },
      { id: 'k2-4', user: 'taeo', day: 'd3', at: '09:02', body: [{ p: ['견적서 새로 올립니다'] }], files: [{ name: '견적서_v2.pdf', type: 'pdf', size: '412 KB' }] },
      { id: 'k2-5', user: 'minjae', day: 'd3', at: '09:20', body: [], video: { length: '0:42' } },
      { id: 'k2-6', user: 'minjae', day: 'd3', at: '09:21', body: [{ p: ['배선 정리 영상이에요. 길어서 앞부분만'] }] },
      { id: 'k2-7', user: 'sua', day: 'd3', at: '09:35', body: [], emoticon: true },
      { id: 'k2-8', user: 'me', day: 'd3', at: '09:40', body: [{ p: ['다들 고생 많으셨어요. 정리해서 공유할게요'] }] },
    ],
  },
];

const INBOX_ITEMS = [MAIL_ITEMS[0], ROOM_ITEMS[0], KAKAO_ITEMS[1], ROOM_ITEMS[1], KAKAO_ITEMS[0], MAIL_ITEMS[1], ROOM_ITEMS[2], MAIL_ITEMS[2]];

const INBOX_SOURCES = [
  { id: 'all', label: '전체' },
  { id: 'mail', label: '메일' },
  { id: 'slack', label: '슬랙' },
  { id: 'kakao', label: '카톡' },
];

Object.assign(window, { SLACK_USERS, KAKAO_USERS, MAIL_ITEMS, ROOM_ITEMS, KAKAO_ITEMS, INBOX_ITEMS, INBOX_SOURCES });
