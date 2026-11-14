"""Plurality-language review (November 2026).

Basis agreed with the user: the main language spoken at home where a census or large survey asks it;
otherwise mother tongue / first language; where no language data exist, the largest ethnic group's language
(census ethnicity) or a standard regional reference, and the source says which.

DEFAULTS: country default language changes.  CHANGES: (iso3, region) -> (language, source).
CONFIRMED: (iso3, region) -> source, for existing overrides checked and kept.
"""

DEFAULTS = {
    'twn': ('Mandarin', 'Taiwan 2020 census: main language Mandarin 66.3%, Hokkien 31.7%, Hakka 1.5% (LINE Today / The News Lens report on the census)'),
    'sgp': ('English', 'Singapore 2020 census: language most frequently spoken at home English 48.3%, Mandarin 29.9% (CIA World Factbook)'),
    'cpv': ('Cape Verdean Creole', 'Cape Verdean Creole (Kabuverdianu) is the home language of nearly all residents; Portuguese is the official written language (Wikipedia: Cape Verdean Creole)'),
    'gnb': ('Guinea-Bissau Creole', 'Guinea-Bissau Creole (Kriol) is the most widely spoken home language; Portuguese is spoken at home by a small minority (Wikipedia: Guinea-Bissau Creole)'),
    'slb': ('Pijin', 'Solomon Islands Pijin is the lingua franca; local languages are fragmented (70+), and English is a home language for very few (Wikipedia: Pijin)'),
}

UG = {  # Uganda districts by sub-region (Wikipedia: Sub-regions of Uganda; 2014 census ethnic homelands)
    'Luganda': 'Kalangala Kayunga Mukono Sembabule Mpigi Kampala Kiboga Nakasongola Wakiso Luweero Mubende Mityana Nakaseke Rakai Masaka Buikwe Buvuma Butambala Gomba Kyankwanzi Lwengo Lyantonde Bukomansimbi Kalungu',
    'Soga': 'Jinja Iganga Kamuli Kaliro Namutumba Mayuge Bugiri Luuka Buyende Namayingo',
    'Teso': 'Kumi Soroti Katakwi Amuria Ngora Bukedea Serere Kaberamaido',
    'Lango': 'Amolatar Lira Dokolo Oyam Apac Kole Alebtong Otuke',
    'Acholi': 'Kitgum Gulu Pader Amuru Lamwo Agago Nwoya Abim',
    'Lugbara': 'Arua Maracha Yumbe',
    'Kakwa': 'Koboko',
    'Alur': 'Nebbi Zombo',
    "Ma'di": 'Moyo Adjumani',
    'Nyoro-Tooro': 'Masindi Hoima Kibale Buliisa Kiryandongo Kabarole Kyenjojo Kamwenge Kyegegwa Ntoroko',
    'Konzo': 'Kasese Bundibugyo',
    'Nyankore-Kiga': 'Bushenyi Ibanda Isingiro Mbarara Ntungamo Rubirizi Mitooma Sheema Buhweju Kabale Rukungiri Kanungu',
    'Kinyarwanda': 'Kisoro',
    'Masaba': 'Mbale Manafwa Sironko Bulambuli Bududa',
    'Kalenjin': 'Kapchorwa Bukwa Kween Amudat',
    'Adhola': 'Tororo',
    'Luhya': 'Busia Butaleja',
    'Gwere': 'Pallisa Budaka Kibuku',
    'Karamojong': 'Moroto Kotido Kaabong Napak Nakapiripirit',
}
UG_SRC = 'Uganda district by sub-region: main language of the largest ethnic group, 2014 census ethnic homelands (Wikipedia: Sub-regions of Uganda); Luganda and Swahili are lingua francas'

C = {}
def add(iso, regions, lang, src):
    for r in regions: C[(iso, r)] = (lang, src)

