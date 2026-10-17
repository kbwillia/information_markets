"""Map every open Kalshi and Polymarket contract to a public data source and a strategy.

Rules are ordered. The first match wins. Kalshi is matched on the series ticker
(the segment before the first hyphen). Polymarket is matched on the title.
"""

from __future__ import annotations

PLAYBOOKS: dict[str, dict] = {
    "us_props": {
        "label": "US and college player props",
        "api": "League live box scores (NHL, NBA, MLB, ESPN)",
        "cost": "Free, no key",
        "limit": "Public endpoints. No published daily cap. Send a User-Agent.",
        "endpoint": "https://api-web.nhle.com/v1/score/now",
        "also": "cdn.nba.com live boxscore, statsapi.mlb.com feed/live, site.api.espn.com scoreboard and summary",
        "strategy": "Nowcast remaining-time arrival rates from the live box score and buy stale prop brackets before the book catches the latest play.",
    },
    "us_lines": {
        "label": "US and college game lines",
        "api": "BetStack consensus lines plus ESPN scoreboard",
        "cost": "Free",
        "limit": "BetStack is free with an email key and refreshes about once a minute. ESPN needs no key.",
        "endpoint": "https://api.betstack.dev/api/v1/lines",
        "also": "The Odds API free tier is 500 credits a month. TheRundown free tier is 20,000 data points a day.",
        "strategy": "Strip the vig from sharp moneylines, spreads, and totals, then buy the Kalshi or Polymarket side when the mid is more than about 3.5 points away after fees.",
    },
    "soccer": {
        "label": "Global soccer",
        "api": "Bzzoiro football plus ClubElo",
        "cost": "Free, no key",
        "limit": "Bzzoiro football is unlimited and free. API-Football free tier is 100 requests a day. Football-Data.org free tier is 10 requests a minute.",
        "endpoint": "https://sports.bzzoiro.com/api/",
        "also": "http://api.clubelo.com/YYYY-MM-DD for daily club Elo. No key.",
        "strategy": "Fit home and away goal rates, price the exact-score and both-teams-to-score grid together, and fade strike ladders that do not add up.",
    },
    "tennis": {
        "label": "Tennis match, set, and game markets",
        "api": "Bzzoiro tennis and Live Tennis API",
        "cost": "Free",
        "limit": "Bzzoiro tennis is unlimited and free. Live Tennis free tier is 30 requests a minute and 100 a day, and covers ATP, WTA, Challenger, and ITF.",
        "endpoint": "https://tennis.bzzoiro.com/api/live/",
        "also": "Jeff Sackmann tennis_atp and tennis_wta GitHub sets for surface hold rates.",
        "strategy": "On each changeover, recompute the Markov match, set, game-spread, and total-games probabilities from surface-adjusted serve points.",
    },
    "esports": {
        "label": "Esports maps and objectives",
        "api": "LoL Esports feed, OpenDota, Bzzoiro CS",
        "cost": "Free",
        "limit": "LoL esports public key, no signup. OpenDota is 60 calls a minute. Bzzoiro CS is unlimited. PandaScore free plan is 1,000 requests an hour.",
        "endpoint": "https://esports-api.lolesports.com/persisted/gw/getLive",
        "also": "https://api.opendota.com/api/ and https://csgo.bzzoiro.com/",
        "strategy": "Compare live gold, dragon, baron, and round-score win probability with the map market, and check map handicap against the individual map contracts.",
    },
    "niche_sports": {
        "label": "Cricket, darts, UFC, and motorsport",
        "api": "ESPN scoreboard",
        "cost": "Free, no key",
        "limit": "No key. Live summaries refresh on the order of a minute.",
        "endpoint": "https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard",
        "also": "Same host covers cricket and racing scoreboards when the league is in season.",
        "strategy": "Use the live summary win probability and method-of-victory splits to fade retail prices that still reflect the pre-fight line.",
    },
    "crypto": {
        "label": "Crypto candles, strikes, and ranges",
        "api": "Coinbase, Kraken, and Deribit public books",
        "cost": "Free, no key",
        "limit": "Coinbase and Kraken public market data need no key. Deribit public options summaries need no key. Binance global often returns HTTP 451 from the US; use Binance.US or Kraken instead.",
        "endpoint": "https://api.coinbase.com/v2/prices/BTC-USD/spot",
        "also": "https://www.deribit.com/api/v2/public/get_book_summary_by_currency and https://api.hyperliquid.xyz/info",
        "strategy": "Price daily above-strikes as digital options and touch markets as barriers using Deribit implied volatility, and track the 60-second settlement average into each 15-minute candle.",
    },
    "weather": {
        "label": "Temperature, rain, and earthquakes",
        "api": "NWS observations and AviationWeather METAR",
        "cost": "Free, no key",
        "limit": "api.weather.gov and aviationweather.gov need only a User-Agent. Open-Meteo is free to about 10,000 calls a day. USGS earthquake queries need no key.",
        "endpoint": "https://api.weather.gov/stations/KNYC/observations/latest",
        "also": "https://aviationweather.gov/api/data/metar and https://earthquake.usgs.gov/fdsnws/event/1/query",
        "strategy": "Once the station high is locked for the day, buy the settled temperature bracket. Before the day, buy brackets priced below the Open-Meteo ensemble share.",
    },
    "energy": {
        "label": "Oil, gas, power, and spot commodities",
        "api": "EIA Open Data and ERCOT public data",
        "cost": "Free with a key",
        "limit": "EIA is free. A demo key works for small pulls. FRED is free at 120 requests a minute.",
        "endpoint": "https://api.eia.gov/v2/",
        "also": "AAA daily state averages, CME RBOB via Yahoo, gridstatus for ERCOT and PJM hubs.",
        "strategy": "Forecast the next AAA state print from yesterday's price plus the lagged RBOB move, and forecast ERCOT peak load from the hourly temperature forecast plus live grid load.",
    },
    "macro": {
        "label": "CPI, yields, indexes, and corporate prints",
        "api": "FRED, BLS, and Treasury Fiscal Data",
        "cost": "Free",
        "limit": "FRED needs a free key, 120 requests a minute. BLS registered tier is 500 queries a day. Treasury Fiscal Data needs no key.",
        "endpoint": "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/",
        "also": "https://api.stlouisfed.org/fred/series/observations and https://api.bls.gov/publicAPI/v2/timeseries/data/",
        "strategy": "Build the CPI print from rent, gasoline, and electricity components already released, and trade yield brackets off the live Treasury curve before the official average posts.",
    },
    "politics": {
        "label": "Elections, approval, and appointments",
        "api": "Congress.gov, OpenFEC, and official election feeds",
        "cost": "Free",
        "limit": "api.data.gov keys allow about 1,000 requests an hour. Brazil TSE results need no key.",
        "endpoint": "https://api.congress.gov/v3/",
        "also": "https://api.openfec.gov/v1/ and https://resultados.tse.jus.br/",
        "strategy": "Recompute the approval or generic-ballot average from the same pollsters the index uses, and trade the print before the aggregator page updates.",
    },
    "mentions": {
        "label": "Speech mentions and social post counts",
        "api": "Polymarket XTracker and YouTube captions",
        "cost": "Free, no key",
        "limit": "XTracker needs no key and is the settlement counter for tweet and Truth Social markets. youtube-transcript-api runs locally with no key.",
        "endpoint": "https://xtracker.polymarket.com/api/users/elonmusk/trackings?activeOnly=true",
        "also": "YouTube Data API free quota is 10,000 units a day. SEC EDGAR is free at 10 requests a second with a User-Agent.",
        "strategy": "Project the remaining post count with an hour-of-day Poisson process, and read live captions so mention words are seen before manual traders update.",
    },
    "culture": {
        "label": "YouTube charts, AI usage, and culture",
        "api": "YouTube Data API and OpenRouter rankings",
        "cost": "Free",
        "limit": "YouTube videos.list is 1 quota unit, so 10,000 checks a day on the free quota. OpenRouter rankings need any free API key, 500 requests a day.",
        "endpoint": "https://openrouter.ai/api/v1/datasets/rankings-daily",
        "also": "https://www.googleapis.com/youtube/v3/videos",
        "strategy": "Sum the first several days of the weekly token window and buy the bracket the cumulative path already implies. Track daily view velocity for chart-rank markets.",
    },
    "geopolitics": {
        "label": "Ceasefires and conflict calendars",
        "api": "GDELT DOC 2.0",
        "cost": "Free, no key",
        "limit": "One request every 5 seconds. A faster burst returns HTTP 429.",
        "endpoint": "https://api.gdeltproject.org/api/v2/doc/doc",
        "also": "OpenSky Network for diplomatic and military aircraft, free daily credits.",
        "strategy": "Read the implied daily hazard across ceasefire dates and cut risk when the 15-minute conflict-news volume jumps well above its recent baseline.",
    },
    "transport": {
        "label": "Airport throughput",
        "api": "TSA passenger volumes",
        "cost": "Free, no key",
        "limit": "The daily checkpoint table is public HTML. Same-weekday history is the useful series.",
        "endpoint": "https://www.tsa.gov/travel/passenger-volumes",
        "also": "Bureau of Transportation Statistics airline traffic, free bulk files.",
        "strategy": "Forecast today's screened-passenger print from the same weekday last week plus the recent airline schedule change, and buy the bracket that history already implies.",
    },
    "other": {
        "label": "Other open contracts",
        "api": "The settlement source named in the rules",
        "cost": "Mixed",
        "limit": "Read the rules first. Trade only when that source is public and timestamped.",
        "endpoint": "https://gamma-api.polymarket.com/markets",
        "also": "Kalshi market payload includes the rules text on the trade API.",
        "strategy": "Do not force a model. Use the named public source only when it updates before the book does.",
    },
}

