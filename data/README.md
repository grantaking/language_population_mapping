# Globe data

`index.html` reads these CSV files when the page loads. Edit a file, commit it, and the live map picks up the change on the next GitHub Pages deploy. Nothing in `index.html` needs to change.

The first four files describe the map as it is now ("Current"). `population_by_year.csv` and `speakers_by_year.csv` drive the **Population year** switch (1980, 2000, 2050); if either is missing, the switch is hidden and the map works as before. `gdp_by_year.csv` and `world_by_year.csv` add GDP and world shares to the selection panel; if they are missing, those figures are left out.

All files are UTF-8. If you edit them in Excel, save with **File > Save As > CSV UTF-8**, otherwise accented region names (Québec, Bayan-Ölgiy, Đông Bắc) get mangled and stop matching the map. Spreadsheet apps that add or drop the byte-order mark are fine; the page handles both.

Blank cells mean "no value". Booleans accept TRUE/FALSE (also yes/no, 1/0).

## languages.csv

One row per language.

| column | meaning |
|---|---|
| `language` | Name used everywhere else in the data. Must match exactly. |
| `family` | Group heading in the legend. |
| `legend_order` | Position in the legend (any increasing numbers work; gaps are fine). Families appear in the order of their first language. Leave blank to keep a language out of the legend. |
| `color` | Hex color for the map and legend. |
| `native_millions`, `total_millions` | Global speaker counts shown in the tooltip and summed in the selection panel. |
| `merge_into` | If filled, this language is drawn as the named language instead (for example `Hindi` with `merge_into = Hindustani`). The merged-into language needs its own row with its own color, counts, and legend position. The member row's color and counts are kept for reference but are not shown. Clear this cell to split a language back out (and give it a `legend_order`). |
| `arabic_dialect` | TRUE for Arabic varieties. When Modern Standard Arabic is selected, these regions get the MSA tint. |

A language appears in the legend only if some region uses it or it has rows in `second_language.csv`.

## countries.csv

One row per country or territory.

| column | meaning |
|---|---|
| `iso3` | Lowercase three-letter code (plus `somld` for Somaliland). |
| `country` | Readable name. Not used by the map. |
| `default_language` | Plurality language for every region in the country that has no language of its own in `regions.csv`. |
| `national_density_per_km2` | Fallback density for regions without a usable population figure: the UN 2026 population divided by the country's total area on the map. |
| `national_population_thousands` | UN World Population Prospects 2024 estimate for 2026. Used to sanity-check region populations (see below). |
| `geometry` | `admin1` = drawn region by region from the datamaps province files. `country` = drawn as one shape from the world-atlas country layer, for places with no province file. |
| `atlas_names` | For `geometry = country` only: the name(s) of the shape in the world-atlas layer, separated by `|`. The first name is the region name used in `regions.csv` and `second_language.csv`. |

To add a country that has a datamaps province file, add a row with `geometry = admin1`, then add its regions to `regions.csv` (optional; regions not listed just use the default language and national density).

## regions.csv

One row per admin-1 region (province, state, oblast, and so on).

| column | meaning |
|---|---|
| `iso3` | Country code from `countries.csv`. |
| `region` | Region name exactly as it appears in the map files. Do not rename these; a changed name will no longer match a shape. |
| `language` | Plurality language for this region. Blank = use the country's `default_language`. |
| `population_thousands` | Region population in thousands, estimated for 2026 (see below). Blank = use the national density. |
| `population_year` | Year of the underlying census or estimate, before it was brought forward to 2026. |
| `population_source` | Where the figure comes from: the source unit's name, its Wikidata item or the census table it was taken from, and any adjustment (a share by area, a city subtracted from its county, two units added together). Not read by the map. |
| `exclude` | TRUE to leave the region off the map. |

**How height is computed:** if a region has a population and it is less than 80% of its country's national population, density = population / region area. Otherwise the region uses `national_density_per_km2`. (The 80% check screens out bad source figures that equal a whole country's population.) When several shapes share one region name (an island group, or a city and province drawn separately under one name), their areas are added together. Heights are then scaled so the 97th-percentile density is the tallest.