# ---------------- Asia ----------------
add('ind', ['Lakshadweep'], 'Malayalam', 'India 2011 census: Malayalam is the largest mother tongue (Wikipedia: Indian states by most spoken scheduled languages)')
add('ind', ['Andaman and Nicobar'], 'Bengali', 'India 2011 census: Bengali is the largest mother tongue (Wikipedia: Indian states by most spoken scheduled languages)')
add('ind', ['Daman and Diu', 'Dadra and Nagar Haveli'], 'Gujarati', 'India 2011 census: Gujarati is the largest scheduled mother tongue (Wikipedia: Indian states by most spoken scheduled languages)')
add('ind', ['Nagaland'], 'Konyak', 'India 2011 census: Konyak is the largest mother tongue in Nagaland (Morung Express on census language data)')
add('pak', ['F.C.T.'], 'Punjabi', 'Pakistan 2023 census, mother tongue in Islamabad: Punjabi 51%, Pashto 18%, Urdu 16% (Gallup Pakistan)')
add('twn', ['Changhua', 'Nantou', 'Yunlin', 'Chiayi', 'Tainan City', 'Pingtung'], 'Min', 'Taiwan 2020 census: Hokkien (Min) is the most used main language in Changhua, Nantou, Yunlin, Chiayi County, Tainan and Pingtung (LINE Today / The News Lens report on the census)')
add('lka', ['Ampāra'], 'Tamil', 'Sri Lanka 2012 census: Moors 43.6% and Tamils 17.4% (both Tamil-speaking) vs Sinhalese 38.7% (Wikipedia: Ampara District)')
add('lka', ['Nuvara Ĕliya'], 'Tamil', 'Sri Lanka 2024 census: Indian Tamils 362,299 + Sri Lankan Tamils 60,288 vs Sinhalese 281,904 (citypopulation.de)')
add('npl', ['Sagarmatha'], 'Maithili', 'Nepal 2011 census: Saptari and Siraha districts, which are Maithili-speaking, hold about half of the zone (statoids.com: Districts of Nepal; Wikipedia: Maithili language)')
add('tha', ['Amnat Charoen', 'Bueng Kan', 'Buri Ram', 'Chaiyaphum', 'Kalasin', 'Khon Kaen', 'Loei', 'Maha Sarakham', 'Mukdahan', 'Nakhon Phanom', 'Nong Bua Lam Phu', 'Nong Khai', 'Roi Et', 'Sakon Nakhon', 'Si Sa Ket', 'Ubon Ratchathani', 'Udon Thani', 'Yasothon'],
    'Lao', 'Isan, a variety of Lao, is the home language of most people in Northeast Thailand; the Thai census counts it as Thai (Wikipedia: Isan language)')
add('tha', ['Surin'], 'Khmer', 'Northern Khmer is the largest home language in Surin (Wikipedia: Northern Khmer language)')
add('tha', ['Chiang Mai', 'Chiang Rai', 'Lampang', 'Lamphun', 'Nan', 'Phayao', 'Phrae'], 'Northern Thai', 'Northern Thai (Kham Mueang) is the main home language of the upper north (Wikipedia: Northern Thai language)')
add('tha', ['Mae Hong Son'], 'Shan', 'Shan (Tai Yai) is the largest group in Mae Hong Son (Wikipedia: Mae Hong Son province)')
add('tha', ['Chumphon', 'Ranong', 'Surat Thani', 'Phangnga', 'Phuket', 'Krabi', 'Nakhon Si Thammarat', 'Trang', 'Phatthalung', 'Satun', 'Songkhla'], 'Southern Thai', 'Southern Thai (Pak Tai) is the main home language of southern Thailand outside the Malay-speaking provinces (Wikipedia: Southern Thai language)')
add('mmr', ['Kayin', 'Kayah'], 'Karen', 'Karen (Karenic) peoples are the largest group in Kayin and Kayah states; Myanmar has published no census language data (Wikipedia: Kayin State, Kayah State)')
add('mmr', ['Chin'], 'Chin', 'Chin (Kuki-Chin) languages are spoken by most of Chin State; several close varieties merged (Wikipedia: Chin State)')
add('mys', ['Sarawak'], 'Iban', 'Malaysia 2020 census: Iban is the largest group in Sarawak, ahead of Chinese and Malay (Wikipedia: Sarawak)')
add('idn', ['Lampung'], 'Javanese', 'Indonesia 2010 census: Javanese 64.2%, Lampung 13.6%, Sundanese 11.9% (Wikipedia: Lampung)')
add('idn', ['Kalimantan Timur'], 'Javanese', 'Indonesia 2010 census: Javanese are the largest group in East Kalimantan, ahead of Bugis and Banjar (Wikipedia: East Kalimantan)')
add('idn', ['Kalimantan Tengah'], 'Banjar', 'Indonesia 2010 census: Banjar is the largest group and the lingua franca of Central Kalimantan (Wikipedia: Central Kalimantan)')
add('idn', ['Gorontalo'], 'Gorontalo', 'Indonesia 2010 census: Gorontalo people are about 90% of the province (Wikipedia: Gorontalo)')
add('vnm', ['Son La'], 'Tai Dam', 'Vietnam 2019 census: Thái 53.6% of Sơn La (Wikipedia: List of ethnic groups in Vietnam)')
add('vnm', ['Lai Chau'], 'Tai Dam', 'Vietnam 2019 census: Thái are the largest group in Lai Châu (Wikipedia: List of ethnic groups in Vietnam)')
add('vnm', ['Điện Biên', 'Hà Giang'], 'Hmong', "Vietnam 2019 census: H'Mông are the largest group (Điện Biên 228,279 vs Thái 213,714; Hà Giang 292,677) (Wikipedia: List of ethnic groups in Vietnam)")
add('vnm', ['Cao Bằng', 'Đông Bắc'], 'Tày', 'Vietnam 2019 census: Tày 40.8% of Cao Bằng and the majority of Bắc Kạn (the shape labelled Đông Bắc) (Wikipedia: List of ethnic groups in Vietnam)')
add('vnm', ['Lạng Sơn'], 'Nùng', 'Vietnam 2019 census: Nùng 42.9% of Lạng Sơn (Wikipedia: List of ethnic groups in Vietnam)')
add('vnm', ['Hòa Bình'], 'Mường', 'Vietnam 2019 census: Mường 64.3% of Hòa Bình (Wikipedia: List of ethnic groups in Vietnam)')
add('irn', ['Lorestan', 'Kohgiluyeh and Buyer Ahmad', 'Chahar Mahall and Bakhtiari'], 'Luri', 'Luri (including Bakhtiari) is the main home language of these provinces; Iran publishes no census language data (Wikipedia: Luri language)')
add('irn', ['Gilan'], 'Gilaki', 'Gilaki is the main home language of Gilan; Iran publishes no census language data (Wikipedia: Gilaki language)')
add('irn', ['Mazandaran'], 'Mazandarani', 'Mazandarani is the main home language of Mazandaran; Iran publishes no census language data (Wikipedia: Mazandarani language)')
add('syr', ['Dayr Az Zawr', 'Ar Raqqah'], 'Mesopotamian', 'North Mesopotamian Arabic is the local dialect of the Euphrates valley (Wikipedia: North Mesopotamian Arabic)')
add('yem', ['Ta`izz', 'Ibb', 'Lahij', '`Adan', 'Abyan', "Al Dali'"], "Ta'izzi-Adeni Arabic", "Ta'izzi-Adeni Arabic is the dialect of southwestern Yemen (Wikipedia: Ta'izzi-Adeni Arabic)")
add('rus', ['Bashkortostan'], 'Russian', 'Russia 2010/2021 censuses: Russians 36-38% of Bashkortostan and Bashkir speakers about a quarter, so Russian is the largest native language (Wikipedia: Bashkir language; 2021 Russian census)')
add('rus', ['Kalmyk'], 'Russian', 'Russia 2010 census: about 80,500 Kalmyk speakers against a population of about 289,000, so Russian is the main language (Wikipedia: Kalmyk Oirat)')
add('kaz', ['North Kazakhstan'], 'Russian', 'Kazakhstan 2021 census: Russians 44.5%, Ukrainians 5.5%, Germans 4.1% (mostly Russian-speaking) vs Kazakhs 37.6% (Wikipedia: North Kazakhstan Region)')
add('geo', ['Samtskhe-Javakheti'], 'Armenian', 'Georgia 2014 census: Armenians 50.5%, Georgians 48.3% (Wikipedia: Samtskhe-Javakheti)')
add('geo', ['Abkhazia'], 'Abkhaz', 'Abkhazia 2011 census: Abkhaz 50.7% of the population (Wikipedia: Abkhazia)')

