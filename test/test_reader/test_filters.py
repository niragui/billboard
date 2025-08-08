from src.reader.filters import evaluate_rule, attrs_filter, get_filter, Actions, NodeFilter


def test_evaluate_rule_equals():
    rule = {"action": "equals", "value": "music"}
    assert evaluate_rule("music", rule) is True
    assert evaluate_rule("pop", rule) is False


def test_evaluate_rule_contains():
    rule = {"action": "contains", "value": "rock"}
    assert evaluate_rule("indie rock", rule) is True
    assert evaluate_rule("jazz", rule) is False


def test_evaluate_rule_starts():
    rule = {"action": "starts_with", "value": "top"}
    assert evaluate_rule("top 100", rule) is True
    assert evaluate_rule("chart", rule) is False


def test_evaluate_rule_ends():
    rule = {"action": "ends_with", "value": "hit"}
    assert evaluate_rule("chart-hit", rule) is True
    assert evaluate_rule("hitlist", rule) is False


def test_evaluate_rule_not_equals():
    rule = {"action": "not_equals", "value": "pop"}
    assert evaluate_rule("rock", rule) is True
    assert evaluate_rule("pop", rule) is False


def test_evaluate_rule_invalid_input():
    assert evaluate_rule("value", {}) is False
    assert evaluate_rule("value", {"action": "equals"}) is False
    assert evaluate_rule("value", {"value": "something"}) is False
    assert evaluate_rule("value", "not_a_dict") is False


def test_attrs_filter_single_condition_pass():
    attrs = {"class": "chart-title"}
    rules = {"class": {"action": "equals", "value": "chart-title"}}
    assert attrs_filter(attrs, rules) is True


def test_attrs_filter_multiple_conditions_pass():
    attrs = {"class": "credits big-text"}
    rules = {
        "class": [
            {"action": "contains", "value": "credits"},
            {"action": "ends_with", "value": "text"}
        ]
    }
    assert attrs_filter(attrs, rules) is True


def test_attrs_filter_attribute_missing():
    attrs = {"id": "main"}
    rules = {"class": {"action": "equals", "value": "test"}}
    assert attrs_filter(attrs, rules) is False


def test_attrs_filter_no_match():
    attrs = {"class": "foo bar"}
    rules = {"class": {"action": "equals", "value": "baz"}}
    assert attrs_filter(attrs, rules) is False


def test_get_filter_builds_node_filter():
    dummy_rules = {
        "tag": "div",
        "attributes": {
            "class": {"action": "equals", "value": "container"}
        }
    }

    nf = get_filter(dummy_rules)
    assert isinstance(nf, NodeFilter)
    assert nf.name == "div"
    assert nf.attrs({"class": "container"}) is True
    assert nf.attrs({"class": "box"}) is False
