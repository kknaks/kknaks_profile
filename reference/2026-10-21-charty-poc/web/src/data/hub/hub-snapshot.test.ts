import { describe, expect, it } from 'vitest';
import hubRefs from './hub-refs.json';
import snapshot from './hub-snapshot.json';
import { HUB, ONSET_KEYS, SAFETY_KEYS, hubPath, modalSections } from './hub';

const HAN = /[一-鿿]/;
const chips = Object.values(hubRefs.areas).flatMap((a) => a.chips);

describe('Hub 스냅샷(SPEC §4-5)', () => {
  it('R-4 refs 의 모든 hubId 가 nodes 에 · modalityId 가 modalities 에 · 프로필 8개', () => {
    for (const c of chips) {
      const n = HUB.nodes[c.hubId];
      expect(n, c.hubId).toBeTruthy();
      expect(HUB.modalities[n.modalityId], n.modalityId).toBeTruthy();
    }
    expect(new Set(chips.map((c) => c.hubId)).size).toBe(16);
    expect(chips.length).toBe(19);
    const mods = Object.values(HUB.modalities);
    expect(mods.length).toBe(8);
    expect(mods.every((m) => m.profile && m.profile.durationMin != null && !!m.profile.needsAnesthesia)).toBe(true);
  });

  it('R-5 상향 대체 — M8-4-1 은 받으면 안 되는 경우만 M8, M8-2 는 전부 M8', () => {
    const vb = Object.fromEntries(modalSections('M8-4-1').map((s) => [s.key, s]));
    expect(vb.contraindications.sourceId).toBe('M8');
    expect(vb.contraindications.inheritedLabel).toBe('레이저 전체 기준');
    expect(vb.mechanism.sourceId).toBe('M8-4-1');
    expect(vb.mechanism.inheritedLabel).toBeNull();
    const fr = modalSections('M8-2');
    expect(fr.length).toBeGreaterThan(0);
    expect(fr.every((s) => s.sourceId === 'M8' && s.inheritedLabel === '레이저 전체 기준')).toBe(true);
    expect(hubPath('M8-4-1')).toBe('레이저 › 혈관 › 브이빔');
    expect(hubPath('M8-2')).toBe('레이저 › 프락셔널');
  });

  it('modality 칩은 상향 표기 없음 · 보톡스(주름) 시술 시간은 보톡스 전체 기준 10–15분 마취 없음', () => {
    expect(modalSections('M2').every((s) => s.inheritedLabel == null)).toBe(true);
    const bt = Object.fromEntries(modalSections('M1-3-1').map((s) => [s.key, s]));
    expect(bt.procedure.inheritedLabel).toBe('보톡스 전체 기준');
    expect(bt.procedure.body).toEqual({ kind: 'pairs', pairs: [{ label: '시술 시간', text: '10–15분' }, { label: '마취', text: '마취 없음' }] });
  });

  it('R-6 §4-2 에 없는 onset_duration · safety 하위 키 0 · 한자 0 · meta', () => {
    const onset = new Set(ONSET_KEYS.map(([k]) => k as string));
    const safety = new Set(SAFETY_KEYS.map(([k]) => k as string));
    const all = [...Object.values(HUB.nodes).map((n) => n.extracted), ...Object.values(HUB.modalities).map((m) => m.extracted)];
    for (const e of all) {
      if (!e) continue;
      for (const k of Object.keys(e.onset_duration ?? {})) expect(onset.has(k), `onset_duration.${k}`).toBe(true);
      for (const k of Object.keys(e.safety ?? {})) expect(safety.has(k), `safety.${k}`).toBe(true);
    }
    expect(HAN.test(JSON.stringify(snapshot))).toBe(false);
    expect(HUB.meta.fetchedAt).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    expect(HUB.meta.sha256.taxonomy).toMatch(/^[0-9a-f]{64}$/);
  });

  it('칩 16개 노드 모두 모달 섹션이 나온다', () => {
    for (const id of new Set(chips.map((c) => c.hubId))) expect(modalSections(id).length, id).toBeGreaterThan(3);
  });
});