# ---------------- Europe ----------------
add('mda', ['Comrat'], 'Gagauz', 'Moldova 2014 census: Gagauz 83.8% of Gagauzia (Wikipedia: Gagauzia)')
add('mda', ['Taraclia'], 'Bulgarian', 'Moldova 2014 census: Bulgarians are about two thirds of Taraclia district (Wikipedia: Taraclia District)')
add('rou', ['Harghita', 'Covasna'], 'Hungarian', 'Romania 2021 census: Hungarian is the majority mother tongue in Harghita and Covasna (Wikipedia: Harghita County, Covasna County)')
add('bgr', ['Kardzhali'], 'Turkish', 'Bulgaria 2021 census, mother tongue: Turkish 65.3%, Bulgarian 30.6% (NSI Census 2021 ethnocultural report)')
add('bgr', ['Razgrad'], 'Turkish', 'Bulgaria 2021 census, mother tongue: Turkish 53.4%, Bulgarian 41.1% (NSI Census 2021 ethnocultural report)')
add('mne', ['Ulcinj'], 'Albanian', 'Montenegro 2023 census: Albanians 73.5% of Ulcinj (Wikipedia: Municipalities of Montenegro)')
MK_ALB = ['Aracinovo', 'Lipkovo', 'Želino', 'Saraj', 'Bogovinje', 'Tearce', 'Tetovo', 'Studenicani', 'Cair', 'Gostivar', 'Debar', 'Brvenica', 'Caška', 'Struga', 'Zajas', 'Oslomej', 'Polog']
add('mkd', MK_ALB, 'Albanian', 'North Macedonia 2021 census: Albanian majority (Doc.surf / Wikipedia: Albanians in North Macedonia); Zajas, Oslomej and the Polog region shape are Albanian-majority areas')
add('mkd', ['Centar župa', 'Plasnica'], 'Turkish', 'North Macedonia census: Turks are the majority in Centar Župa and Plasnica (Wikipedia: Turks in North Macedonia)')
add('mkd', ['Šuto Orizari'], 'Romani', 'North Macedonia census: Roma are the majority in Šuto Orizari (Wikipedia: Šuto Orizari Municipality)')
add('est', ['Ida-Viru'], 'Russian', 'Estonia 2021 census: Russian is the majority mother tongue in Ida-Viru County (Wikipedia: Ida-Viru County)')
add('lva', ['Riga'], 'Russian', 'Latvia 2011 census: Russian 50%, Latvian 43% as the everyday language in Riga (LSM, from CSB data)')
add('lva', ['Daugavpils', 'Rezekne'], 'Russian', 'Latvia 2011 census: Russian is the main home language in Daugavpils and Rēzekne cities (Wikipedia: Russian language in Latvia)')
add('fin', ['Ostrobothnia'], 'Swedish', 'Statistics Finland 2025: Swedish 49.1%, Finnish 39.4% registered mother tongue (Wikipedia: Ostrobothnia (region))')
add('ita', ['Bozen'], 'German', 'South Tyrol 2011 census language-group declarations: German 69.4%, Italian 26.1%, Ladin 4.5% (ASTAT)')
add('esp', ['Barcelona', 'Tarragona'], 'Spanish', 'EULP 2023 (Generalitat de Catalunya): Spanish is the main habitual language; Catalan about 25% in the Barcelona area (Catalan News, Nov 2025)')
add('esp', ['Gipuzkoa', 'Bizkaia'], 'Spanish', 'Basque Sociolinguistic Survey 2021: Spanish is the main home language in both provinces')
add('esp', ['La Coruña', 'Pontevedra'], 'Spanish', 'IGE 2023: Galicia is 54% Spanish-dominant overall; the coastal cities (Vigo 20%, A Coruña 25% Galician-dominant) make both provinces Spanish-dominant (IGE, Coñecemento e uso do galego)')