_PROP_BITS = (
    "GOAL",
    "PTS",
    "AST",
    "REB",
    "REC",
    "RSH",
    "PASS",
    "3PT",
    "PRA",
    "STL",
    "BLK",
    "SAVE",
    "HIT",
    "HRR",
    "HR",
    "TB",
    "RBI",
    "SB",
    "SACK",
    "FIRST",
    "MOSTR",
    "LADDER",
    "STOCK",
    "FFPTS",
)
_US_SPORT = (
    "NHL",
    "NBA",
    "WNBA",
    "NFL",
    "NCAAF",
    "NCAAB",
    "NCAAH",
    "MLB",
    "CFL",
    "AHL",
    "KHL",
    "KBO",
    "CBA",
    "ACB",
    "NBL",
    "LKL",
    "LNBP",
    "NCAAWV",
    "KBL",
    "PBA",
    "SLB",
    "PHKL",
    "WDBBL",
)
_SOCCER = (
    "EPL",
    "LALIGA",
    "SERIE",
    "BUNDES",
    "LIGUE",
    "MLS",
    "NWSL",
    "USL",
    "EFL",
    "BRASIL",
    "LIGAMX",
    "EREDIV",
    "TACAPORT",
    "LIGAPORT",
    "SAUDI",
    "ARG",
    "PERLIGA",
    "VENFUT",
    "DIMAYOR",
    "ECULP",
    "THAI",
    "ETTAN",
    "ALLSVENS",
    "ELITE",
    "FROPL",
    "SLGREECE",
    "J2",
    "DENSUPER",
    "LIGAF",
    "TFF",
    "URY",
    "VLEAGUE",
    "SUPERLIG",
    "CHN",
    "GER3",
    "CZE",
    "K2LEAGUE",
    "KLEAGUE",
    "EKSTRA",
    "UAE",
    "SRB",
    "AUTBUND",
    "SCOT",
    "IDN",
    "HNL",
    "EGY",
    "EERSTE",
    "CANPL",
    "SVK",
    "ISR",
    "CONMEBOL",
    "ROM",
    "HUN",
    "SVN",
    "IND",
    "MYS",
    "UEFA",
    "UCL",
    "FACUP",
    "EFLCUP",
    "COPPA",
    "DFB",
    "COUPE",
    "LIBERT",
    "SUDAM",
    "WC",
    "FIFA",
    "APFDDH",
    "LIGAEXP",
    "JLEAGUE",
    "SGPPL",
    "LVAVIR",
    "QSTARS",
    "SAPSL",
    "FRAPLW",
    "ALEAGUE",
    "SESBL",
    "ISL",
)
_CRYPTO = ("BTC", "ETH", "SOL", "XRP", "DOGE", "SHIB", "BNB", "HYPE", "ZEC", "NEAR", "CRYPTO")
_WEATHER = ("TEMP", "HIGH", "LOWT", "LOW", "RAIN", "QUAKE", "WARMING", "HURRICANE", "SNOW", "CO2")
_ENERGY = ("AAAGAS", "WTI", "BRENT", "NATGAS", "DIESEL", "COPPER", "ERCOT", "PJM", "MISO", "DDR5", "AMSAVO", "GOLD", "SILVER")
_MACRO = ("CPI", "OER", "SHELTER", "GDP", "10YR", "UST", "INX", "NASDAQ", "DJI", "FED", "LULU", "SBUX", "EARNING", "UNEMP", "PAYROLL")
_MENTION = ("MENTION", "TRUTH", "TWEET")
_CULTURE = ("YT", "TOKEN", "VSPEND", "VREQ", "OPENSOURCE", "OPENROUTER", "GAMEAWARD", "RESTAURANT")
_POLITICS = ("TRUMP", "PRESSSEC", "BESSENT", "RUBIO", "ZELENSK", "FOX", "MTP", "VHGCB", "APPROVE", "NOEM", "COOK", "SENATE", "HOUSE", "GOV", "ELECTION", "PRES", "ZACHARIA")


