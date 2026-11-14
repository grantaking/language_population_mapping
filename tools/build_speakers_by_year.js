// Builds data/speakers_by_year.csv (speaker estimates for 1980, 2000 and 2050).
//
// Inputs (all relative to the repo root):
//   index.html                  the data loader (buildData) is read from here, so the map and this script agree
//   data/languages.csv          current native and total speakers
//   data/countries.csv, data/regions.csv, data/second_language.csv
//   data/population_by_year.csv UN WPP 2024 country populations for 1980, 2000, 2026, 2050
//   tools/census_anchors.csv    census language shares (India, Pakistan, China)
//
// Method, per language:
//   native(year) = native(current) x F(year)
//     F is a weighted average of country growth factors. Weights are the language's current speakers in each country:
//     for a country with census anchors, census share x current population; elsewhere, the current population of
//     the map regions where the language is the plurality language.
//     Growth factor for a country = (share in year / share now) x (population in year / population now) when census
//     anchors exist for both that year and now; otherwise population in year / population now.
//   total(year) = native(year) + (total(current) - native(current)) x F2(year)
//     F2 is the population growth of the language's second-language zones (or F when it has none).
//   2050 always uses population change only (shares held at their latest census value).
//
// Run from the repo root:  (cd tools && npm install) && node tools/build_speakers_by_year.js

const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const NM = path.join(__dirname, 'node_modules');
const d3geo = require(path.join(NM, 'd3-geo'));
const { csvParse, csvFormatRows } = require(path.join(NM, 'd3-dsv'));
const topojson = require(path.join(NM, 'topojson-client'));

const read = f => csvParse(fs.readFileSync(path.join(ROOT, f), 'utf8').replace(/^﻿/, ''));
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const bd = html.slice(html.indexOf('/* BUILD-DATA START */'), html.indexOf('/* BUILD-DATA END */'));
const buildData = new Function(bd + '\nreturn buildData;')();
const D = buildData({
  languages: read('data/languages.csv'), countries: read('data/countries.csv'),
  regions: read('data/regions.csv'), second_language: read('data/second_language.csv'),
  population_by_year: read('data/population_by_year.csv'),
});
const canon = l => D.ALIAS[l] || l;
const YEARS = ['1980', '2000', '2050'];
const CUR_POP_YEAR = '2026';

// ---- regions with their current population, exactly as the map computes density ----
const DM = path.join(NM, 'datamaps/src/js/data');
const world = require(path.join(NM, 'world-atlas/countries-110m.json'));
const worldF = topojson.feature(world, world.objects.countries).features;
const regions = [];
function collect(iso, name, feat, forceLang) {
  if (D.SKIP.has(iso + '|' + name)) return;
  let lang = forceLang;
  if (!lang) { const cf = D.CFG[iso]; if (!cf) return; lang = cf.ov[name] || cf.def; }
  if (!lang) return;
  regions.push({ iso, name, feat, lang: canon(lang) });
}
for (const iso of D.isoList) {
  const f = path.join(DM, iso + '.topo.json'); if (!fs.existsSync(f)) continue;
  const t = JSON.parse(fs.readFileSync(f, 'utf8'));
  topojson.feature(t, t.objects[Object.keys(t.objects)[0]]).features.forEach(ft => { if (ft.properties.name) collect(iso, ft.properties.name, ft); });
}
D.ATLAS_COUNTRIES.forEach(c => {
  const f = worldF.find(x => c.names.indexOf(x.properties.name) >= 0); if (!f) return;
  const cf = D.CFG[c.iso]; collect(c.iso, c.names[0], f, (cf && (cf.ov[c.names[0]] || cf.def)) || null);
});
regions.forEach(o => {
  const pk = D.POP[o.iso + '|' + o.name]; const areaKm = d3geo.geoArea(o.feat) * 6371 * 6371; let dn = 0;
  if (pk != null && (D.NATPOP[o.iso] == null || pk < 0.8 * D.NATPOP[o.iso])) dn = areaKm > 0 ? pk * 1000 / areaKm : 0;
  else if (D.NATDENS[o.iso] != null) dn = D.NATDENS[o.iso];
  else if (pk != null && areaKm > 0) dn = pk * 1000 / areaKm;
  o.pop = dn * areaKm; // people, current
});

