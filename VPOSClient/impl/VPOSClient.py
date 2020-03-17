import urllib.parse as urlparse

import requests

from VPOSClient.response.ResponseMapper import map_order_status_response, map_operation_response, \
    map_authorize_response, map_three_ds_authorize0, map_three_ds_authorize1, map_three_ds_authorize2
from VPOSClient.utils.RequestValidator import *
from VPOSClient.utils.Utils import map_for_verify_url_mac
from VPOSClient.request.RequestXML import *


class VPosClient:

    def __init__(self, vpos_config):

        validate_config(vpos_config)

        self._start_key = vpos_config.redirect_key
        self._api_result_key = vpos_config.api_key
        self._digest_mode = vpos_config.algorithm
        # api endpoint
        self._web_api = vpos_config.api_url
        self._url_redirect = vpos_config.redirect_url
        self._shop_id = vpos_config.shop_id
        if (vpos_config.proxy_host is not None) & (vpos_config.proxy_port is not None):
            self._set_proxy(vpos_config.proxy_host, vpos_config.proxy_port, vpos_config.proxy_username,
                            vpos_config.proxy_password)
        self._proxies = None

    def buildHTMLRedirectFragment(self, paymentInfo):
        """Create an HTML fragment for payment initiation.
        :param paymentInfo: data transfer object containing all the payment parameters
        :return: the HTML fragment for redirect
        """
        validate_redirect_request(paymentInfo)
        paymentRequest = PaymentRequest(paymentInfo, self._shop_id)
        return Utils.getHtml(self._url_redirect, paymentRequest.getParametersMap(self._start_key, self._digest_mode))

    def authorize(self, authorization_request):
        validate_authorize(authorization_request)
        authorization = OnlineAuthorizationRequestXml(authorization_request, self._shop_id)
        request_xml = authorization.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        return map_authorize_response(response)

    def threeDSAuthorize0(self, threeDS0_request):
        validate_threeDSAuthorization0_request(threeDS0_request)
        three_ds0_auth = ThreeDSAuthorization0RequestXML(threeDS0_request, self._shop_id)
        request_xml = three_ds0_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        return map_three_ds_authorize0(response)

    def threeDSAuthorize1(self, threeDS1_request):
        validate_threeDSAuthorization1_request(threeDS1_request)
        three_ds1_auth = ThreeDSAuthorization1RequestXML(threeDS1_request, self._shop_id)
        request_xml = three_ds1_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        return map_three_ds_authorize1(response)

    def threeDSAuthorize2(self, threeDS2_request):
        validate_threeDSAuthorization2_request(threeDS2_request)
        three_ds2_auth = ThreeDSAuthorization2RequestXML(threeDS2_request, self._shop_id)
        request_xml = three_ds2_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        return map_three_ds_authorize2(response)

    def capture(self, capture_request):
        """
        :param capture_request: data transfer object containing all the required parameters to perform a
        payment confirmation
        :return:
        """
        validate_capture_request(capture_request)
        capture = CaptureRequestXml(capture_request, self._shop_id)
        requestXml = capture.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(requestXml)
        self.verifyMacResponse(response)
        return map_operation_response(response)

    def getOrderStatus(self, order_status_request):
        validate_order_status_request(order_status_request)
        order_status = OrderStatusRequestXml(order_status_request, self._shop_id)
        request_xml = order_status.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self.verifyMacResponse(response)
        return map_order_status_response(response)

    def refund(self, refund_request):
        """
        :param refund_request: data transfer object containing all the required parameters to perform a payment refund
        :return:
        """
        validate_refund_payment_request(refund_request)
        refund = RefundRequestXml(refund_request, self._shop_id)
        request_xml = refund.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self.verifyMacResponse(response)
        return map_operation_response(response)

    def verifyMacResponse(self, response):
        response = Utils.stringToXML(response)
        receivedMac = response.find(Constants.getMacName())
        calculatedMac = Encoder.getMac(Utils.geResultStringForMac(response), self._api_result_key, self._digest_mode)

        if (not receivedMac.text == "NULL") & (not Encoder.compareDigest(receivedMac.text, calculatedMac)):
            raise VPOSException("Response MAC is not valid")

        data = response.find(TagConstants.getDataTag())
        if (data is not None) & (data.find(TagConstants.getOperationTag()) is not None):
            operation_calculated_mac = Encoder.getMac(
                Utils.getOperationStringForMac(data.find(TagConstants.getOperationTag())), self._api_result_key,
                self._digest_mode)
            operation_received_mac = data.find(TagConstants.getOperationTag()).find(TagConstants.getMACTag())
            if (not operation_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(operation_received_mac.text, operation_calculated_mac)):
                raise VPOSException("Operation MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getAuthorizationTag()) is not None):
            authorization_calculated_mac = Encoder.getMac(
                Utils.getAuthorizationStringForMac(data.find(TagConstants.getAuthorizationTag())), self._api_result_key,
                self._digest_mode)
            authorization_received_mac = data.find(TagConstants.getAuthorizationTag()).find(TagConstants.getMACTag())
            if (not authorization_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(authorization_received_mac.text, authorization_calculated_mac)):
                raise VPOSException("Authorization MAC is not valid")

    def verifyMAC(self, url):
        """
        Validate the result of a payment initiation verifying the integrity of the data contained in URMLS/URLDONE
        :param url:  url generated from SIA VPOS redirect
        """
        parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
        receivedMac = parsed.get(Constants.getMacName())
        calculated_mac = Encoder.getMac(map_for_verify_url_mac(parsed), self._api_result_key, self._digest_mode)
        if not Encoder.compareDigest(calculated_mac, receivedMac):
            return False
        else:
            return True

    def _set_proxy(self, proxy_name, proxy_port, username=None, password=None):
        proxy = "http://" + str(proxy_name) + ":" + str(proxy_port)
        if username is not None and password is not None:
            proxy = proxy + username + ":" + password + "@" + str(proxy_name) + ":" + str(proxy_port)
        self._proxies = {"http": proxy}

    def _execute_call(self, requestXml):
        requestXml = 'data=' + str(requestXml, "utf-8")
        print("REQUEST: " + requestXml)
        response = requests.post(self._web_api, requestXml,
                                 headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=self._proxies)
        print("RESPONSE: " + response.text)
        return response.text
