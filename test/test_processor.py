from unittest import TestCase
from copy import deepcopy
from processor import evaluate_parse_condition, perform_action


class TestEventStreamProcessor(TestCase):
    def test_evaluate_parse_condition_with_true(self):
        event_stream = {
            "begin_ts": "2020-09-16 15:00:58.16",
            "end_ts": "2020-09-16 15:01:01.456",
            "fin_extension_version": "1.05",
            "id": 1003,
            "is_in_browser": True,
            "page_host": "fin.zendesk.com",
            "page_title": "Zendesk - Ticket 1234",
            "page_url": "https://fin.zendesk.com/ticket/1234",
            "ui_events": {
                "n_keypress": 62,
                "n_mouse_click": 0,
                "n_mouse_move": 10,
                "n_mouse_scroll": 1
            },
            "user_id": 56183
        }
        rule = {
            "conditions": {
                "all": [
                    {
                        "any": [
                            {"operator": "matchesRegex", "left": "$page_host", "right": ".*\\.zendesk\\.com$"},
                            {"operator": "matchesRegex", "left": "$page_host", "right": "^kb\\.fin\\.com$"}
                        ]
                    },
                    {"operator": "greaterThan", "left": "$ui_events.n_keypress", "right": 0}
                ]
            }
        }
        result = evaluate_parse_condition(rule['conditions'], event_stream)
        self.assertTrue(result)

    def test_evaluate_parse_condition_with_false(self):
        event_stream = {
            "begin_ts": "2020-09-16 15:00:58.16",
            "end_ts": "2020-09-16 15:01:01.456",
            "fin_extension_version": "1.05",
            "id": 1003,
            "is_in_browser": True,
            "page_host": "fin.zendesk.com",
            "page_title": "Zendesk - Ticket 1234",
            "page_url": "https://fin.zendesk.com/ticket/1234",
            "ui_events": {
                "n_keypress": -62,
                "n_mouse_click": 0,
                "n_mouse_move": 10,
                "n_mouse_scroll": 1
            },
            "user_id": 56183
        }
        rule = {
            "conditions": {
                "all": [
                    {
                        "any": [
                            {"operator": "matchesRegex", "left": "$page_host", "right": ".*\\.zendesk\\.com$"},
                            {"operator": "matchesRegex", "left": "$page_host", "right": "^kb\\.fin\\.com$"}
                        ]
                    },
                    {"operator": "greaterThan", "left": "$ui_events.n_keypress", "right": 0}
                ]
            }
        }
        result = evaluate_parse_condition(rule['conditions'], event_stream)
        self.assertFalse(result)

    def test_perform_action_for_write_field(self):
        action_payload = {"action": "writeField", "keyPath": "$tags", "value": [], "overwriteIfExists": False}
        event = {
            "begin_ts": "2020-09-16 15:00:58.16",
            "end_ts": "2020-09-16 15:01:01.456",
            "fin_extension_version": "1.05",
            "id": 1003,
            "is_in_browser": True,
            "page_host": "fin.zendesk.com",
            "page_title": "Zendesk - Ticket 1234",
            "page_url": "https://fin.zendesk.com/ticket/1234",
            "ui_events": {
                "n_keypress": 62,
                "n_mouse_click": 0,
                "n_mouse_move": 10,
                "n_mouse_scroll": 1
            },
            "user_id": 56183
        }
        expected_answer = deepcopy(event)
        event = perform_action(action_payload, event)
        expected_answer['tags'] = []
        self.assertEqual(expected_answer, event)