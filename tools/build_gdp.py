"""Country GDP (PPP, constant 2017 international $) for 1980, 2000, 2026 and 2050, plus world totals.
Main source: OECD ENV-Growth 2025 in the IIASA SSP database v3.2 (historical reference + SSP2 projection).
Gaps in 1980/2000 are filled backwards with Maddison Project 2023 real GDP growth, else with constant GDP per person.

Inputs (in a gdp/ folder next to site/):
  gdp/ssp2025.csv.gz    https://raw.githubusercontent.com/JGCRI/gcam-core/master/input/gcamdata/inst/extdata/socioeconomics/SSP/SSP_database_2025.csv.gz
  gdp/maddison2023.csv  data/MaddisonData.rda from the MaddisonData R package (https://github.com/cran/MaddisonData), saved as CSV
Run from the folder that contains site/:  python3 gdp/build_gdp.py site   (needs: pip install country_converter)"""
import csv, gzip, json, collections, sys, warnings
warnings.filterwarnings('ignore')
import country_converter as coco
import logging; logging.getLogger('country_converter').setLevel(logging.ERROR)
SITE = sys.argv[1] if len(sys.argv) > 1 else 'site'
lines = [l for l in gzip.open('gdp/ssp2025.csv.gz', 'rt') if not l.startswith('#')]
rows = list(csv.reader(lines)); H = rows[0]; col = {y: H.index(y) for y in H[5:]}
def series(model, scen, var, unit):
    out = {}
    for x in rows[1:]:
        if x[0].startswith(model) and x[1] == scen and x[3] == var and x[4] == unit:
            out[x[2]] = {int(y): float(x[i]) for y, i in col.items() if i < len(x) and x[i] not in ('',)}
    return out
hist = series('OECD ENV-Growth', 'Historical Reference', 'GDP|PPP', 'billion USD_2017/yr')
ssp2 = series('OECD ENV-Growth', 'SSP2', 'GDP|PPP', 'billion USD_2017/yr')
pop = series('IIASA-WiC POP', 'Historical Reference', 'Population', 'million')
names = sorted(set(hist) | set(ssp2))
iso_of = dict(zip(names, coco.convert(names, to='ISO3', not_found=None)))
bad = [n for n, i in iso_of.items() if not i]
if bad: print('unmapped SSP names:', bad)
# Maddison Project 2023: GDP per person (2011$) x population (thousands) -> real GDP index
mad = collections.defaultdict(dict)
for r in csv.DictReader(open('gdp/maddison2023.csv')):
    if r['gdppc'] and r['pop']: mad[r['ISO']][int(float(r['year']))] = float(r['gdppc']) * float(r['pop'])
popnames = {iso_of.get(n): n for n in pop}
def pop_at(name, y):
    p = pop.get(name, {})
    if y in p: return p[y]
    ys = sorted(p);  # 5-year steps: interpolate
    lo = max([k for k in ys if k <= y], default=None); hi = min([k for k in ys if k >= y], default=None)
    if lo is None or hi is None: return None
    return p[lo] if lo == hi else p[lo] + (p[hi] - p[lo]) * (y - lo) / (hi - lo)
out = {}
for n in names:
    iso = iso_of[n]
    if not iso: continue
    h, s = hist.get(n, {}), ssp2.get(n, {})
    rec = {}
    if 2025 in h and 2030 in s and 2025 in s:
        rec[2026] = (h[2025] * (s[2030] / s[2025]) ** 0.2, 'OECD ENV-Growth 2025 (SSP database v3.2): 2025 estimate moved to 2026 with the SSP2 growth rate for 2025-2030')
    if 2050 in s: rec[2050] = (s[2050], 'OECD ENV-Growth 2025 (SSP database v3.2), SSP2 middle-of-the-road projection')
    first = min(h) if h else None
    for y in (1980, 2000):
        if y in h: rec[y] = (h[y], 'OECD ENV-Growth 2025 (SSP database v3.2), historical reference'); continue
        if first is None: continue
        m = mad.get(iso, {})
        if y in m and first in m:
            rec[y] = (h[first] * m[y] / m[first], f'OECD ENV-Growth {first} value carried back to {y} with Maddison Project 2023 real GDP growth')
        elif y in m and any(k <= first for k in m if k > y):
            last = max(k for k in m if k <= first)  # Maddison ends before the first OECD year: hold GDP flat in between
            rec[y] = (h[first] * m[y] / m[last], f'OECD ENV-Growth {first} value carried back to {y} with Maddison Project 2023 real GDP growth (Maddison to {last})')
        else:
            p0, p1 = pop_at(n, y), pop_at(n, first)
            if p0 and p1: rec[y] = (h[first] * p0 / p1, f'OECD ENV-Growth {first} value carried back to {y} assuming constant GDP per person (IIASA population)')
    out[iso.lower()] = rec
# Somaliland: the sources report Somalia as one; split Somalia's GDP by current population share
regs = list(csv.DictReader(open(f'{SITE}/data/regions.csv', encoding='utf-8-sig')))
psum = collections.Counter()
for r in regs:
    if r['population_thousands'] and r['exclude'].upper() != 'TRUE': psum[r['iso3']] += float(r['population_thousands'])
if 'som' in out:
    f = psum['somld'] / (psum['som'] + psum['somld'])
    som = out['som']; out['somld'] = {}
    for y, (v, s) in list(som.items()):
        out['somld'][y] = (v * f, s + f'; Somaliland\'s share ({f:.0%}) of the Somalia total, by population')
        som[y] = (v * (1 - f), s + f'; Somalia excluding Somaliland ({1-f:.0%} of the total, by population)')
world = {y: sum(r[y][0] for r in out.values() if y in r) for y in (1980, 2000, 2026, 2050)}
countries = [r['iso3'] for r in csv.DictReader(open(f'{SITE}/data/countries.csv', encoding='utf-8-sig'))]
missing = {y: [c for c in countries if y not in out.get(c, {})] for y in (1980, 2000, 2026, 2050)}
print('map countries missing GDP:', missing)
with open(f'{SITE}/data/gdp_by_year.csv', 'w', newline='', encoding='utf-8') as fh:
    fh.write('﻿'); w = csv.writer(fh, lineterminator='\n')
    w.writerow(['iso3', 'year', 'gdp_billion_usd', 'source'])
    for c in countries:
        for y in (1980, 2000, 2026, 2050):
            if y in out.get(c, {}): w.writerow([c, y, f'{out[c][y][0]:.3f}', out[c][y][1]])
WPOP = {1980: 4487654.790, 2000: 6213462.023, 2026: 8335111.500, 2050: 9684720.958}
with open(f'{SITE}/data/world_by_year.csv', 'w', newline='', encoding='utf-8') as fh:
    fh.write('﻿'); w = csv.writer(fh, lineterminator='\n')
    w.writerow(['year', 'population_thousands', 'population_source', 'gdp_billion_usd', 'gdp_source'])
    for y in (1980, 2000, 2026, 2050):
        w.writerow([y, f'{WPOP[y]:.1f}', 'UN World Population Prospects 2024, world total' + (' (medium-variant projection)' if y > 2023 else ''),
                    f'{world[y]:.1f}', f'Sum of all {sum(1 for c, r in out.items() if y in r and c != "somld")} economies in the GDP series (PPP, 2017 international dollars)'])
print({y: round(v / 1000, 1) for y, v in world.items()}, 'trillion')
print('filled:', collections.Counter(v[1].split(' value carried')[0][:60] if 'carried' in v[1] else 'direct' for r in out.values() for y, v in r.items() if y in (1980, 2000)))
