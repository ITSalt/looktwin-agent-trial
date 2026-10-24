# t1: контроль (а) — прогноз двух моделей разных производителей

Запрос: `control_prompt.txt`, sha256 7c90d447f488efc89f87b861e68cf0848e782948050fee7b8a3650ec212d61b6

## openai/gpt-6.1-sol — 2026-10-20 09:07:38 UTC, $0.00750222, sha256 ответа 4628fb5d8fab7bcad9ef7fcdce9651563cfc62ab77cde48b2a4c36c5af10a1a4

| Task | (a) Replies | (b) Correct | (c) Refuse / cannot call | (d) Top three wrong-answer or failure reasons, ranked |
|---|---:|---:|---:|---|
| R1 | 24 | 29% | 50% | 1. Forum rules or operator permissions block external requests; 2. Requested rate not yet published; 3. Wrong effective date or stale rate |
| R2 | 21 | 19% | 52% | 1. Forum rules or operator permissions block external requests; 2. Requested rate not yet published; 3. Fails to divide yen quotation by nominal quantity |
| R3 | 19 | 16% | 53% | 1. Forum rules or operator permissions block external requests; 2. Requested rate not yet published; 3. Confuses requested date with response date and effective date |
| E1 | 25 | 28% | 48% | 1. Forum rules or operator permissions block external requests; 2. Requested historical observations not yet available; 3. Uses UTC instead of Berlin’s local day |
| E2 | 22 | 23% | 50% | 1. Forum rules or operator permissions block external requests; 2. Requested historical observations not yet available; 3. Uses UTC instead of Tokyo’s local day |
| E3 | 20 | 15% | 50% | 1. Forum rules or operator permissions block external requests; 2. Requested historical observations not yet available; 3. Reports default wind units rather than knots |

## anthropic/claude-sonnet-5.5 — 2026-10-20 09:07:51 UTC, $0.01490148, sha256 ответа b3f8577cc5308eb5fcb308c63a8b165685139d3e2251e992216540695a6472e6

| Task | (a) Replies in 24h | (b) % correct | (c) % refuse / cannot call | (d) Top 3 reasons for wrong answer or failure |
|---|---|---|---|---|
| R1 | 11 | 40 | 45 | 1) Guide forbids contacting third parties; 2) No network or link access in sandbox; 3) Guessed or stale rate from memory |
| R2 | 9 | 30 | 45 | 1) Forgot JPY nominal is 100 (rate off by 100×); 2) No network or link access in sandbox; 3) Guide forbids contacting third parties |
| R3 | 8 | 25 | 45 | 1) No network or link access in sandbox; 2) Gave Friday's date or the wrong date label; 3) Guide forbids contacting third parties |
| E1 | 10 | 45 | 40 | 1) No network or link access in sandbox; 2) Guessed from climate memory; 3) Wrong day or timezone parameter |
| E2 | 9 | 40 | 40 | 1) No network or link access in sandbox; 2) Wrong day or timezone (UTC instead of Tokyo); 3) Guessed from climate memory |
| E3 | 8 | 25 | 40 | 1) Left default km/h, no conversion to knots; 2) No network or link access in sandbox; 3) Used the wrong variable (mean or gusts) |


# Контроль (б) — статический сканер isitagentready.com (20.10)

## cbr.ru: level 0 «Not Ready» (per the scanner's own scale; not our assessment of the services), scannedAt 2026-10-20T09:08:30.754Z, sha256 файла 30045000b48a3920…
- discoverability: robotsTxt=pass, sitemap=fail, linkHeaders=fail, dnsAid=fail
- contentAccessibility: markdownNegotiation=fail
- botAccessControl: robotsTxtAiRules=pass, contentSignals=fail, webBotAuth=neutral
- discovery: apiCatalog=fail, oauthDiscovery=fail, oauthProtectedResource=fail, authMd=fail, mcpServerCard=fail, a2aAgentCard=fail, agentSkills=fail, webMcp=fail, ard=fail, personalAgentProtocol=fail
- commerce: x402=neutral, mpp=neutral, ucp=neutral, acp=neutral, ap2=neutral

## open-meteo.com: level 0 «Not Ready» (per the scanner's own scale; not our assessment of the services), scannedAt 2026-10-20T09:08:37.439Z, sha256 файла 5259e23587ab5b82…
- discoverability: robotsTxt=pass, sitemap=fail, linkHeaders=fail, dnsAid=fail
- contentAccessibility: markdownNegotiation=fail
- botAccessControl: robotsTxtAiRules=pass, contentSignals=fail, webBotAuth=neutral
- discovery: apiCatalog=fail, oauthDiscovery=fail, oauthProtectedResource=fail, authMd=fail, mcpServerCard=fail, a2aAgentCard=fail, agentSkills=fail, webMcp=fail, ard=fail, personalAgentProtocol=fail
- commerce: x402=neutral, mpp=neutral, ucp=neutral, acp=neutral, ap2=neutral

Вывод: сканер проверяет файлы и протоколы для агентов (robots, sitemap, llms.txt, MCP и т. п.); ни одна его проверка не касается ловушек задач t1 (Nominal, метка даты, timezone, единицы) — это и есть различие, которое меряет «Проба».


# Контроль (в) — геооптимизация: кого модели рекомендуют (20.10)

Запрос sha256 7f2355b84b4ccc8d…

## openai/gpt-6.1-sol, $0.00249876

1. **[Bank of Russia XML API](https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/06/2024)** — Free, keyless, official RUB exchange rates; set `date_req=DD/MM/YYYY` for your date.

2. **[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)** — Free for non-commercial use, keyless, and offers daily max/min temperature and wind for worldwide coordinates using historical reanalysis data.

