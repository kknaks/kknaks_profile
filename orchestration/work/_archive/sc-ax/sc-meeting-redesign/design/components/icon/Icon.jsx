import icons from './icon-data.js';
import { iconAliases } from './icon-aliases.js';

/* Icon/Normal glyph geometry — line paths on a 24px grid, inlined here on purpose:
   this is the only consumer, and a separate module mis-binds through the bundler.
   Geometry: Lucide (ISC), mapped onto this kit's icon names. `fill: true` entries
   are the *-fill variants (same geometry, painted solid). The older traced
   outline-as-fill set (icon-data.js) stays as a fallback for names not listed. */
const strokeIcons = {
  'agent': { viewBox: '0 0 24 24', body: '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>', stroke: true, fill: false },
  'ai-review': { viewBox: '0 0 24 24', body: '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/><path d="m16 16-1.9-1.9"/>', stroke: true, fill: false },
  'align-justify': { viewBox: '0 0 24 24', body: '<path d="M3 12h18"/><path d="M3 18h18"/><path d="M3 6h18"/>', stroke: true, fill: false },
  'arrow-left': { viewBox: '0 0 24 24', body: '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>', stroke: true, fill: false },
  'arrow-left-thick': { viewBox: '0 0 24 24', body: '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>', stroke: true, fill: false },
  'arrow-right': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', stroke: true, fill: false },
  'arrow-right-thick': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', stroke: true, fill: false },
  'arrow-turn-down': { viewBox: '0 0 24 24', body: '<polyline points="9 10 4 15 9 20"/><path d="M20 4v7a4 4 0 0 1-4 4H4"/>', stroke: true, fill: false },
  'bell': { viewBox: '0 0 24 24', body: '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>', stroke: true, fill: false },
  'bell-fill': { viewBox: '0 0 24 24', body: '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>', stroke: true, fill: true },
  'blank': { viewBox: '0 0 24 24', body: '<rect width="18" height="18" x="3" y="3" rx="2"/>', stroke: true, fill: false },
  'bookmark': { viewBox: '0 0 24 24', body: '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>', stroke: true, fill: false },
  'bookmark-fill': { viewBox: '0 0 24 24', body: '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>', stroke: true, fill: true },
  'bubble-plus': { viewBox: '0 0 24 24', body: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M12 7v6"/><path d="M9 10h6"/>', stroke: true, fill: false },
  'bubble-plus-fill': { viewBox: '0 0 24 24', body: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M12 7v6"/><path d="M9 10h6"/>', stroke: true, fill: true },
  'business-bag': { viewBox: '0 0 24 24', body: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>', stroke: true, fill: false },
  'business-bag-fill': { viewBox: '0 0 24 24', body: '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>', stroke: true, fill: true },
  'calendar': { viewBox: '0 0 24 24', body: '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>', stroke: true, fill: false },
  'calendar-person': { viewBox: '0 0 24 24', body: '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>', stroke: true, fill: false },
  'camera': { viewBox: '0 0 24 24', body: '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>', stroke: true, fill: false },
  'camera-fill': { viewBox: '0 0 24 24', body: '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>', stroke: true, fill: true },
  'caret-down': { viewBox: '0 0 24 24', body: '<path d="m6 9 6 6 6-6"/>', stroke: true, fill: false },
  'caret-up': { viewBox: '0 0 24 24', body: '<path d="m18 15-6-6-6 6"/>', stroke: true, fill: false },
  'chat': { viewBox: '0 0 24 24', body: '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>', stroke: true, fill: false },
  'check': { viewBox: '0 0 24 24', body: '<path d="M20 6 9 17l-5-5"/>', stroke: true, fill: false },
  'check-thick': { viewBox: '0 0 24 24', body: '<path d="M20 6 9 17l-5-5"/>', stroke: true, fill: false },
  'chevron-down': { viewBox: '0 0 24 24', body: '<path d="m6 9 6 6 6-6"/>', stroke: true, fill: false },
  'chevron-down-small': { viewBox: '0 0 24 24', body: '<path d="m6 9 6 6 6-6"/>', stroke: true, fill: false },
  'chevron-down-thick': { viewBox: '0 0 24 24', body: '<path d="m6 9 6 6 6-6"/>', stroke: true, fill: false },
  'chevron-down-thick-small': { viewBox: '0 0 24 24', body: '<path d="m6 9 6 6 6-6"/>', stroke: true, fill: false },
  'chevron-left': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-small': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-thick': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-thick-small': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-tight': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-tight-small': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-tight-thick': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-left-tight-thick-small': { viewBox: '0 0 24 24', body: '<path d="m15 18-6-6 6-6"/>', stroke: true, fill: false },
  'chevron-right': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-small': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-thick': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-thick-small': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-tight': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-tight-small': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-tight-thick': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-right-tight-thick-small': { viewBox: '0 0 24 24', body: '<path d="m9 18 6-6-6-6"/>', stroke: true, fill: false },
  'chevron-up': { viewBox: '0 0 24 24', body: '<path d="m18 15-6-6-6 6"/>', stroke: true, fill: false },
  'chevron-up-small': { viewBox: '0 0 24 24', body: '<path d="m18 15-6-6-6 6"/>', stroke: true, fill: false },
  'chevron-up-thick': { viewBox: '0 0 24 24', body: '<path d="m18 15-6-6-6 6"/>', stroke: true, fill: false },
  'chevron-up-thick-small': { viewBox: '0 0 24 24', body: '<path d="m18 15-6-6-6 6"/>', stroke: true, fill: false },
  'circle-check': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>', stroke: true, fill: false },
  'circle-check-fill': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>', stroke: true, fill: true },
  'circle-close': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>', stroke: true, fill: false },
  'circle-close-fill': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>', stroke: true, fill: true },
  'circle-exclamation': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>', stroke: true, fill: false },
  'circle-exclamation-fill': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>', stroke: true, fill: true },
  'circle-up-right': { viewBox: '0 0 24 24', body: '<path d="M22 12A10 10 0 1 1 12 2"/><path d="M22 2 12 12"/><path d="M16 2h6v6"/>', stroke: true, fill: false },
  'circle-up-right-fill': { viewBox: '0 0 24 24', body: '<path d="M22 12A10 10 0 1 1 12 2"/><path d="M22 2 12 12"/><path d="M16 2h6v6"/>', stroke: true, fill: true },
  'clock': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>', stroke: true, fill: false },
  'clock-fill': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>', stroke: true, fill: true },
  'close': { viewBox: '0 0 24 24', body: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', stroke: true, fill: false },
  'close-thick': { viewBox: '0 0 24 24', body: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', stroke: true, fill: false },
  'coffee': { viewBox: '0 0 24 24', body: '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>', stroke: true, fill: false },
  'coffee-fill': { viewBox: '0 0 24 24', body: '<path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/>', stroke: true, fill: true },
  'column': { viewBox: '0 0 24 24', body: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="M15 3v18"/>', stroke: true, fill: false },
  'company': { viewBox: '0 0 24 24', body: '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>', stroke: true, fill: false },
  'company-fill': { viewBox: '0 0 24 24', body: '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>', stroke: true, fill: true },
  'desktop': { viewBox: '0 0 24 24', body: '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>', stroke: true, fill: false },
  'desktop-fill': { viewBox: '0 0 24 24', body: '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>', stroke: true, fill: true },
  'document': { viewBox: '0 0 24 24', body: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>', stroke: true, fill: false },
  'document-fill': { viewBox: '0 0 24 24', body: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>', stroke: true, fill: true },
  'document-text': { viewBox: '0 0 24 24', body: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>', stroke: true, fill: false },
  'document-text-fill': { viewBox: '0 0 24 24', body: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>', stroke: true, fill: true },
  'dot': { viewBox: '0 0 24 24', body: '<circle cx="12.1" cy="12.1" r="1"/>', stroke: true, fill: true },
  /* 「신규」 expand / collapse — kit 에 전체화면 글리프가 없다. 회의에 집중하는 자리(목록 접기)에 필요해 같은 선 규칙(24 그리드·1.5·currentColor)으로 더한다. */
  'expand': { viewBox: '0 0 24 24', body: '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/>', stroke: true, fill: false },
  'collapse': { viewBox: '0 0 24 24', body: '<path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M3 21l7-7"/>', stroke: true, fill: false },
  'external-link': { viewBox: '0 0 24 24', body: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>', stroke: true, fill: false },
  'flip-backward': { viewBox: '0 0 24 24', body: '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"/>', stroke: true, fill: false },
  'graduation': { viewBox: '0 0 24 24', body: '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>', stroke: true, fill: false },
  'graduation-fill': { viewBox: '0 0 24 24', body: '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>', stroke: true, fill: true },
  'history': { viewBox: '0 0 24 24', body: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>', stroke: true, fill: false },
  'home': { viewBox: '0 0 24 24', body: '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>', stroke: true, fill: false },
  'home-fill': { viewBox: '0 0 24 24', body: '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>', stroke: true, fill: true },
  'image': { viewBox: '0 0 24 24', body: '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>', stroke: true, fill: false },
  'inbox': { viewBox: '0 0 24 24', body: '<path d="M21.2 8.4c.5.38.8.97.8 1.6v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V10a2 2 0 0 1 .8-1.6l8-6a2 2 0 0 1 2.4 0l8 6Z"/><path d="m22 10-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 10"/>', stroke: true, fill: false },
  'left-side': { viewBox: '0 0 24 24', body: '<rect width="18" height="18" x="3" y="3" rx="4"/><path d="M8 8v8"/>', stroke: true, fill: false },
  'line-horizontal': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/>', stroke: true, fill: false },
  'line-horizontal-thick': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/>', stroke: true, fill: false },
  'link': { viewBox: '0 0 24 24', body: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>', stroke: true, fill: false },
  'list-category': { viewBox: '0 0 24 24', body: '<path d="M3 12h.01"/><path d="M3 18h.01"/><path d="M3 6h.01"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M8 6h13"/>', stroke: true, fill: false },
  'logout': { viewBox: '0 0 24 24', body: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>', stroke: true, fill: false },
  'mail': { viewBox: '0 0 24 24', body: '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>', stroke: true, fill: false },
  'message': { viewBox: '0 0 24 24', body: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', stroke: true, fill: false },
  'message-fill': { viewBox: '0 0 24 24', body: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', stroke: true, fill: true },
  'minus': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/>', stroke: true, fill: false },
  'minus-thick': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/>', stroke: true, fill: false },
  'more-vertical': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>', stroke: true, fill: false },
  'more-vertical-tight': { viewBox: '0 0 24 24', body: '<circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>', stroke: true, fill: false },
  'pencil': { viewBox: '0 0 24 24', body: '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/>', stroke: true, fill: false },
  'pencil-fill': { viewBox: '0 0 24 24', body: '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/>', stroke: true, fill: true },
  'person': { viewBox: '0 0 24 24', body: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>', stroke: true, fill: false },
  'person-fill': { viewBox: '0 0 24 24', body: '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>', stroke: true, fill: true },
  'persons': { viewBox: '0 0 24 24', body: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', stroke: true, fill: false },
  'persons-fill': { viewBox: '0 0 24 24', body: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', stroke: true, fill: true },
  /* 「신규」 play / play-fill — 소스 kit 에 재생 글리프가 없다. 회의 「빠른 시작」에 필요해 같은 선 규칙(24 그리드·1.5·currentColor)으로 더한다. */
  'play': { viewBox: '0 0 24 24', body: '<path d="M6 4.5a1 1 0 0 1 1.53-.85l10 7.5a1 1 0 0 1 0 1.7l-10 7.5A1 1 0 0 1 6 19.5z"/>', stroke: true, fill: false },
  'play-fill': { viewBox: '0 0 24 24', body: '<path d="M6 4.5a1 1 0 0 1 1.53-.85l10 7.5a1 1 0 0 1 0 1.7l-10 7.5A1 1 0 0 1 6 19.5z"/>', stroke: true, fill: true },
  'plus': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/><path d="M12 5v14"/>', stroke: true, fill: false },
  'plus-thick': { viewBox: '0 0 24 24', body: '<path d="M5 12h14"/><path d="M12 5v14"/>', stroke: true, fill: false },
  'reset': { viewBox: '0 0 24 24', body: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>', stroke: true, fill: false },
  'search': { viewBox: '0 0 24 24', body: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>', stroke: true, fill: false },
  'search-thick': { viewBox: '0 0 24 24', body: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>', stroke: true, fill: false },
  'send': { viewBox: '0 0 24 24', body: '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>', stroke: true, fill: false },
  'send-fill': { viewBox: '0 0 24 24', body: '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>', stroke: true, fill: true },
  'setting': { viewBox: '0 0 24 24', body: '<path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>', stroke: true, fill: false },
  'square-check': { viewBox: '0 0 24 24', body: '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 12 2 2 4-4"/>', stroke: true, fill: false },
  'star': { viewBox: '0 0 24 24', body: '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>', stroke: true, fill: false },
  'star-fill': { viewBox: '0 0 24 24', body: '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>', stroke: true, fill: true },
  'trash': { viewBox: '0 0 24 24', body: '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>', stroke: true, fill: false },
  'tune': { viewBox: '0 0 24 24', body: '<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>', stroke: true, fill: false },
  'write': { viewBox: '0 0 24 24', body: '<path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"/>', stroke: true, fill: false },
};

/* The kit's icon surface. Glyphs paint with currentColor, so set `color` on the
   icon or an ancestor. Sizes in the file are 12 / 16 / 18 / 20 / 24 px.
   `strokeWidth` goes heavier on demand; the *-thick names render +0.5. */
export function Icon({ name, size = 20, strokeWidth = 1.5, style, ...rest }) {
  /* the line set is keyed by friendly name; iconAliases maps friendly → legacy key */
  const s = strokeIcons[name] || strokeIcons[iconAliases[name] || name];
  if (s) {
    return (
      <svg
        width={size}
        height={size}
        viewBox={s.viewBox}
        fill={s.fill ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth={/-thick/.test(name) ? strokeWidth + 0.5 : strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden={rest['aria-label'] ? undefined : 'true'}
        style={{ display: 'block', flexShrink: 0, ...style }}
        dangerouslySetInnerHTML={{ __html: s.body }}
        {...rest}
      />
    );
  }
  const d = icons[iconAliases[name] || name];
  if (!d) return null;
  return (
    <svg
      width={size}
      height={size}
      viewBox={d.viewBox}
      fill="none"
      aria-hidden={rest['aria-label'] ? undefined : 'true'}
      style={{ display: 'block', flexShrink: 0, ...style }}
      dangerouslySetInnerHTML={{ __html: d.body }}
      {...rest}
    />
  );
}
/** Every valid `name`, in alphabetical order. */
Icon.names = Object.keys(iconAliases);
export default Icon;