def _has(series: str, bits: tuple[str, ...]) -> bool:
    return any(bit in series for bit in bits)


def family_for(platform: str, market_id: str, title: str = "") -> str:
    plat = (platform or "").lower()
    if plat == "kalshi":
        series = (market_id or "").upper().split("-", 1)[0]
        if series.startswith("KX"):
            series = series[2:]
        if _has(series, ("ATP", "WTA", "ITF")):
            return "tennis"
        if _has(series, ("CS2", "LOL", "DOTA", "VALORANT", "ESOCCER", "EBASKET")):
            return "esports"
        if _has(series, ("DART", "T20", "ODI", "UFC", "F1", "PGA", "NASCAR")):
            return "niche_sports"
        if _has(series, _CRYPTO):
            return "crypto"
        if _has(series, _WEATHER):
            return "weather"
        if _has(series, _ENERGY):
            return "energy"
        if _has(series, _MACRO):
            return "macro"
        if _has(series, _MENTION):
            return "mentions"
        if _has(series, _CULTURE):
            return "culture"
        if _has(series, _SOCCER):
            return "soccer"
        if _has(series, _US_SPORT):
            return "us_props" if _has(series, _PROP_BITS) else "us_lines"
        if "TSA" in series:
            return "transport"
        if _has(series, _POLITICS):
            return "politics"
        return "other"
    text = f"{title} {market_id}".lower()
    checks = (
        ("esports", ("counter-strike", "lol:", "dota", "valorant", "map handicap", "game handicap", "worlds", "total kills")),
        ("weather", ("temperature", "degrees", "rain in", "earthquake", "typhoon", "cyclone")),
        ("crypto", ("bitcoin", "ethereum", "solana", "xrp", "dogecoin", "crypto", "hyperliquid", "fdv", "token")),
        ("mentions", ("tweet", "truth social", "elon musk #", "posts from")),
        ("culture", ("youtube", "spotify", "box office", "rotten tomatoes", "trailer", "game award", "views", "netflix", "academy", "mrbeast", "searched")),
        ("energy", ("crude", "natural gas", "wti", "brent", "copper", "gold", "silver", "diesel")),
        ("macro", ("fed ", "interest rate", "cpi", "inflation", "recession", "s&p", "nasdaq", "treasury", "largest company", "earnings", " ipo", "market cap")),
        ("geopolitics", ("ceasefire", "hormuz", "nato", "ukraine", "taiwan", "military", "iran", "russia", "israel", "airspace", "strait", "houthi", "blockade")),
        ("politics", ("election", "senate", "house", "president", "approval", "governor", "midterm", "bolsonaro", "lula", "prime minister", "out as", "out before", "referendum", "signed into law")),
        ("niche_sports", ("ufc", "cricket", "darts", "formula 1", "grand prix")),
        ("tennis", ("atp", "wta", "itf", "tennis")),
        ("soccer", ("exact score", "both teams", "leading at halftime", "win on 20", "ballon", "fc win", " cf ", "calcio", "united win")),
        ("us_lines", ("world series", " cfb ", "spread:", "o/u ", " vs", "vs.", "nfl", "nba", "mlb", "nhl", "wnba")),
    )
    for family, words in checks:
        if any(word in text for word in words):
            return family
    return "other"


