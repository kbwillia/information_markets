"""Rules scored by buying one share and holding to resolution.

Prices are probabilities. A winning share pays 1. Slippage is added to every
purchase and subtracted from every sale so a rule has to clear more than the
raw mispricing.
"""
SLIPPAGE = 0.01
CUTOFF = "2025-07-01"
MIN_SAMPLE = 40


def buy(price, won):
    if price is None:
        return None
    if price <= 0.02 or price >= 0.98:
        return None
    cost = price + SLIPPAGE
    if cost >= 1:
        return None
    payout = 1.0 if won else 0.0
    return {"cost": round(cost, 4), "won": bool(won), "pnl": round(payout - cost, 4)}


def _yes(obs, horizon):
    price = obs.get(horizon)
    if price is None or obs.get("yes_won") is None:
        return None, None
    return price, bool(obs["yes_won"])


def _cheap_side(obs, horizon, low, high):
    price, yes_won = _yes(obs, horizon)
    if price is None:
        return None
    if price < 0.5:
        cheap, cheap_won = price, yes_won
    else:
        cheap, cheap_won = 1 - price, not yes_won
    if cheap < low or cheap >= high:
        return None
    return buy(cheap, cheap_won)


def _favorite_side(obs, horizon, minimum):
    price, yes_won = _yes(obs, horizon)
    if price is None:
        return None
    if price >= 0.5:
        favorite, favorite_won = price, yes_won
    else:
        favorite, favorite_won = 1 - price, not yes_won
    if favorite < minimum:
        return None
    return buy(favorite, favorite_won)


def rule_underdog_1d(obs):
    if obs.get("kind") != "binary":
        return None
    return _cheap_side(obs, "p1", 0.03, 0.15)


def rule_underdog_7d(obs):
    if obs.get("kind") != "binary":
        return None
    return _cheap_side(obs, "p7", 0.03, 0.15)


def rule_underdog_30d(obs):
    if obs.get("kind") != "binary":
        return None
    return _cheap_side(obs, "p30", 0.03, 0.15)


def rule_favorite_80(obs):
    if obs.get("kind") != "binary":
        return None
    return _favorite_side(obs, "p1", 0.80)


def rule_favorite_95(obs):
    if obs.get("kind") != "binary":
        return None
    return _favorite_side(obs, "p1", 0.95)


def rule_fade_90(obs):
    if obs.get("kind") != "binary":
        return None
    return _cheap_side(obs, "p1", 0.02, 0.10)


def rule_yes_mid(obs):
    if obs.get("kind") != "binary":
        return None
    price, yes_won = _yes(obs, "p1")
    if price is None or price < 0.40 or price >= 0.60:
        return None
    return buy(price, yes_won)


def rule_follow_week(obs):
    if obs.get("kind") != "binary":
        return None
    now, yes_won = _yes(obs, "p1")
    earlier = obs.get("p7")
    if now is None or earlier is None or abs(now - earlier) < 0.08:
        return None
    if now <= 0.10 or now >= 0.90:
        return None
    if now > earlier:
        return buy(now, yes_won)
    return buy(1 - now, not yes_won)


def rule_fade_week(obs):
    if obs.get("kind") != "binary":
        return None
    now, yes_won = _yes(obs, "p1")
    earlier = obs.get("p7")
    if now is None or earlier is None or abs(now - earlier) < 0.08:
        return None
    if now <= 0.10 or now >= 0.90:
        return None
    if now > earlier:
        return buy(1 - now, not yes_won)
    return buy(now, yes_won)


def rule_quiet_underdog(obs):
    if obs.get("kind") != "binary":
        return None
    volume = obs.get("volume") or 0
    if volume < 5000 or volume >= 50000:
        return None
    return _cheap_side(obs, "p1", 0.03, 0.15)


def rule_liquid_underdog(obs):
    if obs.get("kind") != "binary":
        return None
    if (obs.get("volume") or 0) < 100000:
        return None
    return _cheap_side(obs, "p1", 0.03, 0.15)


def _topic_underdog(topic):
    def rule(obs):
        if obs.get("kind") != "binary" or obs.get("topic") != topic:
            return None
        return _cheap_side(obs, "p1", 0.03, 0.15)

    return rule


def rule_cheap_basket(obs):
    if obs.get("kind") != "basket":
        return None
    legs = obs.get("n_legs") or 0
    total = obs.get("sum_yes")
    if legs < 3 or total is None or not obs.get("exactly_one"):
        return None
    if total >= 0.97:
        return None
    cost = total + SLIPPAGE * legs
    if cost >= 1:
        return None
    return {"cost": round(cost, 4), "won": True, "pnl": round(1 - cost, 4)}


def rule_rich_basket(obs):
    if obs.get("kind") != "basket":
        return None
    legs = obs.get("n_legs") or 0
    total = obs.get("sum_yes")
    if legs < 3 or total is None or not obs.get("exactly_one"):
        return None
    if total <= 1.03:
        return None
    proceeds = total - SLIPPAGE * legs
    pnl = proceeds - 1
    return {"cost": 1.0, "won": pnl > 0, "pnl": round(pnl, 4)}


