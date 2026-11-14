// Language adjacency on the map: pairs of plurality languages whose regions touch (shared 0.25-degree grid cells along borders)
// Run from the folder that contains data/ (needs: npm install topojson-client d3-dsv datamaps@0.5.10 world-atlas@2)
const fs=require('fs'), topojson=require('topojson-client'), d3=require('d3-dsv');
const S='data/', rd=f=>d3.csvParse(fs.readFileSync(S+f,'utf8').replace(/^﻿/,''));
const langs=rd('languages.csv'), countries=rd('countries.csv'), regions=rd('regions.csv');
const merge={}; langs.forEach(r=>{ if(r.merge_into) merge[r.language]=r.merge_into; });
const canon=l=>merge[l]||l;
const def={}, ov={}, skip=new Set();
countries.forEach(c=>{ def[c.iso3]=c.default_language; });
regions.forEach(r=>{ const k=r.iso3+'|'+r.region; if(r.language) ov[k]=r.language; if(String(r.exclude).toUpperCase()==='TRUE') skip.add(k); });
const feats=[];
const DM='node_modules/datamaps/src/js/data/';
countries.forEach(c=>{
  if(c.geometry==='country') return;
  const p=DM+c.iso3+'.topo.json'; if(!fs.existsSync(p)) return;
  const t=JSON.parse(fs.readFileSync(p)); const o=t.objects[Object.keys(t.objects)[0]];
  topojson.feature(t,o).features.forEach(f=>{ const n=f.properties.name; if(!n) return; const k=c.iso3+'|'+n; if(skip.has(k)) return;
    feats.push({lang:canon(ov[k]||def[c.iso3]), f}); });
});
const w=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json'));
const wf=topojson.feature(w,w.objects.countries).features;
countries.forEach(c=>{ if(c.geometry!=='country') return; const names=c.atlas_names.split('|'); const f=wf.find(x=>names.includes(x.properties.name)); if(!f) return;
  const k=c.iso3+'|'+names[0]; if(skip.has(k)) return; feats.push({lang:canon(ov[k]||def[c.iso3]), f}); });
const G=0.25, cells=new Map();
function ring(r,lang){ for(let i=1;i<r.length;i++){ const [x0,y0]=r[i-1],[x1,y1]=r[i]; const n=Math.max(1,Math.ceil(Math.hypot(x1-x0,y1-y0)/(G/2)));
  for(let j=0;j<=n;j++){ const x=x0+(x1-x0)*j/n, y=y0+(y1-y0)*j/n; const key=Math.floor(x/G)+','+Math.floor(y/G); let s=cells.get(key); if(!s){s=new Set();cells.set(key,s);} s.add(lang);} } }
feats.forEach(({lang,f})=>{ const g=f.geometry; if(!g) return; const polys=g.type==='Polygon'?[g.coordinates]:g.coordinates; polys.forEach(p=>p.forEach(r=>ring(r,lang))); });
const adj={};
cells.forEach(s=>{ const a=[...s].sort(); for(let i=0;i<a.length;i++) for(let j=i+1;j<a.length;j++){ const k=a[i]+'||'+a[j]; adj[k]=(adj[k]||0)+1; } });
const used=[...new Set(feats.map(o=>o.lang))].sort();
fs.writeFileSync('tools/language_adjacency.json', JSON.stringify({used, adj}));
console.log('features', feats.length, 'languages used', used.length, 'adjacent pairs', Object.keys(adj).length);
