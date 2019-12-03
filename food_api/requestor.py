#!/usr/bin/env python3
"""
This file will hold the various functions
required to send an API request to the food
database using the required pieces of information
"""
import json
from io import StringIO

import requests

from food_api import keys


def pretty_print_response(response) -> str:
    """
    Description
    -----------
    This function pretty prints a json text response that comes from a
    requests.Response object

    Params
    ------
    :response: requests.Response or dict
    The response object received from an API call via the python
    requests library.

    Return
    ------
    str
    A pretty printed representation of the json response text.
    """
    return(json.dumps((response if type(response) == dict else json.loads(response.text)), indent=4, sort_keys=True))


def response_code_alerting(response: requests.Response, verbose: bool = True) -> None:
    """
    Description
    -----------
    This function parses the `requests.Response` object to
    determine if the API call is returning successful responses
    or not. If not exceptions will be raised and the details
    will be printed.

    Params
    ------
    :response: requests.Response
    The response object received from an API call via the python
    requests library.

    :verbose: bool = True
    Whether or not to likewise print the json text of the requests.Response

    Return
    ------
    None
    This function returns nothing, only raises an error
    on unsuccessful responses.
    """
    if response.status_code < 200 or response.status_code >= 300:
        if verbose:
            print("Ruh roh, this was not successful! See below...")
            print(pretty_print_response(response))
        if response.status_code < 200:
            raise(requests.exceptions.RequestsWarning(f"Response code is {response.status_code}, and is an informational response"))
        elif 300 <= response.status_code < 400:
            raise(requests.exceptions.RequestsWarning(f"Response code is {response.status_code}, and is a redirect"))
        elif 400 <= response.status_code < 500:
            raise(requests.exceptions.RequestsWarning(f"Response code is {response.status_code}, and is an ERROR"))
        elif 500 <= response.status_code:
            raise(requests.exceptions.RequestsWarning(f"Response code is {response.status_code}, and is an INTERNAL SERVER ERROR"))


def get_food_from_upc(
    upc: str,
    app_id: str = keys.MYFRIDGE_APP_ID,
    app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
) -> dict:
    """
    Description
    -----------
    This function passes a upc to the food requests
    database API and returns information about the food

    Params
    ------
    :upc: str
    a string 12 difit UPC (universal product code)
    for the API to fetch

    :app_id: str = keys.MYFRIDGE_APP_ID
    The edamam food api app id for calling the food database API

    :app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
    The food database API key for calling the food database API

    Return
    ------
    dict
    The JSON response of the API call in the form of a dictionary
    """
    url = 'https://api.edamam.com/api/food-database/parser'
    params = {"upc": upc, "app_id": app_id, "app_key": app_key}
    response = requests.get(url=url, params=params)
    response_code_alerting(response)
    return json.loads(response.text)


