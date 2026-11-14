"""Recolor languages.csv from a language family tree.
Hue: each family gets its own hue band; leaves are laid out depth-first along the band, with wider gaps between
higher-level branches, so closer relatives get closer hues. Lightness and chroma: chosen per language so that languages
whose regions border each other on the map are easy to tell apart (adjacency from color/adjacency.js).
European families, Japanese and Korean keep their colors. Minor isolates, the Caucasian languages, Georgian, Hmong and the
indigenous languages of the Americas are shades of grey. Arabic varieties form a smooth gradient by geography (see ARABIC)."""
import csv, json, math, random, sys, collections
# ---- OKLab / OKLCH helpers ----
def srgb2lin(c): c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lin2srgb(c): return 12.92*c if c<=0.0031308 else 1.055*c**(1/2.4)-0.055
def hex2lab(h):
    r,g,b=(srgb2lin(int(h[i:i+2],16)) for i in (1,3,5))
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=(math.copysign(abs(x)**(1/3),x) for x in (l,m,s))
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
def lab2rgb(L,a,b):
    l=(L+0.3963377774*a+0.2158037573*b)**3; m=(L-0.1055613458*a-0.0638541728*b)**3; s=(L-0.0894841775*a-1.2914855480*b)**3
    return (4.0767416621*l-3.3077115913*m+0.2309699292*s, -1.2684380046*l+2.6097574011*m-0.3413193965*s, -0.0041960863*l-0.7034186147*m+1.7076147010*s)
def oklch2hex(L,C,h):
    # reduce chroma until in sRGB gamut
    for _ in range(60):
        a,b=C*math.cos(math.radians(h)),C*math.sin(math.radians(h)); rgb=lab2rgb(L,a,b)
        if all(-1e-4<=x<=1+1e-4 for x in rgb): break
        C*=0.95
    return '#%02X%02X%02X'%tuple(round(max(0,min(1,lin2srgb(max(0,x))))*255) for x in rgb)
def hex2lch(h):
    L,a,b=hex2lab(h); return L, math.hypot(a,b), math.degrees(math.atan2(b,a))%360
def dE(h1,h2):
    a,b=hex2lab(h1),hex2lab(h2); return math.dist(a,b)
# ----
S = 'data/languages.csv'   # run from the folder that contains data/
KEEP_FAM = {'Slavic', 'Germanic', 'Romance', 'Baltic', 'Hellenic', 'Albanian', 'Uralic', 'Japonic', 'Koreanic', 'Other'}
KEEP_LANG = {'Mandarin', 'Modern Standard Arabic'}
# greys: bordering pairs get different shades
GREY = {'Basque': '#9C9C9C', 'Georgian': '#A3A3A3', 'Abkhaz': '#868686', 'Chechen': '#999999', 'Ingush': '#B8B8B8', 'Avar': '#828282',
        'Kabardian': '#ADADAD', 'Hmong': '#A0A0A0', 'Quechua': '#9A9A9A', 'Aymara': '#BABABA', 'Guarani': '#A6A6A6',
        "K'iche'": '#959595', "Q'eqchi'": '#B4B4B4', 'Inuktitut': '#A8A8A8', 'Greenlandic': '#B6B6B6'}
# Arabic varieties: one rose band; hue follows longitude and lightness follows latitude of where each is mostly spoken,
# so neighbouring varieties shade into each other (Moroccan -> Algerian -> Tunisian -> Libyan -> Egyptian ...)
ARABIC = {'Hassaniya Arabic': (-12, 21), 'Moroccan Arabic': (-6, 32), 'Algerian Arabic': (3, 34), 'Tunisian Arabic': (10, 36),
          'Libyan Arabic': (17, 29), 'Egyptian': (30, 27), 'Chadian Arabic': (19, 13), 'Sudanese Arabic': (31, 15),
          'Levantine': (36, 34.5), 'Mesopotamian': (44, 32), 'Hijazi': (40, 22), 'Gulf/Najdi': (47, 25), 'Yemeni': (46, 15), 'Omani': (57, 21)}
def arabic_color(lon, lat):
    t = (lon + 12) / 69; u = (lat - 13) / 23   # west -> east: pink-rose -> clay; south -> north: darker -> lighter
    return oklch2hex(0.58 + 0.18 * u, 0.105, 345 + 65 * t)