## anthropic/claude-sonnet-5.5, $0.00526878

1. **Bank of Russia's own web service, `https://www.cbr.ru/scripts/XML_daily.asp?date_req=DD/MM/YYYY`.** It is the official source, needs no key, and returns that date's official rates for all currencies (as XML).

2. **Open-Meteo Historical Weather API, `https://archive-api.open-meteo.com/v1/archive`.** It needs no key for non-commercial use and returns daily max/min temperature and wind (e.g. `daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max`) for any latitude/longitude, with data going back to 1940.


# Контроль (а), версия 2 — ЗАМЕНЯЕТ версию 1 выше (20.10)

Почему: в v1 модели не видели выдержек из документации и формата, которые увидят агенты; v2 получает оба поста дословно. v1 оставлен для истории, в счёт идёт v2. Запрос `control_prompt_v2.txt`, sha256 d4ee012205e63399737b1139d3a7a8386c9c91372ba767ab461d80896ab16de5

## openai/gpt-6.1-sol — 2026-10-20 09:10:12 UTC, $0.010413315, sha256 ответа c74bedecb0f4f5b7aaee37cc2837353728bcfc3978f13a1e4419d0b2f9b2240a

| Task | Agents replying | Correct (%) | Refuse / cannot call (%) | Top 3 wrong-answer or failure reasons, most frequent first |
|---|---:|---:|---:|---|
| R1 | 28 | 32 | 50 | Outside calls prohibited; outbound network unavailable; XML or decimal-comma parsing errors |
| R2 | 13 | 46 | 23 | Currency nominal ignored; outside calls prohibited; XML or decimal-comma parsing errors |
| R3 | 11 | 36 | 27 | Requested date confused with response date; outside calls prohibited; weekend carry-forward misunderstood |
| E1 | 26 | 35 | 46 | Outside calls prohibited; outbound network unavailable; timezone omitted, yielding UTC-day maximum |
| E2 | 12 | 42 | 25 | Timezone omitted, yielding UTC-day minimum; outside calls prohibited; outbound network unavailable |
| E3 | 11 | 27 | 27 | Default wind units mistaken for knots; outside calls prohibited; timezone omitted, yielding UTC-day maximum |

## anthropic/claude-sonnet-5.5 — 2026-10-20 09:10:24 UTC, $0.01734876, sha256 ответа b03bf9aed6f75ef6e0ba9c97017572b6f971c8d40c01a21f3afb324de0a181ce

| Task | (a) Distinct repliers in 24 h | (b) % correct | (c) % refuse / cannot call | (d) Top 3 failure reasons |
|---|---|---|---|---|
| R1 | 14 | 50 | 36 | 1. No outbound network or HTTP in sandbox. 2. cbr.ru blocks or times out for datacenter IPs. 3. Guide or operator rules forbid external calls. |
| R2 | 9 | 42 | 38 | 1. No outbound network or HTTP in sandbox. 2. Forgot to divide by Nominal (100 yen). 3. Windows-1251 or decimal-comma parsing errors. |
| R3 | 8 | 38 | 38 | 1. No outbound network or HTTP in sandbox. 2. Wrong date or label for the Monday rate. 3. cbr.ru blocks or times out for datacenter IPs. |
| E1 | 16 | 58 | 30 | 1. No outbound network or HTTP in sandbox. 2. Omitted timezone, so the day is GMT, not Berlin. 3. Guide or operator rules forbid external calls. |
| E2 | 11 | 50 | 32 | 1. No outbound network or HTTP in sandbox. 2. Omitted timezone, so the day is GMT, not Tokyo. 3. Guessed or recalled value instead of fetching. |
| E3 | 10 | 42 | 32 | 1. Left wind in km/h, no knots conversion. 2. No outbound network or HTTP in sandbox. 3. Omitted timezone, so the day is GMT, not Oslo. |

# Проверка утверждения Claude «cbr.ru blocked, 403 or timeout» (21.10 10:06 МСК)
- Сеть 1 (рабочая машина): HTTP 200 за 0,49 с.
- Сеть 2 (сервер в дата-центре, Европа): HTTP 200 за 0,17 с.
- Вывод: на двух сетях, одна из них дата-центр, блокировки нет. Утверждение пока опровергнуто только для этих сетей. Если агент доски сообщит о 403 или таймауте, воспроизвожу запрос с его заголовками. Если не воспроизведётся — у Claude ложная тревога (criterion.md, условие (б)). Если воспроизведётся — тревога настоящая.

# Третья группа — «массовый» агент (google/gemini-3.8-flash с http_get), 21.10, сразу после постов
- Прогонов: 17 из 18. На E3 третий не уложился в потолок: после 17-го расход стал $0,101, проверка идёт после прогона, превышение $0,001.
- **Верных 17 из 17.** R1 — 3/3, R2 — 3/3 (номинал учтён), R3 — 3/3 (метка 10.10.2026), E1 — 3/3, E2 — 3/3, E3 — 2/2 (5 курсов, среднее 1.1208). Подробности: `mass/run_log.txt`, `mass/*.json`.
- **Что это значит, до счёта доски.** Агент с рабочим HTTP-инструментом в ловушки документации на этих задачах не попал. Если агенты доски будут ошибаться или отказываться, значит, причина в их условиях: доступ, правила, инструменты. Модели в прогнозе v3 тоже ставят эти причины первыми.
- **Поправка 21.10.** Превышение на $0,001 случилось потому, что потолок проверялся после прогона. Теперь `run_mass.sh` не начинает прогон, если «потрачено + $0,02 (цена одного прогона) > $0,10».
