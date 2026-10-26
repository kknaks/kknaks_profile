// 화면 ① 뷰어 패널(1040 폭) 안 배치 상수 — 카드 열 · 지시선은 패널 좌표(왼쪽 위 원점), 투영은 캔버스 좌표 + (FACE_X0, 0).
export const VIEWER_W = 1040;
/** 캔버스 = 패널 높이 − 필터 바 96 */
export const FILTER_BAR_H = 96;
export const LEGEND_H = 40;
export const COL_W = 240;
export const COL_PAD = 16;
export const COL_GAP = 12;
/** 카드 부위명 줄 가운데 — 카드 top 기준(지시선 카드 쪽 끝점 y) */
export const CARD_TITLE_Y = 30;
/** 두 카드 열 사이 = 얼굴 구역 = 3D 캔버스(R-12 「C 구역」). 캔버스 원점 = 패널 x FACE_X0 */
export const FACE_X0 = COL_PAD + COL_W; // 256
export const FACE_X1 = VIEWER_W - COL_PAD - COL_W; // 784
