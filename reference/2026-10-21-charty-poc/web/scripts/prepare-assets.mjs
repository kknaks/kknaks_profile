#!/usr/bin/env node
// M3D 원본 에셋 + HAR → public/m3d/ (SPEC §7).
// 산출물은 얼굴 사진·메시·측정값이라 전부 gitignore 대상이다. 멱등: 매번 public/m3d 를 지우고 다시 만든다.
import { execFileSync } from 'node:child_process';
import { copyFile, mkdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.resolve(ROOT, process.env.M3D_SRC ?? '../m3d-assets');
const HAR = path.resolve(ROOT, process.env.M3D_HAR ?? '../m3d-ai-h5.migamedi.co.kr.har');
const OUT = path.join(ROOT, 'public/m3d');

const TEX_W = 3242;
const TEX_H = 1621;
const OVERLAY_GAIN = Number(process.env.OVERLAY_GAIN ?? 3);

const MESH = { src: 'obj/Rgb.obj', out: 'mesh/Rgb.obj' };
const TEXTURES = {
  natural: 'thumb/Rgb_M.jpg',
  cool: 'thumb/RgbCool_M.jpg',
  'red-heat': 'thumb/RedHeat_M.jpg',
  'brown-heat': 'thumb/BrownHeat_M.jpg',
  uv: 'thumb/Uv_M.jpg',
};
const OVERLAYS = {
  'fine-wrinkle': 'hd_ai/wrinkle_mixed.png',
  'deep-wrinkle': 'hd_ai/rough_wrinkle_mask.png',
  pore: 'hd_ai/pores.png',
};
// 주름 선은 1–2px 라 1/3 평균 축소에서 거의 사라진다. 풀해상도에서 팽창(max filter)으로 선을 굵힌 뒤
// max 축소로 줄인다 — blur 와 달리 선 모양이 그대로 남는다(fix1 · AC-20/21). 위치는 원본 그대로. 값 = 풀해상도 팽창 폭(px)
const OVERLAY_DILATE_BY_KEY = { 'fine-wrinkle': 15, 'deep-wrinkle': 15 };
// HAR 응답 경로 → 출력 파일
const API = {
  measure: '/api/skin/measure/results/render',
  render: '/api/skin/report/render.v3',
};
// 키 이름에 이 낱말이 들어 있으면 개인 식별 값일 수 있다 → 쓰기 전에 멈춘다
const GUARD_WORDS = ['hash', 'user', 'url', 'icon', 'scanner', 'unique'];

function fail(msg) {
  console.error(`✗ ${msg}`);
  process.exit(1);
}

async function checkInputs() {
  const need = [MESH.src, ...Object.values(TEXTURES), ...Object.values(OVERLAYS)].map((p) => path.join(SRC, p));
  need.push(HAR);
  const missing = need.filter((p) => !existsSync(p));
  if (missing.length) {
    fail(`입력 파일이 없습니다 (${missing.length}개):\n${missing.map((p) => `  - ${path.relative(ROOT, p)}`).join('\n')}`);
  }
}

function findGuardKeys(obj, at = '$', out = []) {
  if (Array.isArray(obj)) obj.forEach((v, i) => findGuardKeys(v, `${at}[${i}]`, out));
  else if (obj && typeof obj === 'object') {
    for (const [k, v] of Object.entries(obj)) {
      if (GUARD_WORDS.some((w) => k.toLowerCase().includes(w))) out.push(`${at}.${k}`);
      findGuardKeys(v, `${at}.${k}`, out);
    }
  }
  return out;
}

async function writeJsonGuarded(rel, data) {
  const bad = findGuardKeys(data);
  if (bad.length) fail(`${rel} 에 개인정보 가드 키가 남아 있습니다: ${bad.slice(0, 5).join(', ')}`);
  await writeFile(path.join(OUT, rel), JSON.stringify(data, null, 2) + '\n');
}

async function readHarResponses() {
  const har = JSON.parse(await readFile(HAR, 'utf8'));
  const found = {};
  for (const e of har.log?.entries ?? []) {
    let pathname;
    try {
      pathname = new URL(e.request.url).pathname;
    } catch {
      continue;
    }
    for (const [key, p] of Object.entries(API)) {
      if (pathname === p && e.response?.content?.text) {
        const text =
          e.response.content.encoding === 'base64'
            ? Buffer.from(e.response.content.text, 'base64').toString('utf8')
            : e.response.content.text;
        found[key] = JSON.parse(text).data;
      }
    }
  }
  for (const key of Object.keys(API)) if (!found[key]) fail(`HAR 에 ${API[key]} 응답이 없습니다`);
  return found;
}

// measure: 측정 수치만. 리포트 식별자(id·hash)는 버린다.
function pickMeasure(m) {
  const { type, version, results_version, categories, features } = m;
  return { type, version, results_version, categories, features };
}

// render: 화이트리스트만(SPEC §7) — date, atlas[], three_dimensional.mappings[].{flag,title}
function pickRender(r) {
  return {
    date: r.date,
    atlas: (r.atlas ?? []).map(({ flag, name, type }) => ({ flag, name, type })),
    three_dimensional: {
      mappings: (r.three_dimensional?.mappings ?? []).map(({ flag, title }) => ({ flag, title })),
    },
  };
}

async function copyTexture(key, rel) {
  const src = path.join(SRC, rel);
  const meta = await sharp(src).metadata();
  if (meta.width !== TEX_W || meta.height !== TEX_H) {
    fail(`${rel} 크기가 ${meta.width}×${meta.height} — ${TEX_W}×${TEX_H} 이어야 합니다`);
  }
  const out = `tex/${key}.jpg`;
  await copyFile(src, path.join(OUT, out));
  return { file: out, w: meta.width, h: meta.height };
}

/** 풀해상도 L 채널 → 칸마다 최댓값으로 줄인다(가는 선이 평균에 묻히지 않게) */
function maxPool(src, sw, sh, dw, dh) {
  const out = Buffer.alloc(dw * dh);
  const x0s = new Int32Array(dw + 1);
  for (let x = 0; x <= dw; x++) x0s[x] = Math.min(sw, Math.floor((x * sw) / dw));
  for (let y = 0; y < dh; y++) {
    const ya = Math.floor((y * sh) / dh);
    const yb = Math.max(ya + 1, Math.floor(((y + 1) * sh) / dh));
    for (let x = 0; x < dw; x++) {
      let m = 0;
      const xa = x0s[x];
      const xb = Math.max(xa + 1, x0s[x + 1]);
      for (let yy = ya; yy < yb; yy++) {
        const row = yy * sw;
        for (let xx = xa; xx < xb; xx++) if (src[row + xx] > m) m = src[row + xx];
      }
      out[y * dw + x] = m;
    }
  }
  return out;
}

// 흰 선·점 마스크(L) → 흰색 + 알파 PNG. 색은 셰이더가 입힌다.
async function makeOverlay(key, rel) {
  const dilate = OVERLAY_DILATE_BY_KEY[key];
  const gain = OVERLAY_GAIN;
  let data;
  if (dilate) {
    // ⚠ libvips 형태 연산은 검정을 전경으로 본다 — 흰 선을 굵히는(max filter) 쪽이 erode 다(dilate 는 흰 선을 지운다, 실측 0.013%→0%)
    const full = await sharp(path.join(SRC, rel)).toColourspace('b-w').erode(dilate).raw().toBuffer({ resolveWithObject: true });
    data = maxPool(full.data, full.info.width, full.info.height, TEX_W, TEX_H);
  } else {
    data = (await sharp(path.join(SRC, rel)).toColourspace('b-w').resize(TEX_W, TEX_H, { kernel: 'lanczos3' }).raw().toBuffer());
  }
  const px = TEX_W * TEX_H;
  const rgba = Buffer.alloc(px * 4, 255);
  let covered = 0;
  for (let i = 0; i < px; i++) {
    const a = Math.min(255, Math.round(data[i] * gain));
    rgba[i * 4 + 3] = a;
    if (a > 32) covered++;
  }
  const out = `overlay/${key}.png`;
  await sharp(rgba, { raw: { width: TEX_W, height: TEX_H, channels: 4 } })
    .png({ compressionLevel: 9 })
    .toFile(path.join(OUT, out));
  return { file: out, w: TEX_W, h: TEX_H, gain, dilate: dilate ?? 0, coverage: Number((covered / px).toFixed(4)) };
}

async function main() {
  await checkInputs();
  const { measure, render } = await readHarResponses();

  await rm(OUT, { recursive: true, force: true });
  for (const d of ['mesh', 'tex', 'overlay', 'report']) await mkdir(path.join(OUT, d), { recursive: true });

  await copyFile(path.join(SRC, MESH.src), path.join(OUT, MESH.out));
  const meshBytes = (await stat(path.join(OUT, MESH.out))).size;

  const textures = {};
  for (const [k, rel] of Object.entries(TEXTURES)) textures[k] = await copyTexture(k, rel);
  const overlays = {};
  for (const [k, rel] of Object.entries(OVERLAYS)) overlays[k] = await makeOverlay(k, rel);

  await writeJsonGuarded('report/measure.json', pickMeasure(measure));
  await writeJsonGuarded('report/render.json', pickRender(render));

  const manifest = {
    generatedAt: new Date().toISOString(),
    mesh: { file: MESH.out, bytes: meshBytes },
    textures,
    overlays,
    report: { measure: 'report/measure.json', render: 'report/render.json' },
  };
  await writeFile(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');

  console.log(`✓ public/m3d 생성 — 메시 ${(meshBytes / 1e6).toFixed(1)}MB · 텍스처 ${Object.keys(textures).length} · 오버레이 ${Object.keys(overlays).length}`);
  for (const [k, o] of Object.entries(overlays)) console.log(`  overlay ${k}: coverage ${(o.coverage * 100).toFixed(2)}%`);

  try {
    execFileSync('git', ['check-ignore', '-q', 'public/m3d'], { cwd: ROOT, stdio: 'ignore' });
  } catch {
    console.warn('⚠ public/m3d 가 git 에서 무시되지 않습니다 — 얼굴 데이터가 커밋될 수 있어요. .gitignore 를 확인하세요.');
  }
}

main().catch((e) => fail(e.stack ?? String(e)));