# ---------------- Americas ----------------
add('bol', ['La Paz', 'Oruro', 'Chuquisaca', 'Cochabamba'], 'Spanish', 'Bolivia 2024 census, main language: Spanish leads (La Paz 2.38M Spanish vs 0.50M Aymara; Cochabamba 1.47M vs 0.45M Quechua) (citypopulation.de)')
add('pry', ['Asunción', 'Central'], 'Spanish', 'Paraguay EPHC 2024: Guaraní-only at home 3% in Asunción and 10% in Central, against majorities speaking Spanish (Última Hora, Jul 2026)')
add('gtm', ['Totonicapán', 'Quiché'], "K'iche'", "Guatemala 2018 census: K'iche' communities form the large Maya majorities of Totonicapán (98% indigenous) and Quiché (89%) (Wikipedia: Indigenous peoples in Guatemala)")
add('gtm', ['Sololá'], "K'iche'", "Guatemala 2018 census, mother tongue in Sololá: K'iche' 148,341, Kaqchikel 110,380, Spanish 69,788 (citypopulation.de)")
add('gtm', ['Alta Verapaz'], "Q'eqchi'", "Guatemala 2018 census: Alta Verapaz is 93% indigenous, mostly Q'eqchi' (Wikipedia: Indigenous peoples in Guatemala)")
add('blz', ['Cayo', 'Corozal', 'Orange Walk'], 'Spanish', 'Belize 2010 census: Spanish is the most common home language in the western and northern districts (Wikipedia: Languages of Belize)')
add('blz', ['Toledo'], "Q'eqchi'", "Belize 2010 census: Q'eqchi' Maya are the largest group in Toledo (Wikipedia: Toledo District)")