# family: (hue start, hue end, chroma, tree)   hues are OKLCH degrees
T = {
 'Semitic': (356, 384, 0.095, [
    ['Tigre', 'Tigrinya', 'Amharic'],                                   # Ethiosemitic
    ['Hebrew'],                                                         # Northwest Semitic
    [['Modern Standard Arabic'], ['Hassaniya Arabic', 'Moroccan Arabic', 'Algerian Arabic', 'Tunisian Arabic', 'Libyan Arabic', 'Maltese'],   # Arabic: Maghrebi
     ['Egyptian', 'Sudanese Arabic', 'Chadian Arabic'],
     ['Levantine'], ['Mesopotamian'],
     ['Gulf/Najdi', 'Hijazi', 'Yemeni', 'Omani']]]),
 'Cushitic': (40, 48, 0.10, [['Afar', 'Somali', 'Oromo'], ['Sidamo']]),
 'Turkic': (52, 78, 0.075, [['Chuvash'], ['Turkish', 'Gagauz', 'Azerbaijani', 'Turkmen'],
    [['Tatar', 'Bashkir'], ['Karachay'], ['Kazakh', 'Karakalpak'], ['Kyrgyz']], ['Uzbek', 'Uyghur'], ['Yakut', 'Tuvan']]),
 'Berber': (60, 68, 0.165, [['Kabyle', 'Tachelhit'], ['Tamasheq']]),
 'Mongolic': (80, 84, 0.09, [['Mongolian', 'Kalmyk']]),
 'Chadic': (92, 92, 0.12, [['Hausa']]),
 'Tai-Kadai': (94, 108, 0.13, [[['Thai', 'Northern Thai', 'Southern Thai', 'Lao', 'Shan', 'Tai Dam'], ['Tày', 'Nùng'], ['Zhuang']]]),
 'Niger-Congo': (120, 147, 0.15, [
    [['Bambara', 'Dyula', 'Maninka', 'Mandinka'], ['Soninke'], ['Susu'], ['Kpelle', 'Loma', 'Mende'], ['Vai'], ['Dan']],   # Mande
    [['Wolof', 'Serer', 'Fula'], ['Jola', 'Balanta'], ['Temne', 'Kissi']],                                                 # Atlantic
    [['Bassa', 'Grebo']],                                                                                                    # Kru
    [['Mossi', 'Farefare', 'Dagbani', 'Dagaare', 'Moba', 'Kabiye', 'Tem', 'Gourmanché'], ['Senufo'], ['Lobi'], ['Bariba']],  # Gur
    [['Akan', 'Baoulé'], ['Ewe', 'Fon', 'Gun', 'Aja']],                                                                      # Kwa
    [['Yoruba', 'Igala'], ['Igbo'], ['Edo', 'Urhobo'], ['Ijaw']],                                                            # Volta-Niger, Ijoid
    [['Efik', 'Tiv'], ['Sango']],                                                                                            # Benue-Congo (non-Bantu), Ubangian
    [['Fang'], ['Kikongo', 'Lingala', 'Tshiluba'],                                                                           # Bantu
     ['Kinyarwanda', 'Kirundi', 'Luganda', 'Soga', 'Gwere', 'Masaba', 'Nyankore-Kiga', 'Nyoro-Tooro', 'Konzo', 'Luhya'],
     ['Kikuyu', 'Kamba'], ['Swahili'], ['Makhuwa', 'Lomwe', 'Yao'],
     ['Bemba', 'Tonga', 'Chichewa', 'Tumbuka', 'Sena'], ['Shona'], ['Oshiwambo', 'Kwangali', 'Herero'],
     ['Tswana', 'Sotho', 'Northern Sotho', 'Lozi'], ['Zulu', 'Xhosa', 'Swazi', 'Ndebele'], ['Tsonga', 'Tswa']]]),
 'Sino-Tibetan': (152, 175, 0.12, [['Mandarin', 'Wu', 'Gan', 'Xiang', 'Min', 'Cantonese'],
    [['Tibetan', 'Dzongkha'], ['Burmese'], ['Karen'], ['Mizo', 'Chin'], ['Meitei'], ['Angami', 'Konyak'], ['Nyishi']]]),
 'Austroasiatic': (316, 326, 0.12, [['Vietnamese', 'Mường'], ['Khmer'], ['Khasi']]),
 'Indo-Aryan': (195, 238, 0.11, [['Kashmiri', 'Shina'], ['Punjabi', 'Sindhi'], ['Gujarati'], ['Marathi', 'Konkani'], ['Sinhala'],
    ['Hindustani', 'Romani'], ['Nepali'], ['Maithili', 'Oriya', 'Bengali', 'Assamese']]),
 'Iranian': (242, 264, 0.10, [[['Kurdish', 'Balochi', 'Gilaki', 'Mazandarani'], ['Persian', 'Luri']], ['Pashto', 'Pamiri', 'Ossetian']]),
 'Nilo-Saharan': (268, 284, 0.15, [['Songhay', 'Zarma'], ['Kanuri'], ['Berta'], ['Sara', 'Lugbara', "Ma'di"],
    [['Dinka', 'Nuer', 'Luo', 'Acholi', 'Lango', 'Alur', 'Adhola'], ['Karamojong', 'Teso', 'Kakwa'], ['Kalenjin']]]),
 'Austronesian': (333, 349, 0.14, [
    [['Ilocano', 'Pangasinan'], ['Kapampangan'], ['Tagalog', 'Bikol', 'Cebuano', 'Hiligaynon', 'Waray', 'Tausug'], ['Maguindanao', 'Maranao'], ['Gorontalo']],
    [['Malay', 'Minangkabau', 'Banjar', 'Iban'], ['Acehnese'], ['Sundanese'], ['Balinese', 'Sasak'], ['Javanese'], ['Batak'], ['Buginese'], ['Malagasy']],
    [['Tetum'], ['Fijian', 'Tongan', 'Samoan']]]),
 'Dravidian': (351, 361, 0.13, [['Tamil', 'Malayalam', 'Kannada'], ['Telugu']]),
}
def walk(tree, path=()):
    for i, x in enumerate(tree):
        if isinstance(x, list): yield from walk(x, path + (i,))
        else: yield x, path + (i,)