def get_attribute_from_food_id(
    food_id: str,
    quantity: float,
    measure_uri: str,
    attribute: str = 'calories',
    qualifiers: list = None,
    app_id: str = keys.MYFRIDGE_APP_ID,
    app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
) -> int:
    """
    Description
    -----------
    This function calls for the nutritional content of a particular
    food based off of the food_id (retrieved from the `get_food_from_upc()`
    function) and quantity. Particularly this function returns the
    calorie content of that food.

    Params
    ------
    :food_id: str
    This is the food id corresponding to a particular piece of food in the food database

    :quantity: float
    The quantity of this particular food you are requesting for

    :measure_uri: str
    The Edamam API food measurement URI's. Find the options here:
    (https://developer.edamam.com/food-database-api-docs) under
    *Nutrition Data Requests

    :attribute: str = calories
    This function returns the calories of a particular food
    by default, but any attrbutes (or all) can be pulled as well.

    :qualifiers: list = None
    --Additional qualifier documentation is lacking--
    Optional, a list of any qualifiers that would accompany a particular food.
    Example would be "Large" for a larger version of an apple.
    This must be a valid URI below is the example for "Large".
    (http://www.edamam.com/ontologies/edamam.owl#Qualifier_large)

    :app_id: str = keys.MYFRIDGE_APP_ID
    The edamam food api app id for calling the food database API

    :app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
    The food database API key for calling the food database API

    Return
    ------
    int
    The numer of some particular attribute present in the provided food id
    for the given measurement. Depending on the value selected, an int may
    be returned or potentially a list of strings, or a float.
    Depends on the attribute you select.
    """
    url = 'https://api.edamam.com/api/food-database/nutrients'
    headers = {"Content-Type": "application/json"}
    params = {"app_id": app_id, "app_key": app_key}

    # store as a python dict
    json_data = {
        "ingredients": [
            {
                "foodId": food_id,
                "quantity": quantity,
                "measureURI": measure_uri
            }
        ]
    }

    if qualifiers:
        if type(qualifiers) == list:
            json_data["ingredients"][0]["qualifiers"] = qualifiers
        else:
            raise(TypeError("`qualifiers` parameter must be of type `list` even if only one value is passed. If no values then type must be `None`."))

    response = requests.post(
        url=url,
        params=params,
        headers=headers,
        # Convert to file-like object for passing to requests
        data=StringIO(json.dumps(json_data))
        )

    return json.loads(response.text)[attribute]


def get_attribute_from_upc(
    upc: str,
    quantity: float = 1.0,
    measure: str = "Ounce",
    attribute: str = "calories",
    qualifiers: list = None,
    app_id: str = keys.MYFRIDGE_APP_ID,
    app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
) -> int:
    """
    Description
    -----------
    This function will combine the 2 above functions
    and use a provided UPC to pull the attribute information
    for a given piece of food based off of its provided
    UPC. The default attribute is calories and the default
    measurement is ounce.

    Params
    ------
    :upc: str
    a string 12 difit UPC (universal product code)
    for the API to fetch

    :quantity: float = 1.0
    The quantity of this particular food you are requesting for
    defaults to one

    :measure: str="Ounce"
    A valid measurement for the given food,
    example "Gallon" for milk. First letter should be capitalized.

    :attribute: str = calories
    The attribute whose value you seek. Default is calories.
    See the API documentation for a list of values to select form.

    :qualifiers: list = None
    --Additional qualifier documentation is lacking--
    Optional, a list of any qualifiers that would accompany a particular food.
    Example would be "Large" for a larger version of an apple.
    This must be a valid URI below is the example for "Large".
    (http://www.edamam.com/ontologies/edamam.owl#Qualifier_large)

    :app_id: str = keys.MYFRIDGE_APP_ID
    The edamam food api app id for calling the food database API

    :app_key: str = keys.EDAMAM_FOOD_DATABASE_API_KEY
    The food database API key for calling the food database API

    Return
    ------
    int
    The numer of some particular attribute present in the provided food id
    for the given measurement. Depending on the value selected, an int may
    be returned or potentially a list of strings, or a float.
    Depends on the attribute you select.
    """
    upc_details = get_food_from_upc(upc=upc, app_id=app_id, app_key=app_key)
    food_id = upc_details["hints"][0]["food"]["foodId"]

    # The available measures are stored in a list of dictionaries
    available_measures = upc_details["hints"][0]["measures"]

    # Grab the first matching label URI from the list of available measures
    measure_uri = [each_measure["uri"] for each_measure in available_measures if each_measure["label"] == measure]
    if not measure_uri:
        print(pretty_print_response(available_measures)
        raise(KeyError(f"Oh no, something went wrong trying to get that measure '{measure}'! Above are the available measures to choose from for this product"))
    else:
        measure_uri = measure_uri[0]
    return get_attribute_from_food_id(
        food_id=food_id,
        quantity=quantity,
        measure_uri=measure_uri,
        attribute=attribute,
        qualifiers=qualifiers,
        app_id=app_id,
        app_key=app_key
    )