# ---------------- Africa ----------------
add('zaf', ['Limpopo'], 'Northern Sotho', 'South Africa 2022 census, home language in Limpopo: Sepedi (Northern Sotho) 55.5%, Tshivenda 17.4% (Wikipedia: 2022 South African census)')
add('zwe', ['Matabeleland North', 'Matabeleland South', 'Bulawayo'], 'Ndebele', 'Northern Ndebele is the main language of Matabeleland and Bulawayo (Wikipedia: Northern Ndebele language)')
add('zmb', ['Eastern', 'Lusaka'], 'Chichewa', 'Nyanja (Chichewa) is the major language of Eastern and Lusaka provinces (Wikipedia: Languages of Zambia, from the 2010 census)')
add('zmb', ['Southern'], 'Tonga', 'Tonga is the major language of Southern Province (Wikipedia: Languages of Zambia, from the 2010 census)')
add('zmb', ['Western'], 'Lozi', 'Lozi is the major language of Western Province (Wikipedia: Languages of Zambia, from the 2010 census)')
add('nam', ['Kavango'], 'Kwangali', 'Kavango languages (RuKwangali and relatives) are the main household languages of Kavango (Wikipedia: Languages of Namibia)')
add('nam', ['Caprivi'], 'Lozi', 'Silozi is the main household language of Zambezi (Caprivi) (Wikipedia: Languages of Namibia)')
add('nam', ['Karas', 'Hardap'], 'Afrikaans', 'Namibia 2011 census: Afrikaans is the largest household language in the south (Wikipedia: Languages of Namibia)')
add('nam', ['Kunene', 'Omaheke'], 'Herero', 'Otjiherero is the largest household language of Kunene and Omaheke (Wikipedia: Languages of Namibia)')
add('mwi', ['Chitipa', 'Rumphi', 'Mzimba'], 'Tumbuka', 'Tumbuka is the main language of northern Malawi (Wikipedia: Tumbuka language)')
add('mwi', ['Mangochi', 'Machinga'], 'Yao', 'Malawi 2018 census: Yao are the majority in Mangochi and Machinga (Wikipedia: Yao people)')
add('mwi', ['Nsanje', 'Chikwawa'], 'Sena', 'Sena is the main language of the Lower Shire districts (Wikipedia: Sena language)')
add('moz', ['Nampula', 'Cabo Delgado', 'Niassa'], 'Makhuwa', 'Mozambique 2017 census: Emakhuwa is the largest mother tongue nationally (26.3%) and in the north (Wikipedia: Languages of Mozambique; AIR language mapping 2017)')
add('moz', ['Zambezia'], 'Lomwe', 'Elomwe is the most common first language in Zambézia (AIR language mapping study, 2017)')
add('moz', ['Sofala'], 'Sena', 'Cisena is the main language of Sofala (Wikipedia: Sena language)')
add('moz', ['Manica'], 'Shona', 'Shona varieties (Ndau, Manyika, Teve) are the main languages of Manica (Wikipedia: Languages of Mozambique)')
add('moz', ['Tete'], 'Chichewa', 'Nyanja (Chichewa) and the related Nyungwe are the main languages of Tete (Wikipedia: Languages of Mozambique)')
add('moz', ['Inhambane'], 'Tswa', 'Citshwa is the largest language of Inhambane (Wikipedia: Tswa language)')
add('moz', ['Gaza', 'Maputo'], 'Tsonga', 'Changana (Tsonga) is the main language of Gaza and Maputo province (Wikipedia: Tsonga language)')
add('ken', ['Central'], 'Kikuyu', 'Kenya 2019 census: Kikuyu are the large majority of the former Central Province (KNBS via Wikipedia: Kikuyu people)')
add('ken', ['Nyanza'], 'Luo', 'Kenya 2019 census: Luo are the largest group in the former Nyanza Province (Wikipedia: Luo people of Kenya and Tanzania)')
add('ken', ['Western'], 'Luhya', 'Kenya 2019 census: Luhya are the large majority of the former Western Province (Wikipedia: Luhya people)')
add('ken', ['Rift Valley'], 'Kalenjin', 'Kenya 2019 census: Kalenjin are the largest group in the former Rift Valley Province (Wikipedia: Kalenjin people)')
add('ken', ['Eastern'], 'Kamba', 'Kenya 2019 census: Kamba are the largest group in the former Eastern Province (Wikipedia: Kamba people)')
add('ken', ['North-Eastern'], 'Somali', 'Kenya 2019 census: Somali are the large majority of the former North Eastern Province (Wikipedia: Somalis in Kenya)')
for lang, ds in UG.items():
    add('uga', ds.split(), lang, UG_SRC)
