# Globe data

`index.html` reads these four CSV files when the page loads. Edit a file, commit it, and the live map picks up the change on the next GitHub Pages deploy. Nothing in `index.html` needs to change.

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
| `national_density_per_km2` | Fallback density for regions without a usable population figure. |
| `national_population_thousands` | Used to sanity-check region populations (see below). |
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
| `population_thousands` | Region population in thousands. Blank = use the national density. |
| `exclude` | TRUE to leave the region off the map. |

**How height is computed:** if a region has a population and it is less than 80% of its country's national population, density = population / region area. Otherwise the region uses `national_density_per_km2`. (The 80% check screens out bad source figures that equal a whole country's population.) Heights are then scaled so the 97th-percentile density is the tallest.

## second_language.csv

One row per second-language glow zone.

| column | meaning |
|---|---|
| `language` | The lingua franca (must match `languages.csv`; use the merged name, for example `Hindustani`). |
| `iso3` | Country. |
| `region` | Blank = the whole country glows. Filled = only that region (name must match `regions.csv` exactly). |

Regions where the language is already the plurality language show the full highlight instead of the glow, so a whole-country row is safe even when the language is native in part of that country.

## Testing locally

Browsers block data files on pages opened straight from disk. From the folder that holds `index.html`, run

```
python3 -m http.server
```

and open http://localhost:8000.
