#!/usr/bin/env python3
# stub processor. to be run in python 3.7.0

import copy as cp
import json
import os
import re
import subprocess
from typing import List, Dict, Union

conditions = {
    'all': all,
    'any': any
}

evaluator = {
    "matchesRegex": re.search,
    "lessThanEqual": lambda a, b: int(a) <= int(b),
    "greaterThan": lambda a, b: int(a) > int(b),
    "notEqualTo": lambda a, b: int(a) != int(b),
    "greaterThanEqual": lambda a, b: int(a) >= int(b),
    "lessThen": lambda a, b: int(a) < int(b),
    "equalTo": lambda a, b: int(a) == int(b)
}


def perform_action(action_stream, event):
    '''
    :param action_stream: This's the DSL for the action that would be executed
    :param event: This's the event payload for the DSL would be executed on.
    :return:
    '''
    action = action_stream.get('action')
    key_path = action_stream.get('keyPath', '')
    value = cp.deepcopy(action_stream.get('value'))
    tag, node = __interpolate_tag(key_path, event)
    if "writeField" == action:
        overWriteIfExists = action_stream.get('overwriteIfExists')
        if not overWriteIfExists:
            node.setdefault(tag, value)
        else:
            node[tag] = value
        return event
    elif "arrayAppend" == action:
        lst = node.setdefault(tag, [])
        lst.append(value)
        return event
    elif "regexReplace" == action:
        node[tag] = re.sub(action_stream['pattern'], action_stream['replacement'], node.get(tag, ''))
        return event
    elif "dropEvent" == action:
        return None

def evaluate(payload, event):
    '''
    This function evaluates the DSL conditions payload operator.
    By interpolating the left tag actions listed in the actions dictionary against the right value.
    :param payload: operator payload we expect the payload to be something like this
    { "operator": "matchesRegex", "left": "$page_host", "right": ".*\\.zendesk\\.com$" }
    :param event: This's the event stream payload.
    :return:
    '''
    func = payload.get('operator')
    left_tag, l_event = __interpolate_tag(payload.get('left'), event)
    left_val, right_val = l_event[left_tag], payload.get('right')
    if func == "matchesRegex":
        return bool(evaluator[func](right_val, left_val))
    return bool(evaluator[func](left_val, right_val))


def evaluate_parse_condition(condition, event):
    """
    This function is used to evaluate the junctions, this function would evaluate from the base case then move upward.
    :param condition: This is the condition defined in the rule.json
    :param event: This is the event stream from the queue
    :return: bool
    """
    if __check_for_operator(condition):
        return evaluate(condition, event)
    operator_lst = condition_key = None
    for condition_key, operator_lst in condition.items():
        break
    if isinstance(operator_lst, list):
        lst = []
        for operator in operator_lst:
            lst.append(evaluate_parse_condition(operator, event))
        return conditions[condition_key](lst)
    return False


def __check_for_operator(operator_or_condition: Dict):
    """
    :param operator_or_condition:
    Check is the operator is actually an operator like this: { "operator": "matchesRegex", "left": "$page_host", "right": ".*\\.gusto\\.com$" }
    or not.
    :return:
    """
    return "operator" in operator_or_condition.keys()


def __interpolate_tag(tag, event):
    """
    This function would evaluate the tag and return the dictionary instance of that tag.
    :param tag: Tag is keyword that needs to be expressed from the event, sub tag are divided with dot(.).
    A tag expression mostly start with dollar sign($).
    :param event: Event is a payload in which the tag and sub-tags are reading from
    :return: Tuple[str,Dict]
    """
    if not isinstance(tag, str) or not tag or not "$" == tag[0]:
        return tag, event
    node = event
    prev = None
    for t in tag[1:].split('.'):
        if prev:
            node = event[prev]
        prev = t
    return prev, node


# You need to implement this function.
# Feel free to organize your code into
# whatever other classes and functions you see fit.
def process_events(event_stream, rules):
    lst = []
    for event in event_stream:
        for r in rules['rules']:
            result = evaluate_parse_condition(r['conditions'], event)
            if result:
                for action in r['actions']:
                    event = perform_action(action, event)
            if not event:
                break
        if event:
            lst.append(event)
    print_and_write_file(lst, True, True)
    return lst


def print_and_write_file(processed_events: Union[List, Dict], compare_to_expected: bool, show_diff: bool = False):
    j = json.dumps(processed_events, indent=2)
    with open("output.json", "w") as f:
        f.write(j)
    if compare_to_expected:
        exp = json.load(open("expectedOutput.json"))
        e = json.dumps(exp, indent=2)
        m = "✅ matches expected" if e == j else "❌ does not match expected"
        print("\n")
        print("--------------------")
        if e != j and show_diff:
            # use git diff for colorized output
            subprocess.run(
                ["git", "diff", "--no-index", "expectedOutput.json", "output.json"],
                env=dict(os.environ, PAGER="cat"),
            )
        print(m)
        print("--------------------")

##########
# main
##########


def usage():
    print("processor.py [rules.json] [eventStream.json]")
    exit(1)