### How the region populations were built

1. **Matching.** Each map region was matched to Natural Earth 10m admin-1 units by overlapping area. Natural Earth carries each unit's ISO 3166-2 code and Wikidata item.
2. **Figures.** For each unit, the latest population statement on Wikidata was taken, looked up by ISO code and by Natural Earth's link, with the better name match kept. Stale codes and wrong links were checked by hand (Morocco's ISO codes were reassigned in 2015, so its pre-2015 regions use census tables instead). Vietnam uses figures from before its 2025 province merger, because the map shows the old provinces.
3. **Census tables.** Where Wikidata has no figure or the map shows older borders, figures come from census tables on Wikipedia and statoids.com, listed in `tools/hand_pops.csv` (by Natural Earth unit) and `tools/hand_map_pops.csv` (by map region). Former regions are rebuilt by adding up their present-day parts, for example Ghana's pre-2019 Northern Region = Northern + Savannah + North East.
4. **Clean-up.** A Wikidata item used by several units is shared by area. A city counted inside its county is subtracted from the county. Units still without a figure get a share of the remaining national total by area, capped at 3 times the national mean density; their source says so.
5. **2026 estimate.** Each figure is moved from its own year to 2026 with the country's UN growth over the same years, then every country is scaled so its regions add up to the UN 2026 total (except Somalia and Somaliland, which the UN reports together). For most countries the scaling is within a few percent; it is larger where the latest census is old (Libya, Eritrea), where only a proxy exists (Singapore, which uses each district's share of registered voters), or where districts were split after the census (Uganda).