def rule_event_longshot(obs):
    if obs.get("kind") != "basket":
        return None
    if not obs.get("exactly_one"):
        return None
    price = obs.get("cheapest")
    if price is None or price < 0.03 or price >= 0.15:
        return None
    return buy(price, bool(obs.get("cheapest_won")))


RULES = [
    ("underdog_1d", "Buy the underdog a day before close", "Cheap side priced from 0.03 to 0.15, entered on the last trade at least 24 hours before close.", rule_underdog_1d),
    ("underdog_7d", "Buy the underdog a week before close", "Same cheap-side rule, using the price a week before close.", rule_underdog_7d),
    ("underdog_30d", "Buy the underdog a month before close", "Same cheap-side rule, using the price a month before close.", rule_underdog_30d),
    ("favorite_80", "Buy the favorite above 0.80", "Buy the side priced at 0.80 or higher, a day before close.", rule_favorite_80),
    ("favorite_95", "Buy the favorite above 0.95", "Buy the side priced at 0.95 or higher, a day before close.", rule_favorite_95),
    ("fade_90", "Fade a 0.90 favorite", "Buy the side priced under 0.10 a day before close.", rule_fade_90),
    ("yes_mid", "Buy Yes between 0.40 and 0.60", "Buy the Yes share when it is near a toss-up a day before close.", rule_yes_mid),
    ("follow_week", "Follow a week-long move", "If Yes moved at least 0.08 over the prior week, buy the side it moved toward.", rule_follow_week),
    ("fade_week", "Fade a week-long move", "If Yes moved at least 0.08 over the prior week, buy the side it moved away from.", rule_fade_week),
    ("quiet_underdog", "Buy underdogs in quieter markets", "Cheap side from 0.03 to 0.15 when volume is between 5,000 and 50,000.", rule_quiet_underdog),
    ("liquid_underdog", "Buy underdogs in liquid markets", "Cheap side from 0.03 to 0.15 when volume is at least 100,000.", rule_liquid_underdog),
    ("underdog_sports", "Buy sports underdogs", "Cheap-side rule limited to markets whose question looks like sports.", _topic_underdog("sports")),
    ("underdog_politics", "Buy politics underdogs", "Cheap-side rule limited to markets whose question looks like politics.", _topic_underdog("politics")),
    ("underdog_crypto", "Buy crypto underdogs", "Cheap-side rule limited to markets whose question looks like crypto.", _topic_underdog("crypto")),
    ("cheap_basket", "Buy a cheap complete set", "On a multi-outcome event, buy every Yes if the prices sum to less than 0.97.", rule_cheap_basket),
    ("rich_basket", "Sell a rich complete set", "On a multi-outcome event, sell every Yes if the prices sum to more than 1.03.", rule_rich_basket),
    ("event_longshot", "Buy the cheapest outcome in an event", "Buy the lowest-priced outcome when it is between 0.03 and 0.15.", rule_event_longshot),
]


def summarize(trades):
    count = len(trades)
    if count == 0:
        return {
            "n": 0,
            "wins": 0,
            "win_rate": None,
            "cost": 0,
            "pnl": 0,
            "roi": None,
        }
    cost = sum(trade["cost"] for trade in trades)
    pnl = sum(trade["pnl"] for trade in trades)
    wins = sum(1 for trade in trades if trade["won"])
    return {
        "n": count,
        "wins": wins,
        "win_rate": round(wins / count, 4),
        "cost": round(cost, 2),
        "pnl": round(pnl, 2),
        "roi": None if cost == 0 else round(pnl / cost, 4),
    }


def score_rules(observations, cutoff=CUTOFF):
    rows = []
    for name, label, description, rule in RULES:
        train = []
        test = []
        for obs in observations:
            trade = rule(obs)
            if trade is None:
                continue
            anchor = obs.get("anchor") or ""
            if anchor >= cutoff:
                test.append(trade)
            else:
                train.append(trade)
        train_summary = summarize(train)
        test_summary = summarize(test)
        kept = (
            train_summary["n"] >= MIN_SAMPLE
            and test_summary["n"] >= MIN_SAMPLE
            and (train_summary["roi"] or 0) > 0
            and (test_summary["roi"] or 0) > 0
        )
        rows.append(
            {
                "name": name,
                "label": label,
                "description": description,
                "train": train_summary,
                "test": test_summary,
                "kept": kept,
            }
        )
    rows.sort(key=lambda row: (row["kept"], row["test"]["roi"] if row["test"]["roi"] is not None else -9), reverse=True)
    return rows


def topic_of(question):
    text = (question or "").lower()
    if any(word in text for word in ("bitcoin", "btc", "ethereum", "eth ", "crypto", "solana", "dogecoin")):
        return "crypto"
    if any(word in text for word in ("nfl", "nba", "mlb", "nhl", "ufc", "premier league", "super bowl", "world series", " vs ", " vs.")):
        return "sports"
    if any(word in text for word in ("trump", "biden", "harris", "election", "president", "senate", "congress", "democrat", "republican", "governor")):
        return "politics"
    if any(word in text for word in ("fed ", "cpi", "inflation", "interest rate", "s&p", "nasdaq", "above $", "price of")):
        return "macro"
    return "other"
