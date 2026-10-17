from src.research.backtest import buy, rule_cheap_basket, rule_follow_week, rule_underdog_1d, score_rules


def test_buy_adds_slippage_and_pays_one_on_a_win():
    trade = buy(0.10, True)
    assert trade["cost"] == 0.11
    assert trade["pnl"] == 0.89
    assert trade["won"] is True


def test_underdog_buys_the_cheap_side():
    yes_longshot = rule_underdog_1d({"kind": "binary", "p1": 0.08, "yes_won": True, "anchor": "2024-01-01"})
    no_longshot = rule_underdog_1d({"kind": "binary", "p1": 0.90, "yes_won": False, "anchor": "2024-01-01"})
    favorite = rule_underdog_1d({"kind": "binary", "p1": 0.40, "yes_won": True, "anchor": "2024-01-01"})
    assert yes_longshot["won"] is True
    assert no_longshot["won"] is True
    assert favorite is None


def test_follow_week_buys_the_side_that_moved():
    up = rule_follow_week({"kind": "binary", "p7": 0.40, "p1": 0.55, "yes_won": True})
    down = rule_follow_week({"kind": "binary", "p7": 0.60, "p1": 0.45, "yes_won": False})
    assert up["won"] is True
    assert down["won"] is True


def test_cheap_basket_requires_room_after_slippage():
    cheap = rule_cheap_basket({"kind": "basket", "n_legs": 3, "sum_yes": 0.90, "exactly_one": True})
    tight = rule_cheap_basket({"kind": "basket", "n_legs": 4, "sum_yes": 0.97, "exactly_one": True})
    assert cheap["pnl"] == round(1 - (0.90 + 0.03), 4)
    assert tight is None


def test_score_keeps_a_rule_only_when_both_periods_make_money():
    observations = []
    for index in range(50):
        observations.append({"kind": "binary", "p1": 0.08, "yes_won": True, "anchor": "2024-06-01"})
        observations.append({"kind": "binary", "p1": 0.08, "yes_won": True, "anchor": "2026-01-01"})
    rows = {row["name"]: row for row in score_rules(observations)}
    assert rows["underdog_1d"]["kept"] is True
    assert rows["favorite_80"]["kept"] is False
