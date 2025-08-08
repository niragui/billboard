import json

from enum import Enum

from functools import partial

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.elements.filter import NodeFilter

THIS_FOLDER = os.path.dirname(__file__)
FILTERS_FILE = os.path.join(THIS_FOLDER, "filters.json")

with open(FILTERS_FILE) as f:
    FILTERS_DATA = json.load(f)

ACTION_FIELD = "action"
VALUE_FIELD = "value"


class Actions(Enum):
    EQUALS = "equals"
    STARTS = "starts_with"
    CONTAINS = "contains"
    ENDS = "ends_with"
    NOT_EQUALS = "not_equals"


def evaluate_rule(attr_value: str,
                  rule: dict) -> bool:
    """
    Evaluates a single attributes rule

    Parameters:
        - attr_value: Value of the attribute being evaluted
        - rule: Dictionary of the rule {action: value}
    """
    if not isinstance(rule, dict):
        return False

    action = rule.get(ACTION_FIELD)
    value = rule.get(VALUE_FIELD)

    if not action or value is None:
        return False

    action = Actions(action)
    attr_value = attr_value.strip()

    if action == Actions.EQUALS:
        return attr_value == value
    elif action == Actions.STARTS:
        return attr_value.startswith(value)
    elif action == Actions.CONTAINS:
        return value in attr_value
    elif action == Actions.ENDS:
        return attr_value.endswith(value)
    elif action == Actions.NOT_EQUALS:
        return attr_value != value
    else:
        raise ValueError(f"Unsupported action: {action}")


def attrs_filter(attrs: dict,
                 rules: dict):
    """
    Evalutates the attributes to match the rules dictionary

    Parameters:
        - attrs: Attibutes dictionary to evalute
        - rules: Dictionary of rules to use for the given item
    """
    for attr_key, condition in rules.items():
        if attr_key not in attrs:
            return False

        attr_val = attrs[attr_key].strip()

        rule_list = condition if isinstance(condition, list) else [condition]

        if not any(evaluate_rule(attr_val, rule) for rule in rule_list):
            return False

    return True


def get_filter(rules: dict):
    """
    Returns the NodeFilter for the json data given

    Parameters:
        - rules: Dictionary with the rules to follow
    """
    tag_name = rules.get("tag", None)
    attr_rules = rules.get("attributes", {})

    attr_rules = partial(attrs_filter, rules=attr_rules)

    return NodeFilter(tag_name, None, attr_rules)


TITLES_FILTER = get_filter(FILTERS_DATA.get("title", {}))
CREDITS_FILTER = get_filter(FILTERS_DATA.get("credits", {}))
POSITIONS_FILTER = get_filter(FILTERS_DATA.get("position", {}))
IMAGES_FILTER = get_filter(FILTERS_DATA.get("image", {}))
EXTRAS_FILTER = get_filter(FILTERS_DATA.get("extra_values", {}))
MEANINGUL_POSITIONS_FILTER = get_filter(FILTERS_DATA.get("meaningful_positions", {}))
MEANINGUL_DATES_FILTER = get_filter(FILTERS_DATA.get("meaningful_dates", {}))
CARDS_FILTER = get_filter(FILTERS_DATA.get("node", {}))
DATE_FILTER = get_filter(FILTERS_DATA.get("date", {}))