def playbook_for(platform: str, market_id: str, title: str = "") -> dict:
    family = family_for(platform, market_id, title)
    book = PLAYBOOKS[family]
    return {
        "family": family,
        "label": book["label"],
        "api": book["api"],
        "cost": book["cost"],
        "limit": book["limit"],
        "endpoint": book["endpoint"],
        "also": book["also"],
        "strategy": book["strategy"],
    }


def summarize(rows: list[dict]) -> list[dict]:
    totals: dict[str, dict] = {}
    for row in rows:
        book = playbook_for(row.get("platform") or "", row.get("id") or "", row.get("title") or "")
        slot = totals.setdefault(
            book["family"],
            {
                "family": book["family"],
                "label": book["label"],
                "api": book["api"],
                "cost": book["cost"],
                "limit": book["limit"],
                "endpoint": book["endpoint"],
                "also": book["also"],
                "strategy": book["strategy"],
                "markets": 0,
                "kalshi": 0,
                "polymarket": 0,
                "volume": 0.0,
            },
        )
        slot["markets"] += 1
        slot["volume"] += float(row.get("volume") or 0)
        if row.get("platform") == "kalshi":
            slot["kalshi"] += 1
        elif row.get("platform") == "polymarket":
            slot["polymarket"] += 1
    ranked = sorted(totals.values(), key=lambda item: item["markets"], reverse=True)
    for item in ranked:
        item["volume"] = round(item["volume"], 2)
    return ranked