Uninhabited regions (Bouvet Island, New Zealand's subantarctic islands, the Paracel Islands) are set to 0.

Three Vietnamese rows (Đông Bắc, Đồng Bằng Sông Hồng, Đông Nam Bộ) carry regional names in the map files, but their shapes are the provinces of Bắc Kạn, Hưng Yên and Đồng Nai. They are now included and use those provinces' populations.

## second_language.csv

One row per second-language glow zone.

| column | meaning |
|---|---|
| `language` | The lingua franca (must match `languages.csv`; use the merged name, for example `Hindustani`). |
| `iso3` | Country. |
| `region` | Blank = the whole country glows. Filled = only that region (name must match `regions.csv` exactly). |

Regions where the language is already the plurality language show the full highlight instead of the glow, so a whole-country row is safe even when the language is native in part of that country.

## population_by_year.csv

UN World Population Prospects 2024 country populations, used for the year switch. Estimates for 1980 and 2000; medium-variant projections for 2026 and 2050.

| column | meaning |
|---|---|
| `iso3` | Country code. |
| `year` | 1980, 2000, 2026 or 2050. |
| `population_thousands` | Population in thousands. |
| `source` | Where the figure comes from. Somaliland uses Somalia's figures, since the UN does not report it separately; only the growth ratios are used. |

**How heights change by year:** each region's current density is multiplied by its country's population ratio (population in the chosen year / population in 2026), so a country's regional pattern stays as it is today and only its overall level moves. The height scale is fixed at the current map's scale for every year, so 1980 reads lower and 2050 taller. Regions are not re-drawn for past borders.

## speakers_by_year.csv

Native and total speaker estimates for 1980, 2000 and 2050, shown in tooltips and in the selection totals when a year is picked. "Current" figures still come from `languages.csv`.

| column | meaning |
|---|---|
| `language` | Must match `languages.csv` (merged names, for example `Hindustani`). |
| `year` | 1980, 2000 or 2050. |
| `native_millions`, `total_millions` | Estimates, rounded to three significant figures. |
| `method` | `census`: anchored to census language shares; `scaled`: scaled by UN population change only. |
| `source` | Plain-language description of how the row was produced. |

This file is generated by `tools/build_speakers_by_year.js`; re-run it after changing current speaker counts, regions, second-language zones, or the census anchors. The method:

- **Native speakers:** the current figure is multiplied by a growth factor. The factor averages each country's growth, weighted by where the language's speakers live today. Population growth comes from the UN figures above. For India, Pakistan and China, it also uses the change in the language's share of the population between censuses (`tools/census_anchors.csv`): India 1991, 2001 and 2011; Pakistan 1981, 1998 and 2023; China 1990, 2000 and 2020 (ethnic group counts as a proxy for Zhuang, Uyghur and Tibetan). 1980 uses the nearest available census (India 1991, China 1990). 2050 uses population change only.
- **Total speakers:** native estimate plus the current second-language speakers scaled by population change in the language's second-language zones. This does not capture changes in how widely a language is learned (for example the growth of English as a second language since 1980), so totals for global lingua francas are conservative.
- Published counts from different sources and editions (Ethnologue editions, censuses) define languages differently, so they are used as growth anchors rather than copied in directly. Copying them would create artificial jumps between years.

To regenerate (needs Node.js):

```
cd tools && npm install && cd ..
node tools/build_speakers_by_year.js
```

## gdp_by_year.csv

Country GDP for each year the map shows. One row per country and year.

| column | meaning |
|---|---|
| `iso3` | Country code from `countries.csv`. |
| `year` | 1980, 2000, 2026 (used for "Current") or 2050. |
| `gdp_billion_usd` | GDP in billions of US dollars at purchasing power parity, constant 2017 prices, so every year is on the same scale. |
| `source` | Where the figure comes from and how any gap was filled. |

Sources and method:

- **Main series:** OECD ENV-Growth 2025, published in the IIASA Shared Socioeconomic Pathways (SSP) database v3.2. It gives historical estimates to 2025 and projections after that.
- **2026:** the 2025 estimate moved forward one year at the SSP2 growth rate for 2025 to 2030.
- **2050:** the SSP2 ("middle of the road") projection.
- **Gaps in 1980 and 2000** (mostly former Soviet, Yugoslav and Czechoslovak states, plus a few countries whose series start later): the earliest OECD value is carried back with Maddison Project Database 2023 real GDP growth. Where Maddison has no data, GDP per person is held constant and scaled by IIASA population.
- **Somaliland:** the sources report Somalia as a whole, so Somalia's GDP is split between the two by current population.
- **Greenland** has no figure in these sources and is left out of the GDP sums.

**Regional GDP** is not stored. The page splits each country's GDP among its regions by population (`regions.csv`), using the same regional pattern for every year.

**Language GDP** in the selection panel and tooltips:

- **Plurality-region GDP:** GDP of the regions where a selected language is the plurality language.
- **Lingua franca GDP:** GDP of the regions where a selected language has a second-language glow (`second_language.csv`, plus every Arabic-dialect region for Modern Standard Arabic) and no selected language is the plurality.

Each region is counted once, so the two figures can be added. Shares are out of the world total in `world_by_year.csv`.

## world_by_year.csv

The denominators for the shares shown in the selection panel.

| column | meaning |
|---|---|
| `year` | 1980, 2000, 2026, 2050. |
| `population_thousands` | World population, UN World Population Prospects 2024 (medium variant for 2026 and 2050). |
| `gdp_billion_usd` | World GDP: the sum of every economy in the GDP series, including ones not drawn on the map. Same units as `gdp_by_year.csv`. |

The share of total speakers can be overstated, because people who speak several languages are counted once for each language.

## tools/census_anchors.csv

The census language shares used above. One row per language, country and census.

| column | meaning |
|---|---|
| `language` | Map language (for example `Hindustani` = census Hindi + Urdu). |
| `iso3` | Country of the census. |
| `census_year` | Census year. |
| `used_for` | Which map year the census stands for: `1980`, `2000` or `current`. A language needs a `current` row for a country before its other rows are used. |
| `speakers`, `population_base` | Speaker count and the population it is a share of. |
| `share_percent` | Used instead when the census reports a percentage. |
| `source`, `note` | Citation and caveats. |

## Testing locally

Browsers block data files on pages opened straight from disk. From the folder that holds `index.html`, run

```
python3 -m http.server
```

and open http://localhost:8000.