add('eth', ['Southern Nations, Nationalities and Peoples'], 'Sidamo', 'Ethiopia 2007 census: Sidama 19.3% of SNNPR, the largest group (Wikipedia: Southern Nations, Nationalities, and Peoples\' Region)')
add('eth', ['Gambela Peoples'], 'Nuer', 'Ethiopia 2007 census: Nuer 46.7% of Gambela (Wikipedia: Gambela Region)')
add('eth', ['Benshangul-Gumaz'], 'Berta', 'Ethiopia 2007 census: Berta 25.9% of Benishangul-Gumuz, the largest group (Wikipedia: Benishangul-Gumuz Region)')
add('eth', ['Dire Dawa', 'Harari People'], 'Oromo', 'Ethiopia 2007 census: Oromo are the largest group in Dire Dawa (46%) and Harari (56%) (Wikipedia: Dire Dawa, Harari Region)')
add('eri', ['Anseba', 'Semenawi Keyih Bahri', 'Gash Barka'], 'Tigre', 'Tigre is the largest language of western and northern Eritrea (Wikipedia: Tigre language)')
add('eri', ['Debubawi Keyih Bahri'], 'Afar', 'Afar is the main language of the Southern Red Sea region (Wikipedia: Afar people)')
add('dji', ['Obock', 'Tadjourah', 'Dikhil'], 'Afar', 'Afar are the majority in the northern and western regions of Djibouti (Wikipedia: Afar people)')
add('nga', ['Benue'], 'Tiv', 'Tiv are the majority of Benue State; Nigeria publishes no census language data (Wikipedia: Tiv people)')
add('nga', ['Kwara'], 'Yoruba', 'Yoruba are the majority of Kwara State (Wikipedia: Kwara State)')
add('nga', ['Kogi'], 'Igala', 'Igala are the largest group in Kogi State (Wikipedia: Kogi State)')
add('nga', ['Borno', 'Yobe'], 'Kanuri', 'Kanuri are the largest group in Borno and Yobe (Wikipedia: Kanuri people)')
add('nga', ['Delta'], 'Urhobo', 'Urhobo are the largest group in Delta State (Wikipedia: Delta State)')
add('gha', ['Volta'], 'Ewe', 'Ghana 2021 census: Ewe 87.9% of Volta Region (citypopulation.de); the map\'s Volta also covers Oti')
add('gha', ['Northern'], 'Dagbani', 'Ghana 2021 census: Mole-Dagbani are the largest group, led by the Dagomba (Wikipedia: Dagbani language)')
add('gha', ['Upper East'], 'Farefare', 'Ghana 2021 census: Frafra (Farefare/Gurene speakers) are the largest group in Upper East (Wikipedia: Farefare language)')
add('gha', ['Upper West'], 'Dagaare', 'Dagaare is the main language of Upper West Region (Wikipedia: Dagaare language)')
add('tgo', ['Kara'], 'Kabiye', 'Kabiye are the majority of Kara Region (Wikipedia: Kabiye language)')
add('tgo', ['Savanes'], 'Moba', 'Moba are the largest group in Savanes Region (Wikipedia: Moba language)')
add('tgo', ['Centre'], 'Tem', 'Tem (Kotokoli) are the largest group in Centrale Region (Wikipedia: Tem language)')
add('ben', ['Borgou', 'Alibori'], 'Bariba', 'Benin 2013 census: Bariba are the largest group in Borgou and Alibori (Wikipedia: Bariba people)')
add('ben', ['Plateau'], 'Yoruba', 'Benin 2013 census: Yoruba (Nago) are the largest group in Plateau (Wikipedia: Plateau Department)')
add('ben', ['Kouffo', 'Mono'], 'Aja', 'Benin 2013 census: Aja (Adja) are the largest group in Couffo and Mono (Wikipedia: Aja people)')
add('ben', ['Ouémé'], 'Gun', 'Benin 2013 census: Gun are the largest group in Ouémé (Wikipedia: Gun language)')
add('ner', ['Tillabéri', 'Dosso', 'Niamey'], 'Zarma', 'Niger 2012 census: Zarma-Songhai are the main group of the west (Wikipedia: Zarma language)')
add('ner', ['Agadez'], 'Tamasheq', 'Tuareg are the largest group in Agadez (Wikipedia: Agadez Region)')
add('ner', ['Diffa'], 'Kanuri', 'Kanuri are the majority of the settled population of the southeast (Wikipedia: Demographics of Niger)')
add('mli', ['Timbuktu', 'Gao'], 'Songhay', 'Songhay is the largest language of the Niger bend (Wikipedia: Songhay languages)')
add('mli', ['Kidal'], 'Tamasheq', 'Tuareg are the large majority in Kidal (Wikipedia: Kidal Region)')
add('mli', ['Mopti'], 'Fula', 'Fula (Fulfulde) is the largest language of the inner Niger delta (Wikipedia: Mopti Region)')
add('bfa', ['Soum', 'Oudalan', 'Séno', 'Yagha'], 'Fula', 'Fula (Fulfulde) is the main language of the Sahel region (Wikipedia: Sahel Region (Burkina Faso))')
add('bfa', ['Gourma', 'Gnagna', 'Komondjari', 'Kompienga', 'Tapoa'], 'Gourmanché', 'Gourmanché is the main language of the Est region (Wikipedia: Gourmanché language)')
add('bfa', ['Houet', 'Komoé', 'Léraba', 'Kénédougou'], 'Dyula', 'Dyula is the main home and market language of the southwest (Wikipedia: Dyula language)')
add('bfa', ['Poni', 'Noumbiel'], 'Lobi', 'Lobi is the largest language of Poni and Noumbiel (Wikipedia: Lobi language)')
add('bfa', ['Ioba', 'Bougouriba'], 'Dagaare', 'Dagara (Dagaare) is the largest language of Ioba and Bougouriba (Wikipedia: Dagaare language)')
add('sen', ['Ziguinchor'], 'Jola', 'Senegal 2013 census: Jola are the largest group in Ziguinchor (Wikipedia: Jola people)')
add('sen', ['Kolda', 'Tambacounda', 'Kédougou', 'Matam'], 'Fula', 'Senegal 2013 census: Pulaar (Fula) is the largest language in the east and south (Wikipedia: Pulaar language)')
add('sen', ['Sédhiou'], 'Mandinka', 'Senegal 2013 census: Mandinka are the largest group in Sédhiou (Wikipedia: Sédhiou Region)')
add('sen', ['Fatick'], 'Serer', 'Senegal 2013 census: Serer are the largest group in Fatick (Wikipedia: Serer people)')
add('gin', ['Boffa', 'Boke', 'Conakry', 'Coyah', 'Dubréka', 'Forécariah', 'Fria', 'Kindia'], 'Susu', 'Susu is the main language of Lower Guinea and Conakry (Wikipedia: Susu language)')
add('gin', ['Kankan', 'Kérouané', 'Kouroussa', 'Mandiana', 'Siguiri', 'Faranah', 'Beyla'], 'Maninka', 'Maninka is the main language of Upper Guinea (Wikipedia: Maninka language)')
add('gin', ['Guéckédou', 'Kissidougou'], 'Kissi', 'Kissi is the main language of Guéckédou and Kissidougou (Wikipedia: Kissi language)')
add('gin', ['Nzérékoré', 'Lola', 'Yomou'], 'Kpelle', 'Kpelle (Guerzé) is the main language of the southeastern forest region (Wikipedia: Kpelle language)')
add('gin', ['Macenta'], 'Loma', 'Loma (Toma) is the main language of Macenta (Wikipedia: Loma language)')
add('sle', ['Western'], 'Krio', 'Sierra Leone 2015 census: Krio is the main language of the Western Area (Wikipedia: Krio language)')
add('sle', ['Northern'], 'Temne', 'Sierra Leone 2015 census: Temne are the largest group in the north (Wikipedia: Temne people)')
add('sle', ['Southern', 'Eastern'], 'Mende', 'Sierra Leone 2015 census: Mende are the largest group in the south and east (Wikipedia: Mende people)')
add('lbr', ['Bong', 'Margibi'], 'Kpelle', 'Liberia 2008 census: Kpelle are the largest group in Bong and Margibi (Wikipedia: Kpelle people)')
add('lbr', ['Grand Bassa', 'River Cess'], 'Bassa', 'Liberia 2008 census: Bassa are the largest group in Grand Bassa and River Cess (Wikipedia: Bassa people (Liberia))')
add('lbr', ['Maryland', 'River Gee', 'Grand Kru'], 'Grebo', 'Liberia 2008 census: Grebo are the largest group in the southeast (Wikipedia: Grebo people)')
add('lbr', ['Nimba'], 'Dan', 'Liberia 2008 census: Gio (Dan) are the largest group in Nimba (Wikipedia: Dan people)')
add('lbr', ['Lofa'], 'Loma', 'Liberia 2008 census: Loma are the largest group in Lofa (Wikipedia: Loma people)')
add('lbr', ['Grand Cape Mount'], 'Vai', 'Liberia 2008 census: Vai are the majority in Grand Cape Mount (Wikipedia: Vai people)')
add('gmb', ['Banjul'], 'Wolof', 'Wolof is the main language of Banjul and Kanifing (Wikipedia: Wolof language)')
add('gnb', ['Bafatá', 'Gabú'], 'Fula', 'Fula are the majority in Bafatá and Gabú (Wikipedia: Fula people)')
add('gnb', ['Oio', 'Tombali', 'Quinara'], 'Balanta', 'Balanta are the largest group in Oio, Tombali and Quinara (Wikipedia: Balanta people)')
add('mrt', ['Guidimaka'], 'Soninke', 'Soninke are the largest group in Guidimaka (Wikipedia: Soninke people)')
add('mar', ['Souss - Massa - Draâ'], 'Tachelhit', 'Morocco 2014 census: Tachelhit is the most used local language in Souss-Massa (Wikipedia: Shilha language)')
add('dza', ['Tizi Ouzou', 'Béjaïa', 'Bouira'], 'Kabyle', 'Kabyle is the main language of Kabylia (Tizi Ouzou, Béjaïa, Bouira) (Wikipedia: Kabyle language)')
add('tcd', ['Logone Occidental', 'Logone Oriental', 'Mandoul', 'Moyen-Chari', 'Tandjilé'], 'Sara', 'Sara languages (mainly Ngambay) are the main languages of southern Chad (Wikipedia: Sara languages)')
add('tcd', ['Lac', 'Kanem'], 'Kanuri', 'Kanembu, a Kanuri variety, is the largest language of Lac and Kanem (Wikipedia: Kanembu language)')
add('cmr', ['Extrême-Nord', 'Nord', 'Adamaoua'], 'Fula', 'Fulfulde is the main language of northern Cameroon (Wikipedia: Fula language)')
add('cog', ['Pool', 'Bouenza', 'Kouilou', 'Lékoumou', 'Niari', 'Pointe Noire'], 'Kikongo', 'Kituba (Kikongo) is the main language of southern Congo (Wikipedia: Kituba language)')
add('gab', ['Wouleu-Ntem'], 'Fang', 'Fang are the large majority in Woleu-Ntem (Wikipedia: Fang people)')
add('gnq', ['Litoral', 'Centro Sur', 'Kié-Ntem', 'Wele-Nzás'], 'Fang', 'Fang are the large majority of mainland Equatorial Guinea (Wikipedia: Fang people)')
add('civ', ['Savanes'], 'Senufo', 'Senufo are the largest group in the north (Wikipedia: Senufo languages)')
add('civ', ['Denguélé', 'Worodougou', 'Bafing'], 'Dyula', 'Malinke/Dyula is the main language of the northwest (Wikipedia: Dyula language)')
add('civ', ['Vallée du Bandama', "N'zi-Comoé", 'Lacs'], 'Baoulé', 'Baoulé is the main language of the centre (Wikipedia: Baoulé language)')
add('civ', ['Dix-Huit Montagnes'], 'Dan', 'Dan (Yacouba) is the main language of the west (Wikipedia: Dan language)')

