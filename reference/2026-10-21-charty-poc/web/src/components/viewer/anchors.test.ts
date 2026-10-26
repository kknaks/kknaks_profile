import { describe, expect, it } from 'vitest';
import { FACE_ANCHORS } from '@/data/face-anchors';
import { anchorEditEnabled, anchorFileSource, anchorsUsable, facingOpacity, leaderPoints, polylinesCross } from './anchors';

describe('앵커 — 순수 함수(SPEC §3)', () => {
  it('R-15 메시 가드: mesh.bytes 가 다르면 false', () => {
    expect(anchorsUsable({ mesh: { bytes: FACE_ANCHORS.meshBytes } }, FACE_ANCHORS)).toBe(FACE_ANCHORS.points.length > 0);
    expect(anchorsUsable({ mesh: { bytes: FACE_ANCHORS.meshBytes + 1 } }, FACE_ANCHORS)).toBe(false);
    expect(anchorsUsable(null, FACE_ANCHORS)).toBe(false);
    expect(anchorsUsable({ mesh: { bytes: 5 } }, { meshBytes: 5, points: [] })).toBe(false);
  });
  it('찍기 도구: 개발 + ?anchors=edit 일 때만(W-5)', () => {
    expect(anchorEditEnabled('development', '?anchors=edit')).toBe(true);
    expect(anchorEditEnabled('production', '?anchors=edit')).toBe(false);
    expect(anchorEditEnabled('development', '')).toBe(false);
    expect(anchorEditEnabled('development', '?anchors=view')).toBe(false);
  });
  it('뒷면 opacity 0.10–0.30 선형', () => {
    expect(facingOpacity(0.05)).toBe(0);
    expect(facingOpacity(0.1)).toBe(0);
    expect(facingOpacity(0.2)).toBeCloseTo(0.5);
    expect(facingOpacity(0.5)).toBe(1);
  });
  it('무릎은 얼굴 쪽으로 32px(W-7)', () => {
    expect(leaderPoints([400, 300], [256, 100], 'left')[1]).toEqual([288, 100]);
    expect(leaderPoints([400, 300], [784, 100], 'right')[1]).toEqual([752, 100]);
  });
  it('맨 위 카드는 위로 돌아 수직으로 내려간다(2루프 W-7)', () => {
    expect(leaderPoints([524, 345], [256, 46], 'left', 'top')).toEqual([[524, 345], [524, 46], [256, 46]]);
    expect(leaderPoints([600, 262], [784, 46], 'right', 'top')).toEqual([[600, 262], [600, 46], [784, 46]]);
    // 점이 무릎보다 카드 쪽이면 무릎으로
    expect(leaderPoints([270, 300], [256, 46], 'left', 'top')[1]).toEqual([288, 46]);
  });
  it('꺾은선 교차 판정', () => {
    const a = leaderPoints([400, 200], [256, 100], 'left');
    const b = leaderPoints([400, 400], [256, 300], 'left');
    expect(polylinesCross(a, b)).toBe(false);
    const c = leaderPoints([400, 50], [256, 300], 'left');
    expect(polylinesCross(a, c)).toBe(true);
  });
  it('[복사] 본문은 파일 형식 · 소수 4자리', () => {
    const src = anchorFileSource(10, [{ key: 'eye', p: [0.123456, 0, -1], n: [0, 0, 1] }]);
    expect(src).toContain("{ key: 'eye', p: [0.1235, 0.0000, -1.0000], n: [0.0000, 0.0000, 1.0000] },");
    expect(src).toContain('meshBytes: 10,');
  });
});
