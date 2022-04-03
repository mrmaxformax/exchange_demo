import base64
import hashlib
import hmac
import time
import urllib.parse
import pyotp

from pydantic import ValidationError
from typing import Union, Any

from config import GlobalVariables
from models import ApiResponse, Asset, AssetPair, ErrorMessage, ServerTime, SystemStatus, OpenOrder,\
    OpenOrderResponse, OpenOrderDemoResponse
from request_lib.api_keys import ApiKeys
from request_lib.request_manager import RequestManager
from utilities.logging import LOG
from .endpoints_collection import ASSET_INFO, SERVER_TIME, SYSTEM_STATUS, ASSET_PAIRS, OPEN_ORDERS, OPEN_ORDERS_DEMO
from request_lib.request_property import RequestProperty


class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.__manager = RequestManager()

    def close(self):
        self.__manager.close()
        return

    def get_server_time(self) -> Union[ServerTime, ErrorMessage]:
        response = self.__get_single_value_response(SERVER_TIME, ServerTime)
        if len(response.error) > 0:
            return ErrorMessage(error=response.error)
        return response.result

    def get_system_status(self) -> Union[SystemStatus, ErrorMessage]:
        response = self.__get_single_value_response(SYSTEM_STATUS, SystemStatus)
        if len(response.error) > 0:
            return ErrorMessage(error=response.error)
        return response.result

    def get_asset_info(self, asset: str) -> Union[Asset, ErrorMessage]:
        response = self.__get_multiply_values_response(ASSET_INFO, {"asset": asset}, Asset)
        if len(response.error) > 0:
            return ErrorMessage(error=response.error)
        return response.result

    def get_tradable_asset_pairs(self, pair: str) -> Union[AssetPair, ErrorMessage]:
        pair = pair.replace(" ", "").replace("/", "")
        response = self.__get_multiply_values_response(ASSET_PAIRS, {"pair": pair}, AssetPair)
        if len(response.error) > 0:
            return ErrorMessage(error=response.error)
        return response.result

    def get_open_orders(self, keys: ApiKeys, trades: bool = True):
        data = {
            "nonce": self.__nonce(),
            "trades": trades,
            "otp": self.__mfa()
        }

        headers = self.__auth_header(keys, OPEN_ORDERS, data, False)
        request = RequestProperty(base_url=self.base_url, request_type="POST", endpoint=OPEN_ORDERS,
                                  headers=headers, data=data)
        response = self.__manager.send_request(request)
        error = response.response_json["error"]
        result = response.response_json["result"]
        asset_model = {}
        if len(error) == 0:
            for k, v in result.items():
                if len(v) > 0:
                    try:
                        asset_model[k] = OpenOrder(**v)
                    except ValidationError as e:
                        LOG.error(e.errors())
                        asset_model[k] = e.errors()
                else:
                    asset_model[k] = {}
            result = OpenOrderResponse(**asset_model)
            return ApiResponse(error=error, result=result)
        return ApiResponse(error=error, result=result)

    def get_demo_open_orders(self, keys: ApiKeys):

        headers = self.__auth_header(keys, OPEN_ORDERS_DEMO, "")

        request = RequestProperty(base_url=self.base_url, request_type="GET", endpoint=OPEN_ORDERS_DEMO,
                                  headers=headers)
        response = self.__manager.send_request(request)
        response = OpenOrderDemoResponse(**response.response_json)
        return response

    def __get_multiply_values_response(self, endpoint: str, request_param: dict, obj: Any) -> ApiResponse:
        request = RequestProperty(base_url=self.base_url, request_type="GET", endpoint=endpoint, params=request_param)
        response = self.__manager.send_request(request)
        error = response.response_json["error"]
        result = response.response_json.get("result")
        asset_model = {}

        if len(error) == 0:
            for k, v in result.items():
                try:
                    asset_model[k] = obj(**v)
                except ValidationError as e:
                    item: str = list(request_param.keys())[0]
                    LOG.error(f"Errors in {item}:  {e.errors()}")
                    asset_model[k] = e.errors()
            return ApiResponse(error=error, result=asset_model)
        return ApiResponse(error=error, result=result)

    def __get_single_value_response(self, endpoint: str, obj: Any) -> ApiResponse:
        request = RequestProperty(base_url=self.base_url, endpoint=endpoint, request_type="GET")
        response = self.__manager.send_request(request)
        error = response.response_json["error"]
        result = obj(**response.response_json["result"])
        return ApiResponse(error=error, result=result)

    def __auth_header(self, keys: ApiKeys, endpoint: str, data: Union[str, dict], demo=True) -> dict:

        if demo:
            return {
                'APIKey': keys.api_key,
                'Authent': self.__generate_secret_demo(endpoint, data, keys.secret_key),
            }
        return {
            'API-Key': keys.api_key,
            'API-Sign': self.__generate_secret(data, endpoint, keys.secret_key),
        }

    @staticmethod
    def __mfa():
        totp = pyotp.TOTP(GlobalVariables.OTP)
        return totp.now()

    @staticmethod
    def __nonce():
        return int(1000 * time.time())

    @staticmethod
    def __generate_secret(data: dict, endpoint: str, secret: str) -> str:
        # From: https://github.com/veox/python3-krakenex
        api_secret = base64.b64decode(secret)
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = endpoint.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(api_secret, message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())
        return sigdigest.decode()

    @staticmethod
    def __generate_secret_demo(endpoint: str, post_data: str, secret: str, nonce: str = "") -> bytes:
        """
        Stolen from Gitlab: https://github.com/CryptoFacilities
        """
        if endpoint.startswith('/derivatives'):
            endpoint = endpoint[len('/derivatives'):]

        # step 1: concatenate postData, nonce + endpoint
        message = post_data + nonce + endpoint

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf8'))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secret_decoded = base64.b64decode(secret)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secret_decoded, hash_digest,
                               hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64encode(hmac_digest)
