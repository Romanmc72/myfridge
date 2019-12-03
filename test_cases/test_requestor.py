#!/usr/bin/env python3
"""
These are the unit tests for this program.

They should be run to ensure that everything here works.
"""
import textwrap

import unittest
import requests

from food_api import requestor


class FakeAssResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


class RequestorSendAndResponseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RequestorSendAndResponseTest, self).__init__(*args, **kwargs)
        self.test_upc = "079298000078"
        self.test_bad_upc = "1234567890"
        self.test_food_id = "food_aeqymyrb3waczza6m7kgvbhmkh9q"
        self.test_quantity = 1
        self.test_measure_uri = 'http://www.edamam.com/ontologies/edamam.owl#Measure_ounce'
        self.not_a_measure = "Penguins"
        self.fake_json = '{ "fake": "json" }'
        self.not_a_list = 'http://www.edamam.com/ontologies/edamam.owl#Qualifier_large'
        self.test_response100 = FakeAssResponse(status_code=100, text=self.fake_json)
        self.test_response200 = FakeAssResponse(status_code=200, text=self.fake_json)
        self.test_response300 = FakeAssResponse(status_code=300, text=self.fake_json)
        self.test_response400 = FakeAssResponse(status_code=400, text=self.fake_json)
        self.test_response500 = FakeAssResponse(status_code=500, text=self.fake_json)

    def test_pretty_print_response(self):
        self.assertEqual(
            requestor.pretty_print_response(
                {
                    "key1": [
                        "list1",
                        "list2"
                    ],
                    "key2": "value2"
                }
            ),
            textwrap.dedent("""\
                {
                    "key1": [
                        "list1",
                        "list2"
                    ],
                    "key2": "value2"
                }""")
        )

    def test_response_code_alerting100(self):
        self.assertRaises(
            requests.exceptions.RequestsWarning,
            requestor.response_code_alerting,
            **dict(response=self.test_response100)
        )

    def test_response_code_alerting200(self):
        self.assertEqual(
            requestor.response_code_alerting(response=self.test_response200),
            None
        )

    def test_response_code_alerting300(self):
        self.assertRaises(
            requests.exceptions.RequestsWarning,
            requestor.response_code_alerting,
            **dict(response=self.test_response300)
        )

    def test_response_code_alerting400(self):
        self.assertRaises(
            requests.exceptions.RequestsWarning,
            requestor.response_code_alerting,
            **dict(response=self.test_response400)
        )

    def test_response_code_alerting500(self):
        self.assertRaises(
            requests.exceptions.RequestsWarning,
            requestor.response_code_alerting,
            **dict(response=self.test_response500)
        )

    def test_get_food_from_upc(self):
        self.assertEqual(
            requestor.get_food_from_upc(
                upc=self.test_upc,
            )["hints"][0]["food"]["foodId"],
            self.test_food_id
        )

    def test_get_attribute_from_food_id(self):
        self.assertEqual(
            requestor.get_attribute_from_food_id(
                food_id=self.test_food_id,
                quantity=self.test_quantity,
                measure_uri=self.test_measure_uri
            ),
            0
        )

    def test_get_attribute_from_food_id_qualifier_type_error(self):
        self.assertRaises(
            TypeError,
            requestor.get_attribute_from_food_id,
            **dict(
                food_id=self.test_food_id,
                quantity=self.test_quantity,
                measure_uri=self.test_measure_uri,
                qualifiers=self.not_a_list
            )
        )

    def test_get_attribute_from_food_id_qualifier(self):
        self.assertEqual(
            requestor.get_attribute_from_food_id(
                food_id=self.test_food_id,
                quantity=self.test_quantity,
                measure_uri=self.test_measure_uri,
                qualifiers=[self.not_a_list]
            ),
            0
        )

    def test_get_attribute_from_upc(self):
        self.assertEqual(
            requestor.get_attribute_from_upc(
                upc=self.test_upc
            ),
            0
        )

    def test_get_attribute_from_upc_measure_error(self):
        self.assertRaises(
            KeyError,
            requestor.get_attribute_from_upc,
            **dict(
                upc=self.test_upc,
                measure=self.not_a_measure
            )
        )


if __name__ == "__main__":
    unittest.main()
