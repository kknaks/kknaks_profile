import { fromM3d } from '@/data/adapters/m3d';
import type { M3dMeasure, M3dRender } from '@/data/adapters/m3d-types';
import type { SkinReport, SkinReportSource, TextureKey } from '@/domain/skin-report';

export class ReportMissingError extends Error {}

/** 준비 스크립트가 만든 public/m3d/report/*.json 을 읽는다. 나중엔 3D 스캔 업체 소스가 같은 인터페이스를 구현한다. */
export class M3dMockSource implements SkinReportSource {
  constructor(private readonly opts: { baseUrl: string; customer: { name: string }; manifestUrl?: string }) {}

  async load(): Promise<SkinReport> {
    const [mRes, rRes] = await Promise.all([fetch(`${this.opts.baseUrl}/measure.json`), fetch(`${this.opts.baseUrl}/render.json`)]);
    if (!mRes.ok || !rRes.ok) throw new ReportMissingError('measure/render json 없음');
    const measure = (await mRes.json()) as M3dMeasure;
    const render = (await rRes.json()) as M3dRender;
    let availableTextures: TextureKey[] | undefined;
    if (this.opts.manifestUrl) {
      const man = await fetch(this.opts.manifestUrl).catch(() => null);
      if (man?.ok) availableTextures = Object.keys((await man.json()).textures ?? {}) as TextureKey[];
    }
    return fromM3d(measure, render, { customer: this.opts.customer, availableTextures });
  }
}