hue, fam_of, order = {}, {}, {}
for fam, (h0, h1, c, tree) in T.items():
    leaves = list(walk(tree)); pos = [0.0]
    for (a, pa), (b, pb) in zip(leaves, leaves[1:]):
        d = next(i for i in range(min(len(pa), len(pb))) if pa[i] != pb[i])   # depth where the paths split
        pos.append(pos[-1] + 1 + {0: 2.5, 1: 1.2, 2: 0.4}.get(d, 0))
    span = pos[-1] or 1
    for k, ((n, _), p) in enumerate(zip(leaves, pos)):
        hue[n] = (h0 + (h1 - h0) * p / span) % 360; fam_of[n] = fam; order[n] = k

rows = list(csv.DictReader(open(S, encoding='utf-8-sig'))); cols = list(rows[0].keys())
byname = {r['language']: r for r in rows}
free = [r['language'] for r in rows if not r['merge_into'] and r['family'] not in KEEP_FAM and r['language'] not in KEEP_LANG and r['language'] not in GREY and r['language'] not in ARABIC]
missing = [n for n in free if n not in hue]
if missing: sys.exit('no tree position for: ' + ', '.join(missing))
extra = [n for n in hue if n not in byname]
if extra: print('in tree but not in languages.csv:', extra)
chroma = {n: T[fam_of[n]][2] for n in hue}
color = {r['language']: r['color'] for r in rows if not r['merge_into']}
for n, h in GREY.items(): color[n] = h
for n, (lon, lat) in ARABIC.items(): color[n] = arabic_color(lon, lat)

# optional: keep the current colors of every family not listed in RECOLOR (so a partial recolor leaves the rest alone)
RECOLOR = set(sys.argv[1:])
if RECOLOR:
    free = [n for n in free if fam_of[n] in RECOLOR]
A = json.load(open('tools/language_adjacency.json'))
used = set(A['used'])
pairs = []
for k, w in A['adj'].items():
    a, b = k.split('||')
    if a in color and b in color and (a in free or b in free): pairs.append((a, b, math.log1p(w)))
