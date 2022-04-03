import json

from behave import step
from hamcrest import assert_that, equal_to, instance_of, is_not, has_length, greater_than, not_none
from datetime import datetime
from deepdiff import DeepDiff

from client.client import Client
from config import GlobalVariables
from models import ErrorMessage, OpenOrderResponse
from request_lib.api_keys import ApiKeys


@step('Lets work with real API')
def work_with_real_api(context):
    context.keys = ApiKeys(api_key=GlobalVariables.API_KEY, secret_key=GlobalVariables.SECRET_KEY)
    context.base_url = GlobalVariables.REAL_API_URL
    context.client = Client(context.base_url)
    context.env = "real"


@step('Lets work with demo API')
def work_with_real_api(context):
    context.keys = ApiKeys(api_key=GlobalVariables.DEMO_API_KEY, secret_key=GlobalVariables.DEMO_SECRET_KEY)
    context.base_url = GlobalVariables.DEMO_API_URL
    context.client = Client(context.base_url)
    context.env = "demo"


@step('get server time')
def get_server_time(context):
    context.response = context.client.get_server_time()


@step('validate server time response has equal values')
def validate_server_time_response(context):
    assert_that(context.response, is_not(instance_of(ErrorMessage)))

    date_time = datetime.utcfromtimestamp(context.response.unixtime)
    st = date_time.strftime("%a, %d %b %y %H:%M:%S +0000")
    assert_that(st, equal_to(context.response.rfc1123))


@step('get the asset pair info for "{pair}"')
def get_trading_pair_info(context, pair):
    context.response = context.client.get_tradable_asset_pairs(pair=pair)


@step('validate the asset pair info for "{pair}"')
def validate_trading_pair_info(context, pair):
    pair = pair.replace(" ", "").replace("/", "")
    if len(pair) == 8:
        pair = pair[1:4] + pair[5:]

    with open(f"{GlobalVariables.TEST_DATA_FOLDER}/trading_pairs_params.json", "r") as f:
        js_data = json.loads(f.read())

    for k, v in context.response.items():
        if v.altname == pair:
            result = DeepDiff(v.dict(), js_data[k])
            assert_that(len(result) == 0, equal_to(True), f"Error in pair {k}: {result}")


@step('validate the error for incorrect asset pair "{pair}"')
def validate_trading_pair_error(context, pair):
    assert_that(context.response.error_message, equal_to('EQuery:Unknown asset pair'))


@step("get Open Orders Value")
def get_open_orders_value(context):
    context.response = context.client.get_open_orders(context.keys, trades=True)


@step("validate Open Orders Value is empty")
def validate_open_orders_value_empty(context):
    assert_that(context.response, is_not(instance_of(ErrorMessage)))
    assert_that(context.response.result, instance_of(OpenOrderResponse))
    assert_that(context.response.result.open, has_length(0))


@step("get Demo Open Orders Value")
def get_demo_open_orders_value(context):
    context.response = context.client.get_demo_open_orders(context.keys)


@step("validate Demo Open Orders Value")
def validate_demo_open_orders_value(context):
    assert_that(len(context.response.openOrders), greater_than(0))
    assert_that(context.response.result, equal_to('success'))
    assert_that(context.response.serverTime, not_none())