// ---- population ratios ----
const P = D.POPYR;
const popRatio = (iso, y) => (P[iso] && P[iso][y] && P[iso][CUR_POP_YEAR]) ? P[iso][y] / P[iso][CUR_POP_YEAR] : 1;

// ---- census anchors: share of country population speaking the language ----
const anchors = {}; // lang -> iso -> used_for -> {share, census_year, source}
read('tools/census_anchors.csv').forEach(r => {
  const share = r.share_percent ? +r.share_percent / 100 : (+r.speakers / +r.population_base);
  ((anchors[r.language] ||= {})[r.iso3] ||= {})[r.used_for] = { share, year: r.census_year, source: r.source };
});

// ---- per-language estimates ----
const sig = x => { if (x === 0) return 0; const d = Math.max(0, 2 - Math.floor(Math.log10(Math.abs(x)))); return +x.toFixed(Math.min(d, 4)); };
const COUNTRY = Object.fromEntries(read('data/countries.csv').map(r => [r.iso3, r.country]));
const out = [];
const legend = D.FAMS.flatMap(([, ls]) => ls);
for (const L of legend) {
  const info = D.LANGINFO[L]; if (!info) continue;
  const [nat, tot] = info;
  const isMSA = L === 'Modern Standard Arabic';
  const homeRegions = regions.filter(r => isMSA ? D.ARABIC.has(r.lang) : r.lang === L);
  const A = anchors[L] || {};
  const anchoredIsos = Object.keys(A).filter(iso => A[iso].current);
  // current speakers by country (weights)
  const w = {};
  homeRegions.forEach(r => { if (!anchoredIsos.includes(r.iso)) w[r.iso] = (w[r.iso] || 0) + r.pop; });
  anchoredIsos.forEach(iso => { w[iso] = A[iso].current.share * (P[iso] ? P[iso][CUR_POP_YEAR] * 1000 : 0); });
  const W = Object.values(w).reduce((s, v) => s + v, 0);
  // second-language zones
  const set = D.L2[L];
  const l2Regions = set ? regions.filter(r => r.lang !== L && (set.has(r.iso) || set.has(r.iso + '|' + r.name))) : [];
  const zone = isMSA ? homeRegions.concat(l2Regions) : l2Regions;
  const ZW = zone.reduce((s, r) => s + r.pop, 0);

  for (const y of YEARS) {
    let F = 1, used = [];
    if (W > 0) {
      F = 0;
      for (const iso in w) {
        let g = popRatio(iso, y);
        const a = A[iso];
        if (a && a.current && a[y] && y !== '2050') { g *= a[y].share / a.current.share; used.push(`${COUNTRY[iso] || iso} ${a[y].year}`); }
        F += (w[iso] / W) * g;
      }
    }
    const F2 = ZW > 0 ? zone.reduce((s, r) => s + r.pop * popRatio(r.iso, y), 0) / ZW : F;
    const nY = nat * F, tY = isMSA ? tot * F2 : nY + (tot - nat) * F2;
    const yearWord = y === '2050' ? 'Projected' : 'Estimated';
    let method, source;
    if (used.length) {
      method = 'census';
      source = `${yearWord} from census language shares (${used.join(', ')}) and UN WPP 2024 population; other countries scaled by UN population change`;
    } else {
      method = 'scaled';
      source = `${yearWord} by scaling the current figure with UN WPP 2024 population change where the language is spoken`;
    }
    if (tot > nat) source += '; second-language speakers scaled by population change in second-language zones';
    out.push([L, y, sig(nY), sig(tY), method, source]);
  }
}
fs.writeFileSync(path.join(ROOT, 'data/speakers_by_year.csv'),
  '﻿' + csvFormatRows([['language', 'year', 'native_millions', 'total_millions', 'method', 'source'], ...out]) + '\n');
console.log(`wrote ${out.length} rows (${out.filter(r => r[4] === 'census').length} census-anchored)`);