fam_pairs = []
for fam in T:
    ms = [n for n in free if fam_of.get(n) == fam]
    fam_pairs += [(a, b) for i, a in enumerate(ms) for b in ms[i + 1:]]
LV = [0.50, 0.57, 0.64, 0.71, 0.78, 0.86]; CV = [1.0, 0.72]
def make(n, li, ci, dh=0): return oklch2hex(LV[li], chroma[n] * CV[ci], hue[n] + dh)
native = {r['language']: float(r['native_millions'] or 0) for r in rows}
MINL = {'Turkic': 0.64, 'Tai-Kadai': 0.64, 'Chadic': 0.64, 'Berber': 0.64, 'Mongolic': 0.57, 'Niger-Congo': 0.57, 'Cushitic': 0.57}  # yellows and oranges turn brown when dark
def allowed(n, li, ci):
    if LV[li] < MINL.get(fam_of[n], 0.5): return False
    return native.get(n, 0) < 20 or (1 <= li <= 4)   # big languages: no extremes of lightness
OPTS = {n: {(li, ci, dh): make(n, li, ci, dh) for li in range(len(LV)) for ci in range(2) for dh in (-4, 0, 4) if allowed(n, li, ci)} for n in free}
LAB = {h: hex2lab(h) for o in OPTS.values() for h in o.values()}
for h in color.values(): LAB[h] = hex2lab(h)
nb = collections.defaultdict(list)   # per language: (other, kind, weight)
for a, b, w in pairs: nb[a].append((b, 0, w)); nb[b].append((a, 0, w))
for a, b in fam_pairs: nb[a].append((b, 1, 0)); nb[b].append((a, 1, 0))
def term(kind, w, d): return w * max(0, 0.13 - d) ** 2 * 100 if kind == 0 else max(0, 0.045 - d) ** 2 * 60
def local(n, opt):
    h = OPTS[n][opt]; L = LAB[h]; c = 0.004 * abs(LV[opt[0]] - 0.69) + 0.002 * opt[1] + 0.001 * (opt[2] != 0)
    for m, kind, w in nb[n]: c += term(kind, w, math.dist(L, LAB[color[m]]))
    return c
def total():
    c = sum(term(0, w, math.dist(LAB[color[a]], LAB[color[b]])) for a, b, w in pairs)
    c += sum(term(1, 0, math.dist(LAB[color[a]], LAB[color[b]])) for a, b in fam_pairs)
    return c
random.seed(7)
best = None
for restart in range(80):
    st = {n: random.choice(list(OPTS[n])) for n in free}
    for n in free: color[n] = OPTS[n][st[n]]
    improved = True
    while improved:
        improved = False
        for n in random.sample(free, len(free)):
            cur = local(n, st[n]); bo = st[n]
            for o in OPTS[n]:
                color[n] = OPTS[n][o]; c = local(n, o)
                if c < cur - 1e-12: cur, bo, improved = c, o, True
            st[n] = bo; color[n] = OPTS[n][bo]
    tc = total()
    print('restart', restart, 'cost', round(tc, 4))
    if best is None or tc < best[0]: best = (tc, dict(st))
st = best[1]
for n in free: color[n] = OPTS[n][st[n]]
def cost(st): pass
for r in rows:
    n = r['merge_into'] or r['language']
    if n in color: r['color'] = color[n]
# legend: within each recolored family, list languages in tree order (family positions unchanged)
for fam in set(fam_of.values()):
    rs = [r for r in rows if r['family'] == fam and not r['merge_into'] and r['legend_order']]
    slots = sorted(float(r['legend_order']) for r in rs)
    for r, o in zip(sorted(rs, key=lambda r: order.get(r['language'], 999)), slots): r['legend_order'] = str(int(o))
with open(S, 'w', newline='', encoding='utf-8') as f:
    f.write('﻿'); w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n'); w.writeheader(); w.writerows(rows)
# report the closest bordering pairs
close = sorted(((dE(color[a], color[b]), a, b) for a, b, w in pairs))
print('closest bordering pairs:', [(round(d, 3), a, b) for d, a, b in close[:15]])
