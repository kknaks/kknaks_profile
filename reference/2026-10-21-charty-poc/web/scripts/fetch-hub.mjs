#!/usr/bin/env node
// Procedure Hub(stg) → src/data/hub/hub-snapshot.json (SPEC §4-5).
// hub-refs.json 이 가리키는 노드 + 그 modality(상향 대체용) + 고민 항목 + 시술 프로필만 받는다.
// 의존 0(Node 내장 fetch). 시험용: --refs <path> 로 다른 refs 파일을 줄 수 있다(W-8).
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE = 'https://stg-procedure-hub.medisolveai.com';
const ENDPOINTS = ['/api/taxonomy', '/api/procedure-profiles'];
const OUT = path.join(ROOT, 'src/data/hub/hub-snapshot.json');

const argRefs = process.argv.indexOf('--refs');
const REFS = argRefs > 0 ? path.resolve(process.argv[argRefs + 1]) : path.join(ROOT, 'src/data/hub/hub-refs.json');

// 화면에 쓰는 프로필 필드만(§4-2 시술 시간 · 마취)
const PROFILE_KEYS = ['id', 'name', 'durationMin', 'durationMax', 'needsAnesthesia'];

async function get(endpoint) {
  const res = await fetch(SOURCE + endpoint);
  if (!res.ok) throw new Error(`${endpoint} → HTTP ${res.status}`);
  const text = await res.text();
  return { json: JSON.parse(text), sha256: createHash('sha256').update(text).digest('hex') };
}

/** taxonomy 를 id → 노드 색인으로 편다 */
function indexTaxonomy(tax) {
  const nodes = new Map();
  for (const m of tax.modality) {
    nodes.set(m.id, { level: 'modality', modalityId: m.id, path: [m.category], extracted: null });
    for (const s of m.subcategories ?? []) {
      nodes.set(s.id, { level: 'subcategory', modalityId: m.id, path: [m.category, s.label], extracted: s.extracted ?? null });
      for (const i of s.items ?? []) {
        nodes.set(i.id, { level: 'item', modalityId: m.id, path: [m.category, s.label, i.name], extracted: i.extracted ?? null });
      }
    }
  }
  return nodes;
}

/** 같은 이름(포함 관계) 노드 → 없으면 id 앞부분이 같은 형제 노드 */
function candidates(nodes, label, hubId) {
  const fmt = ([id, n]) => `${id} (${n.path.join(' › ')})`;
  const all = [...nodes];
  const byName = all.filter(([, n]) => {
    const name = n.path[n.path.length - 1];
    return name.includes(label) || label.includes(name);
  });
  if (byName.length) return byName.slice(0, 10).map(fmt);
  const prefix = hubId.slice(0, hubId.lastIndexOf('-'));
  return all.filter(([id]) => prefix && id.startsWith(prefix)).slice(0, 10).map(fmt);
}

async function main() {
  const refs = JSON.parse(await readFile(REFS, 'utf8'));
  const [tax, prof] = await Promise.all(ENDPOINTS.map(get));
  const index = indexTaxonomy(tax.json);

  const chips = Object.values(refs.areas).flatMap((a) => a.chips);
  const missing = chips.filter((c) => !index.has(c.hubId));
  if (missing.length > 0) {
    for (const c of missing) {
      console.error(`[hub] 노드 없음: ${c.label} → ${c.hubId}`);
      const cand = candidates(index, c.label, c.hubId);
      console.error(cand.length ? cand.map((x) => `  후보: ${x}`).join('\n') : '  후보 없음');
    }
    process.exit(1);
  }

  const nodes = {};
  const modalityIds = [];
  for (const c of chips) {
    if (nodes[c.hubId]) continue;
    nodes[c.hubId] = index.get(c.hubId);
    const mid = nodes[c.hubId].modalityId;
    if (!modalityIds.includes(mid)) modalityIds.push(mid);
  }

  const modalities = {};
  for (const mid of modalityIds) {
    const m = tax.json.modality.find((x) => x.id === mid);
    const p = prof.json.profiles.find((x) => x.id === mid);
    if (!p) {
      console.error(`[hub] 프로필 없음: ${mid}`);
      process.exit(1);
    }
    modalities[mid] = {
      category: m.category,
      extracted: m.extracted ?? null,
      profile: Object.fromEntries(PROFILE_KEYS.map((k) => [k, p[k] ?? null])),
    };
  }

  const problemIds = [...new Set(Object.values(refs.areas).flatMap((a) => a.problems))];
  const problems = {};
  for (const pid of problemIds) {
    const s = tax.json.problem.flatMap((p) => p.subcategories ?? []).find((x) => x.id === pid);
    if (!s) {
      console.error(`[hub] 고민 항목 없음: ${pid}`);
      process.exit(1);
    }
    problems[pid] = { label: s.label, items: s.items.map((i) => i.name) };
  }
  // 칩이 근거로 대는 고민 이름이 그 부위 problems 안에 실제로 있는지
  for (const [key, a] of Object.entries(refs.areas)) {
    const names = new Set(a.problems.flatMap((pid) => problems[pid].items));
    for (const c of a.chips) {
      for (const n of c.problemItems) {
        if (!names.has(n)) {
          console.error(`[hub] ${key} · ${c.label}: 고민 항목 「${n}」 이 ${a.problems.join(',')} 에 없음`);
          process.exit(1);
        }
      }
    }
  }

  const snapshot = {
    meta: {
      source: SOURCE,
      endpoints: ENDPOINTS,
      fetchedAt: new Date().toISOString(),
      versions: { taxonomy: null, procedureProfiles: `${prof.json.version} (${prof.json.updated})` },
      sha256: { taxonomy: tax.sha256, procedureProfiles: prof.sha256 },
    },
    modalities,
    nodes,
    problems,
  };
  const body = JSON.stringify(snapshot, null, 1) + '\n';
  await writeFile(OUT, body);
  const levels = Object.values(nodes).reduce((acc, n) => ({ ...acc, [n.level]: (acc[n.level] ?? 0) + 1 }), {});
  console.log(
    `[hub] nodes ${Object.keys(nodes).length} ${JSON.stringify(levels)} · modalities ${modalityIds.length} · problems ${problemIds.length} · ${Buffer.byteLength(body)} bytes`,
  );
  console.log(`[hub] taxonomy sha256 ${tax.sha256} · profiles ${snapshot.meta.versions.procedureProfiles} ${prof.sha256}`);
  console.log(`[hub] → ${path.relative(ROOT, OUT)}`);
}

main().catch((e) => {
  console.error(`[hub] 실패: ${e.message}`);
  process.exit(1);
});
