from dashboard_helpers import action_class, clean_market, normalized_confidence, parse_json, star_rating


def test_normalized_confidence_accepts_fraction_and_percent():
    assert normalized_confidence(0.82) == 82.0
    assert normalized_confidence(82) == 82.0


def test_star_rating_is_bounded():
    assert star_rating(100) == "★★★★★"
    assert len(star_rating(0)) == 5


def test_market_and_action_labels():
    assert clean_market("cash") == "stock"
    assert action_class("BUY") == "buy"
    assert action_class("unknown") == "hold"


def test_parse_json_is_safe():
    assert parse_json('{"reason":"test"}') == {"reason": "test"}
    assert parse_json("bad-json") == {}