CONFIRMED = {
    ('pak', 'Punjab'): 'Pakistan 2023 census: Punjabi 67%, Saraiki 21%, Urdu 7% (Gallup Pakistan)',
    ('pak', 'Sind'): 'Pakistan 2023 census: Sindhi 60%, Urdu 22% (Gallup Pakistan)',
    ('pak', 'N.W.F.P.'): 'Pakistan 2023 census: Pashto 81%, Hindko 9% (Gallup Pakistan)',
    ('pak', 'F.A.T.A.'): 'Pakistan 2023 census (now part of Khyber Pakhtunkhwa): Pashto 81% (Gallup Pakistan)',
    ('pak', 'Baluchistan'): 'Pakistan 2023 census: Balochi 40%, Pashto 34%, Brahui 17% (Gallup Pakistan)',
    ('zaf', 'Western Cape'): 'South Africa 2022 census: Afrikaans 41.2%, isiXhosa 31.4%',
    ('zaf', 'Northern Cape'): 'South Africa 2022 census: Afrikaans 54.6%, Setswana 35.7%',
    ('zaf', 'Eastern Cape'): 'South Africa 2022 census: isiXhosa 81.8%',
    ('zaf', 'Orange Free State'): 'South Africa 2022 census: Sesotho 72.3%',
    ('zaf', 'KwaZulu-Natal'): 'South Africa 2022 census: isiZulu 80%',
    ('zaf', 'North West'): 'South Africa 2022 census: Setswana 72.8%',
    ('zaf', 'Gauteng'): 'South Africa 2022 census: isiZulu 23.1%, Sesotho 13.1%',
    ('zaf', 'Mpumalanga'): 'South Africa 2022 census: siSwati 30.5%, isiZulu 27.8%',
    ('bol', 'Potosí'): 'Bolivia 2012 census, first language: Quechua 50.2%, Spanish 40.4% (2024 figures not yet published for Potosí)',
    # Ukraine (Nov 2026 rule from Grant): Russian only in oblasts mostly controlled by Russia (Crimea, Sevastopol, Luhansk,
    # Donetsk, Zaporizhzhia, Kherson); every other oblast Ukrainian. Set directly in site/data/regions.csv with sources there.
    ('esp', 'Gerona'): 'Girona survey 2026: Catalan is the priority habitual language of 48% (Ara)',
    ('esp', 'Lérida'): 'EULP 2023: Catalan is the initial language of about 40-45% in western Catalonia, the largest share (Catalan News)',
    ('fin', 'Uusimaa'): 'Statistics Finland: Finnish majority (Swedish about 8%)',
    ('srb', 'Severno-Backi'): '2022 census, mother tongue: Serbian 45.2%, Hungarian 35.2% (Wikipedia: North Bačka District)',
    ('srb', 'Severno-Banatski'): '2022 census: Serbs 44%, Hungarians 43% (Wikipedia: North Banat District)',
    ('nld', 'Friesland'): 'Fryske Taalatlas 2020: language spoken with partner Dutch 49.2%, Frisian 43.1% (Frisian is a (co-)mother tongue of 57.3%)',
    ('ind', 'Meghalaya'): 'India 2011 census: Khasi is the largest mother tongue, ahead of Garo',
    ('ind', 'Arunachal Pradesh'): 'India 2011 census: Nyishi is the largest mother tongue, ahead of Adi',
    ('ind', 'Jammu and Kashmir'): 'India 2011 census (with Ladakh): Kashmiri is the largest mother tongue, ahead of Dogri',
    ('ind', 'Tripura'): 'India 2011 census: Bengali is the largest mother tongue, ahead of Kokborok',
}
